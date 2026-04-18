# game/logic/combat.py

"""
CORE COMBAT ENGINE - The Archivus (ADVANCED & REFACTORED EDITION)
Sistem Pertarungan Berbasis Data: 
Mendukung Mitigasi Damage Rasio, Turn-Based Logic, 
Modular Status Effects, dan Immersive Battle Logging.
"""
import time
import random

# --- IMPORT SYSTEM (MODULAR ARCHITECTURE) ---
from game.entities.monsters import get_random_monster, get_random_mini_boss, get_random_main_boss
from game.puzzles.manager import get_random_puzzle

# === KONFIGURASI ELEMEN & STATUS ===
ELEMENTAL_CHART = {
    "fire": {"strong": "ice", "weak": "water"},
    "water": {"strong": "fire", "weak": "lightning"},
    "lightning": {"strong": "water", "weak": "earth"},
    "earth": {"strong": "lightning", "weak": "wind"},
    "wind": {"strong": "earth", "weak": "ice"},
    "ice": {"strong": "wind", "weak": "fire"},
    "dark": {"strong": "light", "weak": "light"},
    "light": {"strong": "dark", "weak": "dark"},
    "void": {"strong": "all", "weak": "light"},
    "none": {"strong": "none", "weak": "none"}
}

STATUS_ICONS = {
    "poison": "🤢", "burn": "🔥", "regen": "💖", "stun": "💫", 
    "bleed": "🩸", "atk_buff": "⚔️↑", "def_buff": "🛡️↑"
}

# === SISTEM STATUS EFFECTS ===
def apply_turn_status_effects(entity, is_player=True):
    """
    Memproses DoT/Regen per ronde.
    Mengembalikan total perubahan HP dan list log status.
    """
    hp_change = 0
    logs = []
    effects = entity.get('active_effects' if is_player else 'monster_effects', [])
    
    for effect in effects:
        eff_type = effect.get('type', '').lower()
        val = effect.get('value', 0)
        
        if eff_type == 'poison':
            # Racun: Mengurangi HP berdasarkan persentase atau nilai tetap
            max_hp = entity.get('max_hp' if is_player else 'monster_max_hp', 100)
            dmg = max(1, int(max_hp * 0.05))
            hp_change -= dmg
            logs.append(f"{STATUS_ICONS['poison']}-{dmg}")
        elif eff_type == 'burn':
            # Burn: Damage tetap
            hp_change -= val
            logs.append(f"{STATUS_ICONS['burn']}-{val}")
        elif eff_type == 'regen':
            # Regen: Memulihkan HP
            hp_change += val
            logs.append(f"{STATUS_ICONS['regen']}+{val}")

    return hp_change, logs

# === SISTEM UI RAMPING ===
def get_compact_bar(current, maximum, length=8, bar_type="hp"):
    """Visual Bar padat untuk layar mobile."""
    if maximum <= 0: return "[EMPTY]"
    percent = max(0, min(1, current / maximum))
    filled = int(length * percent)
    empty = length - filled
    
    if bar_type == "hp":
        color = "🟩" if percent > 0.5 else "🟨" if percent > 0.2 else "🟥"
    else:
        color = "🟦"
        
    return f"{color * filled}{'⬜' * empty} `{int(current)}/{int(maximum)}`"

def render_live_battle(player, monster, log_msg="Menunggu tindakanmu..."):
    """Render UI utama pertarungan (Refactored for Cleanliness)."""
    p_status = "".join([STATUS_ICONS.get(e['type'], "") for e in player.get('active_effects', [])])
    m_status = "".join([STATUS_ICONS.get(e['type'], "") for e in monster.get('monster_effects', [])])

    text = (
        f"⚔️ **BATTLE: {monster['monster_name'].upper()}** {m_status}\n"
        f"HP: {get_compact_bar(monster['monster_hp'], monster['monster_max_hp'], bar_type='hp')}\n"
        f"🛡️ Elem: `{monster['monster_element'].title()}`\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **{player.get('name', 'Weaver')}** {p_status}\n"
        f"HP: {get_compact_bar(player['hp'], player['max_hp'], bar_type='hp')}\n"
        f"MP: {get_compact_bar(player.get('mp', 0), player.get('max_mp', 50), bar_type='mp')}\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"📜 **BATTLE LOG:**\n_{log_msg}_\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🧩 **PUZZLE SEALS:**\n`{monster['question']}`\n"
        f"⏳ Sisa Waktu: `{monster['timer']}s`"
    )
    return text

# === MESIN KALKULASI DAMAGE (MITIGASI RASIO) ===
def calculate_damage(attacker, defender, is_attacker_player=True):
    """
    RUMUS: Damage = ATK * (ATK / (ATK + DEF))
    Menjamin damage selalu rasional dan DEF sangat berharga.
    """
    log = []
    
    # Ambil statistik dari player atau data monster
    atk_stats = attacker.get('stats', attacker) if is_attacker_player else attacker
    def_stats = defender.get('stats', defender) if not is_attacker_player else defender

    # 1. Check Dodge
    dodge_chance = def_stats.get("dodge", 0.05)
    if random.random() < dodge_chance:
        return 0, "💨 *MISS!* Serangan meleset."

    # 2. Base Damage Calculation (Mitigasi Rasio)
    atk_type = atk_stats.get("attack_type", "physical")
    if atk_type == "physical":
        atk_val = atk_stats.get("p_atk", 10)
        def_val = def_stats.get("p_def", 5)
    else:
        atk_val = atk_stats.get("m_atk", 10)
        def_val = def_stats.get("m_def", 5)

    # Formula Mitigasi: Mencegah damage 1 jika DEF tinggi, mencegah OP jika ATK tinggi
    # Damage = ATK^2 / (ATK + DEF + 1)
    base_dmg = (atk_val ** 2) / (atk_val + def_val + 1)
    
    # Variance (0.9x - 1.1x) untuk variasi damage
    base_dmg *= random.uniform(0.9, 1.1)

    # 3. Elemental & Crit
    multiplier = 1.0
    atk_element = atk_stats.get("element", attacker.get("element", "none")).lower()
    
    # Cek kelemahan elemen
    def_weakness = def_stats.get("monster_weakness" if not is_attacker_player else "weakness", "none").lower()
    if atk_element == def_weakness and atk_element != "none":
        multiplier *= 1.5
        log.append("🔥 *WEAKNESS!*")

    # Critical Hit
    if random.random() < atk_stats.get("crit_chance", 0.05):
        multiplier *= atk_stats.get("crit_damage", 1.5)
        log.append("💥 *CRITICAL!*")

    final_dmg = max(1, int(base_dmg * multiplier))
    log_msg = " ".join(log) if log else "⚔️ *HIT!*"
    return final_dmg, log_msg

# === GENERATOR PERTEMPURAN ===
def generate_battle_puzzle(player, tier_level=1, is_boss=False, is_miniboss=False):
    """Merakit data pertarungan dengan Scaling & Dynamic Timer."""
    if is_boss:
        m_data = get_random_main_boss()
    elif is_miniboss:
        m_data = get_random_mini_boss()
    else:
        m_data = get_random_monster(tier_level)

    # Scaling HP (Cycle Based) agar musuh makin kuat tiap cycle
    cycle = player.get('cycle', 1)
    hp_scaling = 1 + (cycle * 0.15)
    
    # Dynamic Timer (Berdasarkan Speed Monster)
    m_speed = m_data.get("speed", 5)
    # Kecepatan monster mengurangi waktu yang tersedia bagi pemain
    final_timer = max(10, int(35 - (m_speed * 1.2) + (tier_level * 1.5)))

    # Ambil teka-teki acak sesuai tier
    puzzle_data = get_random_puzzle(tier_level)

    return {
        "monster_name": m_data["name"],
        "monster_hp": int(m_data["base_hp"] * hp_scaling),
        "monster_max_hp": int(m_data["base_hp"] * hp_scaling),
        "monster_element": m_data.get("element", "none"),
        "monster_weakness": m_data.get("weakness", "none"),
        "monster_race": m_data.get("race", "unknown"),
        "monster_effects": [],
        "p_atk": m_data.get("p_atk", 10),
        "m_atk": m_data.get("m_atk", 10),
        "p_def": m_data.get("p_def", 5),
        "m_def": m_data.get("m_def", 5),
        "attack_type": m_data.get("attack_type", "physical"),
        "dodge": m_data.get("dodge_chance", 0.05),
        "crit_chance": m_data.get("crit_chance", 0.05),
        "crit_damage": m_data.get("crit_damage", 1.5),
        "question": puzzle_data["question"],
        "answer": str(puzzle_data["answer"]).strip().lower(),
        "timer": final_timer,
        "tier": tier_level,
        "is_boss": is_boss,
        "exp_reward": m_data.get("exp", 10),
        "gold_reward": m_data.get("gold", 5),
        "drops": m_data.get("drops", []),
        "generated_time": time.time()
    }

def validate_answer(user_answer, correct_answer, generated_time, time_limit):
    """Validasi jawaban dengan pengecekan waktu presisi."""
    time_taken = time.time() - generated_time
    if time_taken > time_limit:
        return (False, True, time_taken) # (Salah, Timeout, Waktu)
    
    is_correct = str(user_answer).strip().lower() == str(correct_answer).strip().lower()
    return (is_correct, False, time_taken)

def process_loot(monster_drops):
    """Sistem Looting Berbasis Chance."""
    obtained = []
    for item in monster_drops:
        if isinstance(item, dict):
            # Cek probabilitas drop (0.0 - 1.0)
            if random.random() <= item.get("chance", 1.0):
                obtained.append(item["id"])
        else:
            obtained.append(item)
    return obtained
