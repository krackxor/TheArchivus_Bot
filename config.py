import os
from dotenv import load_dotenv

# Memuat isi dari file .env ke dalam sistem
load_dotenv()

# Mengambil variabel rahasia
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/") # Beri default lokal jika kosong
DB_NAME = os.getenv("DB_NAME", "TheArchivus_Game")

# Validasi Keamanan: Matikan bot jika Token tidak ditemukan
if not BOT_TOKEN:
    raise ValueError("⚠️ FATAL ERROR: BOT_TOKEN tidak ditemukan di file .env!")
