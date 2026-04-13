import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Memuat variabel dari .env
load_dotenv()

# Koneksi ke MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["the_archivus_db"]

# Koleksi (Tables)
players_col = db["players"]
narratives_col = db["narratives"]
leaderboard_col = db["leaderboard"]

# --- LOKASI ENDLESS ---
LOCATIONS = [
    "The Whispering Hall", 
    "Forgotten Script-Vault", 
    "The Inky Mire", 
    "Echoing Abyss", 
    "The Final Archive"
]

def get_player(user_id, username="Weaver"):
    """Mengambil data pemain atau membuat baru jika belum ada (ENHANCED)"""
    player = players_col.find_one({"user_id": user_id})
    
    if not player:
        new_player = {
            "user_id": user_id,
            "username": username,
            
            # Basic Stats
            "hp": 100,
            "max_hp": 100,
            "mp": 50,
            "max_mp": 50,
            "gold": 0,
            "kills": 0,
            "boss_kills": 0,
            
            # Progression System (NEW)
            "level": 1,
            "exp": 0,
            "exp_needed": 100,
            
            # Inventory & Items
            "inventory": [],
            
            # Endless System
            "cycle": 1,
            "location": LOCATIONS[0],
            "history": [],
            "step_counter": 0,
            "monster_streak": 0,
            "steps_since_event": 0,
            "miniboss_slain": False,
            
            # Combat System (NEW)
            "current_combo": 0,
            "max_combo_reached": 0,
            "flawless_boss_count": 0,
            
            # Achievement & Quest System (NEW)
            "achievements_unlocked": [],
            "daily_quests": [],
            "daily_stats": {},
            "last_login": None,
            
            # Tracking untuk Easter Eggs (NEW)
            "recent_moves": [],
            "total_gold_earned": 0,
            "locations_visited": [LOCATIONS[0]],
            "trap_survived": 0,
            "quiz_correct_count": 0,
            
            # Buffs & Debuffs (NEW) - TERMASUK RESIN/MANTRA
            "active_buffs": [],
            "active_resin": None, # Menyimpan elemen mantra sementara (misal: "Api")
            "resin_duration": 0,  # Berapa turn lagi mantra aktif
            "has_companion": False,
            "companion_duration": 0,
            
            # Leaderboard Stats (NEW)
            "highest_cycle": 1,
            "highest_combo": 0,
            "total_playtime": 0,
            
            # Timestamps
            "created_at": datetime.datetime.now(),
            "last_seen": datetime.datetime.now()
        }
        players_col.insert_one(new_player)
        return new_player
    
    # --- LOGIKA MIGRASI OTOMATIS (ENHANCED) ---
    updates = {}
    
    # Basic fields
    if "inventory" not in player: updates["inventory"] = []
    if "cycle" not in player: updates["cycle"] = 1
    if "location" not in player: updates["location"] = LOCATIONS[0]
    if "history" not in player: updates["history"] = []
    if "monster_streak" not in player: updates["monster_streak"] = 0
    if "steps_since_event" not in player: updates["steps_since_event"] = 0
    if "miniboss_slain" not in player: updates["miniboss_slain"] = False
    if "boss_kills" not in player: updates["boss_kills"] = 0
    
    # NEW Progression fields
    if "level" not in player: updates["level"] = 1
    if "exp" not in player: updates["exp"] = 0
    if "exp_needed" not in player: updates["exp_needed"] = 100
    
    # NEW Combat fields
    if "current_combo" not in player: updates["current_combo"] = 0
    if "max_combo_reached" not in player: updates["max_combo_reached"] = 0
    if "flawless_boss_count" not in player: updates["flawless_boss_count"] = 0
    
    # NEW Achievement fields
    if "achievements_unlocked" not in player: updates["achievements_unlocked"] = []
    if "daily_quests" not in player: updates["daily_quests"] = []
    if "daily_stats" not in player: updates["daily_stats"] = {}
    if "last_login" not in player: updates["last_login"] = None
    
    # NEW Tracking fields
    if "recent_moves" not in player: updates["recent_moves"] = []
    if "total_gold_earned" not in player: updates["total_gold_earned"] = 0
    if "locations_visited" not in player: updates["locations_visited"] = [player.get('location', LOCATIONS[0])]
    if "trap_survived" not in player: updates["trap_survived"] = 0
    if "quiz_correct_count" not in player: updates["quiz_correct_count"] = 0
    
    # NEW Buff fields (Resin System)
    if "active_buffs" not in player: updates["active_buffs"] = []
    if "active_resin" not in player: updates["active_resin"] = None
    if "resin_duration" not in player: updates["resin_duration"] = 0
    if "has_companion" not in player: updates["has_companion"] = False
    if "companion_duration" not in player: updates["companion_duration"] = 0
    
    # NEW Leaderboard fields
    if "highest_cycle" not in player: 
        updates["highest_cycle"] = player.get('cycle', 1)
    if "highest_combo" not in player: updates["highest_combo"] = 0
    if "total_playtime" not in player: updates["total_playtime"] = 0
    
    if updates:
        players_col.update_one({"user_id": user_id}, {"$set": updates})
        player.update(updates)
    
    # Update last seen
    players_col.update_one(
        {"user_id": user_id},
        {"$set": {"last_seen": datetime.datetime.now()}}
    )
        
    return player

def update_player(user_id, data):
    """Memperbarui data spesifik pemain"""
    # Auto-update highest stats untuk leaderboard
    if 'cycle' in data:
        player = players_col.find_one({"user_id": user_id})
        if player and data['cycle'] > player.get('highest_cycle', 0):
            data['highest_cycle'] = data['cycle']
    
    if 'current_combo' in data:
        player = players_col.find_one({"user_id": user_id})
        if player and data['current_combo'] > player.get('highest_combo', 0):
            data['highest_combo'] = data['current_combo']
    
    players_col.update_one({"user_id": user_id}, {"$set": data})

def add_history(user_id, event_text):
    """Mencatat sejarah epik pemain ke MongoDB"""
    player = get_player(user_id)
    log = f"[Siklus {player['cycle']} - {player['location']}] {event_text}"
    
    history = player.get("history", [])
    history.append(log)
    
    # Simpan max 20 sejarah terakhir
    if len(history) > 20:
        history.pop(0)
        
    update_player(user_id, {"history": history})

def reset_player_death(user_id, cause):
    """Logika Endless Roguelite: Penalti kematian tanpa menghapus sejarah (ENHANCED)"""
    player = get_player(user_id)
    
    # Catat kematian di sejarah
    add_history(user_id, f"Gugur karena {cause}.")
    
    # Penalti yang lebih graduated berdasarkan cycle
    cycle = player.get('cycle', 1)
    
    # Gold loss: 30% di cycle 1, turun ke 10% di cycle 5+
    gold_loss_percent = max(0.10, 0.30 - (cycle * 0.04))
    gold_lost = int(player['gold'] * gold_loss_percent)
    new_gold = player['gold'] - gold_lost
    
    # Level drop: Kehilangan 20% exp (tapi level tidak turun)
    exp_penalty = int(player.get('exp', 0) * 0.20)
    new_exp = max(0, player.get('exp', 0) - exp_penalty)
    
    # Reset stats tapi pertahankan progression
    updates = {
        "hp": player.get("max_hp", 100),
        "mp": player.get("max_mp", 50),
        "step_counter": 0,
        "gold": new_gold,
        "exp": new_exp,
        "kills": 0,
        "inventory": [],  # ITEM HILANG (Termasuk equip, durability, dll - Sangat Hardcore)
        "monster_streak": 0,
        "steps_since_event": 0,
        "current_combo": 0,
        "active_buffs": [],  # Buff hilang
        "active_resin": None, # Resin/Mantra hilang
        "resin_duration": 0,
        "has_companion": False,
        "companion_duration": 0
    }
    
    players_col.update_one({"user_id": user_id}, {"$set": updates})
    
    # Update leaderboard dengan death count
    update_leaderboard_death(user_id, player['username'], cause)
    
    death_message = f"""
💀 **KEMATIAN #{player.get('death_count', 0) + 1}**

Jiwa Weaver hancur berkeping-keping...

**Penalti:**
• 💰 Gold: -{gold_lost} ({gold_loss_percent * 100:.0f}%)
• ⭐ EXP: -{exp_penalty} (20%)
• 🎒 Semua item & equipment hancur lebur
• 🔥 Combo reset

**Yang Tersisa:**
• 🔄 Cycle: {cycle}
• 📊 Level: {player.get('level', 1)}
• 🏆 Achievements: Aman
• 📜 Sejarah: Tertulis abadi

"Archivus menarikmu kembali... namun kau masih belum terlupakan."
"""
    
    # Increment death counter
    players_col.update_one(
        {"user_id": user_id},
        {"$inc": {"death_count": 1}}
    )
    
    return death_message

def update_leaderboard(user_id, username, stat_type, value):
    """Update leaderboard untuk berbagai kategori"""
    leaderboard_col.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "username": username,
                stat_type: value,
                "last_updated": datetime.datetime.now()
            }
        },
        upsert=True
    )

def update_leaderboard_death(user_id, username, cause):
    """Track death statistics"""
    leaderboard_col.update_one(
        {"user_id": user_id},
        {
            "$set": {"username": username},
            "$inc": {"total_deaths": 1, f"deaths_by_{cause}": 1},
            "$set": {"last_death": datetime.datetime.now()}
        },
        upsert=True
    )

def get_global_leaderboard(stat_type, limit=10):
    """Ambil top players berdasarkan stat tertentu"""
    results = leaderboard_col.find({stat_type: {"$exists": True}}).sort(stat_type, -1).limit(limit)
    return list(results)

def auto_seed_content():
    """Menyuntikkan naskah awal jika database narasi masih kosong (ENHANCED)"""
    if narratives_col.count_documents({}) == 0:
        print("[SISTEM] Database narasi kosong. Menyuntikkan naskah awal...")
        content = [
            # --- PERJALANAN AMAN (EXPANDED) ---
            {"category": "safe_travel", "text": "Hanya suara langkah kakimu yang bergema di lorong sunyi ini."},
            {"category": "safe_travel", "text": "Cahaya redup dari lentera Weaver-mu membelah kegelapan pekat."},
            {"category": "safe_travel", "text": "Kamu merasakan hembusan angin dingin, tapi tidak ada jendela di sini."},
            {"category": "safe_travel", "text": "Dinding-dinding ini seperti bernapas mengikuti ritme langkahmu."},
            {"category": "safe_travel", "text": "Arsitektur Archivus berubah tanpa kau sadari. Jalan ini tidak sama dengan tadi."},
            {"category": "safe_travel", "text": "Debu menari dalam cahaya lentera, membentuk pola yang hampir memiliki makna."},
            
            # --- EVENT MONSTER (EXPANDED) ---
            {"category": "monster_event", "text": "Tiba-tiba, bayangan di dinding memisahkan diri dan menyerang!"},
            {"category": "monster_event", "text": "Ruang di depanmu terdistorsi. Sesuatu yang haus akan memori muncul."},
            {"category": "monster_event", "text": "Gemuruh dari kegelapan! Entitas menghadangmu dengan auranya yang mencekik."},
            {"category": "monster_event", "text": "Tinta hitam mengalir dari langit-langit, membentuk sosok yang mengerikan!"},
            
            # --- EVENT NPC (EXPANDED) ---
            {"category": "npc_event", "text": "Seorang sosok berjubah duduk di sudut, menatapmu dengan mata kosong."},
            {"category": "npc_event", "text": "Suara bisikan memanggil namamu dari kegelapan di depan."},
            {"category": "npc_event", "text": "Seseorang berdiri di tengah lorong. Tapi apa mereka benar-benar ada di sana?"},
            {"category": "npc_event", "text": "Kau mendengar tawa samar. Sumber suaranya tidak jelas."}
        ]
        narratives_col.insert_many(content)
        print(f"[SISTEM] {len(content)} Naskah berhasil disuntikkan!")

# Utility functions untuk buff management
def add_buff(user_id, buff_data):
    """Tambahkan buff ke player"""
    player = get_player(user_id)
    buffs = player.get('active_buffs', [])
    buffs.append(buff_data)
    update_player(user_id, {'active_buffs': buffs})

def tick_buffs(user_id):
    """Kurangi duration buff dan Resin/Mantra, remove yang expired"""
    player = get_player(user_id)
    updates = {}
    
    # 1. Update Regular Buffs
    buffs = player.get('active_buffs', [])
    active_buffs = []
    for buff in buffs:
        buff['duration'] = buff.get('duration', 0) - 1
        if buff['duration'] > 0:
            active_buffs.append(buff)
    updates['active_buffs'] = active_buffs
    
    # 2. Update Resin / Mantra Weapon (Berkurang per turn combat)
    if player.get('active_resin') and player.get('resin_duration', 0) > 0:
        new_duration = player['resin_duration'] - 1
        if new_duration <= 0:
            updates['active_resin'] = None
            updates['resin_duration'] = 0
            # Kita bisa nge-print notif ke user di main.py nanti "Efek Mantramu habis!"
        else:
            updates['resin_duration'] = new_duration
            
    if updates:
        update_player(user_id, updates)

if __name__ == "__main__":
    auto_seed_content()
