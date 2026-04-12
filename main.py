import asyncio
import time
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext

from engine import process_move
from database import get_player, update_player, auto_seed_content, reset_player_death
from combat import generate_battle_puzzle, validate_answer
from states import GameState

TOKEN = "TOKEN_BOT_MU_DI_SINI"
dp = Dispatcher()

def get_nav_keyboard():
    """Membuat susunan tombol navigasi utama"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬆️ Utara", callback_data="move_utara")],
        [InlineKeyboardButton(text="⬅️ Barat", callback_data="move_barat"), 
         InlineKeyboardButton(text="Timur ➡️", callback_data="move_timur")],
        [InlineKeyboardButton(text="⬇️ Selatan", callback_data="move_selatan")],
        [InlineKeyboardButton(text="📊 Cek Status", callback_data="check_status")]
    ])

# --- HANDLER: START (AWAL PERMAINAN) ---
@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    get_player(user_id, message.from_user.first_name)
    
    # Kunci status pemain ke mode jalan-jalan
    await state.set_state(GameState.exploring)
    
    welcome_text = (
        f"📜 **Selamat Datang di The Archivus, {message.from_user.first_name}.**\n\n"
        "Dunia ini telah kehilangan ceritanya. Kamu adalah seorang Weaver, "
        "satu-satunya yang bisa menyusun kembali realita lewat kata-kata.\n\n"
        "Pilih arah jalanmu di bawah ini untuk mulai menjelajah."
    )
    # Munculkan tombol navigasi
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=get_nav_keyboard())

# --- HANDLER: CEK STATUS (TOMBOL) ---
@dp.callback_query(GameState.exploring, F.data == "check_status")
async def status_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    player = get_player(user_id)
    
    status_text = (
        f"📊 **Buku Catatan Weaver**\n"
        f"❤️ HP: {player['hp']}/{player['max_hp']} | 🔮 MP: {player['mp']}/{player['max_mp']}\n"
        f"💰 Gold: {player['gold']} | 💀 Kills: {player['kills']}\n"
        f"📍 Kewaspadaan: {player['step_counter']}/15"
    )
    # Edit pesan yang ditekan menjadi status, lalu kembalikan tombol navigasi
    await callback.message.edit_text(status_text, reply_markup=get_nav_keyboard())
    await callback.answer()

# --- HANDLER: BERJALAN (TOMBOL ARAH) ---
@dp.callback_query(GameState.exploring, F.data.startswith("move_"))
async def move_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    arah = callback.data.split("_")[1].capitalize()
    
    event_type, event_data, narration = process_move(user_id)
    
    if event_type == "monster":
        player = get_player(user_id)
        puzzle = generate_battle_puzzle(player['kills'])
        
        # Pindah ke mode pertarungan
        await state.set_state(GameState.in_combat)
        await state.update_data(puzzle=puzzle)
        
        text = (
            f"👣 Kamu melangkah ke {arah}.\n{narration}\n\n"
            f"⚔️ **{puzzle['monster_name']} MUNCUL!**\n"
            f"Cepat ketik jawabanmu dalam **{puzzle['timer']} detik**:\n\n"
            f"🔥 `\"{puzzle['question']}\"`"
        )
        # Hilangkan tombol navigasi agar pemain fokus mengetik jawaban
        await callback.message.edit_text(text, parse_mode="Markdown")
    
    elif event_type in ["npc_baik", "npc_jahat"]:
        text = (
            f"👣 Kamu melangkah ke {arah}.\n{narration}\n\n"
            f"👤 **{event_data['identity']}** mendekat dan berbisik:\n"
            f"*\"{event_data['dialog']}\"*"
        )
        # Munculkan narasi NPC, lalu kembalikan tombol navigasi
        await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_nav_keyboard())
    
    else:
        text = f"👣 Kamu berjalan ke {arah}.\n{narration}\nArea ini terasa aman. Ke mana selanjutnya?"
        await callback.message.edit_text(text, reply_markup=get_nav_keyboard())
    
    await callback.answer()

# --- HANDLER: JAWAB PUZZLE (KETIK TEKS) ---
@dp.message(GameState.in_combat)
async def combat_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    puzzle = data.get("puzzle")
    
    is_correct, is_timeout = validate_answer(
        user_answer=message.text,
        correct_answer=puzzle['answer'],
        generated_time=puzzle['generated_time'],
        time_limit=puzzle['timer']
    )

    if is_correct:
        # MENANG - Kembalikan ke mode exploring dan berikan tombol
        player = get_player(user_id)
        update_player(user_id, {"kills": player['kills'] + 1, "gold": player['gold'] + 10})
        await state.set_state(GameState.exploring)
        
        text = "✅ **BENAR!**\nMonster hancur menjadi debu (+10 Gold). Ke mana selanjutnya?"
        await message.answer(text, parse_mode="Markdown", reply_markup=get_nav_keyboard())
    
    else:
        # KALAH / TIMEOUT
        player = get_player(user_id)
        new_hp = player['hp'] - 35
        
        if new_hp <= 0:
            # MATI - Kembalikan ke mode exploring, berikan pesan kematian dan tombol
            pesan_mati = reset_player_death(user_id, "death_combat")
            await state.set_state(GameState.exploring)
            
            text = (
                f"🌑 **KEMATIAN MENJEMPUT.**\n\n"
                f"*{pesan_mati}*\n\n"
                f"📍 Kamu terbangun kembali. Tentukan arah barumu."
            )
            await message.answer(text, parse_mode="Markdown", reply_markup=get_nav_keyboard())
        else:
            # MASIH HIDUP - Tidak ada tombol navigasi karena masih harus jawab
            update_player(user_id, {"hp": new_hp})
            label = "WAKTU HABIS!" if is_timeout else "JAWABAN SALAH!"
            text = f"❌ **{label}**\nHP kamu berkurang! (Sisa: {new_hp}). Cepat jawab lagi!"
            await message.answer(text, parse_mode="Markdown")

async def main():
    auto_seed_content()
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
