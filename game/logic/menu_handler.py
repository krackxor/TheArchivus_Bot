# game/logic/menu_handler.py

from aiogram.types import InlineKeyboardButton
from game.items import get_item
from game.systems.progression import calculate_max_exp

def generate_profile_text(player, stats):
    """Merender teks profil yang sangat rapi dan profesional untuk Mobile."""
    level = player.get('level', 1)
    exp = player.get('exp', 0)
    max_exp = calculate_max_exp(level)
    sp = player.get('stat_points', 0)
    username = player.get('username', player.get('name', 'Weaver'))
    
    text = (
        f"📜 **ARCHIVUS DOSSIER**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Nama:** {username}\n"
        f"🎖️ **Class:** `{player.get('current_job', 'Novice Weaver')}`\n"
        f"📈 **Level:** `{level}` *(EXP: {exp}/{max_exp})*\n"
        f"💰 **Gold:** `{player.get('gold', 0):,}G` | 💀 **Kills:** `{player.get('kills', 0)}`\n\n"
        
        f"❤️ **HP:** `{int(player.get('hp', 100))}/{int(player.get('max_hp', 100))}`\n"
        f"🔵 **MP:** `{int(player.get('mp', 0))}/{int(player.get('max_mp', 50))}`\n"
        f"⚡ **EN:** `{int(player.get('energy', 100))}/{int(player.get('max_energy', 100))}`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 **COMBAT STATS (Termasuk Equip):**\n"
        f"⚔️ **P.ATK:** `{stats.get('p_atk', 10)}` | 🔮 **M.ATK:** `{stats.get('m_atk', 10)}`\n"
        f"🛡️ **P.DEF:** `{stats.get('p_def', 5)}` | ✨ **M.DEF:** `{stats.get('m_def', 5)}`\n"
        f"💨 **SPEED:** `{stats.get('speed', 10)}` | ⚖️ **BERAT:** `{stats.get('total_weight', 0)}`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
    )
    
    if sp > 0:
        text += f"✨ **STAT POINTS (SP) TERSEDIA: {sp}**\n_Gunakan tombol di bawah untuk memperkuat dirimu._"
    else:
        text += "🔒 _Kumpulkan EXP dan naik level untuk mendapatkan Stat Points (SP)._"
        
    return text

def get_profile_main_menu(player):
    """Menghasilkan tombol navigasi untuk profil utama."""
    buttons = []
    sp = player.get('stat_points', 0)
    
    # Tombol alokasi stat jika ada SP
    if sp > 0:
        buttons.append([
            InlineKeyboardButton(text="⚔️ + P.ATK", callback_data="addstat_p_atk"),
            InlineKeyboardButton(text="🔮 + M.ATK", callback_data="addstat_m_atk")
        ])
        buttons.append([
            InlineKeyboardButton(text="🛡️ + P.DEF", callback_data="addstat_p_def"),
            InlineKeyboardButton(text="💨 + SPEED", callback_data="addstat_speed")
        ])
    
    # Menu Navigasi Barang
    buttons.append([InlineKeyboardButton(text="🎒 Buka Tas (Equipment)", callback_data="menu_inventory")])
    buttons.append([InlineKeyboardButton(text="🧪 Gunakan Ramuan", callback_data="menu_consumables")])
    buttons.append([InlineKeyboardButton(text="👕 Lihat Gear Terpakai", callback_data="menu_profile")])
    
    # Fitur Perbaikan
    buttons.append([InlineKeyboardButton(text="🔨 Perbaiki Gear (Pandai Besi)", callback_data="menu_repair")])
    
    return buttons

def get_inventory_menu(player):
    """Menampilkan isi tas khusus untuk Equipment (Senjata, Armor, dll)."""
    buttons = []
    inventory = player.get('inventory', [])

    equipable_types = ['weapon', 'armor', 'head', 'mask', 'gloves', 'boots', 'cloak', 'artifact']
    equipables = [item_id for item_id in inventory if get_item(item_id) and get_item(item_id).get('type') in equipable_types]

    if not equipables:
        return [[InlineKeyboardButton(text="⬅️ Kembali", callback_data="menu_main_profile")]]

    current_row = []
    for item_id in equipables:
        item = get_item(item_id)
        if not item: continue
        
        icon = "⚔️" if item['type'] == 'weapon' else "👕"
        current_row.append(InlineKeyboardButton(text=f"{icon} {item['name']}", callback_data=f"equip_{item_id}"))
        
        # Buat 2 tombol per baris
        if len(current_row) == 2:
            buttons.append(current_row)
            current_row = []
    
    if current_row: buttons.append(current_row)
    buttons.append([InlineKeyboardButton(text="⬅️ Kembali", callback_data="menu_main_profile")])
    
    return buttons

def get_consumable_menu(player):
    """
    Menampilkan item yang bisa dikonsumsi (Potions, dll).
    Mendukung sistem stacking (jumlah item dihitung otomatis).
    """
    buttons = []
    inventory = player.get('inventory', [])
    
    # Hitung jumlah item yang sama (Stacking)
    item_counts = {}
    for item_id in inventory:
        item = get_item(item_id)
        if item and item.get('type') == 'consumable':
            item_counts[item_id] = item_counts.get(item_id, 0) + 1

    if not item_counts:
        return [[InlineKeyboardButton(text="⬅️ Kembali", callback_data="menu_main_profile")]]

    current_row = []
    for item_id, count in item_counts.items():
        item = get_item(item_id)
        # Tampilan: "Red Potion (5x)"
        current_row.append(InlineKeyboardButton(text=f"{item['name']} ({count}x)", callback_data=f"useitem_{item_id}"))
        
        if len(current_row) == 2:
            buttons.append(current_row)
            current_row = []

    if current_row: buttons.append(current_row)
    buttons.append([InlineKeyboardButton(text="⬅️ Kembali", callback_data="menu_main_profile")])
    
    return buttons

def get_profile_menu(player):
    """Menampilkan slot yang sedang terpakai untuk di-unequip."""
    buttons = []
    equipped = player.get('equipped', {})
    durability_data = player.get('equipment_durability', {})

    if not equipped:
        return [[InlineKeyboardButton(text="⬅️ Kembali", callback_data="menu_main_profile")]]

    for slot, item_id in equipped.items():
        item = get_item(item_id)
        if item:
            dur = durability_data.get(slot, 50)
            status = "🟢" if dur > 20 else "🟡" if dur > 5 else "🔴"
            buttons.append([InlineKeyboardButton(text=f"{status} Lepas {item['name']} ({dur}/50)", callback_data=f"unequip_{slot}")])

    buttons.append([InlineKeyboardButton(text="⬅️ Kembali", callback_data="menu_main_profile")])
    return buttons
