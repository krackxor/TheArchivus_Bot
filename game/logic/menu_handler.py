# game/logic/menu_handler.py

from game.items import get_item
from game.systems.progression import calculate_max_exp

def generate_profile_text(player, stats):
    """Merender teks profil yang sangat rapi dan profesional."""
    level = player.get('level', 1)
    exp = player.get('exp', 0)
    max_exp = calculate_max_exp(level)
    sp = player.get('stat_points', 0)
    
    text = (
        f"📜 **ARCHIVUS DOSSIER**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Nama:** {player.get('name', 'Weaver')}\n"
        f"🎖️ **Class:** {player.get('current_job', 'Novice Weaver')}\n"
        f"📈 **Level:** {level}  *(EXP: {exp}/{max_exp})*\n"
        f"💰 **Gold:** {player.get('gold', 0)}G | 💀 **Kills:** {player.get('kills', 0)}\n\n"
        
        f"❤️ **HP:** {player.get('hp', 100)}/{player.get('max_hp', 100)}\n"
        f"🔵 **MP:** {player.get('mp', 0)}/{player.get('max_mp', 50)}\n"
        f"⚡ **EN:** {player.get('energy', 100)}/{player.get('max_energy', 100)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 **COMBAT STATS (Termasuk Equip):**\n"
        f"⚔️ **P.ATK:** {stats.get('p_atk', 10)}  |  🔮 **M.ATK:** {stats.get('m_atk', 10)}\n"
        f"🛡️ **P.DEF:** {stats.get('p_def', 5)}  |  ✨ **M.DEF:** {stats.get('m_def', 5)}\n"
        f"💨 **SPEED:** {stats.get('speed', 10)}  |  ⚖️ **BERAT:** {stats.get('total_weight', 0)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
    )
    
    if sp > 0:
        text += f"✨ **STAT POINTS (SP) TERSEDIA: {sp}**\n_Gunakan tombol di bawah untuk memperkuat dirimu._"
    else:
        text += "🔒 _Kumpulkan EXP dan naik level untuk mendapatkan Stat Points (SP)._"
        
    return text

def get_profile_main_menu(player):
    """Menghasilkan tombol navigasi untuk profil, termasuk tombol Stat Points dan Repair."""
    buttons = []
    sp = player.get('stat_points', 0)
    
    # Tombol alokasi stat
    if sp > 0:
        buttons.append([
            {"text": "⚔️ + P.ATK", "callback_data": "addstat_p_atk"},
            {"text": "🔮 + M.ATK", "callback_data": "addstat_m_atk"}
        ])
        buttons.append([
            {"text": "🛡️ + P.DEF", "callback_data": "addstat_p_def"},
            {"text": "💨 + SPEED", "callback_data": "addstat_speed"}
        ])
    
    # Menu utama
    buttons.append([{"text": "🎒 Buka Tas (Equip Item)", "callback_data": "menu_inventory"}])
    buttons.append([{"text": "👕 Lihat Baju Terpakai", "callback_data": "menu_profile"}])
    
    # INTEGRASI PANDAI BESI: Tombol perbaikan
    buttons.append([{"text": "🔨 Perbaiki Gear (Pandai Besi)", "callback_data": "menu_repair"}])
    
    return buttons

def get_inventory_menu(player):
    """Menampilkan isi tas dalam bentuk tombol untuk di-equip."""
    buttons = []
    inventory = player.get('inventory', [])

    equipable_types = ['weapon', 'armor', 'head', 'mask', 'gloves', 'boots', 'cloak', 'artifact']
    equipables = [item_id for item_id in inventory if get_item(item_id) and get_item(item_id).get('type') in equipable_types]

    if not equipables:
        return [[{"text": "⬅️ Kembali ke Profil", "callback_data": "menu_main_profile"}]]

    current_row = []
    for item_id in equipables:
        item = get_item(item_id)
        if not item: continue
        
        icon = "📦"
        item_type = item.get('type')
        if item_type == 'weapon': icon = "⚔️"
        elif item_type == 'armor': icon = "👕"
        elif item_type == 'artifact': icon = "🔮"
        elif item_type == 'head': icon = "🪖"
        elif item_type == 'boots': icon = "👞"
        elif item_type == 'gloves': icon = "🧤"

        current_row.append({"text": f"{icon} {item['name']}", "callback_data": f"equip_{item_id}"})
        
        if len(current_row) == 2:
            buttons.append(current_row)
            current_row = []
    
    if current_row: 
        buttons.append(current_row)
    
    buttons.append([{"text": "⬅️ Kembali ke Profil", "callback_data": "menu_main_profile"}])
    return buttons

def get_profile_menu(player):
    """Menampilkan slot yang sedang terpakai dengan info durabilitas."""
    buttons = []
    equipped = player.get('equipped', {})
    # Ambil data durabilitas dinamis pemain
    durability_data = player.get('equipment_durability', {})

    if not equipped:
        return [[{"text": "⬅️ Kembali ke Profil", "callback_data": "menu_main_profile"}]]

    for slot, item_id in equipped.items():
        item = get_item(item_id)
        if item:
            # Ambil durabilitas saat ini (default 50 jika belum tercatat)
            current_dur = durability_data.get(slot, 50)
            
            # Tampilan tombol dengan status kondisi item
            status_icon = "🟢" if current_dur > 20 else "🟡" if current_dur > 5 else "🔴"
            buttons.append([{
                "text": f"{status_icon} Lepas {item['name']} ({current_dur}/50)", 
                "callback_data": f"unequip_{slot}"
            }])

    buttons.append([{"text": "⬅️ Kembali ke Profil", "callback_data": "menu_main_profile"}])
    return buttons
