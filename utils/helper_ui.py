# utils/helper_ui.py

"""
Helper UI - The Archivus (Refactored for Compact Mobile View)
Dibuat untuk tampilan Telegram Mobile yang bersih, padat, dan dramatis.
Sinkronisasi Penuh dengan main.py, Logic Stats, & Environment System.
"""

import math
from game.logic.stats import calculate_total_stats
from game.items import get_item

# --- PROGRESS BARS (REFOCUSED: COMPACT & BLOCK) ---

def create_hp_bar(current, maximum, length=8):
    if maximum <= 0: maximum = 1
    current = max(0, min(current, maximum))
    percent = current / maximum
    filled = int(percent * length)
    empty = length - filled
    
    # Warna Bar dinamis
    if percent > 0.6: bar_char = "🟩"
    elif percent > 0.2: bar_char = "🟨"
    else: bar_char = "🟥"
        
    bar = bar_char * filled + "⬜" * empty
    return f"{bar} `{int(current)}/{int(maximum)}`"

def create_mp_bar(current, maximum, length=8):
    if maximum <= 0: maximum = 1
    current = max(0, min(current, maximum))
    filled = int((current / maximum) * length)
    empty = length - filled
    bar = "🟦" * filled + "⬜" * empty
    return f"{bar} `{int(current)}/{int(maximum)}`"

def create_energy_bar(current, max_val=100, length=8):
    current = max(0, min(current, max_val))
    filled = int((current / max_val) * length)
    empty = length - filled
    bar = "🟧" * filled + "⬜" * empty
    return f"{bar} `{int(current)}%`"

# --- ENVIRONMENT & HAZARD UI ---

def create_hazard_alert(hazard_name, danger_msg, is_protected=False):
    """Peringatan area beracun/dingin/gelap."""
    header = "🛡️ **AREA TERKENDALI**" if is_protected else "⚠️ **PERINGATAN BAHAYA**"
    icon = "☣️" if "RACUN" in hazard_name.upper() else "❄️" if "DINGIN" in hazard_name.upper() else "🌑"
    
    return (
        f"{header}\n"
        f"{icon} **{hazard_name}**\n"
        f"_{danger_msg}_"
    )

def create_deadly_event_card(event_name, description, stat_required):
    """Card untuk event maut seperti Jurang atau Trap."""
    return (
        f"💀 **EVENT MAUT: {event_name.upper()}**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"{description}\n\n"
        f"🎲 **MEMBUTUHKAN:** `{stat_required.upper()}`"
    )

# --- COMBAT UI ---

def create_combat_header(monster_name, hp, max_hp):
    return f"⚔️ **{monster_name.upper()}**\n{create_hp_bar(hp, max_hp, 8)}"

def create_combo_indicator(combo_count):
    if combo_count >= 10: return f"🔥 **ULTIMATE x{combo_count}!**"
    elif combo_count >= 5: return f"⚡ **COMBO x{combo_count}!**"
    elif combo_count >= 2: return f"✨ Combo x{combo_count}"
    return ""

# --- SYSTEM NOTIFICATIONS ---

def create_status_card(player):
    stats = calculate_total_stats(player)
    # Render Status Efek Aktif (Buff/Debuff)
    active_effects = player.get('active_effects', [])
    status_icons = "".join([e.get('icon', '') for e in active_effects])
    
    return (
        f"👤 **{player.get('username', 'Weaver')}** {status_icons}\n"
        f"🎖️ `{player.get('current_job', 'Novice')}` | Lvl {player.get('level', 1)}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"⚔️ ATK: `{stats['p_atk']}` | 🛡️ DEF: `{stats['p_def']}`\n"
        f"👟 SPD: `{stats['speed']}` | ⚖️ WGT: `{stats['total_weight']}`\n"
        f"━━━━━━━━━━━━━━━\n"
        f"HP: {create_hp_bar(player.get('hp', 0), player.get('max_hp', 100))}\n"
        f"MP: {create_mp_bar(player.get('mp', 0), player.get('max_mp', 50))}\n"
        f"EN: {create_energy_bar(player.get('energy', 100))}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💰 `{player.get('gold', 0):,} G` | 🔄 Cy: `{player.get('cycle', 1)}`"
    )

def create_loot_drop(items):
    if not items: return "💨 *Hanya debu yang tersisa...*"
    loot_str = "\n".join([f"🔹 {str(i).replace('_', ' ').title()}" for i in items])
    return f"🎁 **LOOT DITEMUKAN:**\n{loot_str}"

def create_death_screen(reason, killer_name="Kegelapan"):
    return (
        f"💀 **KAU TELAH GUGUR**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"Penyebab: _{reason}_\n"
        f"Oleh: **{killer_name}**\n\n"
        f"🕯️ _Jiwa Weaver kembali ke siklus..._"
    )

def create_inventory_display(inventory):
    if not inventory: return "🎒 *Tas Kosong*"
    display = "🎒 **INVENTORY**\n━━━━━━━━━━━━━━━\n"
    counts = {}
    for item in inventory:
        counts[item] = counts.get(item, 0) + 1
    for item_id, count in counts.items():
        item_data = get_item(item_id)
        name = item_data['name'] if item_data else item_id.replace("_", " ").title()
        display += f"• {name} `x{count}`\n"
    return display
