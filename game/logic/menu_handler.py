# game/logic/menu_handler.py

from game.items import get_item, ITEM_TYPES

def get_main_menu():
    """Menu utama yang selalu muncul di bawah."""
    return [
        [{"text": "👤 Profil & Stats", "callback": "menu_profile"}],
        [{"text": "🎒 Tas (Inventory)", "callback": "menu_inventory"}, {"text": "⚔️ Cari Lawan", "callback": "menu_combat"}],
        [{"text": "⚒️ Blacksmith (Repair)", "callback": "menu_forge"}]
    ]

def get_inventory_menu(player):
    """Menampilkan isi tas dalam bentuk tombol."""
    buttons = []
    inventory = player.get('inventory', [])

    if not inventory:
        return [[{"text": "⬅️ Kembali", "callback": "menu_main"}]]

    # Buat tombol per baris (2 tombol per baris agar rapi)
    current_row = []
    for item_id in inventory:
        item = get_item(item_id)
        icon = "📦" # Default
        
        # Beri icon berdasarkan tipe item
        if item['type'] == 'weapon': icon = "⚔️"
        elif item['type'] == 'armor': icon = "👕"
        elif item['type'] == 'artifact': icon = "🔮"

        current_row.append({"text": f"{icon} {item['name']}", "callback": f"equip_{item_id}"})
        
        if len(current_row) == 2:
            buttons.append(current_row)
            current_row = []
    
    if current_row: buttons.append(current_row)
    
    # Tambahkan tombol navigasi bawah
    buttons.append([{"text": "⬅️ Kembali", "callback": "menu_main"}])
    return buttons

def get_profile_menu(player):
    """Menampilkan slot yang sedang terpakai untuk dilepas (unequip)."""
    buttons = []
    equipped = player.get('equipped', {})

    for slot, item_id in equipped.items():
        item = get_item(item_id)
        if item:
            buttons.append([{"text": f"❌ Lepas {item['name']}", "callback": f"unequip_{slot}"}])

    buttons.append([{"text": "⬅️ Kembali", "callback": "menu_main"}])
    return buttons
