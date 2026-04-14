"""
Sistem Pertarungan, Engine Genre, Kalkulasi RPG (Dodge, Element, Weight), dan Validasi Waktu.
Sudah di-balance penuh sesuai GDD Final (Mage Heal, Weight Penalties, Durability, dan Resin Mantra).
Terintegrasi dengan AI Cerdas, Visual UI Ganda, dan Pasif Artefak.
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

# === DATABASE SKILL MUSUH (Total 24 Skill) ===
MONSTER_SKILLS_DB = {
    "Api": [
        {"name": "Semburan Api", "cost": 15, "type": "damage_boost", "multiplier": 1.5, "msg": "menyemburkan api panas!"},
        {"name": "Inferno Pillar", "cost": 30, "type": "heavy_damage", "multiplier": 2.0, "msg": "memanggil pilar api dari dasar bumi!"},
        {"name": "Ember Curse", "cost": 10, "type": "defense_pierce", "multiplier": 1.0, "msg": "melelehkan armormu dengan abu panas!"}
    ],
    "Air": [
        {"name": "Tidal Wave", "cost": 20, "type": "defense_pierce", "multiplier": 1.2, "msg": "menerjang dengan gelombang yang mengabaikan pertahanan!"},
        {"name": "Mist Veil", "cost": 15, "type": "dodge_bypass", "multiplier": 1.0, "msg": "bersembunyi di balik kabut (Sulit dihindari)!"},
        {"name": "Deep Freeze", "cost": 25, "type": "time_cut", "multiplier": 1.2, "msg": "membekukan aliran waktumu!"}
    ],
    "Petir": [
        {"name": "Thunder Strike", "cost": 15, "type": "time_cut", "multiplier": 1.0, "msg": "menyerang secepat kilat (Waktu dikurangi 5s)!"},
        {"name": "Chain Lightning", "cost": 25, "type": "damage_boost", "multiplier": 1.6, "msg": "melepaskan petir beruntun!"},
        {"name": "Overload", "cost": 35, "type": "heavy_damage", "multiplier": 2.2, "msg": "meledakkan energi listrik berkekuatan tinggi!"}
    ],
    "Tanah": [
        {"name": "Earthquake", "cost": 20, "type": "heavy_damage", "multiplier": 1.8, "msg": "mengguncang tanah dengan sangat keras!"},
        {"name": "Rock Shield", "cost": 15, "type": "heal_self", "multiplier": 1.0, "msg": "memperkuat dirinya dengan pecahan batu (+HP)!"},
        {"name": "Quake Stomp", "cost": 25, "type": "dodge_bypass", "multiplier": 1.3, "msg": "menginjak bumi, menciptakan gelombang kejut!"}
    ],
    "Angin": [
        {"name": "Gale Force", "cost": 15, "type": "dodge_bypass", "multiplier": 1.0, "msg": "menyerang dari segala arah (Dodge sulit)!"},
        {"name": "Tornado", "cost": 25, "type": "heavy_damage", "multiplier": 1.7, "msg": "menciptakan badai angin puting beliung!"},
        {"name": "Vacuum Slash", "cost": 20, "type": "defense_pierce", "multiplier": 1.2, "msg": "menebas udara hampa hingga menembus zirahmu!"}
    ],
    "Cahaya": [
        {"name": "Holy Ray", "cost": 20, "type": "heal_self", "multiplier": 1.0, "msg": "memulihkan dirinya dengan pilar cahaya!"},
        {"name": "Blinding Flash", "cost": 15, "type": "time_cut", "multiplier": 1.0, "msg": "menyilaukan pandanganmu, membuatmu panik!"},
        {"name": "Judgement", "cost": 30, "type": "heavy_damage", "multiplier": 1.9, "msg": "menjatuhkan pedang cahaya dari langit!"}
    ],
    "Kegelapan": [
        {"name": "Shadow Drain", "cost": 20, "type": "vampire", "multiplier": 1.3, "msg": "menghisap energi kehidupanmu!"},
        {"name": "Night Terror", "cost": 15, "type": "defense_pierce", "multiplier": 1.1, "msg": "menyerang pikiranmu menembus perlindungan fisik!"},
        {"name": "Void Orb", "cost": 30, "type": "heavy_damage", "multiplier": 1.8, "msg": "melemparkan bola kehampaan absolut!"}
    ],
    "Natural": [
        {"name": "Poison Spores", "cost": 15, "type": "damage_boost", "multiplier": 1.4, "msg": "melepaskan spora beracun yang membakar kulit!"},
        {"name": "Nature's Blessing", "cost": 25, "type": "heal_self", "multiplier": 1.0, "msg": "menyerap energi akar pohon untuk memulihkan diri!"},
        {"name": "Vine Whip", "cost": 20, "type": "dodge_bypass", "multiplier": 1.2, "msg": "mencambuk dengan sulur berduri yang melilitmu!"}
    ]
}

# === SISTEM UI & VISUAL ===
def get_dynamic_bar(current, maximum, length=10, type_bar="hp"):
    """Menghasilkan bar visual untuk HP (Merah/Hijau/Kuning) atau MP (Biru)"""
    if maximum <= 0: return " [Empty] "
    percent = max(0, min(1, current / maximum))
    filled = int(length * percent)
    
    if type_bar == "hp":
        emoji = "🟢" if percent > 0.6 else "🟡" if percent > 0.3 else "🔴"
    else:
        emoji = "🔵"
        
    bar = (emoji * filled) + ("⚫" * (length - filled))
    return f"[{bar}] {int(current)}/{int(maximum)}"

def render_live_battle(player, monster, log_msg="Menunggu tindakanmu..."):
    """Merakit teks tampilan UI Live Battle ganda."""
    p_hp_view = get_dynamic_bar(player.get('hp', 0), player.get('max_hp', 100), type_bar="hp")
    p_mp_view = get_dynamic_bar(player.get('mp', 0), player.get('max_mp', 50), type_bar="mp")
    
    m_hp_view = get_dynamic_bar(monster.get('monster_hp', 0), monster.get('monster_max_hp', 100), type_bar="hp")
    m_mp_view = get_dynamic_bar(monster.get('monster_mp', 0), monster.get('monster_max_mp', 50), type_bar="mp")
    
    puzzle_text = f"`{monster['question']}`" if monster.get('question') else "_Pilih aksimu..._"
    timer_text = f"{monster['timer']}s" if monster.get('timer') and str(monster.get('timer')) != "--" else "--"

    text = (
        f"⚔️ **PERTEMPURAN AKTIF** ⚔️\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"👾 **{monster['monster_name']}**\n"
        f"❤️ HP: {m_hp_view}\n"
        f"🔵 MP: {m_mp_view}\n"
        f"✨ Elemen: {monster['monster_element']}\n\n"
        f"👤 **W E A V E R**\n"
        f"❤️ HP: {p_hp_view}\n"
        f"🔵 MP: {p_mp_view}\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"📜 **LOG:**\n"
        f"_{log_msg}_\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"❓ **TEKA-TEKI:**\n"
        f"{puzzle_text}\n\n"
        f"⏳ Sisa Waktu: {timer_text}"
    )
    return text

# === SISTEM KALKULASI RPG ===
def calculate_equipment_stats(player):
    """Mengekstrak data equipment (Atk, Def, Weight) dan BUFF ARTIFACT."""
    inventory = player.get('inventory', [])
    artifacts = player.get('artifacts', [])
    
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
    
    # 1. Kalkulasi Item Fisik (Equipment)
    for item in inventory:
        if item.get('type') in ['weapon', 'shield', 'chest', 'head', 'gloves', 'boots']:
            # Skip jika barang hancur/rusak
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
            
    # 2. Kalkulasi Pasif Artefak (Integrasi Baru)
    for art in artifacts:
        if art.get('id') == 'combat_manual':
            stats["atk"] += 15 # Buff damage dari kitab
        elif art.get('id') == 'lucky_charm':
            stats["speed"] = "fast" # Meningkatkan kecepatan/dodge
            
    return stats

def calculate_dodge_chance(stats):
    """Peluang Dodge berdasarkan Weight. Semakin ringan, semakin lincah."""
    weight = stats.get('weight', 0)
    chance = 0.80 - (weight * 0.007)
    
    if stats.get("speed") in ["fast", "very_fast"]: chance += 0.05
    if stats.get("gloves_type") == "speed": chance += 0.05
    
    return max(0.10, min(0.75, chance)) # Cap Max 75%, Min 10%

def calculate_block_reduction(stats):
    """Reduksi damage berdasarkan Defense dan Weight."""
    defense = stats.get('def', 0)
    weight = stats.get('weight', 0)
    reduction = (defense / 150) + (weight / 300)
    
    if stats.get("has_shield"): reduction += 0.10
        
    return max(0.15, min(0.85, reduction)) # Meredam 15% s/d 85% damage

def get_element_multiplier(atk_element, def_element):
    """Menghitung kelemahan dan ketahanan elemen."""
    if atk_element in ELEMENT_CHART:
        if ELEMENT_CHART[atk_element]["strong"] == def_element: return 1.5
        elif ELEMENT_CHART[atk_element]["weak"] == def_element: return 0.5
    return 1.0

def process_staff_magic(element):
    """Efek tambahan khusus jika menggunakan Magic Staff."""
    effects = {
        "Api": {"effect": "burn", "value": 0, "desc": "Membakar musuh"},
        "Air": {"effect": "slow", "value": 0, "desc": "Mengurangi kecepatan musuh"},
        "Petir": {"effect": "stun", "value": 0, "desc": "Peluang musuh terkena Stun"},
        "Angin": {"effect": "dodge_up", "value": 0, "desc": "Meningkatkan Dodge Chance"},
        "Tanah": {"effect": "def_up", "value": 0, "desc": "Meningkatkan Defense"},
        "Cahaya": {"effect": "heal", "value": random.randint(25, 40), "desc": "Memulihkan HP secara instan"},
        "Kegelapan": {"effect": "curse", "value": 0, "desc": "Mengurangi Defense musuh"},
        "Natural": {"effect": "cleanse_mp", "value": 15, "desc": "Memulihkan 15 MP"}
    }
    return effects.get(element, {"effect": "none", "value": 0, "desc": "Tidak ada efek"})

# === LOGIKA CERDAS AI MONSTER ===
def select_smart_skill(m_element, tier_level, is_boss, p_hp_pct, m_hp_pct, m_current_mp):
    """AI Monster akan memilih skill sesuai kondisi HP pemain dan HP dirinya sendiri."""
    available_skills = MONSTER_SKILLS_DB.get(m_element, [])
    valid_skills = [s for s in available_skills if s['cost'] <= m_current_mp]
    
    if not valid_skills: return None
        
    skill_chance = 0.25 + (tier_level * 0.10)
    if is_boss: skill_chance += 0.20
    if random.random() > skill_chance: return None 

    for skill in valid_skills:
        if p_hp_pct <= 0.30 and skill['type'] in ["heavy_damage", "damage_boost"]: return skill
        if m_hp_pct <= 0.40 and skill['type'] in ["heal_self", "vampire"]: return skill
            
    return random.choice(valid_skills)

# === GENERATION & VALIDATION ===
def generate_battle_puzzle(player, tier_level=1, is_boss=False, is_miniboss=False, existing_monster=None):
    """Membuat monster dan mengikatnya dengan Puzzle."""
    p_stats = calculate_equipment_stats(player)
    
    if existing_monster:
        m_name, m_element = existing_monster["monster_name"], existing_monster["monster_element"]
        m_hp, m_max_hp = existing_monster["monster_hp"], existing_monster["monster_max_hp"]
        m_mp, m_max_mp = existing_monster["monster_mp"], existing_monster["monster_max_mp"]
        m_atk, m_def, tier_label = existing_monster["monster_atk"], existing_monster["monster_def"], existing_monster["tier"]
    else:
        m_element = random.choice(ELEMENTS)
        cycle_bonus = player.get('cycle', 1) - 1
        
        if is_boss:
            m_name, tier_label = get_random_boss(), "BOSS"
            m_max_hp, m_max_mp = 300 + (tier_level * 100) + (cycle_bonus * 100), 150 + (cycle_bonus * 50)
            m_atk, m_def = 30 + (tier_level * 5) + (cycle_bonus * 5), 15 + (tier_level * 3)
        elif is_miniboss:
            m_name, tier_label = get_random_mini_boss(), "MINI BOSS"
            m_max_hp, m_max_mp = 150 + (cycle_bonus * 50), 80 + (cycle_bonus * 20)
            m_atk, m_def = 20 + (cycle_bonus * 5), 10 + (cycle_bonus * 2)
        else:
            m_name, tier_label = get_random_monster(tier_level), tier_level
            m_max_hp, m_max_mp = 50 + (tier_level * 30) + (cycle_bonus * 10), 20 + (tier_level * 10)
            m_atk, m_def = 10 + (tier_level * 4) + cycle_bonus, 2 + (tier_level * 2)
            
        m_hp, m_mp = m_max_hp, m_max_mp

    p_hp_pct = player.get('hp', 100) / max(1, player.get('max_hp', 100))
    m_hp_pct = m_hp / max(1, m_max_hp)
    m_skill = select_smart_skill(m_element, tier_level, is_boss, p_hp_pct, m_hp_pct, m_mp)
    
    raw_damage, timer_penalty, skill_msg = m_atk, 0, ""
    if m_skill:
        m_mp -= m_skill['cost']
        skill_msg = f"✨ *{m_name} {m_skill['msg']}*"
        if m_skill["type"] in ["damage_boost", "heavy_damage", "defense_pierce", "vampire"]:
            raw_damage = int(m_atk * m_skill["multiplier"])
            if m_skill["type"] == "defense_pierce": p_stats["def"] = int(p_stats["def"] * 0.5)
        elif m_skill["type"] == "time_cut": timer_penalty = 5 
        elif m_skill["type"] == "heal_self":
            heal = int(m_max_hp * 0.15)
            m_hp = min(m_max_hp, m_hp + heal)
            skill_msg += f" (+{heal} HP)"
            
    final_monster_damage = raw_damage

    if is_boss and random.random() > 0.6:
        target_word = random.choice(["PENJAGA GERBANG", "DUNIA HAMPA", "MEMORI HILANG", "ECLIPTIC EXPRESS", "SANG PENGKHIANAT"])
        scrambled = list(target_word.replace(" ", "")); random.shuffle(scrambled)
        question = f"SANG PENJAGA MENGHADANGMU! Susun segel ini (Tanpa spasi): *{''.join(scrambled).upper()}*"
        answer = target_word.replace(" ", "").lower()
    else:
        question, answer = get_random_puzzle(tier_level, monster_element=m_element, win_streak=player.get('monster_streak', 0))

    timer_limit = 25 if is_boss else (35 if is_miniboss else max(15, 70 - (tier_level * 10)))
    timer_limit = max(10, timer_limit - timer_penalty) 

    return {
        "monster_name": m_name, "monster_element": m_element, "monster_hp": m_hp, "monster_max_hp": m_max_hp,
        "monster_mp": m_mp, "monster_max_mp": m_max_mp, "monster_atk": m_atk, "monster_def": m_def,
        "tier": tier_label, "damage": final_monster_damage, "defense_applied": p_stats["def"],
        "active_skill": m_skill, "skill_message": skill_msg, "question": question, "answer": str(answer).lower(),
        "timer": timer_limit, "is_boss": is_boss, "generated_time": time.time()
    }

def validate_answer(user_answer, correct_answer, generated_time, time_limit):
    """Mengecek apakah jawaban benar dan waktu belum habis."""
    time_taken = time.time() - generated_time
    if time_taken > time_limit: return (False, True, time_taken) 
    if str(user_answer).strip().lower() == str(correct_answer).strip().lower(): return (True, False, time_taken)
    return (False, False, time_taken)
