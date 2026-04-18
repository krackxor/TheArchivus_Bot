# utils/helper_ui.py

"""
Helper UI - The Archivus (Refactored for Compact Mobile View)
Dibuat untuk tampilan Telegram Mobile yang bersih, padat, dan dramatis.
Sinkronisasi Penuh dengan main.py & Logic Stats.
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
    
    # Warna Bar berdasarkan persentase
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

def create_exp_bar(current, needed, length=8):
    if needed <= 0: needed = 100
    filled = int((min(current, needed) / needed) * length)
    empty = length - filled
    bar = "🟪" * filled + "⬜" * empty
    return f"{bar} `{int(current)}/{int(needed)}`"

# --- COMBAT UI (REFOCUSED: REDUCED VERTICAL SPACE) ---

def create_combat_header(monster_name, hp, max_hp):
    """Header Ringkas untuk Mobile agar tidak makan tempat."""
    return f"⚔️ **{monster_name.upper()}**\n{create_hp_bar(hp, max_hp, 8)}"

def create_monster_card(monster_name, element, hp, max_hp):
    """Card Monster untuk fase kemunculan."""
    return (f"👾 **{monster_name}**\n"
            f"✨ Elem: `{element.capitalize()}`\n"
            f"❤️ HP: {create_hp_bar(hp, max_hp, 8)}")

def create_combo_indicator(combo_count):
    if combo_count >= 10: return f"🔥 **ULTIMATE x{combo_count}!**"
    elif combo_count >= 5: return f"⚡ **COMBO x{combo_count}!**"
    elif combo_count >= 2: return f"✨ Combo x{combo_count}"
    return ""

def create_boss_warning(boss_name):
    return f"💀 **CRITICAL WARNING** 💀\n⚠️ **{boss_name.upper()} TELAH BANGKIT** ⚠️"

# --- SYSTEM NOTIFICATIONS & SCREENS ---

def create_status_card(player):
    """Refactored: Lebih padat dan informatif tanpa scroll berlebih."""
    stats = calculate_total_stats(player)
    
    # Render Status Efek / Debuff Icon
    status_icons = "".join([e.get('icon', '') for e in player.get('active_effects', [])])
    
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

def create_achievement_notification(ach):
    return f"🏆 **ACHIEVEMENT UNLOCKED**\n{ach.get('icon', '⭐')} **{ach['title']}**\n_{ach['description']}_"

def create_loot_drop(items):
    if not items: return "💨 *Tidak ada loot tersisa...*"
    loot_str = "\n".join([f"🔹 {str(i).replace('_', ' ').title()}" for i in items])
    return f"🎁 **LOOT DITEMUKAN:**\n{loot_str}"

def create_level_up_animation(new_level):
    return f"🆙 **LEVEL UP!**\nSekarang kamu mencapai **Level {new_level}**!"

def create_death_screen(reason, stats):
    return (
        f"💀 **YOU DIED**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"Penyebab: _{reason}_\n\n"
        f"📊 **FINALE:**\n"
        f"⚔️ Kills: `{stats.get('kills', 0)}` | 🔄 Cycle: `{stats.get('cycle', 1)}`"
    )

def create_location_transition(new_loc):
    return f"🌫️ **MEMASUKI AREA BARU**\n📍 **{new_loc.upper()}**"

def create_inventory_display(inventory):
    """Menerima list inventory, merangkum item yang sama."""
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
