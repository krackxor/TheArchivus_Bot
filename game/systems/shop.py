"""
Sistem Toko Archivus (Shop System)
Menangani pembelian item konsumsi dan peralatan (Equipment).
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_player, update_player
import uuid

# --- KATALOG BARANG TOKO ---
# Stat Seimbang: Harga naik seiring kegunaan
SHOP_ITEMS = {
    # KONSUMSI (Langsung Pakai)
    "buy_heal": {"name": "🧪 Ramuan Darah", "desc": "+50 HP", "cost": 25, "type": "heal", "value": 50},
    "buy_mp": {"name": "🔮 Tetesan Memori", "desc": "+40 MP", "cost": 20, "type": "mp", "value": 40},
    
    # PERALATAN (Equip - Masuk Inventory)
    "buy_sword": {
        "name": "⚔️ Pedang Karat", 
        "desc": "+10 Attack", "cost": 150, "type": "weapon", "atk": 10
    },
    "buy_shield": {
        "name": "🛡️ Perisai Kayu", 
        "desc": "+10 Defense", "cost": 120, "type": "armor", "def": 10
    },
    "buy_relic": {
        "name": "🔱 Relik Kuno", 
        "desc": "+50 Max HP", "cost": 300, "type": "artifact", "max_hp": 50
    }
}

def get_shop_keyboard():
    """Membuat susunan tombol toko yang rapi"""
    keyboard = []
    
    for code, item in SHOP_ITEMS.items():
        button_text = f"{item['name']} ({item['desc']}) - 💰 {item['cost']}"
        keyboard.append([InlineKeyboardButton(text=button_text, callback_data=code)])
    
    keyboard.append([InlineKeyboardButton(text="🔙 Keluar", callback_data="close_shop")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def process_purchase(user_id, item_code):
    """Logika transaksi dan penerapan efek item"""
    player = get_player(user_id)
    item = SHOP_ITEMS.get(item_code)
    
    if not item:
        return False, "Barang gaib, tidak ditemukan."
        
    if player['gold'] < item['cost']:
        return False, f"❌ Gold tidak cukup! Kamu butuh *{item['cost']} Gold*."
        
    new_gold = player['gold'] - item['cost']
    update_data = {"gold": new_gold}
    msg = ""

    # --- LOGIKA ITEM KONSUMSI ---
    if item['type'] == "heal":
        new_hp = min(player['hp'] + item['value'], player['max_hp'])
        update_data["hp"] = new_hp
        msg = f"✅ HP pulih! (*{new_hp}/{player['max_hp']}*)"
        
    elif item['type'] == "mp":
        new_mp = min(player['mp'] + item['value'], player['max_mp'])
        update_data["mp"] = new_mp
        msg = f"✅ MP bertambah! (*{new_mp}/{player['max_mp']}*)"

    # --- LOGIKA EQUIPMENT (Masuk Inventory) ---
    elif item['type'] in ["weapon", "armor", "artifact"]:
        inventory = player.get('inventory', [])
        
        # Buat objek item unik untuk inventory
        new_item = {
            "id": str(uuid.uuid4())[:8],
            "name": item['name'],
            "type": item['type'],
            "bonus_atk": item.get('atk', 0),
            "bonus_def": item.get('def', 0),
            "bonus_max_hp": item.get('max_hp', 0)
        }
        
        inventory.append(new_item)
        update_data["inventory"] = inventory
        
        # Jika itu artifact Max HP, langsung tambahkan ke player
        if item['type'] == "artifact" and "max_hp" in item:
            update_data["max_hp"] = player['max_hp'] + item['max_hp']
            update_data["hp"] = player['hp'] + item['max_hp']
            
        msg = f"✅ Berhasil membeli *{item['name']}*! Barang sudah masuk ke tas (Inventory)."

    update_player(user_id, update_data)
    return True, msg
