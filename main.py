import asyncio
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
            [InlineKeyboardButton(text="👣 Abaikan & Pergi", callback_data="npc_ignore", color="red")]
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🤝 Beri {req['amount']} {req['name']}", callback_data="npc_accept", color="green")],
        [InlineKeyboardButton(text="👣 Abaikan & Pergi", callback_data="npc_ignore", color="red")]
    ])

# --- BASIC HANDLERS ---

@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    get_player(user_id, message.from_user.first_name)
    await state.set_state(GameState.exploring)
    await message.answer("📜 **The Archivus telah bangkit.**", reply_markup=get_main_reply_keyboard())

# --- NPC LOGIC ---

@dp.callback_query(F.data == "npc_follow")
async def npc_follow_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    npc_data = data.get("npc_data")
    if not npc_data: return
    
    is_liar = npc_data.get("is_liar")
    user_id = callback.from_user.id
    player = get_player(user_id)

    if is_liar:
        res = "💀 **DIKHIANATI!**\nSaran itu jebakan. Kabut pekat mencekik langkahmu!"
        update_player(user_id, {"mp": max(0, player['mp'] - 15)})
    else:
        res = "😇 **TERBANTU.**\nSaran itu benar. Kamu menemukan jalan pintas yang aman."
        update_player(user_id, {"mp": min(player['max_mp'], player['mp'] + 20)})

    await callback.message.edit_text(res)
    await callback.message.answer("Melanjutkan langkah...", reply_markup=get_main_reply_keyboard())
    await callback.answer()

@dp.callback_query(F.data == "npc_accept")
async def npc_accept_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    player = get_player(user_id)
    data = await state.get_data()
    npc_data = data.get("npc_data")
    if not npc_data: return

    req = npc_data['requirement']
    npc_type = data.get("current_npc_type")

    if req['type'] == "gold":
        if player['gold'] < req['amount']:
            await callback.answer("❌ Gold tidak cukup!", show_alert=True)
            return
        update_player(user_id, {"gold": player['gold'] - req['amount']})
    else:
        inventory = player.get("inventory", [])
        if req['id'] not in inventory:
            await callback.answer(f"❌ Tidak punya {req['name']}!", show_alert=True)
            return
        inventory.remove(req['id'])
        update_player(user_id, {"inventory": inventory})

    if npc_type == "npc_baik":
        update_player(user_id, {"max_hp": player['max_hp'] + 20, "hp": player['max_hp'] + 20})
        msg = "✅ **BERKAH.**\nPengorbananmu dibalas mantra suci. Tubuhmu menguat!"
    else:
        msg = "❌ **DIRAMPOK!**\nDia lenyap tertawa. Kamu berdiri mematung, rugi besar."

    await callback.message.edit_text(msg)
    await callback.message.answer("Melanjutkan langkah...", reply_markup=get_main_reply_keyboard())
    await callback.answer()

# --- CORE MOVE HANDLER (DAMAGE DINAMIS) ---

@dp.message(GameState.exploring, F.text.in_(["⬆️ Utara", "⬅️ Barat", "Timur ➡️", "⬇️ Selatan"]))
async def move_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    event_type, event_data, narration = process_move(user_id)
    
    if event_type == "monster":
        player = get_player(user_id)
        puzzle = generate_battle_puzzle(player['kills'])
        puzzle['current_hint'] = "_" * len(puzzle['answer'])
        
        await state.set_state(GameState.in_combat)
        await state.update_data(puzzle=puzzle)
        
        # UI Combat menampilkan Tier
        tier_label = f"TIER {puzzle['tier']}" if not puzzle['is_boss'] else "⚠️ BOSS"
        text = (
            f"👣 {narration}\n\n"
            f"⚔️ **{puzzle['monster_name']}** ({tier_label})\n"
            f"⏱ **60 detik tersisa!**\n"
            f"🧩 `\"{puzzle['question']}\"`"
        )
        await message.answer(text, parse_mode="Markdown", reply_markup=get_combat_keyboard())
        
        # Menunggu Jawaban (1 Menit)
        await asyncio.sleep(puzzle['timer'])
        
        current_state = await state.get_state()
        if current_state == GameState.in_combat:
            p = get_player(user_id)
            damage_taken = puzzle.get('damage', 5) # Ambil damage dari tier monster
            new_hp = p['hp'] - damage_taken
            
            if new_hp <= 0:
                msg = reset_player_death(user_id, "death_combat")
                await state.set_state(GameState.exploring)
                await message.answer(f"🌑 **MATI.**\n\n{msg}", reply_markup=get_main_reply_keyboard())
            else:
                update_player(user_id, {"hp": new_hp})
                await message.answer(
                    f"⚠️ **WAKTU HABIS!**\n"
                    f"{puzzle['monster_name']} melukaimu: **-{damage_taken} HP**.\n"
                    f"Sisa HP: {new_hp}", 
                    reply_markup=get_main_reply_keyboard()
                )
                await state.set_state(GameState.exploring)
            
    elif event_type in ["npc_baik", "npc_jahat"]:
        await state.update_data(npc_data=event_data, current_npc_type=event_type)
        req = event_data['requirement']
        detail_req = "Dia ingin memberimu petunjuk jalan." if req is None else f"Dia meminta: **{req['amount']} {req['name']}**"

        text = (f"👤 **{event_data['identity']}**:\n*\"{event_data['dialog']}\"*\n\n💎 {detail_req}")
        await message.answer(text, parse_mode="Markdown", reply_markup=get_npc_interaction_keyboard(req))
    else:
        await message.answer(f"👣 {narration}", reply_markup=get_main_reply_keyboard())

# --- COMBAT HANDLER (JAWABAN SALAH) ---

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
        damage_taken = puzzle.get('damage', 5) # Damage sesuai tier
        new_hp = p['hp'] - damage_taken
        
        if new_hp <= 0:
            msg = reset_player_death(user_id, "death_combat")
            await state.set_state(GameState.exploring)
            await message.answer(f"🌑 **MATI.**\n\n{msg}", reply_markup=get_main_reply_keyboard())
        else:
            update_player(user_id, {"hp": new_hp})
            label = "WAKTU HABIS!" if is_timeout else "SALAH!"
            await message.answer(f"❌ **{label}** HP -{damage_taken}. Coba lagi!")

# --- SISTEM HANDLERS ---

@dp.message(GameState.exploring, F.text == "📊 Status")
async def status_handler(message: Message):
    p = get_player(message.from_user.id)
    inv = ", ".join(p.get("inventory", [])) if p.get("inventory") else "Kosong"
    text = f"📊 **Status Weaver**\n❤️ HP: {p['hp']}/{p['max_hp']} | 🔮 MP: {p['mp']}/{p['max_mp']}\n💰 Gold: {p['gold']} | 💀 Kills: {p['kills']}\n🎒 Tas: `{inv}`"
    await message.answer(text, parse_mode="Markdown", reply_markup=get_main_reply_keyboard())

@dp.message(GameState.exploring, F.text == "🛒 Toko")
async def shop_handler(message: Message):
    player = get_player(message.from_user.id)
    text = f"⚖️ **Toko** (Gold: {player['gold']})\n\"Apa yang kau cari, pengembara?\""
    await message.answer(text, reply_markup=get_shop_keyboard())

# --- BOILERPLATE ---
async def main():
    auto_seed_content()
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
