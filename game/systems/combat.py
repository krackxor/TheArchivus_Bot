"""
Sistem Pertarungan, Engine Genre, Kalkulasi RPG (Dodge, Element, Weight), dan Validasi Waktu.
Sudah di-balance penuh sesuai GDD Final (Mage Heal, Weight Penalties, Durability, dan Resin Mantra).
Dilengkapi dengan AI Cerdas dan UI Visual (Live Render & Dynamic Bars).
"""
import time
import random

# Memanggil Entitas
from game.entities.monsters import get_random_monster
from game.entities.bosses import get_random_boss, get_random_mini_boss

# Memanggil Puzzle Manager
from game.puzzles.manager import get_random_puzzle

# === SISTEM ELEMEN ===
ELEMENTS = ["Api", "Air", "Petir", "Tanah", "Angin", "Cahaya", "Kegelapan", "Natural"]
ELEMENT_CHART = {
    "Api": {"strong": "Angin", "weak": "Air"},
    "Air": {"strong": "Api", "weak": "Petir"},
    "Petir": {"strong": "Air", "weak": "Tanah"},
    "Tanah": {"strong": "Petir", "weak": "Angin"},
    "Angin": {"strong": "Tanah", "weak": "Api"},
    "Cahaya": {"strong": "Kegelapan", "weak": "Natural"},
    "Kegelapan": {"strong": "Natural", "weak": "Cahaya"},
    "Natural": {"strong": "Cahaya", "weak": "Kegelapan"}
}

# === SISTEM UI & VISUAL ===
def get_dynamic_bar(current, maximum, length=10):
    """Menghasilkan bar warna dinamis berdasarkan persentase (Hijau/Kuning/Merah)."""
    if maximum <= 0: return " [Empty] "
    
    percent = (current / maximum) * 100
    if percent <= 25:
        emoji_filled = "🔴" # Kritis
    elif percent <= 60:
        emoji_filled = "🟡" # Waspada
    else:
        emoji_filled = "🟢" # Aman
        
    filled_units = int((current / maximum) * length)
    empty_units = length - filled_units
    
    bar = (emoji_filled * filled_units) + ("⚫" * empty_units)
    return f"[{bar}] {int(current)}/{int(maximum)}"

def render_live_battle(player, monster, log_msg="Menunggu tindakanmu..."):
    """
    Merakit teks tampilan UI Live Battle. 
    Tier monster disembunyikan agar lebih misterius.
    """
    hp_view = get_dynamic_bar(player.get('hp', 0), player.get('max_hp', 100))
    mp_view = get_dynamic_bar(player.get('mp', 0), player.get('max_mp', 50))
    
    # Bar HP Monster (Visual merah api)
    m_hp_percent = max(0, min(10, int((monster['monster_hp'] / monster['monster_max_hp']) * 10)))
    m_bar = "🔥" * m_hp_percent + "🌑" * (10 - m_hp_percent)
    
    text = (
        f"⚔️ **PERTEMPURAN AKTIF** ⚔️\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"👾 **{monster['monster_name']}**\n"
        f"[{m_bar}] {int(monster['monster_hp'])} HP\n"
        f"Elemen: {monster['monster_element']}\n\n"
        
        f"👤 **W E A V E R**\n"
        f"❤️ HP: {hp_view}\n"
        f"🧪 MP: {mp_view}\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"📜 **LOG:**\n"
        f"_{log_msg}_\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"❓ **TEKA-TEKI:**\n"
        f"`{monster['question']}`\n\n"
        f"⏳ Sisa Waktu: {monster['timer']}s"
    )
    return text

# === SISTEM KALKULASI RPG ===
def calculate_equipment_stats(player):
    """Mengekstrak data equipment (mengabaikan item hancur & cek elemen Resin)."""
    inventory = player.get('inventory', [])
    stats = {
        "atk": player.get('base_atk', 10),
        "def": player.get('base_def', 0),
        "weight": 0,
        "speed": "medium",
        "weapon_type": "unarmed",
        "gloves_type": "none",
        "has_shield": False,
        "element": player.get('active_resin') or player.get('element', "Netral") 
    }
    
    for item in inventory:
        if item.get('type') in ['weapon', 'shield', 'chest', 'head', 'gloves', 'boots']:
            if item.get('durability', 1) <= 0:
                continue
                
        stats["atk"] += item.get('bonus_atk', 0)
        stats["def"] += item.get('bonus_def', 0)
        stats["weight"] += item.get('weight', 0)
        
        if item.get('type') == 'weapon':
            stats["speed"] = item.get('speed', 'medium')
            stats["weapon_type"] = 'staff' if item.get('is_magic') else 'melee'
        elif item.get('type') == 'gloves':
            stats["gloves_type"] = item.get('bonus_type', 'none')
        elif item.get('type') == 'shield':
            stats["has_shield"] = True
            
    return stats

def calculate_dodge_chance(stats):
    """Kalkulasi peluang Dodge berdasarkan Weight, Speed, dan Elemen."""
    dodge_chance = 0.25 
    
    if stats["speed"] in ["fast", "very_fast"]: dodge_chance += 0.12
    elif stats["speed"] == "medium": dodge_chance += 0.06
        
    if stats["gloves_type"] == "speed": dodge_chance += 0.10
    if stats["element"] == "Angin": dodge_chance += 0.08
        
    w = stats["weight"]
    if 16 <= w <= 30: dodge_chance -= 0.05
    elif 31 <= w <= 50: dodge_chance -= 0.12
    elif 51 <= w <= 70: dodge_chance -= 0.22
    elif w > 70: dodge_chance -= 0.35
        
    return max(0.08, min(0.75, dodge_chance))

def get_element_multiplier(atk_element, def_element):
    if atk_element in ELEMENT_CHART:
        if ELEMENT_CHART[atk_element]["strong"] == def_element: return 1.5
        elif ELEMENT_CHART[atk_element]["weak"] == def_element: return 0.5
    return 1.0

def process_staff_magic(element):
    effects = {
        "Api": {"effect": "burn", "value": 0, "desc": "Membakar musuh (Damage over Time)"},
        "Air": {"effect": "slow", "value": 0, "desc": "Mengurangi kecepatan musuh"},
        "Petir": {"effect": "stun", "value": 0, "desc": "Peluang 20% musuh terkena Stun"},
        "Angin": {"effect": "dodge_up", "value": 0, "desc": "Meningkatkan Dodge Chance pemain sementara"},
        "Tanah": {"effect": "def_up", "value": 0, "desc": "Meningkatkan Defense pemain sementara"},
        "Cahaya": {"effect": "heal", "value": random.randint(25, 40), "desc": "Memulihkan HP pemain secara instan"},
        "Kegelapan": {"effect": "curse", "value": 0, "desc": "Mengurangi Defense musuh secara permanen"},
        "Natural": {"effect": "cleanse_mp", "value": 15, "desc": "Menghapus debuff dan memulihkan 15 MP"}
    }
    return effects.get(element, {"effect": "none", "value": 0, "desc": "Tidak ada efek sihir"})

# === LOGIKA CERDAS AI MONSTER ===
def roll_monster_skill(m_element, tier_level, is_boss, p_hp_pct, m_hp_pct, p_mp):
    """
    Monster sekarang memiliki kepintaran reaktif berdasarkan HP pemain/sendiri.
    """
    skill_chance = 0.15 + (tier_level * 0.05)
    if is_boss: skill_chance += 0.20
        
    if random.random() > skill_chance:
        return None 
        
    monster_skills = {
        "Api": {"name": "Semburan Api", "type": "damage_boost", "multiplier": 1.5, "msg": "menyemburkan api panas!"},
        "Air": {"name": "Tidal Wave", "type": "defense_pierce", "multiplier": 1.2, "msg": "menerjang dengan gelombang mengabaikan pertahanan!"},
        "Petir": {"name": "Thunder Strike", "type": "time_cut", "multiplier": 1.0, "msg": "menyerang secepat kilat (Waktu dikurangi)!"},
        "Tanah": {"name": "Earthquake", "type": "heavy_damage", "multiplier": 1.8, "msg": "mengguncang tanah dengan sangat keras!"},
        "Angin": {"name": "Gale Force", "type": "dodge_bypass", "multiplier": 1.0, "msg": "menyerang dari segala arah (Dodge sulit)!"},
        "Cahaya": {"name": "Holy Ray", "type": "heal_self", "multiplier": 1.0, "msg": "memulihkan dirinya sendiri dengan cahaya!"},
        "Kegelapan": {"name": "Shadow Drain", "type": "vampire", "multiplier": 1.3, "msg": "menghisap energi kehidupanmu!"},
        "Natural": {"name": "Poison Spores", "type": "damage_boost", "multiplier": 1.4, "msg": "melepaskan spora beracun!"}
    }
    
    # AI Reaktif Khusus Boss & Monster Elite (Tier 3+)
    if is_boss or tier_level >= 3:
        if p_hp_pct <= 0.30 and m_element in ["Api", "Tanah"]:
            return monster_skills[m_element] # Eksekusi mati pemain!
        if m_hp_pct <= 0.40 and m_element in ["Cahaya", "Air"]:
            return monster_skills[m_element] # Bertahan hidup!
        if p_mp >= 30 and m_element in ["Kegelapan"]:
            return monster_skills[m_element] # Serap energi pemain!
            
    return monster_skills.get(m_element)

# === MULTI-GENRE ENGINE ===
def generate_battle_puzzle(player, tier_level=1, is_boss=False, is_miniboss=False, existing_monster=None):
    p_stats = calculate_equipment_stats(player)
    
    if existing_monster:
        m_name = existing_monster["name"]
        m_element = existing_monster["element"]
        m_hp = existing_monster["hp"]
        m_max_hp = existing_monster["max_hp"]
        tier_label = existing_monster["tier"]
        base_damage = existing_monster["base_damage"]
    else:
        m_element = random.choice(ELEMENTS)
        if is_boss:
            m_name = get_random_boss()
            tier_label = "BOSS"
            base_damage = random.randint(25, 40) + (tier_level * 5)
            m_max_hp = 300 + (tier_level * 100)
        elif is_miniboss:
            m_name = get_random_mini_boss()
            tier_label = "MINI BOSS"
            base_damage = 25 + (player.get('cycle', 1) * 5)
            m_max_hp = 150 + (player.get('cycle', 1) * 50)
        else:
            m_name = get_random_monster(tier_level)
            tier_label = tier_level
            base_damage = random.randint(8, 15) + (tier_level * random.randint(3, 6))
            m_max_hp = 50 + (tier_level * 30)
        m_hp = m_max_hp

    # Kalkulasi Persentase untuk AI
    p_hp_pct = player.get('hp', 100) / max(1, player.get('max_hp', 100))
    m_hp_pct = m_hp / max(1, m_max_hp)
    p_mp = player.get('mp', 0)

    # Roll Monster Skill (Menggunakan AI Cerdas)
    m_skill = roll_monster_skill(m_element, tier_level, is_boss, p_hp_pct, m_hp_pct, p_mp)
    
    raw_damage = base_damage
    timer_penalty = 0
    skill_msg = ""
    
    if m_skill:
        skill_msg = f"✨ *{m_name} {m_skill['msg']}*"
        
        if m_skill["type"] == "damage_boost" or m_skill["type"] == "heavy_damage":
            raw_damage = int(base_damage * m_skill["multiplier"])
        elif m_skill["type"] == "defense_pierce":
            raw_damage = int(base_damage * m_skill["multiplier"])
            p_stats["def"] = int(p_stats["def"] * 0.5) 
        elif m_skill["type"] == "time_cut":
            timer_penalty = 5 
        elif m_skill["type"] == "heal_self":
            heal_amount = int(m_max_hp * 0.15) 
            m_hp = min(m_max_hp, m_hp + heal_amount)
            skill_msg += f" (+{heal_amount} HP)"
        elif m_skill["type"] == "vampire":
            raw_damage = int(base_damage * m_skill["multiplier"])
            
    final_monster_damage = max(1, raw_damage - p_stats["def"])

    if is_boss and random.random() > 0.6:
        target_word = random.choice(["PENJAGA GERBANG", "DUNIA HAMPA", "MEMORI HILANG", "ECLIPTIC EXPRESS", "SANG PENGKHIANAT"])
        scrambled = list(target_word.replace(" ", ""))
        random.shuffle(scrambled)
        question = f"SANG PENJAGA MENGHADANGMU! Susun segel kutukan ini (Tanpa spasi): *{''.join(scrambled).upper()}*"
        answer = target_word.replace(" ", "").lower()
    else:
        # === TERHUBUNG DENGAN PUZZLE MANAGER YANG CERDAS ===
        p_streak = player.get('monster_streak', 0) 
        question, answer = get_random_puzzle(tier_level, monster_element=m_element, win_streak=p_streak)

    if is_boss: timer_limit = 25
    elif is_miniboss: timer_limit = 35
    else: timer_limit = max(15, 70 - (tier_level * 10))
        
    timer_limit = max(10, timer_limit - timer_penalty) 

    return {
        "monster_name": m_name,
        "monster_element": m_element,
        "monster_hp": m_hp,
        "monster_max_hp": m_max_hp,
        "tier": tier_label,
        "damage": final_monster_damage, 
        "base_damage": base_damage,
        "defense_applied": p_stats["def"],
        "active_skill": m_skill,
        "skill_message": skill_msg,
        "question": question,
        "answer": str(answer).lower(),
        "timer": timer_limit,
        "is_boss": is_boss,
        "generated_time": time.time()
    }

def validate_answer(user_answer, correct_answer, generated_time, time_limit):
    time_taken = time.time() - generated_time
    
    if time_taken > time_limit:
        return (False, True, time_taken) 
    
    clean_user = str(user_answer).strip().lower()
    clean_correct = str(correct_answer).strip().lower()
    
    if clean_user == clean_correct:
        return (True, False, time_taken)
        
    return (False, False, time_taken)
