# game/consumables/items.py

"""
Database Camping Gears (Alat Perkemahan)
Khusus untuk item yang digunakan di Rest Area.
"""

# Dictionary ini hanya menampung item kategori camping/tenda
CAMPING_ITEMS = {
    "tenda": {
        "id": "tenda",
        "name": "Tenda Kemah",
        "type": "consumable",        # Tetap 'consumable' agar muncul di tas ramuan/item
        "effect_type": "camp_gear",  # Identitas unik untuk Rest Area
        "description": "Tenda portabel penahan dingin. Hanya bisa dipasang di Rest Area untuk memulihkan 100% HP, MP, dan Energi.",
        "price": 300,
        "tier": 1
    }
}

def get_item(item_id):
    """
    Mengambil data item dari database perkemahan.
    Gunakan ini sebagai tambahan import jika get_item potion ada di file lain.
    """
    return CAMPING_ITEMS.get(item_id)
