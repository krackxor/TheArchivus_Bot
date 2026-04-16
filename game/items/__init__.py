# game/items/__init__.py

"""
MASTER ITEM DATABASE - The Archivus
Menggabungkan semua kategori perlengkapan ke dalam satu kamus pusat.
"""

from .weapons import WEAPONS
from .armors import ARMORS
from .heads import HEADS
from .masks import MASKS
from .gloves import GLOVES
from .boots import BOOTS
from .cloaks import CLOAKS
from .artifacts import ARTIFACTS

# Master Database gabungan (Menyatukan semua dictionary)
MASTER_ITEM_DB = {
    **WEAPONS,
    **ARMORS,
    **HEADS,
    **MASKS,
    **GLOVES,
    **BOOTS,
    **CLOAKS,
    **ARTIFACTS
}

def get_item(item_id):
    """
    Fungsi helper untuk mengambil data item dengan aman.
    Digunakan oleh main.py dan inventory_manager.py.
    """
    if not item_id:
        return None
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
