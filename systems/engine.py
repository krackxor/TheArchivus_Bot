import random
from database import get_player, update_player, narratives_col, LOCATIONS, add_history
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

def update_location_if_needed(player):
    """Merotasi lokasi berdasarkan jumlah kill. Semakin banyak kill, semakin dalam masuk ke Archivus."""
    kills = player.get('kills', 0)
    current_loc = player.get('location')
    
    # Pindah wilayah setiap kelipatan 5 kill
    loc_idx = min(kills // 5, len(LOCATIONS) - 1)
    new_location = LOCATIONS[loc_idx]
    
    if new_location != current_loc:
        update_player(player['user_id'], {"location": new_location})
        add_history(player['user_id'], f"Menembus gerbang dan memasuki {new_location}.")
        return new_location, True # True berarti ada perpindahan lokasi
    return current_loc, False

def process_move(user_id):
    """
    Logika utama pergerakan Endless RPG Weaver.
    Trigger berdasarkan KILLS dan STEPS.
    """
    player = get_player(user_id)
    kills = player.get("kills", 0)
    cycle = player.get("cycle", 1)
    
    # 1. CEK PERPINDAHAN LOKASI
    current_loc, just_moved = update_location_if_needed(player)
    
    # 2. TRIGGER NPC MISI (Hanya di langkah pertama siklus pertama)
    if player.get("step_counter", 0) == 0 and kills == 0 and cycle == 1:
        update_player(user_id, {"step_counter": 1})
        npc_data = {
            "identity": "The Last Chronicler",
            "dialog": f"Weaver... sejarah di {current_loc} mulai terhapus. Kumpulkan jiwa monster untuk memancing Sang Penjaga keluar dari persembunyiannya.",
            "requirement": None,
            "is_liar": False
        }
        return ("npc_mission", npc_data, "Sebuah proyeksi cahaya muncul di hadapanmu...")

    # Variabel penghitung langkah sejak event terakhir
    steps_since = player.get("steps_since_event", 0) + 1
    new_steps_total = player.get("step_counter", 0) + 1

    # 3. TRIGGER BOSS (Kill-Based)
    is_boss = False
    if kills > 20:
        is_boss = True # Wajib Boss jika lebih dari 20 kill
    elif kills >= 15:
        # Peluang Boss naik bertahap setelah 15 kill (15%, 30%, 45%...)
        chance = (kills - 14) * 15 
        if random.randint(1, 100) <= chance:
            is_boss = True

    if is_boss:
        update_player(user_id, {"steps_since_event": 0})
        return ("boss", None, f"🌑 **UDARA MEMBEKU.**\nDi ujung {current_loc}, kabut membentuk siluet raksasa. Sang Penjaga telah tiba!")

    # 4. TRIGGER MINI BOSS (Area Kill 7-9)
    if kills in [7, 8, 9] and not player.get('miniboss_slain', False):
        update_player(user_id, {"steps_since_event": 0, "miniboss_slain": True})
        return ("mini_boss", None, f"⚔️ **JALAN TERTUTUP.**\nSeekor letnan kegelapan menghalangimu di {current_loc}. Kalahkan dia untuk lanjut!")

    # 5. REGULAR TRIGGER (Monster, NPC Baik, Jahat, Quiz)
    trigger_threshold = random.randint(3, 5) # Acak antara 3-5 langkah hampa
    
    if steps_since >= trigger_threshold:
        update_player(user_id, {"steps_since_event": 0, "step_counter": new_steps_total})
        
        event_roll = random.random()
        
        # 60% Ketemu Monster Biasa, 40% Ketemu NPC
        if event_roll < 0.60:
            return ("monster", None, get_random_narration("monster_event"))
        else:
            # Undi jenis NPC
            npc_type = random.choices(
                ["npc_baik", "npc_jahat", "npc_quiz"], 
                weights=[40, 40, 20], # Quiz lebih jarang muncul
                k=1
            )[0]
            
            is_liar = (npc_type == "npc_jahat")
            
            if npc_type == "npc_quiz":
                # Kita akan modifikasi generators.py untuk quiz nanti
                npc_data = generate_npc(player_gold=player.get("gold", 0), is_liar=False) 
            else:
                npc_data = generate_npc(player_gold=player.get("gold", 0), is_liar=is_liar)
                
            return (npc_type, npc_data, get_random_narration("npc_event"))
            
    # 6. JALAN KOSONG / AMAN
    else:
        update_player(user_id, {"steps_since_event": steps_since, "step_counter": new_steps_total})
        
        narasi_aman = get_random_narration("safe_travel")
        if just_moved:
            narasi_aman = f"🗺️ **LOKASI BARU: {current_loc}**\n" + narasi_aman
            
        return ("safe", None, narasi_aman)
