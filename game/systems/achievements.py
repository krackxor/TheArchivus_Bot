# game/systems/achievements.py

"""
Achievement & Progression System (The Archivus)
Memberikan sense of progress dan reward untuk pemain.
Terintegrasi dengan sistem Leveling, Stat Points, dan Inventory 8-Slot.
"""

import math
import random
import datetime

from database import update_player
from game.systems.progression import add_exp

# Database Achievement
ACHIEVEMENTS = {
    # Combat Achievements
    "first_blood": {
        "id": "first_blood",
        "title": "First Blood",
        "description": "Kalahkan monster pertamamu",
        "condition": {"type": "kills", "value": 1},
        "reward": {"gold": 50, "exp": 100},
        "icon": "⚔️"
    },
    "monster_hunter": {
        "id": "monster_hunter",
        "title": "Monster Hunter",
        "description": "Kalahkan 10 monster",
        "condition": {"type": "kills", "value": 10},
        "reward": {"gold": 200, "exp": 500, "item": "lucky_charm"}, # Pastikan lucky_charm ada di MASTER_ITEM_DB
        "icon": "🏹"
    },
    "slayer": {
        "id": "slayer",
        "title": "Slayer",
        "description": "Kalahkan 50 monster",
        "condition": {"type": "kills", "value": 50},
        "reward": {"gold": 1000, "exp": 2500, "max_hp": 20},
        "icon": "💀"
    },
    
    # Boss Achievements
    "keeper_slayer": {
        "id": "keeper_slayer",
        "title": "Keeper Slayer",
        "description": "Kalahkan Sang Penjaga pertama kali",
        "condition": {"type": "boss_kills", "value": 1},
        "reward": {"gold": 500, "exp": 1000, "item": "void_orb"}, # Void Orb (Artifact)
        "icon": "👑"
    },
    
    # Survival Achievements
    "survivor": {
        "id": "survivor",
        "title": "Survivor",
        "description": "Bertahan hingga Cycle 3",
        "condition": {"type": "cycle", "value": 3},
        "reward": {"gold": 300, "max_hp": 30, "max_mp": 20},
        "icon": "🛡️"
    },
    "immortal": {
        "id": "immortal",
        "title": "Immortal Weaver",
        "description": "Bertahan hingga Cycle 10",
        "condition": {"type": "cycle", "value": 10},
        "reward": {"gold": 2000, "max_hp": 50, "max_mp": 50},
        "icon": "👼"
    },
    
    # Combat Streak Achievements
    "combo_master": {
        "id": "combo_master",
        "title": "Combo Master",
        "description": "Raih combo 5x berturut-turut",
        "condition": {"type": "max_combo", "value": 5},
        "reward": {"gold": 150, "exp": 300},
        "icon": "⚡"
    },
    "perfect_warrior": {
        "id": "perfect_warrior",
        "title": "Perfect Warrior",
        "description": "Kalahkan Boss tanpa terkena damage",
        "condition": {"type": "flawless_boss", "value": 1},
        "reward": {"gold": 1000, "exp": 2000, "item": "everfrost_shard"}, # Artifact
        "icon": "✨"
    },
    
    # Wealth Achievements
    "merchant": {
        "id": "merchant",
        "title": "Merchant of Archivus",
        "description": "Kumpulkan 1000 Gold",
        "condition": {"type": "total_gold_earned", "value": 1000},
        "reward": {"gold": 500, "exp": 500},
        "icon": "💰"
    },
    "tycoon": {
        "id": "tycoon",
        "title": "Tycoon",
        "description": "Kumpulkan 10000 Gold total",
        "condition": {"type": "total_gold_earned", "value": 10000},
        "reward": {"gold": 2000, "max_mp": 30},
        "icon": "💎"
    },
    
    # Exploration Achievements
    "explorer": {
        "id": "explorer",
        "title": "Explorer",
        "description": "Kunjungi semua 5 lokasi Archivus",
        "condition": {"type": "locations_visited", "value": 5},
        "reward": {"gold": 300, "exp": 600},
        "icon": "🗺️"
    },
    
    # Special Achievements
    "lucky_one": {
        "id": "lucky_one",
        "title": "The Lucky One",
        "description": "Selamat dari jebakan NPC penipu",
        "condition": {"type": "trap_survived", "value": 1},
        "reward": {"gold": 100, "exp": 200},
        "icon": "🍀"
    },
    "scholar": {
        "id": "scholar",
        "title": "Scholar of Lore",
        "description": "Jawab benar 10 quiz lore",
        "condition": {"type": "quiz_correct", "value": 10},
        "reward": {"gold": 500, "max_mp": 25},
        "icon": "📚"
    }
}

# Daily Quests Pool (Tetap sama)
DAILY_QUESTS_POOL = [
    {
        "id": "daily_kills",
        "title": "Pemburu Harian",
        "description": "Kalahkan 5 monster",
        "type": "kills",
        "target": 5,
        "reward": {"gold": 100, "exp": 200}
    },
    {
        "id": "daily_gold",
        "title": "Pengumpul Memori",
        "description": "Kumpulkan 200 Gold",
        "type": "gold_earned",
        "target": 200,
        "reward": {"gold": 50, "exp": 150}
    },
    {
        "id": "daily_exploration",
        "title": "Penjelajah Dimensi",
        "description": "Lakukan 20 langkah eksplorasi",
        "type": "steps",
        "target": 20,
        "reward": {"gold": 75, "exp": 100}
    },
    {
        "id": "daily_quiz",
        "title": "Ujian Ingatan",
        "description": "Jawab 3 quiz dengan benar",
        "type": "quiz_correct",
        "target": 3,
        "reward": {"gold": 150, "exp": 250}
    },
    {
        "id": "daily_perfect",
        "title": "Pertarungan Sempurna",
        "description": "Kalahkan monster tanpa salah jawab",
        "type": "perfect_combat",
        "target": 1,
        "reward": {"gold": 200, "exp": 300}
    }
]

def check_achievement_unlock(player, achievement_id):
    """Cek apakah achievement tercapai"""
    achievement = ACHIEVEMENTS.get(achievement_id)
    if not achievement:
        return False
    
    # Cek apakah sudah unlock sebelumnya
    unlocked = player.get('achievements_unlocked', [])
    if achievement_id in unlocked:
        return False
    
    condition = achievement['condition']
    ctype = condition['type']
    value = condition['value']
    
    # Evaluasi kondisi
    if ctype == "kills": return player.get('kills', 0) >= value
    elif ctype == "boss_kills": return player.get('boss_kills', 0) >= value
    elif ctype == "cycle": return player.get('cycle', 1) >= value
    elif ctype == "max_combo": return player.get('max_combo_reached', 0) >= value
    elif ctype == "flawless_boss": return player.get('flawless_boss_count', 0) >= value
    elif ctype == "total_gold_earned": return player.get('total_gold_earned', 0) >= value
    elif ctype == "locations_visited": return len(player.get('locations_visited', [])) >= value
    elif ctype == "trap_survived": return player.get('trap_survived', 0) >= value
    elif ctype == "quiz_correct": return player.get('quiz_correct_count', 0) >= value
    
    return False

def get_all_unlockable_achievements(player):
    """Dapatkan semua achievement yang baru tercapai saat evaluasi"""
    newly_unlocked = []
    for ach_id in ACHIEVEMENTS.keys():
        if check_achievement_unlock(player, ach_id):
            newly_unlocked.append(ach_id)
    return newly_unlocked

def award_achievement(user_id, achievement_id):
    """Berikan reward dari achievement dan catat di database.
    Terintegrasi dengan progression.py untuk logika EXP."""
    
    # Mengambil ulang player karena bisa saja add_exp merubah data
    from database import get_player 
    player_data = get_player(user_id)
    
    achievement = ACHIEVEMENTS.get(achievement_id)
    if not achievement:
        return None
    
    reward = achievement['reward']
    updates = {}
    reward_text = []
    
    # 1. Proses Gold
    if 'gold' in reward:
        updates['gold'] = player_data.get('gold', 0) + reward['gold']
        reward_text.append(f"💰 {reward['gold']} Gold")
    
    # 2. Proses EXP & Level Up (Menggunakan sistem sentral di progression.py)
    if 'exp' in reward:
        leveled_up, new_level, lvl_msg = add_exp(user_id, reward['exp'])
        reward_text.append(f"⭐ {reward['exp']} EXP")
        if leveled_up:
            reward_text.append(f"🎆 LEVEL UP! ({new_level})")
            
        # Panggil get_player lagi karena add_exp telah mengubah nilai di database
        player_data = get_player(user_id) 
    
    # 3. Proses Stat Boost Permanen
    if 'max_hp' in reward:
        updates['max_hp'] = player_data.get('max_hp', 100) + reward['max_hp']
        reward_text.append(f"❤️ +{reward['max_hp']} Max HP")
    
    if 'max_mp' in reward:
        updates['max_mp'] = player_data.get('max_mp', 50) + reward['max_mp']
        reward_text.append(f"🔮 +{reward['max_mp']} Max MP")
    
    # 4. Proses Item / Artefak Reward (MASUK KE INVENTORY)
    if 'item' in reward:
        inventory = player_data.get('inventory', [])
        # Masukkan String ID item ke dalam tas
        item_id = reward['item']
        inventory.append(item_id)
        updates['inventory'] = inventory
        
        # Bersihkan nama untuk teks
        clean_name = item_id.replace('_', ' ').title()
        reward_text.append(f"🎁 {clean_name}")
    
    # 5. Catat Unlocked Achievement
    unlocked = player_data.get('achievements_unlocked', [])
    unlocked.append(achievement_id)
    updates['achievements_unlocked'] = unlocked
    
    # Update ke MongoDB (Hanya update data yang belum ditangani oleh add_exp)
    if updates:
        update_player(user_id, updates)
    
    return {
        'title': achievement['title'],
        'description': achievement['description'],
        'icon': achievement['icon'],
        'rewards': ' | '.join(reward_text)
    }

def generate_daily_quests():
    """Generate 3 daily quests acak berdasarkan seed tanggal hari ini"""
    today = datetime.datetime.now().date()
    random.seed(str(today))
    selected = random.sample(DAILY_QUESTS_POOL, 3)
    random.seed() # Reset seed agar RNG fitur lain tidak rusak
    return selected

def check_daily_quest_progress(player, quest_type):
    """Cek progress daily quest dari statistik harian pemain"""
    daily_stats = player.get('daily_stats', {})
    
    if quest_type == "kills": return daily_stats.get('kills_today', 0)
    elif quest_type == "gold_earned": return daily_stats.get('gold_earned_today', 0)
    elif quest_type == "steps": return daily_stats.get('steps_today', 0)
    elif quest_type == "quiz_correct": return daily_stats.get('quiz_correct_today', 0)
    elif quest_type == "perfect_combat": return daily_stats.get('perfect_combat_today', 0)
    
    return 0
