# game/logic/menu_handler.py

from aiogram.types import InlineKeyboardButton
from game.items import get_item
from game.systems.progression import calculate_max_exp

def create_progress_bar(current, maximum, length=10):
    """Membuat visual progress bar sederhana."""
    filled_length = int(length * current / maximum)
    bar = "🔵" * filled_length + "⚪" * (length - filled_length)
    return bar

def generate_profile_text(player, stats):
    """Merender teks profil dengan desain UI yang bersih untuk Mobile."""
    level = player.get('level', 1)
    exp = player.get('exp', 0)
    max_exp = calculate_max_exp(level)
    sp = player.get('stat_points', 0)
    username = player.get('username', player.get('name', 'Weaver'))
    
    # Header & Basic Info
    text = (
        f"👤 **{username.upper()}**\n"
        f"🎖️ `Lvl.{level} {player.get('current_job', 'Novice')}`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ **EXP:** `{exp}/{max_exp}`\n"
        f"{create_progress_bar(exp, max_exp)}\n\n"
        
        f"❤️ **HP:** `{int(player.get('hp', 100))}/{int(player.get('max_hp', 100))}`\n"
        f"💧 **MP:** `{int(player.get('mp', 0))}/{int(player.get('max_mp', 50))}`\n"
        f"⚡ **EN:** `{int(player.get('energy', 100))}/{int(player.get('max_energy', 100))}`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        
        f"⚔️ **P.ATK:** `{stats.get('p_atk', 10)}`  🛡️ **P.DEF:** `{stats.get('p_def', 5)}`\n"
        f"🔮 **M.ATK:** `{stats.get('m_atk', 10)}`  ✨ **M.DEF:** `{stats.get('m_def', 5)}`\n"
        f"💨 **SPD:** `{stats.get('speed', 10)}`   ⚖️ **WGT:** `{stats.get('total_weight', 0)}`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 `{player.get('gold', 0):,} Gold` | 💀 `{player.get('kills', 0)} Kills` \n"
    )
    
    if sp > 0:
        text += f"\n✨ **STAT POINTS: {sp}**\n_Ketuk tombol + di bawah untuk upgrade!_"
    
    return text

def get_profile_main_menu(player):
    """Tombol navigasi profil dengan layout yang rapi."""
    buttons = []
    sp = player.get('stat_points', 0)
    
    # Baris 1: Upgrade Stat (Hanya muncul jika ada SP)
    if sp > 0:
        buttons.append([
            InlineKeyboardButton(text="⚔️ +ATK", callback_data="addstat_p_atk"),
            InlineKeyboardButton(text="🛡️ +DEF", callback_data="addstat_p_def"),
            InlineKeyboardButton(text="💨 +SPD", callback_data="addstat_speed")
        ])
    
    # Baris 2 & 3: Management
    buttons.append([
        InlineKeyboardButton(text="🎒 TAS PERALATAN", callback_data="menu_inventory"),
        InlineKeyboardButton(text="🧪 RAMUAN", callback_data="menu_consumables")
    ])
    
    buttons.append([
        InlineKeyboardButton(text="👕 GEAR", callback_data="menu_profile"),
        InlineKeyboardButton(text="🔨 BENGKEL", callback_data="menu_repair")
    ])
    
    # Baris Terakhir: Tutup
    buttons.append([InlineKeyboardButton(text="❌ TUTUP MENU", callback_data="close_menu_profile")])
    
    return buttons

def get_inventory_menu(player):
    """Layout Tas Equipment."""
    buttons = []
    inventory = player.get('inventory', [])
    equipable_types = ['weapon', 'offhand', 'shield', 'armor', 'head', 'mask', 'gloves', 'boots', 'cloak', 'artifact']
    
    equipables = [i for i in inventory if get_item(i) and get_item(i).get('type') in equipable_types]

    if not equipables:
        buttons.append([InlineKeyboardButton(text="📭 Tas Kosong", callback_data="none")])
    else:
        row = []
        for item_id in equipables:
            item = get_item(item_id)
            icon = "⚔️" if item['type'] == 'weapon' else "🛡️"
            row.append(InlineKeyboardButton(text=f"{icon} {item['name']}", callback_data=f"equip_{item_id}"))
            if len(row) == 2:
                buttons.append(row)
                row = []
        if row: buttons.append(row)

    buttons.append([InlineKeyboardButton(text="⬅️ KEMBALI", callback_data="menu_main_profile")])
    return buttons

def get_consumable_menu(player):
    """Layout Tas Ramuan dengan Stacking."""
    buttons = []
    inventory = player.get('inventory', [])
    
    # Count stacking
    counts = {}
    for i in inventory:
        it = get_item(i)
        if it and it.get('type') == 'consumable':
            counts[i] = counts.get(i, 0) + 1

    if not counts:
        buttons.append([InlineKeyboardButton(text="📭 Tidak ada ramuan", callback_data="none")])
    else:
        row = []
        for i_id, count in counts.items():
            it = get_item(i_id)
            row.append(InlineKeyboardButton(text=f"🧪 {it['name']} ({count}x)", callback_data=f"useitem_{i_id}"))
            if len(row) == 2:
                buttons.append(row)
                row = []
        if row: buttons.append(row)

    buttons.append([InlineKeyboardButton(text="⬅️ KEMBALI", callback_data="menu_main_profile")])
    return buttons

def get_profile_menu(player):
    """Layout Lepas Equipment dengan status durabilitas."""
    buttons = []
    equipped = player.get('equipped', {})
    durability = player.get('equipment_durability', {})

    if not equipped:
        buttons.append([InlineKeyboardButton(text="📭 Tidak ada gear terpakai", callback_data="none")])
    else:
        for slot, item_id in equipped.items():
            item = get_item(item_id)
            if item:
                d = durability.get(slot, 50)
                # Visual Indicator untuk HP User
                emoji = "🟢" if d > 20 else "🟡" if d > 5 else "🔴"
                buttons.append([
                    InlineKeyboardButton(text=f"{emoji} {slot.upper()}: {item['name']} ({d}/50)", callback_data=f"unequip_{slot}")
                ])

    buttons.append([InlineKeyboardButton(text="⬅️ KEMBALI", callback_data="menu_main_profile")])
    return buttons
