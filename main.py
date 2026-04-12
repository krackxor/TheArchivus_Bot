import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from engine import process_move
from database import get_player, update_player, auto_seed_content, reset_player_death
from combat import generate_battle_puzzle, validate_answer
from states import GameState
from config import BOT_TOKEN
from shop import get_shop_keyboard, process_purchase
from skills import use_skill_reveal

dp = Dispatcher()

# --- KEYBOARDS ---

def get_main_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⬆️ Utara")],
            [KeyboardButton(text="⬅️ Barat"), KeyboardButton(text="Timur ➡️")],
            [KeyboardButton(text="⬇️ Selatan")],
            [KeyboardButton(text="📊 Status"), KeyboardButton(text="🛒 Toko")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Tentukan langkahmu, Weaver..."
    )

def get_combat_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔮 Revelatio (10 MP)", callback_data="use_skill", color="gold")]
    ])

def get_npc_interaction_keyboard(req):
    if req is None:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🧭 Ikuti Sarannya", callback_data="npc_follow", color="blue")],
            [InlineKeyboardButton(text="👣 Abaikan", callback_data="npc_ignore", color="red")]
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🤝 Beri {req['amount']} {req['name']}", callback_data="npc_accept", color="green")],
        [InlineKeyboardButton(text="👣 Abaikan", callback_data="npc_ignore", color="red")]
    ])

# --- BASIC HANDLERS ---

@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    get_player(user_id, message.from_user.first_name)
    await state.set_state(GameState.exploring)
    await message.answer("📜 **The Archivus telah bangkit.**", reply_markup=get_main_reply_keyboard())

# --- NPC LOGIC: MANUAL NAVIGATION TRIGGER ---

@dp.callback_query(F.data == "npc_follow")
async def npc_follow_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    npc_data = data.get("npc_data")
    if not npc_data: return
    
    # Deteksi arah dari dialog NPC secara cerdas
    dialog = npc_data['dialog']
    target_dir = "⬆️ Utara"
    if "Barat" in dialog: target_dir = "⬅️ Barat"
    elif "Timur" in dialog: target_dir = "Timur ➡️"
    elif "Selatan" in dialog: target_dir = "⬇️ Selatan"

    await state.set_state(GameState.traveling)
    await state.update_data(target_direction=target_dir, follow_step=0)

    text = (
        f"📍 **Navigasi Terkunci.**\n\n"
        f"Kamu memutuskan mengikuti petunjuk menuju **{target_dir}**.\n"
        f"Melangkahlah 5x ke arah tersebut untuk sampai."
    )
    await callback.message.edit_text(text)
    await callback.answer()

# --- CORE MOVE HANDLER (NORMAL & TRAVELING) ---

@dp.message(F.text.in_(["⬆️ Utara", "⬅️ Barat", "Timur ➡️", "⬇️ Selatan"]))
async def move_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    current_state = await state.get_state()
    data = await state.get_data()

    # 1. LOGIKA MISI NAVIGASI (5 LANGKAH)
    if current_state == GameState.traveling:
        target_dir = data.get("target_direction")
        follow_step = data.get("follow_step", 0)

        if message.text != target_dir:
            # NARASI HUKUMAN SALAH ARAH
            await state.set_state(GameState.exploring)
            await state.update_data(target_direction=None, follow_step=0)
            update_player(user_id, {"mp": max(0, get_player(user_id)['mp'] - 10)})
            
            narasi_hukuman = (
                "⚠️ **WEAVER KEHILANGAN BENANG.**\n"
                "Archivus tidak menoleransi keraguan. Dengan mengabaikan petunjuk, "
                "benang takdir yang baru saja terajut langsung terputus. "
                "Hawa dingin menyapu jiwamu.\n\n"
                "**Hukuman:** MP -10"
            )
            return await message.answer(narasi_hukuman, reply_markup=get_main_reply_keyboard())

        # Progres Langkah
        follow_step += 1
        if follow_step < 5:
            await state.update_data(follow_step=follow_step)
            progress = "👣" * follow_step
            return await message.answer(f"Melangkah ke {target_dir}... ({follow_step}/5)\n{progress}")
        else:
            # SELESAI 5 LANGKAH - PENENTUAN NASIB
            await state.set_state(GameState.exploring)
            await state.update_data(target_direction=None, follow_step=0)
            npc_data = data.get("npc_data")

            if npc_data['is_liar']:
                # Dikhianati: Bertarung dengan Tier Tinggi
                puzzle = generate_battle_puzzle(random.randint(15, 30)) 
                puzzle['current_hint'] = "_" * len(puzzle['answer'])
                await state.set_state(GameState.in_combat)
                await state.update_data(puzzle=puzzle)
                
                res = (
                    "💀 **DIKHIANATI!**\n"
                    "Saran itu jebakan! Kamu sampai di ujung jalan yang buntu dan monster telah menunggumu.\n\n"
                    f"⚔️ **{puzzle['monster_name']}** (TIER {puzzle['tier']})\n"
                    f"🧩 `\"{puzzle['question']}\"`"
                )
                msg = await message.answer(res, reply_markup=get_combat_keyboard())
                
                # Timeout 1 Menit untuk Monster Jebakan
                await asyncio.sleep(60)
                if await state.get_state() == GameState.in_combat:
                    p = get_player(user_id)
                    damage = puzzle.get('damage', 10)
                    update_player(user_id, {"hp": p['hp'] - damage})
                    await state.set_state(GameState.exploring)
                    await msg.answer(f"⚠️ **WAKTU HABIS!** HP -{damage}")
                return
            else:
                # Berhasil (NPC Jujur)
                update_player(user_id, {"mp": min(100, get_player(user_id)['mp'] + 20)})
                return await message.answer(
                    "😇 **TUJUAN TERCAPAI.**\nSaran itu benar. Kamu menemukan area yang lebih stabil. MP +20",
                    reply_markup=get_main_reply_keyboard()
                )

    # 2. LOGIKA JALAN NORMAL (GameState.exploring)
    if current_state == GameState.exploring:
        event_type, event_data, narration = process_move(user_id)
        
        if event_type == "monster":
            player = get_player(user_id)
            puzzle = generate_battle_puzzle(player['kills'])
            puzzle['current_hint'] = "_" * len(puzzle['answer'])
            await state.set_state(GameState.in_combat)
            await state.update_data(puzzle=puzzle)
            
            text = (
                f"👣 {narration}\n\n"
                f"⚔️ **{puzzle['monster_name']}** (TIER {puzzle['tier']})\n"
                f"⏱ **60 detik tersisa!**\n"
                f"🧩 `\"{puzzle['question']}\"`"
            )
            await message.answer(text, parse_mode="Markdown", reply_markup=get_combat_keyboard())
            
            await asyncio.sleep(60) 
            if await state.get_state() == GameState.in_combat:
                p = get_player(user_id)
                damage = puzzle.get('damage', 5)
                new_hp = p['hp'] - damage
                if new_hp <= 0:
                    msg = reset_player_death(user_id, "death_combat")
                    await state.set_state(GameState.exploring)
                    await message.answer(f"🌑 **MATI.**\n\n{msg}", reply_markup=get_main_reply_keyboard())
                else:
                    update_player(user_id, {"hp": new_hp})
                    await message.answer(f"⚠️ **WAKTU HABIS!** HP -{damage}", reply_markup=get_main_reply_keyboard())
                    await state.set_state(GameState.exploring)
                
        elif event_type in ["npc_baik", "npc_jahat"]:
            await state.update_data(npc_data=event_data, current_npc_type=event_type)
            req = event_data['requirement']
            detail_req = "Dia menawarkan petunjuk jalan." if req is None else f"Dia meminta: **{req['amount']} {req['name']}**"
            text = (f"👤 **{event_data['identity']}**\n*\"{event_data['dialog']}\"*\n\n💎 {detail_req}")
            await message.answer(text, reply_markup=get_npc_interaction_keyboard(req))
        else:
            await message.answer(f"👣 {narration}", reply_markup=get_main_reply_keyboard())

# --- COMBAT & TRANSACTION HANDLERS ---

@dp.message(GameState.in_combat)
async def combat_answer_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    puzzle = data.get("puzzle")
    if not puzzle: return

    is_correct, is_timeout = validate_answer(message.text, puzzle['answer'], puzzle['generated_time'], puzzle['timer'])

    if is_correct:
        p = get_player(user_id)
        reward = 100 if puzzle.get("is_boss") else 10
        update_player(user_id, {"kills": p['kills'] + 1, "gold": p['gold'] + reward})
        await state.set_state(GameState.exploring)
        await message.answer(f"✅ **BENAR!** (+{reward} Gold)", reply_markup=get_main_reply_keyboard())
    else:
        p = get_player(user_id)
        damage = puzzle.get('damage', 5)
        new_hp = p['hp'] - damage
        if new_hp <= 0:
            msg = reset_player_death(user_id, "death_combat")
            await state.set_state(GameState.exploring)
            await message.answer(f"🌑 **MATI.**\n\n{msg}", reply_markup=get_main_reply_keyboard())
        else:
            update_player(user_id, {"hp": new_hp})
            label = "WAKTU HABIS!" if is_timeout else "SALAH!"
            await message.answer(f"❌ **{label}** HP -{damage}. Coba lagi!")

@dp.callback_query(F.data == "npc_accept")
async def npc_accept_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    player = get_player(user_id)
    data = await state.get_data()
    npc_data = data.get("npc_data")
    if not npc_data: return

    req = npc_data['requirement']
    if req['type'] == "gold" and player['gold'] < req['amount']:
        return await callback.answer("❌ Gold tidak cukup!", show_alert=True)
    
    update_player(user_id, {"gold": player['gold'] - req['amount'] if req['type'] == "gold" else player['gold']})
    msg = "✅ **BERKAH.** Tubuhmu menguat!" if data.get("current_npc_type") == "npc_baik" else "❌ **DIRAMPOK!** Barangmu dibawa kabur."
    await callback.message.edit_text(msg)
    await callback.message.answer("Perjalanan berlanjut...", reply_markup=get_main_reply_keyboard())

@dp.callback_query(F.data == "npc_ignore")
async def npc_ignore_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GameState.exploring)
    await callback.message.edit_text("👣 Kamu mengabaikannya dan melangkah pergi.")
    await callback.message.answer("Perjalanan berlanjut...", reply_markup=get_main_reply_keyboard())

# --- STATUS & SHOP ---

@dp.message(GameState.exploring, F.text == "📊 Status")
async def status_handler(message: Message):
    p = get_player(message.from_user.id)
    text = f"📊 **Status Weaver**\n❤️ HP: {p['hp']}/{p['max_hp']} | 🔮 MP: {p['mp']}/{p['max_mp']}\n💰 Gold: {p['gold']} | 💀 Kills: {p['kills']}"
    await message.answer(text, reply_markup=get_main_reply_keyboard())

@dp.message(GameState.exploring, F.text == "🛒 Toko")
async def shop_handler(message: Message):
    p = get_player(message.from_user.id)
    await message.answer(f"⚖️ **Toko** (Gold: {p['gold']})\n\"Pilih pertukaranmu...\"", reply_markup=get_shop_keyboard())

# --- BOILERPLATE ---
async def main():
    auto_seed_content()
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
