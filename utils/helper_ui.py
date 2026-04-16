# utils/helper_ui.py

"""
Helper UI - The Archivus (Advanced Edition)
Dibuat untuk tampilan Telegram Mobile yang bersih dan dramatis.
Sinkronisasi Penuh dengan main.py & Logic Stats.
"""

import math
from game.logic.stats import calculate_total_stats
from game.items import get_item

# --- PROGRESS BARS ---

def create_hp_bar(current, maximum, length=10):
    if maximum <= 0: maximum = 1
    current = max(0, min(current, maximum))
    filled = int((current / maximum) * length)
    empty = length - filled
    
    if current / maximum > 0.6: bar_char = "🟩"
    elif current / maximum > 0.2: bar_char = "🟨"
    else: bar_char = "🟥"
        
    bar = bar_char * filled + "⬜" * empty
    return f"{bar} {int(current)}/{int(maximum)}"

def create_mp_bar(current, maximum, length=10):
    if maximum <= 0: maximum = 1
    current = max(0, min(current, maximum))
    filled = int((current / maximum) * length)
    empty = length - filled
    bar = "🟦" * filled + "⬜" * empty
    return f"{bar} {int(current)}/{int(maximum)}"

def create_energy_bar(current, max_val=100, length=10):
    if max_val <= 0: max_val = 100
    current = max(0, min(current, max_val))
    filled = int((current / max_val) * length)
    empty = length - filled
    bar = "🟧" * filled + "⬜" * empty
    return f"{bar} {int(current)}%"

def create_exp_bar(current, needed, length=10):
    if needed <= 0: needed = 100
    filled = int((min(current, needed) / needed) * length)
    empty = length - filled
    bar = "🟪" * filled + "⬜" * empty
    return f"{bar} {int(current)}/{int(needed)}"

# --- COMBAT UI ---

def create_combat_header(monster_name, hp, max_hp):
    """Sesuai permintaan main.py baris 41"""
    return f"""━━━━━━━━━━━━━━━━━━━━
👾 *{monster_name.upper()}*
{create_hp_bar(hp, max_hp, 10)}
━━━━━━━━━━━━━━━━━━━━"""

def create_monster_card(monster_name, element, hp, max_hp):
    return f"""🦇 *{monster_name}*
✨ Elemen: {element.capitalize()}
❤️ HP: {create_hp_bar(hp, max_hp, 8)}"""

def create_combo_indicator(combo_count):
    if combo_count >= 5: return f"🔥🔥🔥 *LEGENDARY COMBO x{combo_count}!* 🔥🔥🔥"
    elif combo_count >= 3: return f"⚡⚡ *COMBO x{combo_count}!* ⚡⚡"
    elif combo_count >= 2: return f"✨ Combo x{combo_count} ✨"
    return ""

def create_boss_warning(boss_name):
    return f"⚠️ ━━━━━━━━━━━━━━ ⚠️\n💀 *WARNING: {boss_name.upper()}* 💀\n⚠️ ━━━━━━━━━━━━━━ ⚠️"

# --- SYSTEM NOTIFICATIONS ---

def create_status_card(player):
    """Menampilkan stats lengkap sesuai logic/stats.py"""
    stats = calculate_total_stats(player)
    
    debuff_txt = ""
    if player.get('debuffs'):
        debuff_txt = f"\n⚠️ *STATUS:* {', '.join([d.upper() for d in player['debuffs']])}"

    return f"""━━━━━━━━━━━━━━━━━━━━
👤 *{player.get('username', 'Weaver')}*
🎖️ Class: {player.get('current_job', 'Novice Weaver')}
🔄 Cycle: {player.get('cycle', 1)} | Level: {player.get('level', 1)}
━━━━━━━━━━━━━━━━━━━━
⚔️ *Atk:* {stats['p_atk']} | 🛡️ *Def:* {stats['p_def']}
⚖️ *Berat:* {stats['total_weight']} | 💨 *Speed:* {stats['speed']}
✨ *Elemen:* {stats['element'].capitalize()}{debuff_txt}

❤️ HP:  {create_hp_bar(player.get('hp', 0), player.get('max_hp', 100), 8)}
🔮 MP:  {create_mp_bar(player.get('mp', 0), player.get('max_mp', 50), 8)}
⚡ EN:  {create_energy_bar(player.get('energy', 100), 100, 8)}
━━━━━━━━━━━━━━━━━━━━
💰 Gold: {player.get('gold', 0):,} | 💀 Kills: {player.get('kills', 0)}
📍 {player.get('location', 'The Whispering Hall')}
━━━━━━━━━━━━━━━━━━━━"""

def create_achievement_notification(ach):
    """Menerima object achievement sesuai main.py baris 37"""
    return f"🎉 *ACHIEVEMENT UNLOCKED!* 🎉\n{ach.get('icon', '⭐')} *{ach['title']}*\n_{ach['description']}_\n🎁 Reward: {ach.get('rewards', '-')}"

def create_loot_drop(items):
    if not items: return "💨 Tidak ada yang tersisa..."
    loot_str = "\n".join([f"🔹 {str(i).replace('_', ' ').title()}" for i in items])
    return f"🎁 **LOOT DITEMUKAN:**\n{loot_str}"

def create_level_up_animation(new_level):
    return f"✨🎊 **LEVEL UP!** 🎊✨\nKau kini mencapai level **{new_level}**!"

def create_death_screen(reason, stats):
    return f"""━━━━━━━━━━━━━━━━━━━━
💀 *YOU DIED* 💀
━━━━━━━━━━━━━━━━━━━━
Penyebab: {reason}

📊 STATS:
⚔️ Kills: {stats.get('kills', 0)}
🔄 Cycle: {stats.get('cycle', 1)}
💰 Gold Lost: {stats.get('gold_lost', 0)}
━━━━━━━━━━━━━━━━━━━━"""

def create_daily_quest_card(quests, player=None):
    card = "━━━━━━━━━━━━━━━━━━━━\n📋 *DAILY QUESTS*\n━━━━━━━━━━━━━━━━━━━━\n"
    for q in quests:
        card += f"▫️ {q['title']}: {q['target']} (Reward: {q['reward']['gold']}G)\n"
    return card

def create_location_transition(new_loc):
    """Hanya menerima 1 argumen sesuai main.py baris 48"""
    return f"🌫️ ━━━━━━━━━━━━━━ 🌫️\n📍 MEMASUKI AREA BARU\n✨ *{new_loc}* ✨\n🌫️ ━━━━━━━━━━━━━━ 🌫️"

def create_inventory_display(inventory):
    """Menerima list inventory sesuai main.py baris 49"""
    if not inventory: return "🎒 *INVENTORY KOSONG*"
    
    display = "🎒 *INVENTORY*\n━━━━━━━━━━━━━━━━━━━━\n"
    counts = {}
    for item in inventory:
        counts[item] = counts.get(item, 0) + 1
        
    for item_id, count in counts.items():
        item_data = get_item(item_id)
        name = item_data['name'] if item_data else item_id.replace("_", " ").title()
        display += f"• {name} (x{count})\n"
        
    return display + "━━━━━━━━━━━━━━━━━━━━"
