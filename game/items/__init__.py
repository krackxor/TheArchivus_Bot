
# game/items/__init__.py

from .weapons import WEAPON_DB
from .armors import ARMOR_DB
from .heads import HEAD_DB
from .masks import MASK_DB
from .gloves import GLOVES_DB
from .boots import BOOTS_DB
from .cloaks import CLOAK_DB
from .artifacts import ARTIFACT_DB

# Master Database gabungan
MASTER_ITEM_DB = {
    **WEAPON_DB,
    **ARMOR_DB,
    **HEAD_DB,
    **MASK_DB,
    **GLOVES_DB,
    **BOOTS_DB,
    **CLOAK_DB,
    **ARTIFACT_DB
}

def get_item(item_id):
    """Fungsi helper untuk mengambil data item dengan aman."""
    return MASTER_ITEM_DB.get(item_id)

# Kategori untuk keperluan UI/Bot
ITEM_TYPES = {
    "weapon": "⚔️ Senjata",
    "armor": "👕 Zirah",
    "head": "🪖 Kepala",
    "mask": "🎭 Topeng",
    "gloves": "🧤 Tangan",
    "boots": "👞 Sepatu",
    "cloak": "🧣 Jubah",
    "artifact": "🔮 Artefak"
}
