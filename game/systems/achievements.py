# game/systems/achievements.py

"""
Achievement & Progression System (The Archivus)
Memberikan sense of progress dan reward untuk pemain.
Terintegrasi dengan sistem Leveling, Stat Points, dan Inventory 8-Slot.
"""

import math
import random
import datetime

from database import update_player, get_player
from game.systems.progression import add_exp

# --- FUNGSI MANDATORI UNTUK MAIN.PY ---

def calculate_level_from_exp(exp):
    """
    Menghitung level berdasarkan total EXP.
    Rumus eskalasi: Level 1 (0-99), Level 2 (100-249), dst.
    """
    if exp < 100: return 1
    
    level = 1
    requirement = 100
    temp_exp = exp
    
    while temp_exp >= requirement:
        temp_exp -= requirement
        level += 1
        requirement = int(requirement * 1.5) # Kenaikan kesulitan 50% per level
        
    return level

def calculate_exp_needed(level):
    """
    FUNGSI PENTING: Menghitung total EXP yang dibutuhkan untuk naik ke level berikutnya.
    Dibutuhkan oleh main.py untuk menampilkan progress bar level.
    """
    if level <= 1: return 100
    
    requirement = 100
    for _ in range(1, level):
        requirement = int(requirement * 1.5)
    return requirement

# Database Achievement
ACHIEVEMENTS = {
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
        "reward": {"gold": 200, "exp": 500, "item": "lucky_charm"},
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
    "keeper_slayer": {
        "id": "keeper_slayer",
        "title": "Keeper Slayer",
        "description": "Kalahkan Sang Penjaga pertama kali",
        "condition": {"type": "boss_kills", "value": 1},
        "reward": {"gold": 500, "exp": 1000, "item": "void_orb"},
        "icon": "👑"
    },
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
    "scholar": {
        "id": "scholar",
        "title": "Scholar of Lore",
        "description": "Jawab benar 10 quiz lore",
        "condition": {"type": "quiz_correct", "value": 10},
        "reward": {"gold": 500, "max_mp": 25},
        "icon": "📚"
    }
}

# Daily Quests Pool
DAILY_QUESTS_POOL = [
    {"id": "daily_kills", "title": "Pemburu Harian", "type": "kills", "target": 5, "reward": {"gold": 100, "exp": 200}},
    {"id": "daily_gold", "title": "Pengumpul Memori", "type": "gold_earned", "target": 200, "reward": {"gold": 50, "exp": 150}},
    {"id": "daily_exploration", "title": "Penjelajah Dimensi", "type": "steps", "target": 20, "reward": {"gold": 75, "exp": 100}},
    {"id": "daily_quiz", "title": "Ujian Ingatan", "type": "quiz_correct", "target": 3, "reward": {"gold": 150, "exp": 250}}
]

def check_achievement_unlock(player, achievement_id):
    """Cek apakah achievement tercapai"""
    achievement = ACHIEVEMENTS.get(achievement_id)
    if not achievement: return False
    
    unlocked = player.get('achievements_unlocked', [])
    if achievement_id in unlocked: return False
    
    condition = achievement['condition']
    ctype = condition['type']
    value = condition['value']
    
    if ctype == "kills": return player.get('kills', 0) >= value
    elif ctype == "boss_kills": return player.get('boss_kills', 0) >= value
    elif ctype == "cycle": return player.get('cycle', 1) >= value
    elif ctype == "max_combo": return player.get('max_combo_reached', 0) >= value
    elif ctype == "total_gold_earned": return player.get('total_gold_earned', 0) >= value
    elif ctype == "quiz_correct": return player.get('quiz_correct_count', 0) >= value
    
    return False

def get_all_unlockable_achievements(player):
    """Mendapatkan daftar ID achievement yang baru terpenuhi syaratnya."""
    newly_unlocked = []
    already_unlocked = player.get('achievements_unlocked', [])
    
    for ach_id in ACHIEVEMENTS.keys():
        if ach_id not in already_unlocked:
            if check_achievement_unlock(player, ach_id):
                newly_unlocked.append(ach_id)
    return newly_unlocked

def award_achievement(user_id, achievement_id):
    """Memberikan reward dan mencatat progres ke database."""
    player_data = get_player(user_id)
    achievement = ACHIEVEMENTS.get(achievement_id)
    if not achievement: return None
    
    reward = achievement['reward']
    updates = {}
    reward_text = []
    
    if 'gold' in reward:
        updates['gold'] = player_data.get('gold', 0) + reward['gold']
        reward_text.append(f"💰 {reward['gold']} Gold")
    
    if 'exp' in reward:
        leveled_up, new_level, _ = add_exp(user_id, reward['exp'])
        reward_text.append(f"⭐ {reward['exp']} EXP")
        player_data = get_player(user_id) 
    
    if 'max_hp' in reward:
        updates['max_hp'] = player_data.get('max_hp', 100) + reward['max_hp']
        reward_text.append(f"❤️ +{reward['max_hp']} Max HP")
    
    if 'max_mp' in reward:
        updates['max_mp'] = player_data.get('max_mp', 50) + reward['max_mp']
        reward_text.append(f"🔮 +{reward['max_mp']} Max MP")
    
    if 'item' in reward:
        inventory = player_data.get('inventory', [])
        inventory.append(reward['item'])
        updates['inventory'] = inventory
        reward_text.append(f"🎁 {reward['item'].replace('_', ' ').title()}")
    
    unlocked = player_data.get('achievements_unlocked', [])
    unlocked.append(achievement_id)
    updates['achievements_unlocked'] = unlocked
    
    update_player(user_id, updates)
    
    return {
        'title': achievement['title'],
        'description': achievement['description'],
        'icon': achievement['icon'],
        'rewards': ' | '.join(reward_text)
    }

def generate_daily_quests():
    """Generate 3 daily quests acak berdasarkan tanggal hari ini"""
    today = str(datetime.datetime.now().date())
    random.seed(today)
    selected = random.sample(DAILY_QUESTS_POOL, 3)
    random.seed() 
    return selected

def check_daily_quest_progress(player, quest_type):
    """Cek progress daily quest dari statistik harian pemain"""
    daily_stats = player.get('daily_stats', {})
    
    mapping = {
        "kills": "kills_today",
        "gold_earned": "gold_earned_today",
        "steps": "steps_today",
        "quiz_correct": "quiz_correct_today",
        "perfect_combat": "perfect_combat_today"
    }
    
    return daily_stats.get(mapping.get(quest_type, ""), 0)
