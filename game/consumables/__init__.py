# game/items/consumables/__init__.py

from .hp import HP_POTIONS
from .mp import MP_POTIONS
from .food import FOODS
from .utility import UTILITIES # Import yang baru
from .special import SPECIAL_ITEMS

CONSUMABLES = {
    **HP_POTIONS,
    **MP_POTIONS,
    **FOODS,
    **UTILITIES, # Masukkan ke dalam database gabungan
    **SPECIAL_ITEMS
}
