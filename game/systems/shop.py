# game/systems/shop.py

"""
Sistem Toko & Rest Area Archivus (Shop System)
Terintegrasi dengan Folder Consumables Baru dan Master Data Equipment.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_player, update_player
from game.items import get_item  # Memanggil dari MASTER_ITEM_DB gabungan

# --- KATALOG TOKO LENGKAP ---
# Format: "ID_DATABASE": {"cost": Harga, "name": "Nama Tampilan Toko"}
SHOP_CATALOG = {
    # HP POTIONS (Dari hp.py)
    "potion_heal": {"cost": 40, "name": "🧪 Minor HP Potion"},
    "potion_heal_average": {"cost": 85, "name": "🧪 Standard HP Potion"},
    "potion_heal_major": {"cost": 150, "name": "🧪 Major HP Potion"},

    # MP POTIONS (Dari mp.py)
    "potion_mana_minor": {"cost": 35, "name": "💧 Minor Mana Potion"},
    "potion_mana": {"cost": 70, "name": "🔮 Tetesan Memori"},
    "potion_mana_major": {"cost": 140, "name": "🌌 Major Mana Potion"},

    # FOOD / ENERGY (Dari food.py)
    "food_ration": {"cost": 25, "name": "🍞 Roti Kering"},
    "food_meat": {"cost": 60, "name": "🍖 Daging Panggang"},
    "vegetable_stew": {"cost": 45, "name": "🍲 Rebusan Sayur"},

    # UTILITY (Dari utility.py)
    "cure_poison": {"cost": 50, "name": "🌿 Antidote"},
    "repair_kit_minor": {"cost": 100, "name": "⚒️ Minor Repair Kit"},
    "recall_scroll": {"cost": 200, "name": "📜 Recall Scroll"},

    # SPECIAL / QUIZ (Dari special.py)
    "old_book": {"cost": 150, "name": "📖 Buku Berdebu (Quiz)"},
    "mysterious_scroll": {"cost": 300, "name": "📜 Gulungan Rahasia"},

    # EQUIPMENT (ID harus sesuai MASTER_ITEM_DB)
    "iron_sword": {"cost": 250},
    "novice_staff": {"cost": 250},
    "leather_armor": {"cost": 200},
    "cloth_robe": {"cost": 180},
    "wooden_shield": {"cost": 120}
}

# === SISTEM TOKO DINAMIS ===

def get_rest_area_stock(location):
    """Menentukan barang apa saja yang dijual Merchant berdasarkan lokasi."""
    # Stok dasar yang selalu ada di semua Rest Area
    stock = ["potion_heal", "potion_mana_minor", "food_ration", "repair_kit_minor"]
    
    if location == "The Whispering Hall":
        stock.extend(["novice_staff", "cloth_robe", "old_book"])
    elif location == "The Forsaken Mire":
        stock.extend(["cure_poison", "potion_heal_average", "iron_sword", "wooden_shield"])
    elif location == "The Abyssal Depth":
        stock.extend(["potion_heal_major", "potion_mana_major", "mysterious_scroll"]) 
    elif location == "The Frozen Purgatory":
        stock.extend(["food_meat", "vegetable_stew", "recall_scroll"])
    else: 
        # Fallback stock
        stock.extend(["food_meat", "leather_armor", "recall_scroll"])
        
    return stock

def get_rest_area_keyboard():
    """Menu Utama saat pemain berada di Rest Area."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛏️ Istirahat & Pulih (20G)", callback_data="rest_sleep")],
        [InlineKeyboardButton(text="🛒 Lihat Dagangan Merchant", callback_data="rest_shop")],
        [InlineKeyboardButton(text="🚪 Lanjutkan Perjalanan", callback_data="rest_exit")]
    ])

def get_shop_keyboard(player, location="The Whispering Hall"):
    """Membuat tombol toko. Sekarang membutuhkan parameter 'player' untuk cek Gold."""
    keyboard = []
    available_stock = get_rest_area_stock(location)
    current_gold = player.get('gold', 0)
    
    for item_id in available_stock:
        catalog_entry = SHOP_CATALOG.get(item_id)
        if not catalog_entry: continue
            
        item_data = get_item(item_id)
        cost = catalog_entry['cost']
        
        # Penentuan Icon berdasarkan tipe item dari database
        icon = "📦"
        name = catalog_entry.get('name')
        
        if item_data:
            name = item_data.get('name', name)
            itype = item_data.get('type')
            if itype == 'weapon': icon = "⚔️"
            elif itype in ['armor', 'head', 'offhand', 'mask']: icon = "🛡️"
            elif itype == 'consumable':
                eff = item_data.get('effect_type')
                if 'heal' in eff: icon = "💖"
                elif 'mp' in eff: icon = "💧"
                elif 'energy' in eff: icon = "🍖"
                elif 'clear' in eff: icon = "🌿"
        
        # Beri tanda jika uang tidak cukup
        status_icon = "💰" if current_gold >= cost else "❌"
        button_text = f"{icon} {name} - {status_icon} {cost}"
        
        keyboard.append([InlineKeyboardButton(text=button_text, callback_data=f"buy_{item_id}")])
    
    keyboard.append([InlineKeyboardButton(text="🔙 Kembali", callback_data="rest_shop_back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def process_purchase(player, item_id):
    """
    Logika transaksi. 
    Sekarang menerima objek 'player' langsung agar sinkron dengan main.py.
    """
    catalog_item = SHOP_CATALOG.get(item_id)
    
    if not catalog_item:
        return False, "⚠️ Barang tidak tersedia di dimensi ini."
        
    cost = catalog_item["cost"]
        
    # 1. Cek Ketersediaan Gold
    if player.get('gold', 0) < cost:
        return False, f"❌ Gold tidak cukup! Kamu butuh {cost} Gold."
        
    # 2. Masukkan ke Inventory
    inventory = player.get('inventory', [])
    inventory.append(item_id)
    
    # 3. Potong Gold
    player['gold'] -= cost
    player['inventory'] = inventory
    
    # Ambil nama asli dari database untuk pesan sukses
    item_data = get_item(item_id)
    item_name = item_data['name'] if item_data else item_id.replace("_", " ").title()
    
    return True, f"✅ Membeli **{item_name}**!"
