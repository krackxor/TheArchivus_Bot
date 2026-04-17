"""
CORE COMBAT ENGINE - The Archivus (RPG ADVANCED EDITION)
Sistem Pertarungan Berbasis Data: 
Mendukung Physical/Magic Damage, Elemental Multiplier, Speed-based Timer, 
Dodge, Crit, AI Behavior, Loot Drops, dan STATUS EFFECTS (Buff/Debuff).
"""
import time
import random

# --- IMPORT SYSTEM (MODULAR ARCHITECTURE) ---
from game.entities.monsters import get_random_monster, get_random_mini_boss, get_random_main_boss
from game.puzzles.manager import get_random_puzzle

# === KONFIGURASI ELEMEN ===
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
    "blood": {"strong": "none", "weak": "ice"},
    "poison": {"strong": "none", "weak": "fire"},
    "none": {"strong": "none", "weak": "none"}
}

# === SISTEM STATUS EFFECTS ===
STATUS_ICONS = {
    "poison": "🤢",
    "burn": "🔥",
    "regen": "💖",
    "stun": "💫",
    "bleed": "🩸",
    "atk_buff": "⚔️+",
    "def_buff": "🛡️+",
    "speed_debuff": "👟-"
}

def apply_turn_status_effects(entity, is_player=True):
    """
    Memproses efek berkala (DoT/Regen) setiap ronde.
    entity: data player (dict) atau data puzzle monster (dict).
    Mengembalikan: (total_hp_change, list_log_pesan)
    """
    hp_change = 0
    logs = []
    
    # Player menggunakan 'active_effects', monster menggunakan 'monster_effects'
    effects = entity.get('active_effects' if is_player else 'monster_effects', [])
    name_label = "Weaver" if is_player else entity.get('monster_name', 'Musuh')

    for effect in effects:
        eff_type = effect.get('type', '').lower()
        val = effect.get('value', 0)
        
        if eff_type == 'poison':
            # Mengurangi HP berdasarkan persentase (misal 5% Max HP)
            max_hp = entity.get('max_hp' if is_player else 'monster_max_hp', 100)
            dmg = max(1, int(max_hp * 0.05))
            hp_change -= dmg
            logs.append(f"{STATUS_ICONS['poison']} {name_label} terkena racun! (-{dmg} HP)")
            
        elif eff_type == 'regen':
            hp_change += val
            logs.append(f"{STATUS_ICONS['regen']} {name_label} memulihkan diri! (+{val} HP)")
            
        elif eff_type == 'bleed':
            hp_change -= val
            logs.append(f"{STATUS_ICONS['bleed']} Luka {name_label} terbuka! (-{val} HP)")

    return hp_change, logs

# === SISTEM UI & VISUAL ===
def get_dynamic_bar(current, maximum, length=10, type_bar="hp"):
    """Menghasilkan bar visual untuk HP atau MP"""
    if maximum <= 0: return "[Empty]"
    percent = max(0, min(1, current / maximum))
    filled = int(length * percent)
    
    if type_bar == "hp":
        emoji = "🟩" if percent > 0.6 else "🟨" if percent > 0.3 else "🟥"
    else:
        emoji = "🟦"
        
    bar = (emoji * filled) + ("⬜" * (length - filled))
    return f"{bar} {int(current)}/{int(maximum)}"

def render_live_battle(player, monster, log_msg="Menunggu tindakanmu..."):
    """Tampilan UI Pertempuran untuk Telegram dengan Status Effects"""
    p_hp_view = get_dynamic_bar(player.get('hp', 0), player.get('max_hp', 100), type_bar="hp")
    m_hp_view = get_dynamic_bar(monster.get('monster_hp', 0), monster.get('monster_max_hp', 100), type_bar="hp")
    
    # Render Icon Status Player
    p_status = "".join([STATUS_ICONS.get(e['type'], "") for e in player.get('active_effects', [])])
    # Render Icon Status Monster
    m_status = "".join([STATUS_ICONS.get(e['type'], "") for e in monster.get('monster_effects', [])])

    text = (
        f"⚔️ **BATTLE: {monster['monster_name'].upper()}** ⚔️\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"👾 **MUSUH** {m_status}\n"
        f"❤️ HP: {m_hp_view}\n"
        f"✨ Elem: `{monster['monster_element'].capitalize()}` | 🧬 Ras: `{monster['monster_race'].capitalize()}`\n\n"
        f"👤 **WEAVER** {p_status} ({player.get('current_job', 'Novice Weaver')})\n"
        f"❤️ HP: {p_hp_view}\n"
        f"🔵 MP: {player.get('mp', 0)}/{player.get('max_mp', 50)}\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"📜 **LOG:**\n"
        f"_{log_msg}_\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"❓ **TEKA-TEKI:**\n"
        f"`{monster['question']}`\n\n"
        f"⏳ Sisa Waktu: `{monster['timer']}s`"
    )
    return text

# === MESIN KALKULASI DAMAGE ===
def calculate_damage(attacker, defender, is_attacker_player=True):
    """Rumus Damage Utama: ATK vs DEF + Efek Stat + Element + Crit + Dodge"""
    log = []
    
    # Stats pemain sudah termasuk buff dari stats.py
    atk_stats = attacker.get('stats', attacker) if is_attacker_player else attacker
    def_stats = defender.get('stats', defender) if not is_attacker_player else defender

    # 1. Cek Dodge (Stat dodge dipengaruhi weight_penalty di stats.py)
    dodge_chance = def_stats.get("dodge", 0.05) if not is_attacker_player else def_stats.get('stats', {}).get('dodge', 0.05)
    if random.random() < dodge_chance:
        return 0, "💨 *MELLESAT!* Serangan gagal mengenai target."

    # 2. Tentukan Jenis Serangan
    atk_type = atk_stats.get("attack_type", "physical")
    if atk_type == "physical":
        raw_dmg = atk_stats.get("p_atk", 10) - def_stats.get("p_def", 5)
    else:
        raw_dmg = atk_stats.get("m_atk", 10) - def_stats.get("m_def", 5)
    
    raw_dmg = max(1, raw_dmg)

    # 3. Multiplier Elemen
    atk_element = atk_stats.get("element", attacker.get("element", "none")).lower()
    def_element = def_stats.get("monster_element" if not is_attacker_player else "element", "none").lower()
    def_weakness = def_stats.get("monster_weakness" if not is_attacker_player else "weakness", "none").lower()
    
    multiplier = 1.0
    if atk_element == def_weakness and atk_element != "none":
        multiplier = 1.5
        log.append("🔥 *WEAKNESS!*")
    elif def_element in ELEMENTAL_CHART.get(atk_element, {}).get("weak", []):
        multiplier = 0.5
        log.append("🛡️ *RESISTANT.*")

    # 4. Critical
    crit_chance = atk_stats.get("crit_chance", 0.05)
    if random.random() < crit_chance:
        multiplier *= atk_stats.get("crit_damage", 1.5)
        log.append("💥 *CRITICAL!*")

    final_dmg = int(raw_dmg * multiplier)
    log_msg = " ".join(log) if log else "⚔️ *HIT!*"
    return final_dmg, log_msg

# === GENERATOR PERTEMPURAN ===
def generate_battle_puzzle(player, tier_level=1, is_boss=False, is_miniboss=False):
    """Merakit data pertarungan termasuk inisialisasi status monster"""
    if is_boss:
        m_data = get_random_main_boss()
    elif is_miniboss:
        m_data = get_random_mini_boss()
    else:
        m_data = get_random_monster(tier_level)

    cycle = player.get('cycle', 1)
    hp_scaling = 1 + (cycle * 0.1) 
    
    m_speed = m_data.get("speed", 5)
    base_timer = 20 if is_boss else 35
    timer_penalty = m_speed * 1.5
    final_timer = max(10, int(base_timer - timer_penalty + (tier_level * 2)))

    puzzle_data = get_random_puzzle(tier_level)

    return {
        "monster_name": m_data["name"],
        "monster_hp": int(m_data["base_hp"] * hp_scaling),
        "monster_max_hp": int(m_data["base_hp"] * hp_scaling),
        "monster_element": m_data.get("element", "none"),
        "monster_weakness": m_data.get("weakness", "none"),
        "monster_race": m_data.get("race", "unknown"),
        "monster_effects": [], # Inisialisasi daftar Buff/Debuff Monster
        "p_atk": m_data.get("p_atk", 10),
        "m_atk": m_data.get("m_atk", 10),
        "p_def": m_data.get("p_def", 5),
        "m_def": m_data.get("m_def", 5),
        "speed": m_speed,
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
    """Validasi jawaban dan waktu tempuh"""
    time_taken = time.time() - generated_time
    if time_taken > time_limit:
        return (False, True, time_taken)
    
    is_correct = str(user_answer).strip().lower() == str(correct_answer).strip().lower()
    return (is_correct, False, time_taken)

def process_loot(monster_drops):
    """Mengecek item mana yang jatuh dari monster"""
    obtained = []
    for item in monster_drops:
        if isinstance(item, dict):
            if random.random() <= item.get("chance", 1.0):
                obtained.append(item["id"])
        elif isinstance(item, str):
            obtained.append(item)
    return obtained
