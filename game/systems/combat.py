"""
Sistem Pertarungan, Engine Genre, Kalkulasi RPG (Dodge, Element, Weight), dan Validasi Waktu.
Sudah di-balance penuh sesuai GDD Final (Mage Heal, Weight Penalties, Durability, dan Resin Mantra).
"""
import time
import random

# Memanggil Entitas
from game.entities.monsters import get_random_monster
from game.entities.bosses import get_random_boss

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

def calculate_equipment_stats(player):
    """
    Mengekstrak seluruh data equipment (Atk, Def, Weight, Speed, dll) dari inventory/tas pemain.
    FITUR BARU: 
    1. Mengabaikan stat dari barang yang sudah rusak (durability <= 0).
    2. Mengubah elemen secara dinamis jika ada buff Resin/Mantra.
    """
    inventory = player.get('inventory', [])
    stats = {
        "atk": player.get('base_atk', 10),
        "def": player.get('base_def', 0),
        "weight": 0,
        "speed": "medium",
        "weapon_type": "unarmed",
        "gloves_type": "none",
        "has_shield": False,
        # Prioritaskan 'active_resin' (kertas mantra), jika tidak ada gunakan elemen bawaan equip/Netral
        "element": player.get('active_resin') or player.get('element', "Netral") 
    }
    
    for item in inventory:
        # CEK DURABILITY: Abaikan barang yang sudah hancur
        if item.get('type') in ['weapon', 'shield', 'chest', 'head', 'gloves', 'boots']:
            if item.get('durability', 1) <= 0:
                continue # SKIP ITEM RUSAK!
                
        # Kalkulasi Stat Dasar
        stats["atk"] += item.get('bonus_atk', 0)
        stats["def"] += item.get('bonus_def', 0)
        stats["weight"] += item.get('weight', 0)
        
        # Ekstraksi Tipe Spesifik
        if item.get('type') == 'weapon':
            stats["speed"] = item.get('speed', 'medium')
            stats["weapon_type"] = 'staff' if item.get('is_magic') else 'melee'
        elif item.get('type') == 'gloves':
            stats["gloves_type"] = item.get('bonus_type', 'none')
        elif item.get('type') == 'shield':
            stats["has_shield"] = True
            
    return stats

def calculate_dodge_chance(stats):
    """
    Kalkulasi peluang Dodge berdasarkan Weight, Speed Senjata, dan Gloves.
    Rumus: 25% + SpeedBonus + GlovesBonus + ElementBonus - WeightPenalty
    """
    dodge_chance = 0.25 # Base 25% (Sesuai update GDD)
    
    # 1. Speed Bonus
    if stats["speed"] in ["fast", "very_fast"]:
        dodge_chance += 0.12
    elif stats["speed"] == "medium":
        dodge_chance += 0.06
        
    # 2. Gloves Bonus
    if stats["gloves_type"] == "speed": # Light Gloves
        dodge_chance += 0.10
        
    # 3. Element Bonus (Angin sangat lincah)
    if stats["element"] == "Angin":
        dodge_chance += 0.08
        
    # 4. Weight Penalty (Sangat Terkalibrasi)
    w = stats["weight"]
    if 16 <= w <= 30:
        dodge_chance -= 0.05
    elif 31 <= w <= 50:
        dodge_chance -= 0.12
    elif 51 <= w <= 70:
        dodge_chance -= 0.22
    elif w > 70:
        dodge_chance -= 0.35
        
    # Limit Dodge: Min 8%, Max 75%
    return max(0.08, min(0.75, dodge_chance))

def get_element_multiplier(atk_element, def_element):
    """Mengembalikan multiplier 1.5x (Kuat), 0.5x (Lemah), atau 1.0x (Netral)."""
    if atk_element in ELEMENT_CHART:
        if ELEMENT_CHART[atk_element]["strong"] == def_element:
            return 1.5
        elif ELEMENT_CHART[atk_element]["weak"] == def_element:
            return 0.5
    return 1.0

def process_staff_magic(element):
    """
    Mengembalikan efek magic jika player menggunakan Staff.
    Sesuai GDD Final: HANYA Elemen Cahaya yang bisa Heal HP.
    """
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

def roll_monster_skill(m_element, tier_level, is_boss):
    """
    Menentukan apakah monster menggunakan skill khusus berdasarkan elemennya.
    Peluang skill meningkat berdasarkan tier dan status Boss.
    """
    skill_chance = 0.15 + (tier_level * 0.05)
    if is_boss:
        skill_chance += 0.20
        
    if random.random() > skill_chance:
        return None # Serangan biasa
        
    # Dictionary Skill Monster berdasar Elemen
    monster_skills = {
        "Api": {"name": "Semburan Api", "type": "damage_boost", "multiplier": 1.5, "msg": "menyemburkan api panas!"},
        "Air": {"name": "Tidal Wave", "type": "defense_pierce", "multiplier": 1.2, "msg": "menerjang dengan gelombang yang mengabaikan pertahanan!"},
        "Petir": {"name": "Thunder Strike", "type": "time_cut", "multiplier": 1.0, "msg": "menyerang secepat kilat (Waktu dikurangi)!"},
        "Tanah": {"name": "Earthquake", "type": "heavy_damage", "multiplier": 1.8, "msg": "mengguncang tanah dengan sangat keras!"},
        "Angin": {"name": "Gale Force", "type": "dodge_bypass", "multiplier": 1.0, "msg": "menyerang dari segala arah (Dodge sulit)!"},
        "Cahaya": {"name": "Holy Ray", "type": "heal_self", "multiplier": 1.0, "msg": "memulihkan dirinya sendiri dengan cahaya!"},
        "Kegelapan": {"name": "Shadow Drain", "type": "vampire", "multiplier": 1.3, "msg": "menghisap energi kehidupanmu!"},
        "Natural": {"name": "Poison Spores", "type": "damage_boost", "multiplier": 1.4, "msg": "melepaskan spora beracun!"}
    }
    
    return monster_skills.get(m_element)

def generate_battle_puzzle(player, tier_level=1, is_boss=False, existing_monster=None):
    """
    Sistem Multi-Genre Engine yang digabungkan dengan stat Monster RPG.
    Menerima parameter 'existing_monster' agar HP tidak keriset saat lanjut ronde.
    """
    
    # 1. Kalkulasi Stat Pemain
    p_stats = calculate_equipment_stats(player)
    
    # 2. Tentukan Stat Monster (Buat baru atau pakai yang sudah ada)
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
        else:
            m_name = get_random_monster(tier_level)
            tier_label = tier_level
            base_damage = random.randint(8, 15) + (tier_level * random.randint(3, 6))
            m_max_hp = 50 + (tier_level * 30)
        m_hp = m_max_hp

    # 3. Roll Monster Skill
    m_skill = roll_monster_skill(m_element, tier_level, is_boss)
    
    # 4. Kalkulasi Damage Monster Masuk
    raw_damage = base_damage
    timer_penalty = 0
    skill_msg = ""
    
    if m_skill:
        skill_msg = f"✨ *{m_name} {m_skill['msg']}*"
        
        if m_skill["type"] == "damage_boost" or m_skill["type"] == "heavy_damage":
            raw_damage = int(base_damage * m_skill["multiplier"])
        elif m_skill["type"] == "defense_pierce":
            raw_damage = int(base_damage * m_skill["multiplier"])
            p_stats["def"] = int(p_stats["def"] * 0.5) # Kurangi def efektif 50%
        elif m_skill["type"] == "time_cut":
            timer_penalty = 5 # Waktu jawab dipotong 5 detik
        elif m_skill["type"] == "heal_self":
            heal_amount = int(m_max_hp * 0.15) # Heal 15% Max HP
            m_hp = min(m_max_hp, m_hp + heal_amount)
            skill_msg += f" (+{heal_amount} HP)"
        elif m_skill["type"] == "vampire":
            raw_damage = int(base_damage * m_skill["multiplier"])
            # Heal akan dieksekusi di main.py jika serangan kena
            
    final_monster_damage = max(1, raw_damage - p_stats["def"])

    # 5. Pilih Puzzle 
    if is_boss and random.random() > 0.6:
        target_word = random.choice(["PENJAGA GERBANG", "DUNIA HAMPA", "MEMORI HILANG", "ECLIPTIC EXPRESS", "SANG PENGKHIANAT"])
        scrambled = list(target_word.replace(" ", ""))
        random.shuffle(scrambled)
        question = f"SANG PENJAGA MENGHADANGMU! Susun segel kutukan ini (Tanpa spasi): *{''.join(scrambled).upper()}*"
        answer = target_word.replace(" ", "").lower()
    else:
        question, answer = get_random_puzzle(tier_level)

    # 6. Dynamic Timer
    timer_limit = max(25, 60 - (tier_level * 5)) if not is_boss else 45
    timer_limit = max(15, timer_limit - timer_penalty) # Terapkan penalti waktu jika ada skill petir

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
    """
    Validasi jawaban pemain. 
    Mengembalikan 3 nilai: (is_correct, is_timeout, time_taken)
    Waktu (time_taken) ini akan dipakai di main.py untuk mengecek Critical Hit!
    """
    time_taken = time.time() - generated_time
    
    if time_taken > time_limit:
        return (False, True, time_taken) 
    
    clean_user = str(user_answer).strip().lower()
    clean_correct = str(correct_answer).strip().lower()
    
    if clean_user == clean_correct:
        return (True, False, time_taken)
        
    return (False, False, time_taken)
