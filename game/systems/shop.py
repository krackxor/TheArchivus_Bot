# game/systems/shop.py

"""
Sistem Toko & Rest Area Archivus (Shop System)
Terintegrasi dengan Master Data Equipment dan Dinamika Lokasi.
Menyediakan barang unik (Kunci, Gear Survival) berdasarkan wilayah Rest Area.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Memanggil fungsi dari file database dan equipment baru
from database import get_player, update_player
from game.items import get_item # Memanggil dari MASTER_ITEM_DB

# --- KATALOG TOKO LENGKAP ---
# Format item yang dijual adalah "ID item" yang sesuai dengan MASTER_ITEM_DB
SHOP_CATALOG = {
    # RAMUAN HP & MP (ID item harus sesuai dengan database item agar bisa ditumpuk/stacking)
    "potion_heal": {"name": "🧪 Minor HP Potion", "cost": 50},
    "potion_heal_major": {"name": "🧪 Major HP Potion", "cost": 120},
    "potion_mana": {"name": "🔮 Tetesan Memori", "cost": 60},
    
    # MAKANAN (ENERGI)
    "food_ration": {"name": "Status: 🍞 Roti Kering", "cost": 30},
    "food_meat": {"name": "Status: 🍖 Daging Asap", "cost": 75},

    # PENAWAR STATUS & SURVIVAL
    "cure_poison": {"name": "🌿 Antidote", "cost": 45},
    "repair_all_kit": {"name": "⚒️ Repair Kit", "cost": 150},
    
    # KUNCI & SURVIVAL GEAR (Sangat penting untuk eksplorasi)
    "buy_key_iron": {"item_id": "buy_key_iron", "name": "🔑 Iron Key", "cost": 75},
    "buy_key_magic": {"item_id": "buy_key_magic", "name": "🔮 Mana Crystal", "cost": 250},
    "item_masker_gas": {"item_id": "item_masker_gas", "name": "😷 Masker Gas", "cost": 200},
    "item_mantel_bulu": {"item_id": "item_mantel_bulu", "name": "🧥 Mantel Bulu", "cost": 200},
    "item_lentera_jiwa": {"item_id": "item_lentera_jiwa", "name": "🏮 Lentera Jiwa", "cost": 300},

    # EQUIPMENT (Menggunakan ID dari MASTER_ITEM_DB)
    "iron_sword": {"item_id": "iron_sword", "cost": 150},
    "novice_staff": {"item_id": "novice_staff", "cost": 150},
    "leather_armor": {"item_id": "leather_armor", "cost": 120},
    "cloth_robe": {"item_id": "cloth_robe", "cost": 100},
    "wooden_shield": {"item_id": "wooden_shield", "cost": 80}
}

# === SISTEM TOKO DINAMIS ===

def get_rest_area_stock(location):
    """Menentukan barang apa saja yang dijual Merchant berdasarkan lokasi."""
    stock = ["potion_heal", "food_ration", "potion_mana", "repair_all_kit"]
    
    if location == "The Whispering Hall":
        stock.extend(["novice_staff", "cloth_robe", "item_lentera_jiwa"])
    elif location == "The Forsaken Mire":
        stock.extend(["cure_poison", "item_masker_gas", "potion_heal_major", "iron_sword"])
    elif location == "The Abyssal Depth":
        stock.extend(["item_lentera_jiwa", "buy_key_magic", "leather_armor"]) 
    elif location == "The Frozen Purgatory":
        stock.extend(["item_mantel_bulu", "food_meat", "buy_key_magic"])
    else: 
        stock.extend(["food_meat", "leather_armor", "buy_key_magic"])
        
    return stock

def get_rest_area_keyboard():
    """Menu Utama saat pemain berada di Rest Area."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛏️ Istirahat & Pulih (20G)", callback_data="rest_sleep")],
        [InlineKeyboardButton(text="🛒 Lihat Dagangan Merchant", callback_data="rest_shop")],
        [InlineKeyboardButton(text="🚪 Lanjutkan Perjalanan", callback_data="rest_exit")]
    ])

def get_shop_keyboard(location="The Whispering Hall"):
    """Membuat susunan tombol toko yang rapi sesuai stok di wilayah tersebut."""
    keyboard = []
    available_stock = get_rest_area_stock(location)
    
    for code in available_stock:
        catalog_entry = SHOP_CATALOG.get(code)
        if not catalog_entry: continue
            
        # Ambil ID asli yang merujuk ke database item (jika ada)
        item_id = catalog_entry.get("item_id", code)
        item_data = get_item(item_id)
        
        # Format tombol berdasarkan tipe item
        if item_data:
            if item_data.get('type') == 'weapon':
                icon = "⚔️"
            elif item_data.get('type') in ['armor', 'head', 'shield', 'offhand', 'boots', 'gloves', 'mask']:
                icon = "🛡️"
            else:
                icon = "📦"
            
            button_text = f"{icon} {item_data.get('name', 'Unknown Item')} - 💰 {catalog_entry['cost']}"
        else:
            # Fallback untuk item yang tidak ada di MASTER_ITEM_DB (misal: keys/story items)
            button_text = f"📦 {catalog_entry.get('name', code)} - 💰 {catalog_entry['cost']}"
            
        keyboard.append([InlineKeyboardButton(text=button_text, callback_data=f"buy_{code}")])
    
    keyboard.append([InlineKeyboardButton(text="🔙 Kembali ke Tenda", callback_data="rest_main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def process_purchase(user_id, callback_data):
    """Logika transaksi dan memasukkan item ke inventory."""
    item_code = callback_data.replace("buy_", "")
    player = get_player(user_id)
    catalog_item = SHOP_CATALOG.get(item_code)
    
    if not catalog_item:
        return False, "⚠️ Barang tidak tersedia di dimensi ini."
        
    cost = catalog_item["cost"]
        
    # 1. Cek Ketersediaan Gold
    if player.get('gold', 0) < cost:
        return False, f"❌ Gold tidak cukup! Kamu butuh *{cost} Gold*."
        
    # 2. Masukkan ke Inventory (Hanya ID string untuk sinkronisasi database)
    inventory = player.get('inventory', [])
    item_id = catalog_item.get("item_id", item_code)
    
    inventory.append(item_id)
    
    # 3. Update Database
    new_gold = player['gold'] - cost
    update_player(user_id, {"gold": new_gold, "inventory": inventory})
    
    # 4. Ambil nama untuk notifikasi
    item_data = get_item(item_id)
    item_name = item_data['name'] if item_data else catalog_item.get('name', item_id.replace("_", " ").title())
    
    return True, f"✅ Berhasil membeli *{item_name}*!\nBarang sudah masuk ke 🎒 Tasmu."
