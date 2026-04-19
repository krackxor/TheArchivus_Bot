# utils/helper_ui.py

"""
Helper UI - The Archivus (Clean Mobile UI)
Komponen visual yang konsisten dan mudah dibaca di mobile
"""

from game.ui_constants import Icon, Text, BarColor, Lang, format_currency, format_stat

# ============================================================================
# PROGRESS BARS - Ringkas & Konsisten
# ============================================================================

def create_hp_bar(current, maximum, length=8):
    """Bar HP dengan warna dinamis"""
    if maximum <= 0: maximum = 1
    current = max(0, min(current, maximum))
    percent = current / maximum
    filled = int(percent * length)
    empty = length - filled
    
    if percent > 0.6: 
        bar_char = BarColor.HP_HIGH
    elif percent > 0.2: 
        bar_char = BarColor.HP_MID
    else: 
        bar_char = BarColor.HP_LOW
        
    return f"{bar_char * filled}{BarColor.EMPTY * empty} `{int(current)}/{int(maximum)}`"

def create_mp_bar(current, maximum, length=8):
    """Bar MP warna biru"""
    if maximum <= 0: maximum = 1
    current = max(0, min(current, maximum))
    filled = int((current / maximum) * length)
    empty = length - filled
    return f"{BarColor.MP * filled}{BarColor.EMPTY * empty} `{int(current)}/{int(maximum)}`"

def create_energy_bar(current, max_val=100, length=8):
    """Bar Energi warna oranye"""
    current = max(0, min(current, max_val))
    filled = int((current / max_val) * length)
    empty = length - filled
    return f"{BarColor.ENERGY * filled}{BarColor.EMPTY * empty} `{int(current)}%`"

def create_exp_bar(current, needed, length=8):
    """Bar EXP warna ungu"""
    if needed <= 0: needed = 100
    percent = min(current / needed, 1.0)
    filled = int(percent * length)
    empty = length - filled
    return f"{BarColor.EXP * filled}{BarColor.EMPTY * empty} `{int(current)}/{int(needed)}`"


# ============================================================================
# NOTIFIKASI SISTEM - Lebih Ringkas
# ============================================================================

def create_level_up_notification(new_level):
    """Notifikasi level up yang ringkas"""
    return (
        f"{Icon.LEVEL} **NAIK LEVEL!**\n"
        f"{Text.LINE_SHORT}\n"
        f"Kamu sekarang **Level {new_level}**\n"
        f"{Icon.HP} HP/MP pulih penuh!\n"
        f"{Icon.STAR} +3 Stat Points"
    )

def create_achievement_notification(ach):
    """Notifikasi achievement"""
    return (
        f"{Icon.STAR} **ACHIEVEMENT!**\n"
        f"{Text.LINE_SHORT}\n"
        f"{ach.get('icon', '⭐')} **{ach['title']}**\n"
        f"_{ach['description']}_\n"
        f"{Icon.REWARD} {ach.get('rewards', 'Reward')}"
    )

def create_location_transition(new_loc):
    """Notifikasi pindah area"""
    return (
        f"{Icon.LOCATION} **AREA BARU**\n"
        f"{Text.LINE_SHORT}\n"
        f"**{new_loc.upper()}**"
    )

def create_quest_notification(quest_title, progress="", complete=False):
    """Notifikasi quest progress"""
    if complete:
        return f"{Icon.COMPLETE} **{quest_title}** selesai!"
    else:
        return f"{Icon.QUEST} {quest_title} {progress}"


# ============================================================================
# CARD PROFIL & STATUS - Optimized untuk Mobile
# ============================================================================

def create_status_card_compact(player):
    """Profil singkat untuk eksplorasi (Max 4 baris)"""
    return (
        f"{Icon.HP} `{int(player.get('hp', 0))}/{int(player.get('max_hp', 100))}` "
        f"{Icon.MP} `{int(player.get('mp', 0))}/{int(player.get('max_mp', 50))}`\n"
        f"{Icon.ENERGY} `{int(player.get('energy', 100))}%` "
        f"{Icon.GOLD} `{player.get('gold', 0):,}G`"
    )

def create_combat_status(player):
    """Status untuk combat screen"""
    status_icons = "".join([e.get('icon', '') for e in player.get('active_effects', [])])
    
    return (
        f"**{player.get('username', 'Weaver')}** {status_icons}\n"
        f"{create_hp_bar(player.get('hp', 0), player.get('max_hp', 100))}\n"
        f"{create_mp_bar(player.get('mp', 0), player.get('max_mp', 50))}"
    )


# ============================================================================
# COMBAT UI - Lebih Clean
# ============================================================================

def create_combat_header(monster_name, hp, max_hp, is_boss=False):
    """Header musuh di combat"""
    boss_mark = f"{Icon.BOSS} " if is_boss else ""
    return (
        f"{boss_mark}**{monster_name.upper()}**\n"
        f"{create_hp_bar(hp, max_hp, 10)}"
    )

def create_combat_log(actions):
    """Log combat yang ringkas (max 3 baris)"""
    if isinstance(actions, str):
        return actions
    
    # Ambil hanya 3 aksi terakhir
    recent = actions[-3:] if len(actions) > 3 else actions
    return "\n".join(recent)

def create_combo_indicator(combo_count):
    """Indikator combo"""
    if combo_count >= 10: 
        return f"{Icon.COMBO} **ULTIMATE x{combo_count}!**"
    if combo_count >= 5: 
        return f"{Icon.COMBO} **Combo x{combo_count}**"
    if combo_count > 1: 
        return f"✨ x{combo_count}"
    return ""


# ============================================================================
# LOOT & REWARD - Lebih Ringkas
# ============================================================================

def create_loot_summary(items, gold=0, exp=0):
    """Summary loot yang ringkas"""
    parts = []
    
    if exp > 0:
        parts.append(f"{Icon.EXP} +{exp} EXP")
    if gold > 0:
        parts.append(f"{Icon.GOLD} +{gold}G")
    if items:
        item_count = len(items)
        parts.append(f"{Icon.LOOT} {item_count} item")
    
    return " | ".join(parts) if parts else "Tidak ada loot"

def create_item_list(items, show_count=True):
    """List item yang lebih ringkas"""
    if not items:
        return Text.BAG_EMPTY
    
    # Hitung stacking
    counts = {}
    for item in items:
        item_name = item.replace("_", " ").title()
        counts[item_name] = counts.get(item_name, 0) + 1
    
    lines = []
    for name, count in list(counts.items())[:5]:  # Max 5 items
        if show_count and count > 1:
            lines.append(f"• {name} x{count}")
        else:
            lines.append(f"• {name}")
    
    if len(counts) > 5:
        lines.append(f"• ... +{len(counts) - 5} lainnya")
    
    return "\n".join(lines)


# ============================================================================
# DEATH & WIN SCREEN - Lebih Dramatis tapi Ringkas
# ============================================================================

def create_death_screen(reason, cycle=1, kills=0):
    """Screen kematian yang ringkas"""
    return (
        f"{Icon.DEATH} **KAMU MATI**\n"
        f"{Text.LINE}\n"
        f"_{reason}_\n\n"
        f"{Icon.LEVEL} Cycle: {cycle}\n"
        f"{Icon.ATTACK} Kills: {kills}\n"
        f"{Text.LINE}\n"
        f"Kembali ke titik awal..."
    )

def create_victory_screen(enemy_name, rewards):
    """Screen kemenangan yang ringkas"""
    return (
        f"{Icon.WIN} **MENANG!**\n"
        f"{Text.LINE_SHORT}\n"
        f"**{enemy_name}** kalah!\n\n"
        f"{rewards}"
    )

def create_boss_warning(boss_name):
    """Warning boss yang lebih ringkas"""
    return (
        f"{Icon.BOSS} **BOSS MUNCUL!**\n"
        f"{Text.LINE}\n"
        f"**{boss_name.upper()}**"
    )


# ============================================================================
# INVENTORY UI - Grid Style
# ============================================================================

def create_equipment_summary(equipped):
    """Ringkasan equipment yang terpasang"""
    if not equipped:
        return "Tidak ada equipment terpasang"
    
    slots = {
        'weapon': Icon.WEAPON,
        'armor': Icon.ARMOR,
        'offhand': Icon.DEFENSE,
        'head': '🎩',
        'boots': '👢'
    }
    
    lines = []
    for slot, item_id in equipped.items():
        icon = slots.get(slot, Icon.GEAR)
        item_name = item_id.replace("_", " ").title()
        lines.append(f"{icon} {item_name}")
    
    return "\n".join(lines[:4])  # Max 4 items

def create_durability_warning(slot, durability):
    """Warning durability yang ringkas"""
    if durability <= 5:
        return f"🔴 {slot.upper()} rusak!"
    elif durability <= 20:
        return f"🟡 {slot.upper()} hampir rusak"
    return ""


# ============================================================================
# QUICK STAT DISPLAY
# ============================================================================

def create_stat_line(label, value, icon=""):
    """Satu baris stat: Icon Label: Value"""
    if icon:
        return f"{icon} {label}: `{value}`"
    return f"{label}: `{value}`"

def create_stat_comparison(old_val, new_val, label):
    """Tampilkan perubahan stat"""
    diff = new_val - old_val
    if diff > 0:
        return f"{label} `{old_val}` → `{new_val}` (+{diff})"
    elif diff < 0:
        return f"{label} `{old_val}` → `{new_val}` ({diff})"
    return f"{label} `{new_val}`"
