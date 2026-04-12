import random
from database import get_player, update_player, narratives_col
from generators import generate_npc

def get_random_narration(category):
    """
    Mengambil satu naskah acak dari koleksi narasi berdasarkan kategori.
    Jika database kosong, akan mengembalikan pesan default.
    """
    # Mencari narasi acak menggunakan agregasi MongoDB
    result = narratives_col.aggregate([
        {"$match": {"category": category}},
        {"$sample": {"size": 1}}
    ])
    
    try:
        nodes = list(result)
        if nodes:
            return nodes[0]['text']
        else:
            # Fallback jika kategori belum ada isinya
            return "Kamu melangkah menembus kabut Archivus yang pekat..."
    except Exception as e:
        print(f"[ERROR] Gagal mengambil narasi: {e}")
        return "Langkahmu bergema di lorong yang sunyi."

def process_move(user_id):
    """
    Logika utama pergerakan Weaver.
    Menentukan apakah pemain bertemu monster, NPC, atau area aman.
    """
    player = get_player(user_id)
    # Tambah counter langkah (tersembunyi dari user)
    new_steps = player.get("step_counter", 0) + 1
    trigger_event = False
    
    # Peluang munculnya event meningkat seiring jumlah langkah
    if new_steps >= 3:
        # Kalkulasi peluang (persentase)
        chance = (new_steps / 15.0) * 100 
        if random.randint(1, 100) <= chance or new_steps >= 15:
            trigger_event = True

    if trigger_event:
        # Reset langkah jika event terjadi
        update_player(user_id, {"step_counter": 0})
        event_roll = random.random()
        
        # 1. Event NPC Baik (35% peluang)
        if event_roll < 0.35: 
            narasi = get_random_narration("npc_event")
            return ("npc_baik", generate_npc(is_liar=False), narasi)
        
        # 2. Event NPC Jahat/Penipu (35% peluang)
        elif event_roll < 0.70: 
            narasi = get_random_narration("npc_event")
            return ("npc_jahat", generate_npc(is_liar=True), narasi)
        
        # 3. Event Monster (30% peluang)
        else: 
            narasi = get_random_narration("monster_event")
            return ("monster", None, narasi)

    else:
        # Update jumlah langkah di database
        update_player(user_id, {"step_counter": new_steps})
        
        # Kembalikan narasi perjalanan aman
        narasi_aman = get_random_narration("safe_travel")
        return ("safe", None, narasi_aman)
