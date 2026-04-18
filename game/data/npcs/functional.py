# game/data/npcs/functional.py

"""
NPC Functional Database - The Archivus
Berisi NPC dengan fungsi sistem tetap: Blacksmith, Merchant, dan Healer.
"""

FUNCTIONAL_NPCS = {
    # --- PANDAI BESI (BLACKSMITH) ---
    "npc_aethelred": {
        "name": "Aethelred the Blacksmith",
        "role": "blacksmith",
        "desc": "Seorang pria berotot dengan palu raksasa yang tampak lebih tua dari dimensi ini sendiri.",
        "dialog_greetings": [
            "Baja yang bagus... tapi pemiliknya terlihat bodoh. Mau perbaiki apa?",
            "Jangan buang waktuku jika kau tidak punya emas untuk membayar jasaku.",
            "Palu ini sudah menghancurkan ribuan pedang, jangan biarkan pedangmu jadi yang berikutnya."
        ],
        "repair_factor": 1.0 # Faktor pengali biaya perbaikan standar
    },

    # --- PEDAGANG (MERCHANT) ---
    "npc_elara": {
        "name": "Elara the Merchant",
        "role": "shop",
        "desc": "Wanita berjubah sutra kelam yang selalu dikelilingi oleh kotak-kotak kayu tua.",
        "dialog_greetings": [
            "Kau terlihat pucat, Weaver. Mungkin ramuanku bisa membantumu?",
            "Aku punya barang-barang dari Cycle yang sudah lama terlupakan. Lihatlah.",
            "Koin emasmu berisik sekali di dalam kantung itu. Mari kita tukar dengan sesuatu yang berguna."
        ],
        # Daftar ID item yang dijual (Harus sesuai dengan ID di game/items/)
        "inventory": [
            "pot_red_1", 
            "pot_blue_1", 
            "anti_poi_1", 
            "item_masker_gas",  # Item pelindung rawa
            "item_mantel_bulu"   # Item pelindung area dingin
        ]
    },

    # --- PENYEMBUH (HEALER) ---
    "npc_priestess": {
        "name": "Priestess of the Light",
        "role": "healer",
        "desc": "Sosok wanita yang memancarkan cahaya redup, memberikan rasa tenang di tengah kegelapan.",
        "dialog_greetings": [
            "Mendekatlah, Weaver. Biarkan cahaya membasuh luka di jiwamu.",
            "Dunia ini sangat kejam bagi tubuh yang fana. Izinkan aku memulihkanmu.",
            "Cahaya ini tidak gratis, namun ia akan menjamin perjalananmu berlanjut."
        ],
        "heal_cost": 200, # Biaya emas untuk memulihkan HP & MP secara penuh
        "clear_debuff_cost": 100 # Biaya tambahan untuk menghapus status buruk (Poison, dll)
    }
}

def get_functional_npc(npc_id):
    """Mengambil data NPC fungsional berdasarkan ID."""
    return FUNCTIONAL_NPCS.get(npc_id)

def get_all_functional():
    """Mengambil seluruh database NPC fungsional."""
    return FUNCTIONAL_NPCS
