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

# --- LOKASI ENDLESS ---
LOCATIONS = [
    "The Whispering Hall", "Forgotten Script-Vault", 
    "The Inky Mire", "Echoing Abyss", "The Final Archive"
]

def get_player(user_id, username="Weaver"):
    """Mengambil data pemain atau membuat baru jika belum ada."""
    player = players_col.find_one({"user_id": user_id})
    
    if not player:
        new_player = {
            "user_id": user_id,
            "username": username,
            "hp": 100,
            "max_hp": 100,
            "mp": 50,
            "max_mp": 50,
            "gold": 0,
            "kills": 0,
            "inventory": [],
            "step_counter": 0,
            # --- FIELD ENDLESS BARU ---
            "cycle": 1,
            "location": LOCATIONS[0],
            "history": [],
            "monster_streak": 0,
            "steps_since_event": 0,
            "miniboss_slain": False,
            "last_seen": datetime.datetime.now()
        }
        players_col.insert_one(new_player)
        return new_player
    
    # --- LOGIKA MIGRASI OTOMATIS ---
    # Update pemain lama dengan field Endless jika belum ada (tanpa error)
    updates = {}
    if "inventory" not in player: updates["inventory"] = []
    if "cycle" not in player: updates["cycle"] = 1
    if "location" not in player: updates["location"] = LOCATIONS[0]
    if "history" not in player: updates["history"] = []
    if "monster_streak" not in player: updates["monster_streak"] = 0
    if "steps_since_event" not in player: updates["steps_since_event"] = 0
    if "miniboss_slain" not in player: updates["miniboss_slain"] = False

    if updates:
        players_col.update_one({"user_id": user_id}, {"$set": updates})
        player.update(updates)
        
    return player

def update_player(user_id, data):
    """Memperbarui data spesifik pemain."""
    players_col.update_one({"user_id": user_id}, {"$set": data})

def add_history(user_id, event_text):
    """Mencatat sejarah epik pemain ke MongoDB"""
    player = get_player(user_id)
    log = f"[Siklus {player['cycle']} - {player['location']}] {event_text}"
    
    history = player.get("history", [])
    history.append(log)
    
    # Simpan max 10 sejarah terakhir agar memori rapi
    if len(history) > 10:
        history.pop(0)
        
    update_player(user_id, {"history": history})

def reset_player_death(user_id, cause):
    """Logika Endless Roguelite: Penalti kematian tanpa menghapus sejarah."""
    player = get_player(user_id)
    
    # Catat kematian di sejarah
    add_history(user_id, f"Gugur karena {cause}.")
    
    # Penalti: HP/MP balik, Gold hilang 50, Item hilang, Kills reset.
    # TAPI Cycle dan History TETAP AMAN.
    new_gold = max(0, player["gold"] - 50)
    
    players_col.update_one(
        {"user_id": user_id},
        {"$set": {
            "hp": player.get("max_hp", 100),
            "mp": player.get("max_mp", 50),
            "step_counter": 0,
            "gold": new_gold,
            "kills": 0, 
            "inventory": [],
            "monster_streak": 0,
            "steps_since_event": 0
        }}
    )
    
    if cause == "death_combat":
        return "Jiwamu hancur berkeping-keping. Archivus menarikmu kembali ke titik awal tanpa membawa apa pun, namun sejarahmu tetap tertulis."
    else:
        return "Waktu telah memakan ingatanmu. Kamu terbangun dalam kehampaan dengan tas yang kosong."

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
            
            # --- EVENT NPC ---
            {"category": "npc_event", "text": "Seorang sosok berjubah duduk di sudut, menatapmu dengan mata kosong."},
            {"category": "npc_event", "text": "Suara bisikan memanggil namamu dari kegelapan di depan."}
        ]
        narratives_col.insert_many(content)
        print(f"[SISTEM] {len(content)} Naskah berhasil disuntikkan!")

if __name__ == "__main__":
    auto_seed_content()
