# game/items/__init__.py

"""
MASTER ITEM DATABASE - The Archivus
Menggabungkan semua kategori perlengkapan ke dalam satu kamus pusat.
Menghubungkan Weapons, Armors, Heads, Masks, Gloves, Boots, Cloaks, dan Artifacts.
"""

from .weapons import WEAPONS
from .armors import ARMORS
from .heads import HEADS
from .masks import MASKS
from .gloves import GLOVES
from .boots import BOOTS
from .cloaks import CLOAKS
from .artifacts import ARTIFACTS

# --- TAMBAHAN: CONSUMABLES DATABASE ---
# Jika kamu belum membuat file consumables.py tersendiri, 
# kita definisikan ramuan dasar di sini agar get_item tidak return None.
CONSUMABLES = {
    "potion_heal": {
        "id": "potion_heal", "name": "Minor HP Potion", "type": "consumable",
        "effect_type": "heal_hp", "value": 30, "tier": 1,
        "description": "Ramuan merah standar untuk memulihkan 30 HP."
    },
    "potion_heal_major": {
        "id": "potion_heal_major", "name": "Major HP Potion", "type": "consumable",
        "effect_type": "heal_hp", "value": 80, "tier": 3,
        "description": "Ramuan merah pekat untuk memulihkan 80 HP."
    },
    "potion_mana": {
        "id": "potion_mana", "name": "Tetesan Memori", "type": "consumable",
        "effect_type": "restore_mp", "value": 40, "tier": 2,
        "description": "Cairan biru bening yang memulihkan 40 MP."
    },
    "cure_poison": {
        "id": "cure_poison", "name": "Antidote", "type": "consumable",
        "effect_type": "clear_poison", "value": 0, "tier": 2,
        "description": "Ramuan herbal untuk menetralkan racun dalam tubuh."
    },
    "food_ration": {
        "id": "food_ration", "name": "Roti Kering", "type": "consumable",
        "effect_type": "restore_energy", "value": 30, "tier": 1,
        "description": "Makanan keras tapi cukup untuk memulihkan 30 Energi."
    }
}

# Master Database gabungan (Menyatukan lebih dari 230+ item unik)
MASTER_ITEM_DB = {
    **WEAPONS,
    **ARMORS,
    **HEADS,
    **MASKS,
    **GLOVES,
    **BOOTS,
    **CLOAKS,
    **ARTIFACTS,
    **CONSUMABLES
}

def get_item(item_id):
    """
    Fungsi helper untuk mengambil data item dengan aman.
    Digunakan oleh sistem combat, shop, dan inventory_manager.
    """
    if not item_id:
        return None
    # Pastikan ID dalam bentuk string untuk menghindari kesalahan pencarian
    return MASTER_ITEM_DB.get(str(item_id))

# Kategori untuk keperluan UI, Bot, dan Sorting Tas
ITEM_TYPES = {
    "weapon": "⚔️ Senjata",
    "armor": "👕 Zirah Utama",
    "head": "🪖 Pelindung Kepala",
    "mask": "🎭 Topeng Sinergi",
    "gloves": "🧤 Sarung Tangan",
    "boots": "👞 Sepatu Bot",
    "cloak": "🧣 Jubah",
    "artifact": "🔮 Artefak",
    "offhand": "🛡️ Tangan Kiri",
    "consumable": "🧪 Habis Pakai"
}

def get_all_items_by_tier(tier):
    """Fungsi pembantu untuk sistem looting: Ambil semua item berdasarkan tier."""
    return [item for item in MASTER_ITEM_DB.values() if item.get('tier') == tier]
