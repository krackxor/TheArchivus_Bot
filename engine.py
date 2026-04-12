import random
from database import get_player, update_player, narratives_col
from generators import generate_npc

def get_random_narration(category):
    """Mengambil satu naskah acak dari koleksi narasi berdasarkan kategori."""
    result = narratives_col.aggregate([
        {"$match": {"category": category}},
        {"$sample": {"size": 1}}
    ])
    
    try:
        nodes = list(result)
        if nodes:
            return nodes[0]['text']
        else:
            return "Kamu melangkah menembus kabut Archivus yang pekat..."
    except Exception as e:
        print(f"[ERROR] Gagal mengambil narasi: {e}")
        return "Langkahmu bergema di lorong yang sunyi."

def process_move(user_id):
    """
    Logika utama pergerakan Weaver.
    Mendukung Fase Early, Mid, dan Late Game berdasarkan Gold.
    """
    player = get_player(user_id)
    gold = player.get("gold", 0)
    new_steps = player.get("step_counter", 0) + 1
    trigger_event = False
    
    # --- LOGIKA PELUANG EVENT ---
    # Jika Gold tinggi (Late Game), peluang bertemu monster/event meningkat lebih cepat
    step_limit = 10 if gold >= 800 else 15
    
    if new_steps >= 2:
        chance = (new_steps / step_limit) * 100 
        if random.randint(1, 100) <= chance or new_steps >= step_limit:
            trigger_event = True

    if trigger_event:
        update_player(user_id, {"step_counter": 0})
        event_roll = random.random()
        
        # 1. Event NPC (70% peluang gabungan)
        if event_roll < 0.70:
            is_liar = random.choice([True, False])
            event_type = "npc_jahat" if is_liar else "npc_baik"
            narasi = get_random_narration("npc_event")
            
            # Kirim player_gold agar NPC menyesuaikan permintaannya (Early/Mid/Late)
            npc_data = generate_npc(player_gold=gold, is_liar=is_liar)
            return (event_type, npc_data, narasi)
        
        # 2. Event Monster (30% peluang)
        else: 
            narasi = get_random_narration("monster_event")
            return ("monster", None, narasi)

    else:
        update_player(user_id, {"step_counter": new_steps})
        narasi_aman = get_random_narration("safe_travel")
        return ("safe", None, narasi_aman)
