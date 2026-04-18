# game/logic/menu_handler.py

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from game.items import get_item
from game.systems.progression import calculate_max_exp

# ==============================================================================
# 1. HELPER UI & TEXT GENERATION
# ==============================================================================

def create_progress_bar(current, maximum, length=10):
    """
    Membuat visual progress bar sederhana menggunakan emoji.
    Contoh output: 🔵🔵🔵🔵⚪⚪⚪⚪⚪⚪
    """
    if maximum <= 0: return "⚪" * length
    filled_length = int(length * current / maximum)
    # Pastikan tidak melebihi panjang maksimal
    filled_length = min(length, max(0, filled_length))
    bar = "🔵" * filled_length + "⚪" * (length - filled_length)
    return bar

def generate_profile_text(player, stats):
    """
    Merender teks profil pemain dengan desain UI yang bersih untuk Mobile.
    Menggabungkan data pemain dasar dan total stat tempurnya.
    """
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
    
    # Notifikasi jika pemain memiliki poin stat (SP) yang belum dipakai
    if sp > 0:
        text += f"\n✨ **STAT POINTS: {sp}**\n_Ketuk tombol + di bawah untuk upgrade!_"
    
    return text


# ==============================================================================
# 2. MENU PROFIL & INVENTORY (INLINE KEYBOARD)
# ==============================================================================

def get_profile_main_menu(player):
    """
    Membuat layout tombol navigasi untuk menu profil utama.
    Menampilkan tombol upgrade stat jika pemain memiliki SP (Stat Points).
    """
    buttons = []
    sp = player.get('stat_points', 0)
    
    # Baris 1: Upgrade Stat (Hanya muncul jika ada SP)
    if sp > 0:
        buttons.append([
            InlineKeyboardButton(text="⚔️ +ATK", callback_data="addstat_p_atk"),
            InlineKeyboardButton(text="🛡️ +DEF", callback_data="addstat_p_def"),
            InlineKeyboardButton(text="💨 +SPD", callback_data="addstat_speed")
        ])
    
    # Baris 2 & 3: Management Inventory & Peralatan
    buttons.append([
        InlineKeyboardButton(text="🎒 TAS PERALATAN", callback_data="menu_inventory"),
        InlineKeyboardButton(text="🧪 RAMUAN", callback_data="menu_consumables")
    ])
    
    buttons.append([
        InlineKeyboardButton(text="👕 GEAR", callback_data="menu_profile"),
        InlineKeyboardButton(text="🔨 BENGKEL", callback_data="menu_repair")
    ])
    
    # Baris Terakhir: Tutup Menu untuk membersihkan layar chat
    buttons.append([InlineKeyboardButton(text="❌ TUTUP MENU", callback_data="close_menu_profile")])
    
    return buttons

def get_inventory_menu(player):
    """
    Membuat layout tombol untuk tas pemain (Khusus Equipment/Peralatan).
    Memfilter barang-barang yang bisa dipakai (equipable).
    """
    buttons = []
    inventory = player.get('inventory', [])
    equipable_types = ['weapon', 'offhand', 'shield', 'armor', 'head', 'mask', 'gloves', 'boots', 'cloak', 'artifact']
    
    # Filter hanya item yang bertipe perlengkapan
    equipables = [i for i in inventory if get_item(i) and get_item(i).get('type') in equipable_types]

    if not equipables:
        buttons.append([InlineKeyboardButton(text="📭 Tas Kosong", callback_data="none")])
    else:
        row = []
        for item_id in equipables:
            item = get_item(item_id)
            # Beri ikon pedang jika senjata, perisai jika selain senjata
            icon = "⚔️" if item['type'] == 'weapon' else "🛡️"
            row.append(InlineKeyboardButton(text=f"{icon} {item['name']}", callback_data=f"equip_{item_id}"))
            
            # Susun 2 tombol per baris agar rapi di HP
            if len(row) == 2:
                buttons.append(row)
                row = []
        if row: buttons.append(row) # Masukkan sisa tombol

    # Tombol navigasi kembali ke profil utama
    buttons.append([InlineKeyboardButton(text="⬅️ KEMBALI", callback_data="menu_main_profile")])
    return buttons

def get_consumable_menu(player):
    """
    Membuat layout tombol khusus untuk ramuan/consumables.
    Menerapkan sistem stacking (menghitung jumlah barang yang sama).
    """
    buttons = []
    inventory = player.get('inventory', [])
    
    # Hitung jumlah (Stacking) item yang sama
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
            # Format: 🧪 Nama Potion (Jumlah x)
            row.append(InlineKeyboardButton(text=f"🧪 {it['name']} ({count}x)", callback_data=f"useitem_{i_id}"))
            
            # Susun 2 tombol per baris
            if len(row) == 2:
                buttons.append(row)
                row = []
        if row: buttons.append(row)

    buttons.append([InlineKeyboardButton(text="⬅️ KEMBALI", callback_data="menu_main_profile")])
    return buttons

def get_profile_menu(player):
    """
    Membuat layout tombol untuk melepas (unequip) gear yang sedang dipakai.
    Menampilkan status durabilitas item dengan indikator warna.
    """
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
                # Visual Indicator untuk Durabilitas (Hijau=Aman, Kuning=Peringatan, Merah=Rusak)
                emoji = "🟢" if d > 20 else "🟡" if d > 5 else "🔴"
                buttons.append([
                    InlineKeyboardButton(text=f"{emoji} {slot.upper()}: {item['name']} ({d}/50)", callback_data=f"unequip_{slot}")
                ])

    buttons.append([InlineKeyboardButton(text="⬅️ KEMBALI", callback_data="menu_main_profile")])
    return buttons


# ==============================================================================
# 3. GLOBAL KEYBOARDS (DIGUNAKAN DI BANYAK FILE)
# ==============================================================================

def get_main_reply_keyboard(player=None):
    """
    Menghasilkan tombol navigasi bawah layar (Reply Keyboard).
    Digunakan untuk Eksplorasi, Meditasi, dan membuka Profil Utama.
    """
    keyboard = [
        [KeyboardButton(text="⬆️ Utara")],
        [KeyboardButton(text="⬅️ Barat"), KeyboardButton(text="Timur ➡️")],
        [KeyboardButton(text="⬇️ Selatan")],
        [KeyboardButton(text="🧘 Meditasi"), KeyboardButton(text="📊 Profil & Tas")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_stance_keyboard(is_boss=False):
    """
    Menghasilkan tombol aksi pertempuran (Inline Keyboard).
    Digunakan oleh file exploration.py dan combat.py saat in_combat.
    """
    row1 = [
        InlineKeyboardButton(text="⚔️ Serang", callback_data="stance_attack"),
        InlineKeyboardButton(text="🔮 Skill", callback_data="stance_skill")
    ]
    row2 = [
        InlineKeyboardButton(text="🛡️ Bertahan", callback_data="stance_block"),
        InlineKeyboardButton(text="💨 Menghindar", callback_data="stance_dodge")
    ]
    row3 = [InlineKeyboardButton(text="🎒 Item", callback_data="stance_item")]
    
    # Jika menghadapi Boss, pemain tidak diberikan opsi kabur
    if not is_boss: 
        row3.append(InlineKeyboardButton(text="🏃 Kabur", callback_data="stance_run"))
        
    return InlineKeyboardMarkup(inline_keyboard=[row1, row2, row3])
