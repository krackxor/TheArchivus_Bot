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
# Format item yang dijual adalah "ID item" yang sesuai dengan MASTER_ITEM_DB di folder `game/items/`
SHOP_CATALOG = {
    # RAMUAN HP & MP
    "buy_heal_30": {"name": "🧪 Minor HP Potion", "desc": "+30 HP", "cost": 50, "type": "potion", "effect": "heal_30"},
    "buy_heal_80": {"name": "🧪 Major HP Potion", "desc": "+80 HP", "cost": 120, "type": "potion", "effect": "heal_80"},
    "buy_mp_40": {"name": "🔮 Tetesan Memori", "desc": "+40 MP", "cost": 60, "type": "potion", "effect": "mp_40"},
    
    # MAKANAN (ENERGI)
    "buy_food_bread": {"name": "🍞 Roti Kering", "desc": "+30 Energi", "cost": 30, "type": "food", "effect": "energy_30"},
    "buy_food_meat": {"name": "🍖 Daging Asap", "desc": "+80 Energi", "cost": 75, "type": "food", "effect": "energy_80"},

    # PENAWAR STATUS (CURE)
    "buy_cure_poison": {"name": "🌿 Antidote", "desc": "Sembuhkan Racun", "cost": 45, "type": "potion", "effect": "cure_poisoned"},
    "buy_cure_dizzy": {"name": "🧂 Garam Sadar", "desc": "Sembuhkan Pusing", "cost": 40, "type": "potion", "effect": "cure_dizzy"},
    
    # PERAWATAN & BUFF
    "buy_repair_kit": {"name": "⚒️ Repair Kit", "desc": "Perbaiki 100% Equip", "cost": 150, "type": "potion", "effect": "repair_all"},
    "buy_resin_fire": {"name": "📜 Mantra Api", "desc": "Elemen Api ke senjata", "cost": 100, "type": "potion", "effect": "resin_fire"},
    "buy_resin_wind": {"name": "📜 Mantra Angin", "desc": "Elemen Angin ke senjata", "cost": 100, "type": "potion", "effect": "resin_wind"},
    
    # KUNCI & SURVIVAL GEAR (Khusus Eksplorasi)
    "buy_key_iron": {"name": "🔑 Iron Key", "desc": "Membuka Peti Besi", "cost": 75, "type": "utility", "effect": "key_iron"},
    "buy_key_magic": {"name": "🔮 Mana Crystal", "desc": "Membuka Peti Segel", "cost": 250, "type": "utility", "effect": "key_magic"},
    "buy_arm_mask": {"name": "😷 Masker Tinta", "desc": "Menahan Racun Miasma", "cost": 200, "type": "utility", "effect": "gear_mask"},
    "buy_torch_deluxe": {"name": "🏮 Shadow Lantern", "desc": "Obor Tahan Lama", "cost": 300, "type": "utility", "effect": "gear_lantern"},

    # EQUIPMENT (Menggunakan ID dari MASTER_ITEM_DB)
    "iron_sword": {"type": "equipment", "item_id": "iron_sword", "cost": 150},
    "novice_staff": {"type": "equipment", "item_id": "novice_staff", "cost": 150},
    "leather_armor": {"type": "equipment", "item_id": "leather_armor", "cost": 120},
    "cloth_robe": {"type": "equipment", "item_id": "cloth_robe", "cost": 100},
    "wooden_shield": {"type": "equipment", "item_id": "wooden_shield", "cost": 80}
}

# === SISTEM TOKO DINAMIS ===

def get_rest_area_stock(location):
    """Menentukan barang apa saja yang dijual Merchant berdasarkan lokasi."""
    stock = ["buy_heal_30", "buy_food_bread", "buy_mp_40", "buy_repair_kit"]
    
    if location == "The Whispering Hall":
        stock.extend(["novice_staff", "cloth_robe"])
    elif location == "The Forsaken Mire": # Diperbarui sesuai string lokasi baru
        stock.extend(["buy_cure_poison", "buy_arm_mask", "buy_heal_80", "iron_sword"])
    elif location == "The Abyssal Depth":
        stock.extend(["buy_cure_dizzy", "buy_torch_deluxe", "buy_key_magic"]) 
    else: 
        stock.extend(["buy_resin_fire", "buy_resin_wind", "buy_food_meat", "leather_armor", "buy_key_magic"])
        
    return stock

def get_rest_area_keyboard():
    """Menu Utama saat pemain baru saja memasuki Rest Area."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛏️ Menginap & Pulih (20G)", callback_data="rest_sleep")],
        [InlineKeyboardButton(text="🛒 Lihat Dagangan Merchant", callback_data="rest_shop")],
        [InlineKeyboardButton(text="🚪 Lanjutkan Perjalanan", callback_data="rest_exit")]
    ])

def get_shop_keyboard(location="The Whispering Hall"):
    """Membuat susunan tombol toko yang rapi sesuai stok di wilayah tersebut."""
    keyboard = []
    available_stock = get_rest_area_stock(location)
    
    for code in available_stock:
        item = SHOP_CATALOG.get(code)
        if not item: continue
            
        if item.get("type") in ["potion", "food", "utility"]:
            button_text = f"{item['name']} - 💰 {item['cost']}"
            keyboard.append([InlineKeyboardButton(text=button_text, callback_data=f"buy_{code}")])
        else:
            eq = get_item(item["item_id"])
            if not eq: continue
            
            stat_val = f"+{eq.get('p_atk', eq.get('m_atk', 0))} Atk" if eq.get('type') == 'weapon' else f"+{eq.get('p_def', eq.get('m_def', 0))} Def"
            icon = "⚔️" if eq["type"] == "weapon" else "🛡️"
            button_text = f"{icon} {eq['name']} ({stat_val}) - 💰 {item['cost']}"
            
            keyboard.append([InlineKeyboardButton(text=button_text, callback_data=f"buy_{code}")])
    
    keyboard.append([InlineKeyboardButton(text="🔙 Kembali ke Tenda", callback_data="rest_main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def process_purchase(user_id, callback_data):
    """Logika transaksi dan memasukkan item ke inventory."""
    item_code = callback_data.replace("buy_", "")
    player = get_player(user_id)
    catalog_item = SHOP_CATALOG.get(item_code)
    
    if not catalog_item:
        return False, "Barang gaib, tidak ditemukan di toko."
        
    cost = catalog_item["cost"]
        
    # CEK KEUANGAN PEMAIN
    if player.get('gold', 0) < cost:
        return False, f"❌ Gold tidak cukup! Kamu butuh *{cost} Gold*."
        
    # BENTUK DATA ITEM
    # Jika Utility/Consumable, kita simpan dictionary utuh (karena ini item sekali pakai khusus)
    # Jika Equipment, kita hanya perlu menyimpan ID string-nya sesuai arsitektur kita
    inventory = player.get('inventory', [])
    
    if catalog_item.get("type") in ["potion", "food", "utility"]:
        final_item = {
            "id": item_code, 
            "name": catalog_item["name"],
            "type": catalog_item["type"], 
            "effect": catalog_item["effect"]
        }
        inventory.append(final_item)
        item_name = final_item["name"]
    else:
        # Jika itu senjata/armor, simpan nama ID-nya saja ("iron_sword", dll)
        eq_id = catalog_item["item_id"]
        inventory.append(eq_id)
        item_name = get_item(eq_id)["name"]
    
    # EKSEKUSI PEMBELIAN
    new_gold = player['gold'] - cost
    update_player(user_id, {"gold": new_gold, "inventory": inventory})
    
    return True, f"✅ Berhasil membeli *{item_name}*!\nBarang sudah masuk ke 🎒 Tasmu."
