# game/entities/npcs.py

import random
from game.data import NPC_POOL, LORE_STORIES

def get_npc_by_category(category):
    """
    Mengambil satu varian NPC secara acak dari kategori tertentu.
    Contoh: get_npc_by_category('healer')
    """
    category_list = NPC_POOL.get(category)
    if not category_list:
        return None
    
    npc = random.choice(category_list).copy()
    npc['category'] = category # Menandai kategori untuk logika di main logic
    return npc

def get_random_npc_event():
    """
    Mengambil satu NPC secara acak dari seluruh kategori yang ada.
    Digunakan untuk event pertemuan mendadak saat eksplorasi.
    """
    # Ambil kategori secara acak (healer, trickster, dll)
    all_categories = list(NPC_POOL.keys())
    selected_cat = random.choice(all_categories)
    
    return get_npc_by_category(selected_cat)

def get_random_lore():
    """
    Mengambil satu potongan cerita (Lore) secara acak.
    Digunakan saat berinteraksi dengan kategori 'lore_keeper'.
    """
    return random.choice(LORE_STORIES)

def get_npc(npc_id):
    """
    Fungsi fallback jika kamu ingin mencari NPC spesifik berdasarkan ID 
    (Jika ke depannya kamu menambahkan ID unik di npc_data).
    """
    # Mencari di seluruh kategori
    for cat in NPC_POOL:
        for npc in NPC_POOL[cat]:
            if npc.get('id') == npc_id:
                return npc.copy()
    return None
