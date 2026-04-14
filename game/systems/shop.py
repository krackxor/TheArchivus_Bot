"""
Sistem Toko & Rest Area Archivus (Shop System)
Terintegrasi dengan Master Data Equipment dan Dinamika Lokasi.
Menyediakan barang unik (Kunci, Gear Survival) berdasarkan wilayah Rest Area.
"""
import uuid
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Memanggil fungsi dari file database dan equipment
from database import get_player, update_player
from game.systems.equipment import get_equipment_stat

# --- KATALOG TOKO LENGKAP ---
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
    "buy_resin_fire": {"name": "📜 Mantra Api", "desc": "Elemen Api ke senjata", "cost": 100, "type": "potion", "effect": "resin_Api"},
    "buy_resin_wind": {"name": "📜 Mantra Angin", "desc": "Elemen Angin ke senjata", "cost": 100, "type": "potion", "effect": "resin_Angin"},
    
    # KUNCI & SURVIVAL GEAR (Khusus Eksplorasi)
    "buy_key_iron": {"name": "🔑 Iron Key", "desc": "Membuka Peti Besi", "cost": 75, "type": "utility", "effect": "key_iron"},
    "buy_key_magic": {"name": "🔮 Mana Crystal", "desc": "Membuka Peti Segel", "cost": 250, "type": "utility", "effect": "key_magic"},
    "buy_arm_mask": {"name": "😷 Masker Tinta", "desc": "Menahan Racun Miasma", "cost": 200, "type": "utility", "effect": "gear_mask"},
    "buy_torch_deluxe": {"name": "🏮 Shadow Lantern", "desc": "Obor Tahan Lama", "cost": 300, "type": "utility", "effect": "gear_lantern"},

    # EQUIPMENT (Tarik data otomatis dari equipment.py)
    "buy_wpn_katana": {"type": "equipment", "category": "weapon", "equip_id": "wpn_katana", "tier": 1},
    "buy_wpn_staff": {"type": "equipment", "category": "weapon", "equip_id": "wpn_staff", "tier": 1},
    "buy_arm_plate": {"type": "equipment", "category": "chest", "equip_id": "arm_plate_armor", "tier": 1},
    "buy_arm_robe": {"type": "equipment", "category": "chest", "equip_id": "arm_cloth_robe", "tier": 1},
    "buy_shd_buckler": {"type": "equipment", "category": "shield", "equip_id": "shd_buckler", "tier": 1}
}

# === SISTEM TOKO DINAMIS ===

def get_rest_area_stock(location):
    """Menentukan barang apa saja yang dijual Merchant berdasarkan lokasi."""
    # Barang dasar yang SELALU ADA di setiap Rest Area
    stock = ["buy_heal_30", "buy_food_bread", "buy_mp_40", "buy_repair_kit"]
    
    # Barang Spesifik Lokasi (Merchant Unik)
    if location == "The Whispering Hall":
        stock.extend(["buy_wpn_staff", "buy_arm_robe"])
    elif location == "Forgotten Script-Vault":
        stock.extend(["buy_wpn_katana", "buy_arm_plate", "buy_key_iron"]) # Jual Kunci Besi
    elif location == "The Inky Mire":
        stock.extend(["buy_cure_poison", "buy_arm_mask", "buy_heal_80"]) # Jual Masker Anti Racun
    elif location == "Echoing Abyss":
        stock.extend(["buy_cure_dizzy", "buy_torch_deluxe", "buy_key_magic"]) # Jual Obor Terang
    else: # The Final Archive
        stock.extend(["buy_resin_fire", "buy_resin_wind", "buy_food_meat", "buy_key_magic"])
        
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
        if not item:
            continue
            
        # Jika berupa potion, makanan, atau utility (kunci/masker)
        if item.get("type") in ["potion", "food", "utility"]:
            button_text = f"{item['name']} - 💰 {item['cost']}"
            keyboard.append([InlineKeyboardButton(text=button_text, callback_data=code)])
        # Jika berupa senjata/armor
        else:
            eq = get_equipment_stat(item["equip_id"], item["category"], item["tier"])
            if not eq: 
                continue
            
            stat_val = f"+{eq.get('atk', 0)} Atk" if "atk" in eq else f"+{eq.get('def', 0)} Def"
            icon = "⚔️" if item["category"] == "weapon" else "🛡️"
            button_text = f"{icon} {eq['full_name']} ({stat_val}) - 💰 {eq['cost']}"
            
            keyboard.append([InlineKeyboardButton(text=button_text, callback_data=code)])
    
    # Tombol kembali ke menu Rest Area
    keyboard.append([InlineKeyboardButton(text="🔙 Kembali ke Tenda", callback_data="rest_main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def process_purchase(user_id, item_code):
    """Logika transaksi dan memasukkan item ke inventory."""
    player = get_player(user_id)
    catalog_item = SHOP_CATALOG.get(item_code)
    
    if not catalog_item:
        return False, "Barang gaib, tidak ditemukan di toko."
        
    cost = 0
    final_item = None
    
    # 1. BENTUK DATA ITEM (Consumable & Utility)
    if catalog_item.get("type") in ["potion", "food", "utility"]:
        cost = catalog_item["cost"]
        final_item = {
            "id": str(uuid.uuid4())[:8],
            "name": catalog_item["name"],
            "type": catalog_item["type"], 
            "effect": catalog_item["effect"]
        }
    # (Equipment)
    else:
        eq = get_equipment_stat(catalog_item["equip_id"], catalog_item["category"], catalog_item["tier"])
        if not eq: 
            return False, "Data equipment rusak!"
        
        cost = eq["cost"]
        final_item = {
            "id": str(uuid.uuid4())[:8],
            "name": eq["full_name"],
            "type": catalog_item["category"],
            "bonus_atk": eq.get("atk", 0),
            "bonus_def": eq.get("def", 0),
            "weight": eq.get("weight", 0),
            "speed": eq.get("speed", "medium"),
            "bonus_type": eq.get("bonus_type", None),
            "is_magic": eq.get("is_magic", False),
            "durability": eq.get("durability", 50),
            "max_durability": eq.get("max_durability", 50),
            "skill": eq.get("skill", None)
        }
        
    # 2. CEK KEUANGAN PEMAIN
    if player.get('gold', 0) < cost:
        return False, f"❌ Gold tidak cukup! Kamu butuh *{cost} Gold*."
        
    # 3. EKSEKUSI PEMBELIAN
    new_gold = player['gold'] - cost
    inventory = player.get('inventory', [])
    inventory.append(final_item)
    
    update_player(user_id, {"gold": new_gold, "inventory": inventory})
    
    return True, f"✅ Berhasil membeli *{final_item['name']}*!\nBarang sudah masuk ke 🎒 Inventory."
