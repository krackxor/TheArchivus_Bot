"""
Sistem Toko Archivus (Shop System)
Terintegrasi dengan Master Data Equipment (Senjata, Armor, Ramuan, Mantra, dan Repair Kit).
Diperbarui dengan item Makanan (Energi) dan Penawar Status (Cure).
"""
import uuid
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Memanggil fungsi dari file database dan equipment baru
from database import get_player, update_player
from game.systems.equipment import get_equipment_stat

# --- KATALOG TOKO ---
# Menggabungkan konsumsi statik dan equipment dinamis dari equipment.py
SHOP_CATALOG = {
    # RAMUAN HP & MP
    "buy_heal_30": {"name": "🧪 Minor HP Potion", "desc": "+30 HP", "cost": 50, "type": "potion", "effect": "heal_30"},
    "buy_heal_80": {"name": "🧪 Major HP Potion", "desc": "+80 HP", "cost": 120, "type": "potion", "effect": "heal_80"},
    "buy_mp_40": {"name": "🔮 Tetesan Memori", "desc": "+40 MP", "cost": 60, "type": "potion", "effect": "mp_40"},
    
    # MAKANAN (ENGERGI) - Fitur Baru!
    "buy_food_bread": {"name": "🍞 Roti Kering", "desc": "+30 Energi", "cost": 30, "type": "food", "effect": "energy_30"},
    "buy_food_meat": {"name": "🍖 Daging Asap", "desc": "+80 Energi", "cost": 75, "type": "food", "effect": "energy_80"},

    # PENAWAR STATUS (CURE) - Fitur Baru!
    "buy_cure_poison": {"name": "🌿 Antidote", "desc": "Sembuhkan Racun", "cost": 45, "type": "potion", "effect": "cure_poisoned"},
    "buy_cure_dizzy": {"name": "🧂 Garam Sadar", "desc": "Sembuhkan Pusing", "cost": 40, "type": "potion", "effect": "cure_dizzy"},
    
    # PERAWATAN & BUFF
    "buy_repair_kit": {"name": "⚒️ Repair Kit", "desc": "Perbaiki 100% Equip", "cost": 150, "type": "potion", "effect": "repair_all"},
    "buy_resin_fire": {"name": "📜 Mantra Api", "desc": "Elemen Api ke senjata", "cost": 100, "type": "potion", "effect": "resin_Api"},
    "buy_resin_wind": {"name": "📜 Mantra Angin", "desc": "Elemen Angin ke senjata", "cost": 100, "type": "potion", "effect": "resin_Angin"},
    
    # EQUIPMENT (Tarik data otomatis dari equipment.py - Kita sediakan Tier 1)
    "buy_wpn_katana": {"type": "equipment", "category": "weapon", "equip_id": "wpn_katana", "tier": 1},
    "buy_wpn_staff": {"type": "equipment", "category": "weapon", "equip_id": "wpn_staff", "tier": 1},
    "buy_arm_plate": {"type": "equipment", "category": "chest", "equip_id": "arm_plate_armor", "tier": 1},
    "buy_arm_robe": {"type": "equipment", "category": "chest", "equip_id": "arm_cloth_robe", "tier": 1},
    "buy_shd_buckler": {"type": "equipment", "category": "shield", "equip_id": "shd_buckler", "tier": 1}
}

def get_shop_keyboard():
    """Membuat susunan tombol toko yang rapi dan terintegrasi dengan equipment.py"""
    keyboard = []
    
    # Mengelompokkan item agar rapi di UI
    for code, item in SHOP_CATALOG.items():
        if item.get("type") in ["potion", "food"]:
            button_text = f"{item['name']} ({item['desc']}) - 💰 {item['cost']}"
            keyboard.append([InlineKeyboardButton(text=button_text, callback_data=code)])
        else:
            # Ambil stat dari equipment.py
            eq = get_equipment_stat(item["equip_id"], item["category"], item["tier"])
            if not eq: 
                continue
            
            # Format text tombol, contoh: ⚔️ [Basic] Katana (+27 Atk) - 💰 250
            stat_val = f"+{eq.get('atk', 0)} Atk" if "atk" in eq else f"+{eq.get('def', 0)} Def"
            icon = "⚔️" if item["category"] == "weapon" else "🛡️"
            button_text = f"{icon} {eq['full_name']} ({stat_val}) - 💰 {eq['cost']}"
            
            keyboard.append([InlineKeyboardButton(text=button_text, callback_data=code)])
    
    keyboard.append([InlineKeyboardButton(text="🔙 Keluar", callback_data="close_shop")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def process_purchase(user_id, item_code):
    """Logika transaksi dan memasukkan item ke inventory"""
    player = get_player(user_id)
    catalog_item = SHOP_CATALOG.get(item_code)
    
    if not catalog_item:
        return False, "Barang gaib, tidak ditemukan di toko."
        
    cost = 0
    final_item = None
    
    # 1. BENTUK DATA ITEM YANG AKAN MASUK TAS
    if catalog_item.get("type") in ["potion", "food"]:
        cost = catalog_item["cost"]
        final_item = {
            "id": str(uuid.uuid4())[:8],
            "name": catalog_item["name"],
            "type": catalog_item["type"], # Menandai apakah ini potion atau food
            "effect": catalog_item["effect"]
        }
    else:
        # Ambil data komplit dari equipment.py
        eq = get_equipment_stat(catalog_item["equip_id"], catalog_item["category"], catalog_item["tier"])
        if not eq: 
            return False, "Data equipment rusak!"
        
        cost = eq["cost"]
        final_item = {
            "id": str(uuid.uuid4())[:8],
            "name": eq["full_name"],
            "type": catalog_item["category"], # weapon, chest, shield dll
            "bonus_atk": eq.get("atk", 0),
            "bonus_def": eq.get("def", 0),
            "weight": eq.get("weight", 0),
            "speed": eq.get("speed", "medium"),
            "bonus_type": eq.get("bonus_type", None),
            "is_magic": eq.get("is_magic", False),
            
            # Pastikan Durability dan Skill ikut masuk ke tas!
            "durability": eq.get("durability", 50),
            "max_durability": eq.get("max_durability", 50),
            "skill": eq.get("skill", None)
        }
        
    # 2. CEK KEUANGAN PEMAIN
    if player.get('gold', 0) < cost:
        return False, f"❌ Gold tidak cukup! Kamu butuh *{cost} Gold*."
        
    # 3. EKSEKUSI PEMBELIAN (Potong Uang & Masukkan ke Tas)
    new_gold = player['gold'] - cost
    inventory = player.get('inventory', [])
    inventory.append(final_item)
    
    update_player(user_id, {"gold": new_gold, "inventory": inventory})
    
    return True, f"✅ Berhasil membeli *{final_item['name']}*!\nBarang sudah masuk ke 🎒 Inventory."
