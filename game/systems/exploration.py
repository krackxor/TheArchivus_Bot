"""
Sistem Eksplorasi (Exploration System) - ALUR DINAMIS
Menangani logika pergerakan pemain dengan The Journey Driver.
Mengatur pembagian Zona Aman, Transisi, Bahaya, dan Rest Area.
"""

import random

# Panggilan ke database
from database import get_player, update_player, narratives_col, LOCATIONS, add_history

# Panggilan ke sistem NPC & Entitas
from game.entities.npcs import get_npc_encounter
from game.entities.bosses import get_random_mini_boss

# === POOL NARASI DINAMIS ===
NARRATIVES = {
    "safe": [
        "Langkahmu bergema di antara pilar batu yang menjulang tinggi. Keheningan di sini terasa begitu nyata.",
        "Angin sepoi-sepoi membawa aroma kertas tua dan debu bintang. Sejauh mata memandang, hanya ada lorong yang tenang.",
        "Kamu melewati reruntuhan perpustakaan terapung. Kitab-kitab tanpa nama melayang diam, seolah menghormati perjalananmu.",
        "Cahaya temaram dari kristal di langit-langit menyinari jalanmu. Untuk sejenak, dunia ini terasa damai."
    ],
    "transition": [
        "Suasana mulai berubah. Udara yang tadinya tenang kini terasa berat dan menyesakkan.",
        "Kamu merasakan firasat buruk. Bulu kudukmu berdiri saat melihat bayangan aneh di ujung koridor.",
        "Bau anyir belerang dan logam berkarat mulai tercium. Wilayah di depanmu tampak tidak bersahabat.",
        "Keheningan berganti dengan suara bisikan parau yang berasal dari celah-celah dinding."
    ],
    "danger_start": {
        "GELAP": "🌑 **KEGELAPAN TOTAL.** Cahaya seolah terserap oleh dinding. Tanpa obor, kamu hanya bisa meraba-raba.",
        "DINGIN": "❄️ **HAWA MEMBEKU.** Embun beku mulai menutupi senjatamu. Tubuhmu menggigil hebat tanpa perlindungan.",
        "RACUN": "🤢 **MIASMA BERACUN.** Kabut hijau pekat merayap di lantai, mencari celah untuk masuk ke paru-parumu."
    }
}

def update_location_if_needed(player):
    """Merotasi lokasi berdasarkan jumlah kill. Semakin tinggi, semakin dalam."""
    kills = player.get('kills', 0)
    current_loc = player.get('location', LOCATIONS[0] if LOCATIONS else "The Whispering Hall")
    
    if not LOCATIONS:
        return current_loc, False

    # Pindah wilayah setiap kelipatan 5 kill
    loc_idx = min(kills // 5, len(LOCATIONS) - 1)
    new_location = LOCATIONS[loc_idx]
    
    if new_location != current_loc:
        update_player(player['user_id'], {"location": new_location})
        add_history(player['user_id'], f"Menembus gerbang dan memasuki {new_location}.")
        return new_location, True 
        
    return current_loc, False

def process_move(user_id):
    """
    Logika utama pergerakan (Exploration Engine) dengan DRIVER INTENSITAS.
    Membagi perjalanan ke dalam Fase: Tenang -> Transisi -> Bahaya -> Klimaks -> Istirahat.
    """
    player = get_player(user_id)
    kills = player.get("kills", 0)
    cycle = player.get("cycle", 1)
    
    # Counter langkah dalam satu siklus (reset setiap sampai Rest Area)
    steps = player.get('step_in_cycle', 0) + 1
    current_loc, just_moved = update_location_if_needed(player)
    
    # 1. TRIGGER MISI AWAL (Hanya langkah pertama di game)
    if player.get("step_counter", 0) == 0 and kills == 0 and cycle == 1:
        update_player(user_id, {"step_counter": 1, "step_in_cycle": 1})
        npc_data = {
            "identity": "The Last Chronicler",
            "dialog": f"Weaver... sejarah di {current_loc} mulai terhapus. Kumpulkan jiwa monster untuk memancing Sang Penjaga keluar dari persembunyiannya.",
            "requirement": None,
            "is_liar": False
        }
        return ("npc_mission", npc_data, "✨ Sebuah proyeksi cahaya muncul di hadapanmu...")

    # 2. TRIGGER BOSS UTAMA (Override semua alur jika syarat kill terpenuhi)
    is_boss = False
    if kills > 20:
        is_boss = True 
    elif kills >= 15:
        if random.randint(1, 100) <= (kills - 14) * 15:
            is_boss = True

    if is_boss:
        update_player(user_id, {"step_in_cycle": 0})
        return ("boss", None, f"🌑 **UDARA MEMBEKU.**\nDi ujung {current_loc}, kabut membentuk siluet raksasa. Sang Penjaga telah tiba!")

    # Update state langkah
    update_player(user_id, {"step_in_cycle": steps, "step_counter": player.get("step_counter", 0) + 1})

    # ==========================================
    # === THE JOURNEY DRIVER (ALUR DINAMIS) ===
    # ==========================================
    
    # FASE 1: TENANG (Langkah 1 - 15)
    if steps <= 15:
        roll = random.random()
        if roll < 0.10: # 10% Ketemu Kuburan (Restore MP)
            return ("grave", None, "🪦 **NISAN TUA.** Sebuah kuburan Weaver terdahulu berdiri kesepian, memancarkan aura biru yang menenangkan.")
        elif roll < 0.15: # 5% Ketemu NPC Lore
            return ("npc_lore", None, "👤 **GEMA MEMORI.** Sesosok bayangan transparan duduk bersila di tengah jalan. Ia tampak ingin menceritakan sesuatu.")
        elif roll < 0.35: # 20% Monster Lemah
            return ("monster", None, "👾 Sesosok bayangan merayap keluar dari balik reruntuhan!")
        else: # 65% Jalan Aman
            teks = random.choice(NARRATIVES["safe"])
            if just_moved: teks = f"🗺️ **LOKASI BARU: {current_loc}**\n\n" + teks
            return ("safe", None, teks)

    # FASE 2: TRANSISI (Langkah 16 - 18)
    elif 16 <= steps <= 18:
        roll = random.random()
        if roll < 0.30:
            return ("monster", None, "⚔️ Makhluk buas menghadangmu di perbatasan zona!")
        return ("safe", None, random.choice(NARRATIVES["transition"]))

    # FASE 3: BAHAYA / DANGER (Langkah 19 - 30)
    elif 19 <= steps <= 30:
        roll = random.random()
        hazard_type = "GELAP" if "Abyss" in current_loc else "RACUN" if "Mire" in current_loc else "DINGIN"
        
        # Sinyal Hazard Lingkungan setiap 4 langkah di zona bahaya
        if steps % 4 == 0:
            return ("hazard", {"type": hazard_type}, NARRATIVES["danger_start"][hazard_type])
            
        if roll < 0.20: # 20% Trap / Jebakan
            trap_type = random.choice(["tripwire", "acid", "siphon"])
            return ("trap", {"type": trap_type}, "⚠️ **MEKANISME TERPICU!** Kamu mendengar suara aneh di bawah kakimu!")
        
        elif roll < 0.35: # 15% Peti Harta (Risk/Reward)
            chest_type = random.choices(["wood", "iron", "sealed"], weights=[60, 30, 10])[0]
            return ("treasure_chest", {"type": chest_type}, f"📦 **HARTA TERSEMBUNYI.** Di tengah bahaya ini, sebuah peti {chest_type} tampak menggoda untuk dibuka.")
        
        elif roll < 0.45: # 10% Patung Sembahan (Buff/Cursed)
            return ("idol", None, "🗿 **PATUNG KUNO.** Sebuah patung batu raksasa memegang mangkuk persembahan. Aura magis menguar darinya.")
            
        elif roll < 0.75: # 30% Monster Kuat
            return ("monster", None, "⚔️ **PENJAGA WILAYAH.** Monster di sini jauh lebih buas dan agresif!")
            
        else: # 25% Jalan Kosong (Tapi menegangkan)
            return ("safe", None, "Jalanan kosong, namun instingmu mengatakan ada sesuatu yang mengintaimu dalam gelap...")

    # FASE 4: KLIMAKS & GATEKEEPER (Langkah 31 - 35)
    elif 31 <= steps <= 35:
        # Mini-Boss wajib muncul di akhir fase ini jika belum dikalahkan
        has_slain_miniboss = player.get('miniboss_slain_cycle', False)
        if steps == 34 and not has_slain_miniboss:
            update_player(user_id, {"miniboss_slain_cycle": True})
            miniboss_name = get_random_mini_boss()
            return ("miniboss", {"name": miniboss_name}, f"🚨 **AURA MENCEKAM.**\n{miniboss_name} menghalangi jalan menuju tempat peristirahatan!")
            
        roll = random.random()
        if roll < 0.40:
            return ("trap", {"type": "tripwire"}, "🏹 **JEBAKAN TERAKHIR!** Dinding di sekitarmu mulai menembakkan anak panah!")
        return ("safe", None, "Kamu bisa melihat pendar cahaya api unggun di kejauhan. Bertahanlah sedikit lagi!")

    # FASE 5: RELIEF / REST AREA (Langkah 36)
    else:
        # Reset counter langkah untuk siklus berikutnya
        update_player(user_id, {'step_in_cycle': 0, 'miniboss_slain_cycle': False})
        return ("rest_area", None, "🏕️ **CAMPFIRE.** Kamu sampai di perkemahan pengembara. Hawa hangat menyambutmu, dan bahaya tertinggal di belakang.")
