# game/logic/combat.py

"""
CORE COMBAT ENGINE - The Archivus (PURE TURN-BASED EDITION)
Sistem Pertarungan Berbasis Data: 
Mendukung Mitigasi Damage Rasio, Modular Status Effects, 
Daily Quest Tracker, dan Immersive Battle Logging.
"""
import random

# --- IMPORT SYSTEM ---
from game.entities.monsters import get_random_monster, get_random_mini_boss, get_random_main_boss
from game.data.quests import update_quest_progress
from game.data.script import MONSTER_WARNINGS

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
    "poison": "🤢", "burn": "🔥", "regen": "💖", "stun": "💫", "freeze": "🧊", 
    "bleed": "🩸", "atk_buff": "⚔️↑", "def_buff": "🛡️↑", "atk_debuff": "⚔️↓", 
    "def_debuff": "🛡️↓", "dodge_buff": "💨↑", "spd_buff": "⚡↑", "m_atk_buff": "🔮↑"
}

# === SISTEM STATUS EFFECTS ===
def apply_turn_status_effects(entity, is_player=True):
    """Memproses DoT/Regen per ronde dan mengurangi durasi efek."""
    hp_change = 0
    logs = []
    
    effect_key = 'active_effects' if is_player else 'monster_effects'
    effects = entity.get(effect_key, [])
    active_effects = []
    
    for effect in effects:
        eff_type = effect.get('type', '').lower()
        val = effect.get('value', 0)
        duration = effect.get('duration', 3)
        
        if duration <= 0: continue
            
        if eff_type == 'poison':
            max_hp = entity.get('max_hp' if is_player else 'monster_max_hp', 100)
            dmg = max(1, int(max_hp * 0.05))
            hp_change -= dmg
            logs.append(f"{STATUS_ICONS.get('poison', '🤢')}-{dmg}")
        elif eff_type == 'bleed':
            dmg = max(1, int(val))
            hp_change -= dmg
            logs.append(f"{STATUS_ICONS.get('bleed', '🩸')}-{dmg}")
        elif eff_type == 'regen':
            hp_change += val
            logs.append(f"{STATUS_ICONS.get('regen', '💖')}+{val}")
            
        effect['duration'] = duration - 1
        if effect['duration'] > 0:
            active_effects.append(effect)

    entity[effect_key] = active_effects
    return hp_change, logs

# === SISTEM UI BATTLE ===
def get_compact_bar(current, maximum, length=8, bar_type="hp"):
    """Visual Bar padat untuk layar mobile."""
    if maximum <= 0: return "[EMPTY]"
    percent = max(0, min(1, current / maximum))
    filled = int(length * percent)
    empty = length - filled
    color = ("🟩" if percent > 0.5 else "🟨" if percent > 0.2 else "🟥") if bar_type == "hp" else "🟦"
    return f"{color * filled}{'⬜' * empty} `{int(current)}/{int(maximum)}`"

def render_live_battle(player, monster, log_msg="Pilih aksimu..."):
    """Render UI utama pertarungan."""
    p_status = "".join([STATUS_ICONS.get(e.get('type', ''), "") for e in player.get('active_effects', [])])
    m_status = "".join([STATUS_ICONS.get(e.get('type', ''), "") for e in monster.get('monster_effects', [])])

    text = (
        f"⚔️ <b>BATTLE: {monster['monster_name'].upper()}</b> {m_status}\n"
        f"HP: {get_compact_bar(monster['monster_hp'], monster['monster_max_hp'], bar_type='hp')}\n"
        f"🛡️ Elem: <code>{monster['monster_element'].title()}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>{player.get('name', 'Weaver')}</b> {p_status}\n"
        f"HP: {get_compact_bar(player['hp'], player['max_hp'], bar_type='hp')}\n"
        f"MP: {get_compact_bar(player.get('mp', 0), player.get('max_mp', 50), bar_type='mp')}\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"📜 <b>LOG:</b>\n{log_msg}"
    )
    return text

# === MESIN KALKULASI DAMAGE ===
def calculate_damage(attacker, defender, is_attacker_player=True):
    """Rumus Damage: ATK^2 / (ATK + DEF)."""
    log = []
    atk_stats = attacker.get('stats', attacker) if is_attacker_player else attacker
    def_stats = defender.get('stats', defender) if not is_attacker_player else defender

    if random.random() < def_stats.get("dodge", 0.05):
        return 0, "💨 <i>MISS!</i> Serangan meleset."

    atk_type = atk_stats.get("attack_type", "physical")
    atk_val = atk_stats.get("p_atk" if atk_type == "physical" else "m_atk", 10)
    def_val = def_stats.get("p_def" if atk_type == "physical" else "m_def", 5)

    base_dmg = (atk_val ** 2) / (atk_val + def_val + 1)
    base_dmg *= random.uniform(0.9, 1.1)

    multiplier = 1.0
    atk_element = atk_stats.get("element", "none").lower()
    def_weakness = def_stats.get("monster_weakness" if not is_attacker_player else "weakness", "none").lower()
    
    if atk_element == def_weakness and atk_element != "none":
        multiplier *= 1.5
        log.append("🔥 <i>WEAKNESS!</i>")

    if random.random() < atk_stats.get("crit_chance", 0.05):
        multiplier *= atk_stats.get("crit_damage", 1.5)
        log.append("💥 <i>CRITICAL!</i>")

    final_dmg = max(1, int(base_dmg * multiplier))
    return final_dmg, " ".join(log) if log else "⚔️ <i>HIT!</i>"

# === LOGIKA SETELAH PERTARUNGAN (REWARD & QUEST) ===
def finalize_battle(player, monster):
    """Memproses Reward, Loot, dan Update Daily Quest."""
    quest_msgs = []
    
    # 1. Update Progres Quest Slayer
    if monster.get('is_boss'):
        player, quest_msgs = update_quest_progress(player, "kill_boss")
    else:
        player, quest_msgs = update_quest_progress(player, "kill_monsters")
    
    # 2. Update Gold Progress Quest
    player, gold_quest_msg = update_quest_progress(player, "earn_gold", monster['gold_reward'])
    if gold_quest_msg: quest_msgs.extend(gold_quest_msg)
    
    # 3. Proses Loot (Looting Quest)
    loot = process_loot(monster['drops'])
    if loot:
        player, loot_quest_msg = update_quest_progress(player, "collect_drops", len(loot))
        if loot_quest_msg: quest_msgs.extend(loot_quest_msg)
        player.setdefault('inventory', []).extend(loot)

    return player, loot, quest_msgs

# === GENERATOR PERTEMPURAN ===
def generate_battle_data(player, tier_level=1, is_boss=False, is_miniboss=False):
    """Merakit musuh dan menyisipkan peringatan dari script.py."""
    if is_boss: m_data = get_random_main_boss()
    elif is_miniboss: m_data = get_random_mini_boss()
    else: m_data = get_random_monster(tier_level)

    scaling = 1 + (player.get('cycle', 1) * 0.15)
    
    return {
        "monster_name": m_data["name"],
        "monster_hp": int(m_data["base_hp"] * scaling),
        "monster_max_hp": int(m_data["base_hp"] * scaling),
        "monster_element": m_data.get("element", "none"),
        "monster_weakness": m_data.get("weakness", "none"),
        "monster_effects": [],
        "p_atk": m_data.get("p_atk", 10),
        "m_atk": m_data.get("m_atk", 10),
        "p_def": m_data.get("p_def", 5),
        "m_def": m_data.get("m_def", 5),
        "is_boss": is_boss or is_miniboss,
        "exp_reward": m_data.get("exp", 10),
        "gold_reward": m_data.get("gold", 5),
        "drops": m_data.get("drops", []),
        "warning_msg": random.choice(MONSTER_WARNINGS) # Dari script.py
    }

def process_loot(monster_drops):
    obtained = []
    for item in monster_drops:
        chance = item.get("chance", 1.0) if isinstance(item, dict) else 1.0
        if random.random() <= chance:
            obtained.append(item["id"] if isinstance(item, dict) else item)
    return obtained
