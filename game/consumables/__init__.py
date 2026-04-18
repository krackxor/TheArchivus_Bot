# game/items/consumables/__init__.py

from .hp import HP_POTIONS
from .mp import MP_POTIONS
from .food import FOODS
from .utility import UTILITIES
from .special import SPECIAL_ITEMS
from .items import CAMPING_ITEMS

# Database gabungan untuk semua barang habis pakai
CONSUMABLES = {
    **HP_POTIONS,
    **MP_POTIONS,
    **FOODS,
    **UTILITIES,
    **SPECIAL_ITEMS,
    **CAMPING_ITEMS # Masukkan Tenda ke dalam database utama consumables
}

def get_item(item_id):
    """Fungsi pembantu untuk mengambil data item berdasarkan ID."""
    return CONSUMABLES.get(item_id)
