# game/entities/npcs.py

import random
from game.data import NPC_POOL, LORE_STORIES

def get_npc_by_category(category):
    """Mengambil satu varian NPC secara acak dari kategori tertentu."""
    category_list = NPC_POOL.get(category)
    if not category_list: 
        return None
    npc = random.choice(category_list).copy()
    npc['category'] = category
    return npc

def get_random_npc_event():
    """Mengambil kategori acak, lalu ambil satu NPC di dalamnya."""
    if not NPC_POOL:
        return None
    category = random.choice(list(NPC_POOL.keys()))
    return get_npc_by_category(category)

def get_random_lore():
    """Mengambil satu potongan cerita sejarah secara acak."""
    if not LORE_STORIES:
        return "Tidak ada cerita yang tersisa. Hanya kesunyian."
    return random.choice(LORE_STORIES)

def get_npc(npc_id):
    """
    Mencari NPC spesifik (digunakan jika ada sistem quest/ID).
    Jika tidak ketemu, mengembalikan NPC acak agar game tidak crash.
    """
    for category in NPC_POOL.values():
        for npc in category:
            if npc.get('name') == npc_id:
                return npc.copy()
    return get_random_npc_event()

def resolve_npc_action(npc, player):
    """
    LOGIKA EKSEKUSI NPC (Fungsi yang dicari oleh main.py)
    Menentukan hasil interaksi (Heal, Gold, Lore, dll).
    """
    category = npc.get('category', 'wanderer')
    log = f"**{npc['name']}** menatapmu...\n"
    updates = {}

    # 1. HEALER - Memulihkan HP dengan biaya Gold
    if category == "healer":
        cost = npc.get('base_cost', 15)
        heal = npc.get('base_heal', 30)
        if player.get('gold', 0) >= cost:
            updates['hp'] = min(player.get('max_hp', 100), player.get('hp', 0) + heal)
            updates['gold'] = player.get('gold') - cost
            log += f"💉 {npc['narration']}\n\n*HP bertambah {heal}.*"
        else:
            log += f"💸 {npc['name']} mendengus. 'Emasmu kurang, Weaver. Berdarahlah sedikit lagi.'"

    # 2. LORE KEEPER - Memberi EXP dan Cerita
    elif category == "lore_keeper":
        story = get_random_lore()
        updates['exp'] = player.get('exp', 0) + 100
        updates['max_mp'] = player.get('max_mp', 50) + 2
        log += f"📜 {npc['narration']}\n\n_\"{story}\"_\n\n*Pengetahuanmu bertambah (+100 EXP, +2 Max MP)*"

    # 3. WANDERER - Hadiah Acak
    elif category == "wanderer":
        log += f"🎁 {npc['narration']}"
        if random.random() < 0.5:
            updates['gold'] = player.get('gold', 0) + 50
            log += "\n\n*Ia menjatuhkan koin emas sebelum menghilang.*"
        else:
            updates['hp'] = min(player.get('max_hp', 100), player.get('hp', 0) + 20)
            log += "\n\n*Ia memberimu penawar rasa sakit.*"

    # 4. MERCENARY - Buff ATK Permanen (Sangat Mahal)
    elif category == "mercenary":
        cost = npc.get('base_cost', 100)
        if player.get('gold', 0) >= cost:
            stats = player.get('stats', {})
            stats['p_atk'] = stats.get('p_atk', 10) + 2
            updates['stats'] = stats
            updates['gold'] = player.get('gold') - cost
            log += f"⚔️ {npc['narration']}\n\n*Serangan Fisikmu bertambah +2 secara permanen!*"
        else:
            log += f"🚫 'Latihan ini tidak gratis. Kembali jika kau sudah kaya.'"

    # DEFAULT / FALLBACK
    else:
        log += f"👤 {npc['narration']}\n\n*Tidak terjadi apa-apa, tapi perasaanmu tidak enak.*"

    return updates, log
