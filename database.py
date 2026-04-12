from pymongo import MongoClient
import datetime

# Koneksi ke MongoDB (Ubah URI ini jika pakai Atlas atau password di VPS)
client = MongoClient("mongodb://localhost:27017/")
db = client["TheArchivus_Game"]

players_col = db["players"]
narratives_col = db["narratives"]

def auto_seed_content():
    """Mendeteksi database kosong dan otomatis menyuntikkan narasi dasar saat VPS nyala"""
    if narratives_col.count_documents({}) == 0:
        print("⚙️ [SISTEM] Database kosong terdeteksi. Menyuntikkan Naskah Archivus...")
        
        # Naskah Dasar (Kamu bisa tambahkan hingga ribuan di list ini nanti)
        base_narratives = [
            # -- NPC Bohong --
            {"category": "npc_dialog", "reason": "npc_lie", "text": "Ke Utara sana aman, aku bersumpah demi sisa nyawaku. Jangan lihat ke belakang."},
            {"category": "npc_dialog", "reason": "npc_lie", "text": "Matikan lenteramu sekarang! Monster di depan sangat membenci cahaya."},
            
            # -- NPC Jujur --
            {"category": "npc_dialog", "reason": "npc_honest", "text": "Hati-hati dengan bau karat di Selatan. Kematian menunggumu di sana!"},
            {"category": "npc_dialog", "reason": "npc_honest", "text": "Hanya jawaban teka-teki yang dibaca dari belakang yang bisa membunuh bayangan itu."},
            
            # -- Pesan Kematian --
            {"category": "death_note", "reason": "death_trap", "text": "Sial! Kau benar-benar melompat ke maut hanya karena lidah manisnya? Bangun, dasar naif!"},
            {"category": "death_note", "reason": "death_combat", "text": "Pedangmu tumpul, otakmu lebih tumpul lagi. Kau mati konyol. Berdiri!"}
        ]
        
        narratives_col.insert_many(base_narratives)
        print("✅ [SISTEM] Naskah Dasar berhasil ditanam. Archivus siap.")
    else:
        print(f"📚 [SISTEM] Database aman. Ditemukan {narratives_col.count_documents({})} narasi.")

def get_player(user_id, username="Weaver"):
    player = players_col.find_one({"user_id": user_id})
    if not player:
        new_player = {
            "user_id": user_id,
            "username": username,
            "hp": 100, "max_hp": 100,
            "mp": 50, "max_mp": 50,
            "gold": 0, "kills": 0,
            "step_counter": 0,
            "current_zone": "Default",
            "is_confused": False,
            "last_seen": datetime.datetime.now()
        }
        players_col.insert_one(new_player)
        return new_player
    return player

def update_player(user_id, update_data):
    players_col.update_one({"user_id": user_id}, {"$set": update_data})

def get_random_narrative(category, reason=None):
    query = {"category": category}
    if reason:
        query["reason"] = reason
        
    pipeline = [{"$match": query}, {"$sample": {"size": 1}}]
    result = list(narratives_col.aggregate(pipeline))
    return result[0]["text"] if result else "Keheningan menyelimuti Archivus..."
