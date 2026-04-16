# game/systems/combat.py

"""
CORE COMBAT ENGINE - The Archivus (RPG ADVANCED EDITION)
Sistem Pertarungan Berbasis Data: 
Mendukung Physical/Magic Damage, Elemental Multiplier, Speed-based Timer, 
Dodge, Crit, AI Behavior, dan Loot Drops.
"""
import time
import random

# Import Database & Entities
from game.data.monster_data import MONSTER_POOL
from game.entities.monsters import get_random_monster
from game.entities.minibosses import get_random_mini_boss
from game.entities.mainbosses import get_random_main_boss
from game.puzzles.manager import get_random_puzzle

# === KONFIGURASI ELEMEN (Batu-Gunting-Kertas) ===
ELEMENTAL_CHART = {
    "fire": {"strong": "ice", "weak": "water"},
    "water": {"strong": "fire", "weak": "lightning"},
    "lightning": {"strong": "water", "weak": "earth"},
    "earth": {"strong": "lightning", "weak": "ice"},
    "ice": {"strong": "water", "weak": "fire"},
    "dark": {"strong": "light", "weak": "light"}, # Dark/Light saling bunuh
    "light": {"strong": "dark", "weak": "dark"},
    "void": {"strong": "all", "weak": "light"},
    "blood": {"strong": "none", "weak": "ice"},
    "poison": {"strong": "none", "weak": "fire"}
}

# === SISTEM UI & VISUAL ===
def get_dynamic_bar(current, maximum, length=10, type_bar="hp"):
    """Menghasilkan bar visual untuk HP atau MP"""
    if maximum <= 0: return "[Empty]"
    percent = max(0, min(1, current / maximum))
    filled = int(length * percent)
    
    if type_bar == "hp":
        emoji = "🟢" if percent > 0.6 else "🟡" if percent > 0.3 else "🔴"
    else:
        emoji = "🔵"
        
    bar = (emoji * filled) + ("⚫" * (length - filled))
    return f"[{bar}] {int(current)}/{int(maximum)}"

def render_live_battle(player, monster, log_msg="Menunggu tindakanmu..."):
    """Tampilan UI Pertempuran untuk Telegram"""
    p_hp_view = get_dynamic_bar(player.get('hp', 0), player.get('max_hp', 100), type_bar="hp")
    m_hp_view = get_dynamic_bar(monster.get('monster_hp', 0), monster.get('monster_max_hp', 100), type_bar="hp")
    
    # Tambahkan info Elemen dan Ras
    text = (
        f"⚔️ **BATTLE: {monster['monster_name'].upper()}** ⚔️\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"👾 **MUSUH**\n"
        f"❤️ HP: {m_hp_view}\n"
        f"✨ Elem: `{monster['monster_element']}` | 🧬 Ras: `{monster['monster_race']}`\n\n"
        f"👤 **WEAVER**\n"
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
    """Rumus Damage Utama: P_ATK/M_ATK vs P_DEF/M_DEF + Element + Crit + Dodge"""
    log = []
    
    # 1. Cek Dodge (Menghindar)
    dodge_chance = defender.get("dodge_chance", 0.05)
    if random.random() < dodge_chance:
        return 0, "💨 *MELLESAT!* Serangan gagal mengenai target."

    # 2. Tentukan Jenis Serangan (Physical vs Magic)
    atk_type = attacker.get("attack_type", "physical")
    if atk_type == "physical":
        raw_dmg = attacker.get("p_atk", 10) - defender.get("p_def", 5)
    else:
        raw_dmg = attacker.get("m_atk", 10) - defender.get("m_def", 5)
    
    raw_dmg = max(1, raw_dmg)

    # 3. Hitung Multiplier Elemen
    atk_element = attacker.get("element", "none").lower()
    def_element = defender.get("element", "none").lower()
    def_weakness = defender.get("weakness", "none").lower()
    
    multiplier = 1.0
    if atk_element == def_weakness:
        multiplier = 1.5
        log.append("🔥 *WEAKNESS!*")
    elif def_element in ELEMENTAL_CHART.get(atk_element, {}).get("weak", []):
        multiplier = 0.5
        log.append("🛡️ *RESISTANT.*")

    # 4. Hitung Critical
    if random.random() < attacker.get("crit_chance", 0.05):
        multiplier *= attacker.get("crit_damage", 1.5)
        log.append("💥 *CRITICAL!*")

    final_dmg = int(raw_dmg * multiplier)
    return final_dmg, " ".join(log)

# === GENERATOR PERTEMPURAN ===
def generate_battle_puzzle(player, tier_level=1, is_boss=False, is_miniboss=False):
    """Merakit data pertarungan berdasarkan database RPG terbaru"""
    
    # 1. Ambil Data Entitas dari Database
    if is_boss:
        m_data = get_random_main_boss()
    elif is_miniboss:
        m_data = get_random_mini_boss()
    else:
        m_data = get_random_monster(tier_level)

    # 2. Scaling (Opsional - Jika data mentah mau ditambah berdasarkan cycle)
    cycle = player.get('cycle', 1)
    hp_scaling = 1 + (cycle * 0.1) # Naiki 10% per cycle
    
    # 3. Tentukan Puzzle & Timer (Timer dipengaruhi Speed Monster)
    # Semakin tinggi speed monster, timer pemain makin berkurang!
    m_speed = m_data.get("speed", 5)
    base_timer = 20 if is_boss else 35
    timer_penalty = m_speed * 1.5
    final_timer = max(10, int(base_timer - timer_penalty + (tier_level * 2)))

    puzzle = get_random_puzzle(tier_level)

    # 4. Bundle data untuk state game
    return {
        "monster_name": m_data["name"],
        "monster_hp": int(m_data["base_hp"] * hp_scaling),
        "monster_max_hp": int(m_data["base_hp"] * hp_scaling),
        "monster_element": m_data["element"],
        "monster_weakness": m_data["weakness"],
        "monster_race": m_data["race"],
        "monster_p_atk": m_data["p_atk"],
        "monster_m_atk": m_data["m_atk"],
        "monster_p_def": m_data["p_def"],
        "monster_m_def": m_data["m_def"],
        "monster_speed": m_speed,
        "attack_type": m_data["attack_type"],
        "dodge_chance": m_data["dodge_chance"],
        "crit_chance": m_data["crit_chance"],
        "crit_damage": m_data["crit_damage"],
        "ai_behavior": m_data["ai_behavior"],
        "question": puzzle["question"],
        "answer": puzzle["answer"].lower(),
        "timer": final_timer,
        "exp_reward": m_data["exp"],
        "gold_reward": m_data["gold"],
        "drops": m_data["drops"],
        "death_narration": m_data["death_narration"],
        "generated_time": time.time()
    }

def validate_answer(user_answer, correct_answer, generated_time, time_limit):
    """Validasi jawaban dan waktu tempuh"""
    time_taken = time.time() - generated_time
    if time_taken > time_limit:
        return (False, True, time_taken) # (is_correct, is_timeout, time)
    
    is_correct = str(user_answer).strip().lower() == str(correct_answer).strip().lower()
    return (is_correct, False, time_taken)

def process_loot(monster_drops):
    """Mengecek item mana yang jatuh dari monster"""
    obtained = []
    for item in monster_drops:
        if random.random() < item["chance"]:
            obtained.append(item["id"])
    return obtained
