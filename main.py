# main.py

import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher

# === PENGATURAN & DATABASE ===
from config import BOT_TOKEN
from database import auto_seed_content

# === IMPORT SEMUA HANDLER (ARSITEKTUR BARU) ===
# Pastikan folder game/handlers/ memiliki file __init__.py (kosong tidak apa-apa)
from game.handlers import admin, start, exploration, menu, event, combat

async def main():
    # Aktifkan logging dengan format yang lebih detail agar error mudah dilacak
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        stream=sys.stdout
    )

    # 1. Jalankan seed konten awal (NPC, Item, dll) ke database
    auto_seed_content()

    # 2. Inisialisasi Bot & Dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # 3. DAFTARKAN SEMUA ROUTER (URUTAN = PRIORITAS)
    # PERBAIKAN: Router dengan spesifikasi/state ketat harus di atas, 
    # sedangkan router umum (jalan kaki) diletakkan paling bawah.
    dp.include_router(admin.router)       # 1. Prioritas Tertinggi (Bypass State /give, dll)
    dp.include_router(start.router)       # 2. Perintah Dasar (/start, /help)
    dp.include_router(combat.router)      # 3. Sistem Pertarungan (State: in_combat)
    dp.include_router(event.router)       # 4. Event Interaksi (Callback: pool_, exec_, dll)
    dp.include_router(menu.router)        # 5. UI Menu (Profil, Tas, Ramuan, Bengkel)
    dp.include_router(exploration.router) # 6. Prioritas Terendah (Navigasi Arah Umum)

    logging.info("🔮 The Archivus Bot berhasil bangkit dengan Arsitektur Baru!")

    # 4. Mulai bot dengan pembersihan sesi yang aman
    await bot.delete_webhook(drop_pending_updates=True)
    
    try:
        await dp.start_polling(bot)
    finally:
        # PERBAIKAN: Pastikan koneksi aiohttp tertutup sempurna saat bot dimatikan
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Sistem The Archivus dimatikan dengan aman.")
