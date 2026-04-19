# database.py

import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Memuat variabel dari .env
load_dotenv()

# ====================================================================
# KONEKSI DATABASE (DIKUNCI KE LOCAL VPS)
# ====================================================================
MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/")
DB_NAME = os.getenv("DB_NAME", "the_archivus_db")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
db = client[DB_NAME]

# Koleksi (Tables) Utama
players_col = db["players"]
narratives_col = db["narratives"]
leaderboard_col = db["leaderboard"]

# Koleksi Tambahan untuk Master Data
items_col = db["items"]
landmarks_col = db["landmarks"]
npcs_col = db["npcs"]
puzzles_col = db["puzzles"]
monsters_col = db["monsters"]
hazards_col = db["hazards"]
jobs_col = db["jobs"]
skills_col = db["skills"]

# --- LOKASI ENDLESS (DISINKRONKAN DENGAN EXPLORATION.PY) ---
LOCATIONS = [
    "The Whispering Hall", 
    "The Forsaken Mire", 
    "The Abyssal Depth", 
    "The Frozen Purgatory", 
    "The Crimson Throne"
]

def validate_player_data(player_doc, user_id):
    """Memastikan dokumen pemain lama mendapatkan field-field baru tanpa error."""
    updates = {}
    default_fields = {
        "equipped": {}, "current_job": "Novice Weaver",
        "base_p_atk": 10, "base_m_atk": 10, "base_p_def": 5, "base_m_def": 5, "base_speed": 10,
        "stat_points": 0, "artifacts": [], "unlocked_lores": [],
        "step_in_cycle": 0, "miniboss_slain_cycle": False,
        "energy": 100, "max_energy": 100, "active_effects": [], 
        "level": 1, "exp": 0, "exp_needed": 100, "achievements_unlocked": [],
        "inventory": [], "active_buffs": [], "active_resin": None,
        "resin_duration": 0, "has_companion": False, "companion_duration": 0,
        "equipment_durability": {}, "permanent_bonus": {}, 
        "skill_usages": {}, "skill_cooldowns": {}, "last_skill_used": None
    }

    for field, default_value in default_fields.items():
        if field not in player_doc:
            updates[field] = default_value

    if updates:
        players_col.update_one({"user_id": user_id}, {"$set": updates})
        player_doc.update(updates)

    return player_doc


def get_player(user_id, username="Weaver"):
    """Mengambil data pemain atau membuat baru jika belum ada"""
    player = players_col.find_one({"user_id": user_id})
    
    if not player:
        new_player = {
            "user_id": user_id, "username": username,
            "hp": 100, "max_hp": 100, "mp": 50, "max_mp": 50, "gold": 0,
            "kills": 0, "boss_kills": 0, "base_p_atk": 10, "base_m_atk": 10,
            "base_p_def": 5, "base_m_def": 5, "base_speed": 10, "stat_points": 0,
            "energy": 100, "max_energy": 100, "active_effects": [], 
            "level": 1, "exp": 0, "exp_needed": 100, "inventory": [],
            "equipped": {}, "equipment_durability": {}, "current_job": "Novice Weaver",
            "artifacts": [], "permanent_bonus": {}, "skill_usages": {},
            "skill_cooldowns": {}, "last_skill_used": None,
            "cycle": 1, "location": LOCATIONS[0], "history": [],
            "step_counter": 0, "step_in_cycle": 0, "monster_streak": 0,
            "steps_since_event": 0, "miniboss_slain_cycle": False,
            "current_combo": 0, "max_combo_reached": 0, "flawless_boss_count": 0,
            "achievements_unlocked": [], "unlocked_lores": [], "daily_quests": [],
            "daily_stats": {}, "last_login": None, "recent_moves": [],
            "total_gold_earned": 0, "locations_visited": [LOCATIONS[0]],
            "trap_survived": 0, "quiz_correct_count": 0, "active_buffs": [],
            "active_resin": None, "resin_duration": 0, "has_companion": False,
            "companion_duration": 0, "highest_cycle": 1, "highest_combo": 0,
            "total_playtime": 0, "created_at": datetime.datetime.now(),
            "last_seen": datetime.datetime.now()
        }
        players_col.insert_one(new_player)
        return new_player
    
    player = validate_player_data(player, user_id)
    players_col.update_one({"user_id": user_id}, {"$set": {"last_seen": datetime.datetime.now()}})
    return player

def update_player(user_id, data):
    updates = data.copy()
    if 'cycle' in data or 'current_combo' in data:
        player = players_col.find_one({"user_id": user_id}, {"highest_cycle": 1, "highest_combo": 1})
        if player:
            if 'cycle' in data and data['cycle'] > player.get('highest_cycle', 0):
                updates['highest_cycle'] = data['cycle']
            if 'current_combo' in data and data['current_combo'] > player.get('highest_combo', 0):
                updates['highest_combo'] = data['current_combo']
    players_col.update_one({"user_id": user_id}, {"$set": updates})

def add_history(user_id, event_text):
    player = players_col.find_one({"user_id": user_id}, {"cycle": 1, "location": 1, "history": 1})
    if not player: return
    log = f"[Siklus {player.get('cycle', 1)} - {player.get('location', 'Unknown')}] {event_text}"
    history = player.get("history", [])
    history.append(log)
    if len(history) > 20: history.pop(0)
    players_col.update_one({"user_id": user_id}, {"$set": {"history": history}})

def reset_player_death(user_id, cause):
    player = get_player(user_id)
    add_history(user_id, f"Gugur karena {cause}.")
    cycle = player.get('cycle', 1)
    
    gold_loss_percent = max(0.10, 0.30 - (cycle * 0.04))
    gold_lost = int(player.get('gold', 0) * gold_loss_percent)
    new_gold = max(0, player.get('gold', 0) - gold_lost)
    
    exp_penalty = int(player.get('exp', 0) * 0.20)
    new_exp = max(0, player.get('exp', 0) - exp_penalty)
    
    saved_artifacts = player.get('artifacts', [])
    saved_bonus = player.get('permanent_bonus', {})
    saved_skill_usages = player.get('skill_usages', {})
    
    updates = {
        "hp": player.get("max_hp", 100), "mp": player.get("max_mp", 50),
        "energy": player.get("max_energy", 100), "active_effects": [],
        "step_counter": 0, "step_in_cycle": 0, "miniboss_slain_cycle": False,
        "gold": new_gold, "exp": new_exp, "kills": 0, "inventory": [],
        "equipped": {}, "equipment_durability": {}, "current_job": "Novice Weaver",
        "artifacts": saved_artifacts, "permanent_bonus": saved_bonus,
        "skill_cooldowns": {}, "last_skill_used": None, "skill_usages": saved_skill_usages,
        "monster_streak": 0, "steps_since_event": 0, "current_combo": 0,
        "active_buffs": [], "active_resin": None, "resin_duration": 0,
        "has_companion": False, "companion_duration": 0
    }
    
    players_col.update_one({"user_id": user_id}, {"$set": updates})
    update_leaderboard_death(user_id, player['username'], cause)
    
    death_message = f"""
💀 **KEMATIAN #{player.get('death_count', 0) + 1}**

Jiwa Weaver hancur berkeping-keping...

**Penalti Kematian:**
• 💰 Gold: -{gold_lost} ({gold_loss_percent * 100:.0f}%)
• ⭐ EXP: -{exp_penalty} (20%)
• 🎒 Semua Equipment (Tas & Terpakai) lebur menjadi debu.
• 🎖️ Gelarmu kembali menjadi **Novice Weaver**.

**Sisa Kekuatan yang Terjaga:**
• ✨ Atribut & Stat Points (Permanen)
• 💎 Relik Kuno & Bonus Kontrak
• 🔮 Mastery Skill (Level Evolusi Skill tidak hilang)
• 🔄 Cycle: {cycle} | 📊 Level: {player.get('level', 1)}
"""
    players_col.update_one({"user_id": user_id}, {"$inc": {"death_count": 1}})
    return death_message

def update_leaderboard(user_id, username, stat_type, value):
    leaderboard_col.update_one(
        {"user_id": user_id},
        {"$set": {"username": username, stat_type: value, "last_updated": datetime.datetime.now()}},
        upsert=True
    )

def update_leaderboard_death(user_id, username, cause):
    leaderboard_col.update_one(
        {"user_id": user_id},
        {"$set": {"username": username, "last_death": datetime.datetime.now()},
         "$inc": {"total_deaths": 1, f"deaths_by_{cause}": 1}},
        upsert=True
    )

def get_global_leaderboard(stat_type, limit=10):
    return list(leaderboard_col.find({stat_type: {"$exists": True}}).sort(stat_type, -1).limit(limit))

def add_buff(user_id, buff_data):
    player = get_player(user_id)
    buffs = player.get('active_buffs', [])
    buffs.append(buff_data)
    update_player(user_id, {'active_buffs': buffs})

def tick_buffs(user_id):
    player = get_player(user_id)
    updates = {}
    buffs = player.get('active_buffs', [])
    active_buffs = []
    for buff in buffs:
        buff['duration'] = buff.get('duration', 0) - 1
        if buff['duration'] > 0:
            active_buffs.append(buff)
            
    if len(buffs) != len(active_buffs) or any(b.get('duration', 0) < 0 for b in buffs):
        updates['active_buffs'] = active_buffs
    
    if player.get('active_resin') and player.get('resin_duration', 0) > 0:
        new_duration = player['resin_duration'] - 1
        if new_duration <= 0:
            updates['active_resin'] = None
            updates['resin_duration'] = 0
        else:
            updates['resin_duration'] = new_duration
            
    if updates:
        update_player(user_id, updates)

# ====================================================================
# SUPER SEED SYSTEM (SINKRONISASI 100% KE LOKAL DATABASE)
# ====================================================================

def auto_seed_content():
    """Mengunggah SEMUA data Master dari file .py ke Database Lokal secara otomatis"""
    print("[SISTEM] Memeriksa kelengkapan Master Data di Database Lokal...")

    # 1. SEED NARASI DASAR
    if narratives_col.count_documents({}) == 0:
        try:
            from game.data.script import NARRATIVES
            narratives_col.insert_many(NARRATIVES)
            print(f"✅ Local DB: {len(NARRATIVES)} Naskah disuntikkan!")
        except Exception as e:
            print(f"⚠️ Abaikan jika file narasi belum ada: {e}")

    # 2. SEED SEMUA ITEMS (15 Kategori File)
    if items_col.count_documents({}) == 0:
        try:
            from game.items.weapons import WEAPON_DATABASE
            from game.items.armors import ARMOR_DATABASE
            from game.items.masks import MASKS
            from game.items.heads import HEADS
            from game.items.cloaks import CLOAKS
            from game.items.boots import BOOTS
            from game.items.gloves import GLOVES
            from game.items.artifacts import ARTIFACTS
            
            from game.consumables.utility import UTILITIES
            from game.consumables.items import MISC_ITEMS, CAMPING_ITEMS
            from game.consumables.food import FOOD_ITEMS
            from game.consumables.hp import HP_POTIONS
            from game.consumables.mp import MP_POTIONS
            from game.consumables.special import SPECIAL_ITEMS
            
            all_items = {}
            for db_dict in [
                WEAPON_DATABASE, ARMOR_DATABASE, MASKS, HEADS, CLOAKS, BOOTS, GLOVES, ARTIFACTS, 
                UTILITIES, MISC_ITEMS, CAMPING_ITEMS, FOOD_ITEMS, HP_POTIONS, MP_POTIONS, SPECIAL_ITEMS
            ]:
                if db_dict: all_items.update(db_dict)
                
            if all_items:
                items_col.insert_many(list(all_items.values()))
                print(f"✅ Local DB: {len(all_items)} Item (Gear, Senjata, Potion, dll) Sinkron!")
        except Exception as e:
            print(f"⚠️ Ada file item yang belum terbuat/kosong: {e}")

    # 3. SEED LANDMARKS
    if landmarks_col.count_documents({}) == 0:
        try:
            from game.data.environment.landmarks import LANDMARKS
            landmarks_col.insert_many(list(LANDMARKS.values()))
            print(f"✅ Local DB: {len(LANDMARKS)} Landmark Sinkron!")
        except Exception as e:
            pass

    # 4. SEED HAZARDS & DEADLY ZONES
    if hazards_col.count_documents({}) == 0:
        try:
            from game.data.environment.hazards import HAZARDS
            from game.data.environment.deadly import DEADLY_ZONES
            
            all_hazards = {**HAZARDS, **DEADLY_ZONES}
            if all_hazards:
                hazards_col.insert_many(list(all_hazards.values()))
                print(f"✅ Local DB: {len(all_hazards)} Hazards & Deadly Zones Sinkron!")
        except Exception as e:
            print(f"⚠️ File Hazard/Deadly belum lengkap: {e}")

    # 5. SEED MONSTERS & BOSSES
    if monsters_col.count_documents({}) == 0:
        try:
            from game.data.monster_data import MONSTER_POOL
            from game.data.miniboss_data import MINIBOSS_POOL
            from game.data.mainboss_data import MAINBOSS_POOL
            
            flat_monsters = []
            for m_dict in [MONSTER_POOL, MINIBOSS_POOL, MAINBOSS_POOL]:
                if m_dict:
                    for category, m_list in m_dict.items():
                        for m in m_list:
                            m['tier_category'] = category
                            flat_monsters.append(m)
                            
            if flat_monsters:
                monsters_col.insert_many(flat_monsters)
                print(f"✅ Local DB: {len(flat_monsters)} Monster & Boss Sinkron!")
        except Exception as e:
            print(f"⚠️ File Monster/Boss belum lengkap: {e}")

    # 6. SEED NPCS
    if npcs_col.count_documents({}) == 0:
        try:
            from game.data.npc_data import NPC_POOL
            flat_npcs = []
            for cat, npcs in NPC_POOL.items():
                for n in npcs:
                    n['category'] = cat
                    flat_npcs.append(n)
            if flat_npcs:
                npcs_col.insert_many(flat_npcs)
                print(f"✅ Local DB: {len(flat_npcs)} NPC Sinkron!")
        except Exception as e:
            pass

    # 7. SEED PUZZLES
    if puzzles_col.count_documents({}) == 0:
        try:
            from game.puzzles.manager import PUZZLE_DATABASE
            flat_puzzles = []
            for tier, riddles in PUZZLE_DATABASE.items():
                for r in riddles:
                    r['tier'] = tier
                    flat_puzzles.append(r)
            if flat_puzzles:
                puzzles_col.insert_many(flat_puzzles)
                print(f"✅ Local DB: {len(flat_puzzles)} Puzzle/Quiz Sinkron!")
        except Exception as e:
            pass

    # 8. SEED JOBS / CLASSES (Koreksi Path: game.logic)
    if jobs_col.count_documents({}) == 0:
        try:
            from game.logic.job_manager import JOB_DATABASE 
            if JOB_DATABASE:
                jobs_col.insert_many(list(JOB_DATABASE.values()))
                print(f"✅ Local DB: {len(JOB_DATABASE)} Jobs/Class Sinkron!")
        except Exception as e:
            print(f"⚠️ File Job belum lengkap: {e}")

    # 9. SEED SKILLS (Koreksi Path: game.logic)
    if skills_col.count_documents({}) == 0:
        try:
            from game.logic.skills import SKILL_DATABASE
            if SKILL_DATABASE:
                skills_col.insert_many(list(SKILL_DATABASE.values()))
                print(f"✅ Local DB: {len(SKILL_DATABASE)} Skills Sinkron!")
        except Exception as e:
            print(f"⚠️ File Skills belum lengkap: {e}")

    print("🚀 SINKRONISASI VPS TOTAL SELESAI!")

if __name__ == "__main__":
    auto_seed_content()
