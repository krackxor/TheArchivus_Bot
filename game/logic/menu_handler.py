# game/logic/menu_handler.py

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from game.items import get_item
from game.systems.progression import calculate_max_exp
from game.ui_constants import Icon, Text, get_text

# Impor Helper UI terpusat
from utils.helper_ui import create_hp_bar, create_mp_bar, create_energy_bar, create_exp_bar

# ==============================================================================
# 1. PROFILE TEXT GENERATION
# ==============================================================================

def generate_profile_text(player, stats):
    """Merender teks profil pemain dengan desain UI yang bersih dan Multi-Bahasa."""
    lang = player.get('lang', 'id')
    level = player.get('level', 1)
    exp = player.get('exp', 0)
    max_exp = calculate_max_exp(level)
    sp = player.get('stat_points', 0)
    username = player.get('username', player.get('name', 'Weaver'))
    
    # Header & Basic Info
    text = (
        f"{Icon.NPC} **{username.upper()}**\n"
        f"{Icon.LEVEL} `{get_text(lang, 'LEVEL')}.{level} {player.get('current_job', 'Novice')}`\n"
        f"{Text.LINE}\n"
        f"{Icon.EXP} **{get_text(lang, 'EXP')}:** `{exp}/{max_exp}`\n"
        f"{create_exp_bar(exp, max_exp)}\n\n"
        
        f"{Icon.HP} **HP:** {create_hp_bar(player.get('hp', 100), player.get('max_hp', 100))}\n"
        f"{Icon.MP} **MP:** {create_mp_bar(player.get('mp', 0), player.get('max_mp', 50))}\n"
        f"{Icon.ENERGY} **EN:** {create_energy_bar(player.get('energy', 100), player.get('max_energy', 100))}\n"
        f"{Text.LINE}\n"
        
        f"{Icon.ATTACK} **P.ATK:** `{stats.get('p_atk', 10)}`  {Icon.DEFENSE} **P.DEF:** `{stats.get('p_def', 5)}`\n"
        f"{Icon.MAGIC} **M.ATK:** `{stats.get('m_atk', 10)}`  {Icon.GEAR} **M.DEF:** `{stats.get('m_def', 5)}`\n"
        f"{Icon.SPEED} **SPD:** `{stats.get('speed', 10)}`   ⚖️ **WGT:** `{stats.get('total_weight', 0)}`\n"
        f"{Text.LINE}\n"
        f"{Icon.GOLD} `{player.get('gold', 0):,} Gold` | {Icon.KILLS} `{player.get('kills', 0)} Kills` \n"
    )
    
    if sp > 0:
        text += f"\n{get_text(lang, 'STAT_POINTS_INFO', sp=sp)}"
    
    return text


# ==============================================================================
# 2. INLINE KEYBOARDS (MENUS)
# ==============================================================================

def get_profile_main_menu(player):
    lang = player.get('lang', 'id')
    buttons = []
    sp = player.get('stat_points', 0)
    
    if sp > 0:
        buttons.append([
            InlineKeyboardButton(text=f"{Icon.ATTACK} +ATK", callback_data="addstat_p_atk"),
            InlineKeyboardButton(text=f"{Icon.DEFENSE} +DEF", callback_data="addstat_p_def"),
            InlineKeyboardButton(text=f"{Icon.SPEED} +SPD", callback_data="addstat_speed")
        ])
    
    buttons.append([
        InlineKeyboardButton(text=f"{Icon.BAG} {get_text(lang, 'INVENTORY_TITLE').upper()}", callback_data="menu_inventory"),
        InlineKeyboardButton(text=f"{Icon.POTION} {get_text(lang, 'CONSUMABLES_TITLE').split(' ')[0].upper()}", callback_data="menu_consumables")
    ])
    
    buttons.append([
        InlineKeyboardButton(text=f"{Icon.GEAR} EQUIPMENT", callback_data="menu_profile"),
        InlineKeyboardButton(text=f"⚒️ BENGKEL", callback_data="menu_repair")
    ])
    
    buttons.append([InlineKeyboardButton(text=get_text(lang, "BTN_CLOSE"), callback_data="close_menu_profile")])
    return buttons

def get_inventory_menu(player):
    lang = player.get('lang', 'id')
    buttons = []
    inventory = player.get('inventory', [])
    equipable_types = ['weapon', 'offhand', 'shield', 'armor', 'head', 'mask', 'gloves', 'boots', 'cloak', 'artifact']
    
    equipables = [i for i in inventory if get_item(i) and get_item(i).get('type') in equipable_types]

    if not equipables:
        buttons.append([InlineKeyboardButton(text=get_text(lang, "EMPTY_BAG"), callback_data="none")])
    else:
        row = []
        for item_id in equipables:
            item = get_item(item_id)
            # Ambil ikon spesifik senjata/gear
            icon = Icon.GEAR_SWORD if item['type'] == 'weapon' else Icon.GEAR_ARMOR
            row.append(InlineKeyboardButton(text=f"{icon} {item['name']}", callback_data=f"equip_{item_id}"))
            
            if len(row) == 2:
                buttons.append(row)
                row = []
        if row: buttons.append(row)

    buttons.append([InlineKeyboardButton(text=get_text(lang, "BTN_BACK"), callback_data="menu_main_profile")])
    return buttons

def get_consumable_menu(player):
    lang = player.get('lang', 'id')
    buttons = []
    inventory = player.get('inventory', [])
    
    counts = {}
    for i in inventory:
        it = get_item(i)
        if it and it.get('type') == 'consumable':
            counts[i] = counts.get(i, 0) + 1

    if not counts:
        buttons.append([InlineKeyboardButton(text=get_text(lang, "EMPTY_BAG"), callback_data="none")])
    else:
        row = []
        for i_id, count in counts.items():
            it = get_item(i_id)
            # Deteksi ikon potion secara cerdas
            icon = Icon.HP if it.get('effect_type') == 'heal_hp' else Icon.POTION
            row.append(InlineKeyboardButton(text=f"{icon} {it['name']} ({count}x)", callback_data=f"useitem_{i_id}"))
            
            if len(row) == 2:
                buttons.append(row)
                row = []
        if row: buttons.append(row)

    buttons.append([InlineKeyboardButton(text=get_text(lang, "BTN_BACK"), callback_data="menu_main_profile")])
    return buttons

def get_profile_menu(player):
    lang = player.get('lang', 'id')
    buttons = []
    equipped = player.get('equipped', {})
    durability = player.get('equipment_durability', {})

    # Daftar slot yang ingin ditampilkan beserta ikonnya
    slots = {
        "weapon": Icon.GEAR_SWORD, "armor": Icon.GEAR_ARMOR, 
        "head": Icon.GEAR_HELMET, "boots": Icon.GEAR_BOOTS,
        "artifact": Icon.GEAR_AMULET
    }

    found = False
    for slot, icon in slots.items():
        item_id = equipped.get(slot)
        if item_id:
            item = get_item(item_id)
            if item:
                found = True
                d = durability.get(slot, 50)
                status_icon = "🟢" if d > 20 else "🟡" if d > 5 else "🔴"
                buttons.append([
                    InlineKeyboardButton(text=f"{status_icon} {icon} {item['name']} ({d}/50)", callback_data=f"unequip_{slot}")
                ])

    if not found:
        buttons.append([InlineKeyboardButton(text="📭 Gear Kosong", callback_data="none")])

    buttons.append([InlineKeyboardButton(text=get_text(lang, "BTN_BACK"), callback_data="menu_main_profile")])
    return buttons


# ==============================================================================
# 3. GLOBAL REPLY KEYBOARDS (BOTTOM BUTTONS)
# ==============================================================================

def get_main_reply_keyboard(player):
    lang = player.get('lang', 'id')
    keyboard = [
        [KeyboardButton(text=get_text(lang, "NAV_NORTH"))],
        [KeyboardButton(text=get_text(lang, "NAV_WEST")), KeyboardButton(text=get_text(lang, "NAV_EAST"))],
        [KeyboardButton(text=get_text(lang, "NAV_SOUTH"))],
        [KeyboardButton(text=get_text(lang, "NAV_REST")), KeyboardButton(text=get_text(lang, "NAV_PROFILE"))]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_stance_keyboard(is_boss=False):
    # Untuk tombol combat, kita pakai ID bahasa 'id' dulu sebagai standar tempur
    row1 = [
        InlineKeyboardButton(text=f"{Icon.ATTACK} Serang", callback_data="stance_attack"),
        InlineKeyboardButton(text=f"{Icon.SKILL} Skill", callback_data="stance_skill")
    ]
    row2 = [
        InlineKeyboardButton(text=f"{Icon.DEFENSE} Bertahan", callback_data="stance_block"),
        InlineKeyboardButton(text=f"{Icon.DODGE} Menghindar", callback_data="stance_dodge")
    ]
    row3 = [InlineKeyboardButton(text=f"{Icon.BAG} Item", callback_data="stance_item")]
    
    if not is_boss: 
        row3.append(InlineKeyboardButton(text="🏃 Kabur", callback_data="stance_run"))
        
    return InlineKeyboardMarkup(inline_keyboard=[row1, row2, row3])

def get_rest_area_keyboard():
    buttons = [
        [InlineKeyboardButton(text="🔥 Menyalakan Api", callback_data="rest_fire")],
        [InlineKeyboardButton(text="⛺ Pasang Tenda", callback_data="rest_tent")],
        [InlineKeyboardButton(text="🚶‍♂️ Lanjut Berjalan", callback_data="rest_leave")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
