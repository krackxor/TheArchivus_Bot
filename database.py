from pymongo import MongoClient
import datetime

# 1. Koneksi ke MongoDB
# Jika kamu pakai MongoDB Lokal: "mongodb://localhost:27017/"
# Jika kamu pakai MongoDB Atlas, ganti dengan URI dari Atlas.
client = MongoClient("mongodb://localhost:27017/")
db = client["TheArchivus_Game"]

# Koleksi Data
players_col = db["players"]
narratives_col = db["narratives"]

def get_player(user_id, username="Weaver"):
    """Mengambil data pemain. Jika belum ada, buat baru."""
    player = players_col.find_one({"user_id": user_id})
    
    if not player:
        # Skema awal pemain saat pertama kali terbangun di Archivus
        new_player = {
            "user_id": user_id,
            "username": username,
            "hp": 100,
            "max_hp": 100,
            "mp": 50,
            "max_mp": 50,
            "gold": 0,
            "kills": 0,
            "step_counter": 0,          # Counter untuk logika 3-15 langkah
            "current_zone": "Default",
            "is_confused": False,       # Status jika tertipu NPC jahat
            "last_seen": datetime.datetime.now()
        }
        players_col.insert_one(new_player)
        return new_player
    return player

def update_player(user_id, update_data):
    """Mengupdate status pemain (HP, Gold, Langkah, dll)"""
    players_col.update_one(
        {"user_id": user_id}, 
        {"$set": update_data}
    )

def get_random_narrative(category, reason=None):
    """
    Mengambil 1 narasi dari 1.000 list secara acak yang 'Pas'.
    category: 'death_note', 'npc_dialog'
    reason: 'npc_lie', 'monster_combat', 'timeout', dll.
    """
    query = {"category": category}
    if reason:
        query["reason"] = reason
    
    # Menggunakan agregasi $sample untuk mengambil data acak di MongoDB
    pipeline = [
        {"$match": query},
        {"$sample": {"size": 1}}
    ]
    
    result = list(narratives_col.aggregate(pipeline))
    if result:
        return result[0]["text"]
    return "Keheningan menyelimuti Archivus... (Narasi belum tersedia)"
