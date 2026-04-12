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
    """Menggunakan Reply Keyboard untuk navigasi utama agar anti-flood & stabil di VPS"""
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
    """Visual Berwarna: Hijau (Kepercayaan) vs Merah (Kewaspadaan) - Update Feb 2026"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🤝 Beri {req['amount']} {req['name']}", callback_data="npc_accept", color="green")],
        [InlineKeyboardButton(text="👣 Abaikan & Pergi", callback_data="npc_ignore", color="red")]
    ])

# --- HANDLERS ---

@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    get_player(user_id, message.from_user.first_name)
    await state.set_state(GameState.exploring)
    
    text = (
        f"📜 **Selamat Datang di The Archivus, {message.from_user.first_name}.**\n\n"
        "Pilih arah langkahmu melalui tombol navigasi di bawah."
    )
    await message.answer(text, parse_mode="Markdown", reply_markup=get_main_reply_keyboard())

# --- NAVIGASI VIA REPLY KEYBOARD (TEKS) ---

@dp.message(GameState.exploring, F.text.in_(["⬆️ Utara", "⬅️ Barat", "Timur ➡️", "⬇️ Selatan"]))
async def move_text_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    arah = message.text
    event_type, event_data, narration = process_move(user_id)
    
    if event_type == "monster":
        player = get_player(user_id)
        puzzle = generate_battle_puzzle(player['kills'])
        puzzle['current_hint'] = "_" * len(puzzle['answer'])
        await state.set_state(GameState.in_combat)
        await state.update_data(puzzle=puzzle)
        
        text = (
            f"👣 Melangkah ke {arah}.\n{narration}\n\n"
            f"⚔️ **{puzzle['monster_name']} MUNCUL!**\n"
            f"Waktu: **{puzzle['timer']} detik**\n"
            f"🧩 `\"{puzzle['question']}\"`"
        )
        await message.answer(text, parse_mode="Markdown", reply_markup=get_combat_keyboard())
        
        await asyncio.sleep(puzzle['timer'])
        if await state.get_state() == GameState.in_combat:
            p = get_player(user_id)
            if puzzle.get("is_boss"):
                update_player(user_id, {"hp": 1, "gold": int(p['gold'] * 0.5)})
                await state.set_state(GameState.exploring)
                await message.answer("💥 **THE KEEPER MENGHANCURKANMU!**", reply_markup=get_main_reply_keyboard())
            else:
                new_hp = p['hp'] - 35
                if new_hp <= 0:
                    pesan = reset_player_death(user_id, "death_combat")
                    await state.set_state(GameState.exploring)
                    await message.answer(f"⌛ **HABIS WAKTU.**\n\n*{pesan}*", reply_markup=get_main_reply_keyboard())
                else:
                    update_player(user_id, {"hp": new_hp})
                    await message.answer(f"⚠️ **TERLALU LAMA!** HP -35 (Sisa: {new_hp}).")
                    
    elif event_type in ["npc_baik", "npc_jahat"]:
        await state.update_data(npc_data=event_data, current_npc_type=event_type)
        req = event_data['requirement']
        text = (
            f"👣 Melangkah ke {arah}.\n{narration}\n\n"
            f"👤 **{event_data['identity']}**:\n*\"{event_data['dialog']}\"*\n\n"
            f"💎 Minta: **{req['amount']} {req['name']}**"
        )
        await message.answer(text, parse_mode="Markdown", reply_markup=get_npc_interaction_keyboard(req))
    else:
        await message.answer(f"👣 {narration}", reply_markup=get_main_reply_keyboard())

# --- SYSTEM HANDLERS (STATUS & SHOP) ---

@dp.message(GameState.exploring, F.text == "📊 Status")
async def status_text_handler(message: Message):
    p = get_player(message.from_user.id)
    inv_list = ", ".join(p.get("inventory", [])) if p.get("inventory") else "Kosong"
    text = (
        f"📊 **Buku Catatan Weaver**\n"
        f"❤️ HP: {p['hp']}/{p['max_hp']} | 🔮 MP: {p['mp']}/{p['max_mp']}\n"
        f"💰 Gold: {p['gold']} | 💀 Kills: {p['kills']}\n"
        f"🎒 Tas: `{inv_list}`"
    )
    await message.answer(text, parse_mode="Markdown", reply_markup=get_main_reply_keyboard())

# --- NPC INTERACTION HANDLERS ---

@dp.callback_query(F.data == "npc_accept")
async def npc_accept_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    player = get_player(user_id)
    data = await state.get_data()
    npc_data = data.get("npc_data")
    req = npc_data['requirement']
    npc_type = data.get("current_npc_type")

    if req['type'] == "gold":
        if player['gold'] < req['amount']:
            await callback.answer(f"❌ Gold tidak cukup!", show_alert=True)
            return
        update_player(user_id, {"gold": player['gold'] - req['amount']})
    else:
        inventory = player.get("inventory", [])
        if req['id'] not in inventory:
            await callback.answer(f"❌ Kamu tidak memiliki {req['name']}!", show_alert=True)
            return
        inventory.remove(req['id'])
        update_player(user_id, {"inventory": inventory})

    if npc_type == "npc_baik":
        update_player(user_id, {"max_hp": player['max_hp'] + 20, "hp": player['max_hp'] + 20})
        pesan = "😇 **BERUNTUNG!** Tubuhmu terasa lebih kuat! (Max HP +20)"
    else:
        pesan = "💀 **TERTIPU!** Dia menghilang tertawa licik. Asetmu hilang."

    await callback.message.edit_text(pesan, reply_markup=None)
    await callback.message.answer("Perjalanan berlanjut...", reply_markup=get_main_reply_keyboard())
    await callback.answer()

@dp.callback_query(F.data == "npc_ignore")
async def npc_ignore_handler(callback: CallbackQuery):
    await callback.message.edit_text("👣 Kamu mengabaikannya.", reply_markup=None)
    await callback.message.answer("Kamu melangkah pergi.", reply_markup=get_main_reply_keyboard())
    await callback.answer()

# --- COMBAT HANDLER ---

@dp.message(GameState.in_combat)
async def combat_handler(message: Message, state: FSMContext):
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
        new_hp = p['hp'] - 35
        if new_hp <= 0:
            pesan = reset_player_death(user_id, "death_combat")
            await state.set_state(GameState.exploring)
            await message.answer(f"🌑 **MATI.**\n\n*{pesan}*", reply_markup=get_main_reply_keyboard())
        else:
            update_player(user_id, {"hp": new_hp})
            label = "WAKTU HABIS!" if is_timeout else "SALAH!"
            await message.answer(f"❌ **{label}** HP -35. Jawab lagi!")

# --- BOILERPLATE ---
async def main():
    auto_seed_content()
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
