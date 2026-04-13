from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_player, update_player

# --- KATALOG BARANG TOKO ---
SHOP_ITEMS = {
    "buy_heal": {"name": "🧪 Ramuan Darah (+50 HP)", "cost": 20, "type": "heal", "value": 50},
    "buy_maxhp": {"name": "🛡️ Jantung Golem (+20 Max HP)", "cost": 50, "type": "max_hp", "value": 20},
    "buy_mp": {"name": "🔮 Tetesan Memori (+30 MP)", "cost": 15, "type": "mp", "value": 30}
}

def get_shop_keyboard():
    """Membuat susunan tombol untuk barang-barang di toko"""
    keyboard = []
    
    # Looping semua barang di katalog untuk dibuatkan tombolnya
    for callback_data, item in SHOP_ITEMS.items():
        button_text = f"{item['name']} - 💰 {item['cost']} Gold"
        keyboard.append([InlineKeyboardButton(text=button_text, callback_data=callback_data)])
    
    # Tombol untuk keluar dari toko
    keyboard.append([InlineKeyboardButton(text="🔙 Keluar dari Toko", callback_data="close_shop")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def process_purchase(user_id, item_code):
    """Logika transaksi saat pemain klik tombol beli"""
    player = get_player(user_id)
    item = SHOP_ITEMS.get(item_code)
    
    # Validasi 1: Apakah barang ada?
    if not item:
        return False, "Barang tidak ditemukan dalam arsip."
        
    # Validasi 2: Apakah uangnya cukup?
    if player['gold'] < item['cost']:
        return False, f"❌ Pecahan Memorimu (Gold) tidak cukup!\nKamu butuh **{item['cost']} Gold**, tapi kamu hanya punya **{player['gold']} Gold**."
        
    # --- PROSES PEMBELIAN ---
    new_gold = player['gold'] - item['cost']
    update_data = {"gold": new_gold}
    
    # Efek Ramuan Darah
    if item['type'] == "heal":
        new_hp = min(player['hp'] + item['value'], player['max_hp'])
        update_data["hp"] = new_hp
        msg = f"✅ Cairan merah itu terasa pahit, namun lukamu menutup. (HP kamu menjadi {new_hp}/{player['max_hp']})"
        
    # Efek Jantung Golem
    elif item['type'] == "max_hp":
        update_data["max_hp"] = player['max_hp'] + item['value']
        msg = f"✅ Dadamu terasa panas! Batas darahmu telah meningkat. (Max HP menjadi {update_data['max_hp']})"
        
    # Efek Tetesan Memori
    elif item['type'] == "mp":
        new_mp = min(player['mp'] + item['value'], player['max_mp'])
        update_data["mp"] = new_mp
        msg = f"✅ Pikiranmu kembali jernih dari kabut Archivus. (MP kamu menjadi {new_mp}/{player['max_mp']})"
        
    # Simpan ke Database
    update_player(user_id, update_data)
    
    return True, msg
