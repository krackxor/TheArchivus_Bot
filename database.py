import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Memuat variabel dari .env
load_dotenv()

# Koneksi ke MongoDB Lokal
client = MongoClient("mongodb://localhost:27017/")
db = client["the_archivus_db"]

# Koleksi (Tables)
players_col = db["players"]
narratives_col = db["narratives"]

def get_player(user_id, username="Weaver"):
    """Mengambil data pemain atau membuat baru jika belum ada."""
    player = players_col.find_one({"user_id": user_id})
    if not player:
        new_player = {
            "user_id": user_id,
            "username": username,
            "hp": 100,
            "max_hp": 100,
            "mp": 50,      # Status awal MP untuk skill
            "max_mp": 50,
            "gold": 0,
            "kills": 0,
            "step_counter": 0,
            "last_seen": datetime.datetime.now()
        }
        players_col.insert_one(new_player)
        return new_player
    return player

def update_player(user_id, data):
    """Memperbarui data spesifik pemain."""
    players_col.update_one({"user_id": user_id}, {"$set": data})

def reset_player_death(user_id, cause):
    """Logika saat pemain mati: Reset status namun tetap menyimpan identitas."""
    # Kamu bisa menambahkan sistem pengurangan gold di sini jika mau
    players_col.update_one(
        {"user_id": user_id},
        {"$set": {
            "hp": 100,
            "mp": 50,
            "step_counter": 0,
            "gold": 0,    # Hukuman mati: Gold hangus (Roguelike)
            "kills": 0    # Kills reset karena tidak ada sistem level
        }}
    )
    
    if cause == "death_combat":
        return "Jiwamu hancur berkeping-keping. Archivus menarikmu kembali ke titik awal."
    else:
        return "Waktu telah memakan ingatanmu. Kamu terbangun tanpa mengetahui siapa dirimu."

def auto_seed_content():
    """Menyuntikkan naskah awal jika database narasi masih kosong."""
    if narratives_col.count_documents({}) == 0:
        print("[SISTEM] Database narasi kosong. Menyuntikkan naskah awal...")
        content = [
            # --- PERJALANAN AMAN ---
            {"category": "safe_travel", "text": "Hanya suara langkah kakimu yang bergema di lorong sunyi ini."},
            {"category": "safe_travel", "text": "Cahaya redup dari lentera Weaver-mu membelah kegelapan pekat."},
            {"category": "safe_travel", "text": "Kamu merasakan hembusan angin dingin, tapi tidak ada jendela di sini."},
            
            # --- EVENT MONSTER ---
            {"category": "monster_event", "text": "Tiba-tiba, bayangan di dinding memisahkan diri dan menyerang!"},
            {"category": "monster_event", "text": "Ruang di depanmu terdistorsi. Sesuatu yang haus akan memori muncul."},
            {"category": "monster_event", "text": "Langkahmu terhenti oleh geraman rendah dari balik kegelapan."},
            
            # --- EVENT NPC ---
            {"category": "npc_event", "text": "Seorang sosok berjubah duduk di sudut, menatapmu dengan mata kosong."},
            {"category": "npc_event", "text": "Suara bisikan memanggil namamu dari kegelapan di depan."},
            {"category": "npc_event", "text": "Kamu melihat seseorang sedang menulis di udara dengan jari yang gemetar."}
        ]
        narratives_col.insert_many(content)
        print(f"[SISTEM] {len(content)} Naskah berhasil disuntikkan!")

# Jalankan seeding saat file ini diimpor pertama kali
if __name__ == "__main__":
    auto_seed_content()
