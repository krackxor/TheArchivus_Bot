# utils/helper_ui.py

"""
Helper UI - The Archivus (Unified Version)
Menyediakan komponen visual untuk Telegram Mobile.
Sinkronisasi penuh dengan main.py, combat.py, dan achievement.py.
"""

import math
from game.logic.stats import calculate_total_stats
from game.items import get_item

# --- 1. PROGRESS BARS (VISUAL INDICATORS) ---

def create_hp_bar(current, maximum, length=8):
    """Membuat bar HP berwarna dinamis (Hijau/Kuning/Merah)."""
    if maximum <= 0: maximum = 1
    current = max(0, min(current, maximum))
    percent = current / maximum
    filled = int(percent * length)
    empty = length - filled
    
    if percent > 0.6: bar_char = "🟩"
    elif percent > 0.2: bar_char = "🟨"
    else: bar_char = "🟥"
        
    return f"{bar_char * filled}{'⬜' * empty} `{int(current)}/{int(maximum)}`"

def create_mp_bar(current, maximum, length=8):
    """Membuat bar MP berwarna Biru."""
    if maximum <= 0: maximum = 1
    current = max(0, min(current, maximum))
    filled = int((current / maximum) * length)
    empty = length - filled
    return f"{'🟦' * filled}{'⬜' * empty} `{int(current)}/{int(maximum)}`"

def create_energy_bar(current, max_val=100, length=8):
    """Membuat bar Energi berwarna Oranye."""
    current = max(0, min(current, max_val))
    filled = int((current / max_val) * length)
    empty = length - filled
    return f"{'🟧' * filled}{'⬜' * empty} `{int(current)}%`"

def create_exp_bar(current, needed, length=8):
    """Membuat bar EXP berwarna Ungu."""
    if needed <= 0: needed = 100
    percent = min(current / needed, 1.0)
    filled = int(percent * length)
    empty = length - filled
    return f"{'🟪' * filled}{'⬜' * empty} `{int(current)}/{int(needed)}`"


# --- 2. SYSTEM NOTIFICATIONS (CORE) ---

def create_achievement_notification(ach):
    """Tampilan saat pemain mendapatkan Achievement baru."""
    return (
        f"🏆 **ACHIEVEMENT UNLOCKED**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{ach.get('icon', '⭐')} **{ach['title']}**\n"
        f"_{ach['description']}_\n\n"
        f"🎁 **Reward:** {ach.get('rewards', 'Sesuatu yang misterius')}"
    )

def create_level_up_animation(new_level):
    """Pesan dramatis saat pemain naik level."""
    return (
        f"🆙 **LEVEL UP!**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Jiwa Weaver milikmu semakin kuat.\n"
        f"Sekarang kau mencapai **Level {new_level}**!"
    )

def create_location_transition(new_loc):
    """Notifikasi visual saat berpindah area/landmark."""
    return (
        f"🌫️ **MEMASUKI AREA BARU**\n"
        f"📍 **{new_loc.upper()}**\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )

def create_daily_quest_card(quest_list):
    """Menampilkan daftar quest harian yang aktif."""
    text = "📅 **DAILY QUESTS**\n━━━━━━━━━━━━━━━\n"
    if not quest_list:
        text += "_Tidak ada quest hari ini._"
    for q in quest_list:
        text += f"• **{q['title']}**\n  (Hadiah: {q['reward'].get('gold')}G)\n"
    return text


# --- 3. COMBAT & STATUS INTERFACE ---

def create_status_card(player):
    """Profil singkat yang dikirimkan bersama navigasi eksplorasi."""
    stats = calculate_total_stats(player)
    # Ambil icon status efek jika ada
    status_icons = "".join([e.get('icon', '') for e in player.get('active_effects', [])])
    
    return (
        f"👤 **{player.get('username', 'Weaver')}** {status_icons}\n"
        f"🎖️ `{player.get('current_job', 'Novice')}` | Lvl {player.get('level', 1)}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"⚔️ ATK: `{stats['p_atk']}` | 🛡️ DEF: `{stats['p_def']}`\n"
        f"HP: {create_hp_bar(player.get('hp', 0), player.get('max_hp', 100))}\n"
        f"💰 `{player.get('gold', 0):,} G`"
    )

def create_combat_header(monster_name, hp, max_hp):
    """Bar HP musuh untuk header pertarungan."""
    return f"⚔️ **{monster_name.upper()}**\n{create_hp_bar(hp, max_hp, 10)}"

def create_loot_drop(items):
    """Menampilkan item-item yang didapatkan dari musuh/peti."""
    if not items:
        return "💨 *Hanya debu yang tersisa di sini...*"
    
    loot_list = []
    for i in items:
        # Jika item berupa string ID, bersihkan formatnya
        name = i.replace("_", " ").title() if isinstance(i, str) else i.get('name', 'Unknown Item')
        loot_list.append(f"🔹 {name}")
        
    return "🎁 **LOOT DITEMUKAN:**\n" + "\n".join(loot_list)

def create_combo_indicator(combo_count):
    """Indikator combo untuk memberikan bonus damage/gold."""
    if combo_count >= 10: return f"🔥 **ULTIMATE x{combo_count}!**"
    if combo_count >= 5: return f"⚡ **COMBO x{combo_count}!**"
    if combo_count > 1: return f"✨ Combo x{combo_count}"
    return ""

def create_boss_warning(boss_name):
    """Peringatan saat Boss atau Mini-Boss muncul."""
    return (
        f"💀 **CRITICAL WARNING** 💀\n"
        f"⚠️ **{boss_name.upper()} TELAH BANGKIT!**\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )

def create_death_screen(reason, stats=None):
    """Layar terakhir saat pemain mati."""
    text = (
        f"💀 **YOU DIED**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Penyebab: _{reason}_\n"
    )
    if stats:
        text += f"\n📊 **Statistik Terakhir:**\n⚔️ Kills: `{stats.get('kills', 0)}`"
    return text

def create_inventory_display(inventory):
    """Merangkum isi tas (Equipment/Item)."""
    if not inventory:
        return "🎒 **TAS KOSONG**\n_Tidak ada barang berharga._"
    
    counts = {}
    for item in inventory:
        counts[item] = counts.get(item, 0) + 1
        
    display = "🎒 **INVENTORY**\n━━━━━━━━━━━━━━━\n"
    for item_id, count in counts.items():
        name = item_id.replace("_", " ").title()
        display += f"• {name} `x{count}`\n"
        
    return display
