import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from engine import process_move
from database import get_player, update_player, auto_seed_content, reset_player_death
from combat import generate_battle_puzzle, validate_answer
from states import GameState
from config import BOT_TOKEN  # <-- Mengambil token aman dari config.py

dp = Dispatcher()

def get_nav_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬆️ Utara", callback_data="move_utara")],
        [InlineKeyboardButton(text="⬅️ Barat", callback_data="move_barat"), InlineKeyboardButton(text="Timur ➡️", callback_data="move_timur")],
        [InlineKeyboardButton(text="⬇️ Selatan", callback_data="move_selatan")],
        [InlineKeyboardButton(text="📊 Cek Status", callback_data="check_status")]
    ])

@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    get_player(user_id, message.from_user.first_name)
    await state.set_state(GameState.exploring)
    
    text = (
        f"📜 **Selamat Datang di The Archivus, {message.from_user.first_name}.**\n\n"
        "Dunia ini telah kehilangan ceritanya. Kamu adalah seorang Weaver, "
        "satu-satunya yang bisa menyusun kembali realita lewat kata-kata.\n\n"
        "Pilih arah jalanmu di bawah ini untuk mulai menjelajah."
    )
    await message.answer(text, parse_mode="Markdown", reply_markup=get_nav_keyboard())

@dp.callback_query(GameState.exploring, F.data == "check_status")
async def status_handler(callback: CallbackQuery):
    p = get_player(callback.from_user.id)
    text = f"📊 **Buku Catatan Weaver**\n❤️ HP: {p['hp']}/{p['max_hp']} | 🔮 MP: {p['mp']}/{p['max_mp']}\n💰 Gold: {p['gold']} | 💀 Kills: {p['kills']}\n📍 Kewaspadaan: {p['step_counter']}/15"
    await callback.message.edit_text(text, reply_markup=get_nav_keyboard())
    await callback.answer()

@dp.callback_query(GameState.exploring, F.data.startswith("move_"))
async def move_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    arah = callback.data.split("_")[1].capitalize()
    event_type, event_data, narration = process_move(user_id)
    
    if event_type == "monster":
        player = get_player(user_id)
        puzzle = generate_battle_puzzle(player['kills'])
        await state.set_state(GameState.in_combat)
        await state.update_data(puzzle=puzzle)
        
        text = f"👣 Kamu melangkah ke {arah}.\n{narration}\n\n⚔️ **{puzzle['monster_name']} MUNCUL!**\nCepat ketik jawabanmu dalam **{puzzle['timer']} detik**:\n🔥 `\"{puzzle['question']}\"`"
        await callback.message.edit_text(text, parse_mode="Markdown")
        
    elif event_type in ["npc_baik", "npc_jahat"]:
        text = f"👣 Kamu melangkah ke {arah}.\n{narration}\n\n👤 **{event_data['identity']}** mendekat dan berbisik:\n*\"{event_data['dialog']}\"*"
        await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_nav_keyboard())
        
    else:
        text = f"👣 Kamu berjalan ke {arah}.\n{narration}\nArea ini terasa aman. Ke mana selanjutnya?"
        await callback.message.edit_text(text, reply_markup=get_nav_keyboard())
    
    await callback.answer()

@dp.message(GameState.in_combat)
async def combat_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    puzzle = data.get("puzzle")
    
    is_correct, is_timeout = validate_answer(message.text, puzzle['answer'], puzzle['generated_time'], puzzle['timer'])

    if is_correct:
        player = get_player(user_id)
        update_player(user_id, {"kills": player['kills'] + 1, "gold": player['gold'] + 10})
        await state.set_state(GameState.exploring)
        await message.answer("✅ **BENAR!**\nMonster hancur menjadi debu (+10 Gold).", reply_markup=get_nav_keyboard())
    else:
        player = get_player(user_id)
        new_hp = player['hp'] - 35
        
        if new_hp <= 0:
            pesan_mati = reset_player_death(user_id, "death_combat")
            await state.set_state(GameState.exploring)
            await message.answer(f"🌑 **KEMATIAN MENJEMPUT.**\n\n*{pesan_mati}*\n\n📍 Kamu terbangun kembali.", parse_mode="Markdown", reply_markup=get_nav_keyboard())
        else:
            update_player(user_id, {"hp": new_hp})
            label = "WAKTU HABIS!" if is_timeout else "JAWABAN SALAH!"
            await message.answer(f"❌ **{label}**\nHP kamu berkurang! (Sisa: {new_hp}). Cepat jawab lagi!")

async def main():
    auto_seed_content()
    bot = Bot(token=BOT_TOKEN) # <-- Bot sekarang menggunakan token dari file .env
    print("👁️ The Archivus telah bangkit. Bot sedang mendengarkan...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
