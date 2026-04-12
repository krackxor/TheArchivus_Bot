import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart

# Import dari mesin The Archivus yang sudah kita buat
from engine import process_move
from database import get_player, auto_seed_content

TOKEN = "TOKEN_BOT_MU_DI_SINI"

# Inisialisasi Dispatcher
dp = Dispatcher()

def get_nav_keyboard():
    """Membuat susunan tombol Inline Keyboard ala Aiogram"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Utara ⬆️", callback_data="move_utara")],
        [InlineKeyboardButton(text="Barat ⬅️", callback_data="move_barat"), 
         InlineKeyboardButton(text="Timur ➡️", callback_data="move_timur")],
        [InlineKeyboardButton(text="Selatan ⬇️", callback_data="move_selatan")],
        [InlineKeyboardButton(text="📊 Cek Status", callback_data="check_status")]
    ])

@dp.message(CommandStart())
async def start_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.first_name
    
    # Init player di MongoDB
    get_player(user_id, username)

    welcome_text = (
        f"📜 **Selamat Datang di The Archivus, {username}.**\n\n"
        "Dunia ini telah kehilangan ceritanya. Kamu adalah seorang Weaver, "
        "satu-satunya yang bisa menyusun kembali realita lewat kata-kata.\n\n"
        "Pilih arah jalanmu untuk mulai menjelajah."
    )
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=get_nav_keyboard())

@dp.callback_query(F.data == "check_status")
async def status_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    player = get_player(user_id)
    
    status_text = (
        f"📊 **Catatan {player['username']}**\n"
        f"❤️ HP: {player['hp']}/{player['max_hp']} | 🔮 MP: {player['mp']}/{player['max_mp']}\n"
        f"💰 Gold: {player['gold']} | 💀 Kills: {player['kills']}\n"
        f"📍 Kewaspadaan: {player['step_counter']}/15"
    )
    # Kirim pesan status dan berikan tombol navigasi lagi
    await callback.message.answer(status_text, reply_markup=get_nav_keyboard())
    # Wajib memanggil answer() agar tombol di Telegram tidak loading terus
    await callback.answer()

@dp.callback_query(F.data.startswith("move_"))
async def move_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    arah = callback.data.split("_")[1].capitalize()
    
    # Memanggil mesin 3-15 langkah
    event_type, event_data, narration = process_move(user_id)
    
    # Edit pesan tombol yang ditekan menjadi narasi perjalanan
    await callback.message.edit_text(f"👣 Kamu berjalan ke {arah}.\n{narration}")
    
    # Reaksi terhadap Event
    if event_type in ["npc_baik", "npc_jahat"]:
        npc_name = event_data["identity"]
        npc_dialog = event_data["dialog"]
        text = (
            f"👤 **Seseorang muncul!**\n\n"
            f"Kamu bertemu {npc_name}.\n"
            f"Dia berbisik: *\"{npc_dialog}\"*"
        )
        await callback.message.answer(text, parse_mode="Markdown", reply_markup=get_nav_keyboard())
        
    elif event_type == "monster":
        monster_name = event_data["name"]
        text = f"⚔️ **AWAS!**\n**{monster_name}** menghadang jalanmu!"
        await callback.message.answer(text, parse_mode="Markdown", reply_markup=get_nav_keyboard())
        
    else:
        # Jika aman (safe), munculkan tombol arah lagi untuk langkah berikutnya
        await callback.message.answer("Area ini terasa kosong. Ke mana selanjutnya?", reply_markup=get_nav_keyboard())
        
    await callback.answer()

async def main():
    # 1. Jalankan pengecekan dan suntik database MongoDB
    auto_seed_content()

    # 2. Bangun bot dengan Aiogram
    bot = Bot(token=TOKEN)
    
    print("👁️ The Archivus telah bangkit dengan Aiogram. Bot sedang mendengarkan...")
    
    # 3. Jalankan polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
