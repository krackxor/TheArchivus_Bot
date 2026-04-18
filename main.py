# main.py

import asyncio
import logging
from aiogram import Bot, Dispatcher

# === PENGATURAN & DATABASE ===
from config import BOT_TOKEN
from database import auto_seed_content

# === IMPORT SEMUA HANDLER (ARSITEKTUR BARU) ===
# Pastikan folder game/handlers/ memiliki file __init__.py (kosong tidak apa-apa)
from game.handlers import admin, start, exploration, menu, event, combat

# Aktifkan logging agar error mudah dilacak di terminal
logging.basicConfig(level=logging.INFO)

async def main():
    # 1. Jalankan seed konten awal (NPC, Item, dll) ke database
    auto_seed_content()

    # 2. Inisialisasi Bot & Dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # 3. DAFTARKAN SEMUA ROUTER (JALUR KODE)
    # Catatan: Urutan pendaftaran ini penting untuk mengatur prioritas baca bot
    dp.include_router(admin.router)       # Perintah Admin (/give, dll)
    dp.include_router(start.router)       # Perintah /start dan /help
    dp.include_router(exploration.router) # Sistem Jalan Kaki & Meditasi
    dp.include_router(menu.router)        # UI Profil, Tas, Ramuan, Bengkel
    dp.include_router(event.router)       # Interaksi NPC, Puzzle, dan Landmark
    dp.include_router(combat.router)      # Sistem Pertarungan (Attack, Skill, Block, Dodge)

    print("🔮 The Archivus Bot berhasil bangkit dengan Arsitektur Baru!")

    # 4. Mulai bot (drop_pending_updates agar bot tidak membalas chat spam saat ia mati)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Sistem The Archivus dimatikan dengan aman.")
