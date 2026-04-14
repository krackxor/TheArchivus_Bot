"""
Sistem Eksplorasi (Exploration System)
Menangani logika pergerakan pemain, transisi wilayah (Biomes), 
sistem atmosfer/cuaca, dan pemicu kejadian (Encounter Triggers).
Terintegrasi penuh dengan sistem Bos dan Mini-Bos.
"""

import random

# Panggilan ke database
from database import get_player, update_player, narratives_col, LOCATIONS, add_history

# Panggilan ke sistem NPC & Entitas
from game.entities.npcs import get_npc_encounter
from game.entities.bosses import get_random_mini_boss

def get_atmosphere(location_name):
    """
    Menghasilkan efek suasana/cuaca dinamis berdasarkan lokasi saat ini 
    agar teks eksplorasi tidak membosankan.
    """
    atmospheres = {
        "Gerbang Awal": [
            "Kabut tipis menyapu pergelangan kakimu.",
            "Udara terasa dingin dan asing di sini.",
            "Keheningan hanya dipecahkan oleh suara langkahmu sendiri."
        ],
        "Lorong Memori": [
            "Bisikan masa lalu terdengar samar dari balik dinding.",
            "Bayangan dari Weaver terdahulu tampak sekilas lalu menghilang.",
            "Kertas-kertas perkamen tua berterbangan tertiup angin hampa."
        ],
        "Perpustakaan Kelam": [
            "Aroma buku tua dan tinta kering tercium tajam.",
            "Lilin-lilin kebiruan menyala redup tanpa mengeluarkan panas.",
            "Rak-rak raksasa menjulang tinggi hingga tak terlihat ujungnya."
        ],
        "Labirin Waktu": [
            "Detak jam raksasa bergema menggetarkan lantai pijakanmu.",
            "Ruang dan waktu terasa terdistorsi di area ini.",
            "Langkahmu terasa lebih lambat, seolah waktu menahanmu."
        ],
        "Pusat Kehampaan": [
            "Kegelapan absolut. Hanya insting yang menuntunmu.",
            "Gravitasi terasa tidak stabil, debu-debu melayang ke atas.",
            "Udara terasa berat, seolah dimensi ini menolak kehadiranmu."
        ]
    }
    
    # Ambil suasana berdasarkan lokasi, jika lokasi belum terdaftar, pakai default
    safe_atmospheres = atmospheres.get(location_name, ["Kabut menyelimuti jalanmu..."])
    return random.choice(safe_atmospheres)

def get_random_narration(category):
    """Mengambil satu naskah acak dari koleksi narasi MongoDB berdasarkan kategori."""
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
    """Merotasi lokasi berdasarkan jumlah kill. Semakin tinggi, semakin dalam."""
    kills = player.get('kills', 0)
    current_loc = player.get('location', LOCATIONS[0] if LOCATIONS else "Dimensi Awal")
    
    if not LOCATIONS:
        return current_loc, False

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
    Logika utama pergerakan (Exploration Engine).
    Menentukan apakah pemain bertemu Monster, Bos, NPC, atau Jalan Aman.
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

    # Variabel penghitung langkah
    steps_since = player.get("steps_since_event", 0) + 1
    new_steps_total = player.get("step_counter", 0) + 1

    # 3. TRIGGER BOSS UTAMA (Kill-Based: Setelah 15-20 kill)
    is_boss = False
    if kills > 20:
        is_boss = True 
    elif kills >= 15:
        chance = (kills - 14) * 15 
        if random.randint(1, 100) <= chance:
            is_boss = True

    if is_boss:
        update_player(user_id, {"steps_since_event": 0})
        # main.py mengharapkan string "boss"
        return ("boss", None, f"🌑 **UDARA MEMBEKU.**\nDi ujung {current_loc}, kabut membentuk siluet raksasa. Sang Penjaga telah tiba!")

    # 4. TRIGGER MINI BOSS (Area Kill 7-9 atau monster_streak)
    # Kita menggunakan kombinasi kill count ATAU monster streak (untuk memastikan mereka muncul di mid-game)
    monster_streak = player.get('monster_streak', 0)
    has_slain_miniboss = player.get('miniboss_slain', False)
    
    if (kills in [7, 8, 9] or monster_streak >= 7) and not has_slain_miniboss:
        update_player(user_id, {"steps_since_event": 0, "miniboss_slain": True})
        miniboss_name = get_random_mini_boss()
        
        # main.py mengharapkan string "miniboss" (tanpa garis bawah)
        return ("miniboss", {"name": miniboss_name}, f"🚨 **AURA MENCEKAM.**\n{miniboss_name} menghalangi jalanmu di {current_loc}. Kalahkan elit ini untuk maju!")

    # 5. REGULAR ENCOUNTER (Monster / NPC)
    trigger_threshold = random.randint(3, 5) # Butuh 3-5 langkah sebelum ketemu sesuatu
    
    if steps_since >= trigger_threshold:
        update_player(user_id, {"steps_since_event": 0, "step_counter": new_steps_total})
        
        event_roll = random.random()
        
        # 60% Ketemu Monster Biasa, 40% Ketemu NPC
        if event_roll < 0.60:
            # Tambah monster streak setiap kali ketemu monster biasa
            update_player(user_id, {"monster_streak": monster_streak + 1})
            return ("monster", None, get_random_narration("monster_event"))
        else:
            # Memanggil sistem NPC
            npc_encounter = get_npc_encounter(cycle)
            
            # Map tipe NPC untuk main.py
            if npc_encounter['type'] == 'trickster':
                event_type = "npc_jahat"
            elif npc_encounter['type'] == 'scholar':
                event_type = "npc_quiz"
            else:
                event_type = "npc_baik"
            
            return (event_type, npc_encounter, get_random_narration("npc_event"))
            
    # 6. JALAN KOSONG / AMAN (Safe Travel)
    else:
        update_player(user_id, {"steps_since_event": steps_since, "step_counter": new_steps_total})
        
        # Gabungkan narasi dari database dengan atmosfer dinamis
        narasi_aman = get_random_narration("safe_travel")
        atmosfer = get_atmosphere(current_loc)
        
        teks_final = f"*{atmosfer}*\n\n{narasi_aman}"
        
        if just_moved:
            teks_final = f"🗺️ **LOKASI BARU: {current_loc}**\n\n" + teks_final
            
        return ("safe", None, teks_final)
