# game/systems/achievements.py

"""
Achievement & Progression System (The Archivus)
Memberikan sense of progress dan reward untuk pemain.
Terintegrasi dengan sistem Leveling, Stat Points, dan Inventory.
"""

import math
import random
import datetime

from database import update_player, get_player
from game.systems.progression import add_exp

# --- FUNGSI YANG DICARI MAIN.PY ---
def calculate_level_from_exp(exp):
    """
    Menghitung level berdasarkan total EXP.
    Rumus: Setiap naik level, butuh 100 EXP + kenaikan 50% dari sebelumnya.
    """
    if exp < 100: return 1
    
    level = 1
    requirement = 100
    temp_exp = exp
    
    while temp_exp >= requirement:
        temp_exp -= requirement
        level += 1
        requirement = int(requirement * 1.5)
        
    return level

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
    
    # Boss Achievements
    "keeper_slayer": {
        "id": "keeper_slayer",
        "title": "Keeper Slayer",
        "description": "Kalahkan Sang Penjaga pertama kali",
        "condition": {"type": "boss_kills", "value": 1},
        "reward": {"gold": 500, "exp": 1000, "item": "void_orb"},
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

# Daily Quests Pool
DAILY_QUESTS_POOL = [
    {"id": "daily_kills", "title": "Pemburu Harian", "type": "kills", "target": 5, "reward": {"gold": 100, "exp": 200}},
    {"id": "daily_gold", "title": "Pengumpul Memori", "type": "gold_earned", "target": 200, "reward": {"gold": 50, "exp": 150}},
    {"id": "daily_exploration", "title": "Penjelajah Dimensi", "type": "steps", "target": 20, "reward": {"gold": 75, "exp": 100}},
    {"id": "daily_quiz", "title": "Ujian Ingatan", "type": "quiz_correct", "target": 3, "reward": {"gold": 150, "exp": 250}}
]

def check_achievement_unlock(player, achievement_id):
    """Cek apakah achievement tertentu sudah memenuhi syarat."""
    achievement = ACHIEVEMENTS.get(achievement_id)
    if not achievement: return False
    
    unlocked = player.get('achievements_unlocked', [])
    if achievement_id in unlocked: return False
    
    cond = achievement['condition']
    ctype, val = cond['type'], cond['value']
    
    if ctype == "kills": return player.get('kills', 0) >= val
    elif ctype == "boss_kills": return player.get('boss_kills', 0) >= val
    elif ctype == "cycle": return player.get('cycle', 1) >= val
    elif ctype == "max_combo": return player.get('max_combo_reached', 0) >= val
    elif ctype == "total_gold_earned": return player.get('total_gold_earned', 0) >= val
    elif ctype == "quiz_correct": return player.get('quiz_correct_count', 0) >= val
    
    return False

def award_achievement(user_id, achievement_id):
    """Memberikan hadiah achievement dan update database."""
    player_data = get_player(user_id)
    achievement = ACHIEVEMENTS.get(achievement_id)
    if not achievement or achievement_id in player_data.get('achievements_unlocked', []):
        return None
    
    reward = achievement['reward']
    updates = {}
    reward_text = []
    
    # 1. Gold
    if 'gold' in reward:
        updates['gold'] = player_data.get('gold', 0) + reward['gold']
        reward_text.append(f"💰 {reward['gold']} Gold")
    
    # 2. EXP (Via progression system)
    if 'exp' in reward:
        leveled_up, new_level, _ = add_exp(user_id, reward['exp'])
        reward_text.append(f"⭐ {reward['exp']} EXP")
        player_data = get_player(user_id) # Refresh data setelah EXP naik
    
    # 3. Stats Boost
    if 'max_hp' in reward:
        updates['max_hp'] = player_data.get('max_hp', 100) + reward['max_hp']
        reward_text.append(f"❤️ +{reward['max_hp']} Max HP")
    
    if 'max_mp' in reward:
        updates['max_mp'] = player_data.get('max_mp', 50) + reward['max_mp']
        reward_text.append(f"🔮 +{reward['max_mp']} Max MP")
        
    # 4. Item
    if 'item' in reward:
        inv = player_data.get('inventory', [])
        inv.append(reward['item'])
        updates['inventory'] = inv
        reward_text.append(f"🎁 {reward['item'].replace('_', ' ').title()}")

    # 5. Mark as unlocked
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
    """Memilih 3 quest harian acak berdasarkan tanggal."""
    today = str(datetime.datetime.now().date())
    random.seed(today)
    selected = random.sample(DAILY_QUESTS_POOL, min(3, len(DAILY_QUESTS_POOL)))
    random.seed()
    return selected
