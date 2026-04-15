"""
Sistem Eksplorasi (Exploration System) - ALUR DINAMIS & PSYCHO DREAD
Menangani logika pergerakan pemain dengan The Journey Driver.
Mengatur pembagian Zona, Transisi, Bahaya, dan Rest Area dengan narasi teror psikologis.
"""

import random

# Panggilan ke database
from database import get_player, update_player, narratives_col, LOCATIONS, add_history

# Panggilan ke sistem NPC & Entitas
from game.entities.npcs import get_npc_encounter
from game.entities.bosses import get_random_mini_boss

# === POOL NARASI DINAMIS (PARANOID EDITION) ===
NARRATIVES = {
    "safe": [
        "Jari-jarimu kaku. Tinta mulai masuk ke nadimu setiap kali kau melangkah.",
        "Berapa kali kau berkedip sejak langkah pertama? Sesuatu sedang menghitungnya.",
        "Layar ini terasa hangat. Seperti kulit manusia yang baru saja mati.",
        "Ada suara di belakangmu. Jangan menoleh. Lanjutkan saja.",
        "Kau yakin pintumu di dunia nyata terkunci? Coba dengar engselnya.",
        "Kenapa kau masih di sini? Dunia aslimu perlahan melupakan wajahmu.",
        "Napasmu terdengar berat. Kau tidak sendirian di tempatmu berada sekarang."
    ],
    "transition": [
        "Sstt. Dia sudah di belakangmu. Jangan bergerak terlalu cepat.",
        "Kau dengar suara napas di pundakmu? Jangan matikan layar ini.",
        "Bayanganmu baru saja berbisik. Ia ingin bertukar posisi denganmu.",
        "Jangan berkedip. Saat kau berkedip, ia melompat satu meter lebih dekat."
    ],
    "danger_start": {
        "GELAP": "🌑 **KEGELAPAN TOTAL.** Layar ini mulai menghisap cahaya dari matamu. Ia ada di suatu tempat di sekitarmu.",
        "DINGIN": "❄️ **HAWA MEMBEKU.** Darah di ujung jarimu berhenti mengalir. Kau tidak bisa lari jika kakimu membeku.",
        "RACUN": "🤢 **MIASMA MENYEKIK.** Udara berubah menjadi silet. Bernapaslah perlahan, atau biarkan paru-parumu robek."
    }
}

# Narasi saat trigger monster
MONSTER_WARNINGS = [
    "KAU TERLAMBAT MENOLIH!",
    "IA SUDAH BOSAN BERSEMBUNYI.",
    "GIGINYA SUDAH MENYENTUH KULITMU.",
    "IA MEROBEK LAYARMU SEKARANG."
]

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
        add_history(player['user_id'], f"Menembus batas kewarasan dan memasuki {new_location}.")
        return new_location, True 
        
    return current_loc, False

def process_move(user_id):
    """
    Logika utama pergerakan (Exploration Engine) dengan DRIVER INTENSITAS.
    Membagi perjalanan ke dalam Fase: Paranoia -> Stalking -> Despair -> Klimaks -> Relief.
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
            "dialog": f"Kau sudah bangun? Bodoh sekali. Sejarah di {current_loc} tidak untuk dibaca. Kumpulkan jiwa mereka yang gagal sebelum ia menemukanmu.",
            "requirement": None,
            "is_liar": False
        }
        return ("npc_mission", npc_data, "✨ Teks di dinding perlahan membentuk wajah yang hancur...")

    # 2. TRIGGER BOSS UTAMA (Override semua alur jika syarat kill terpenuhi)
    is_boss = False
    if kills > 20:
        is_boss = True 
    elif kills >= 15:
        if random.randint(1, 100) <= (kills - 14) * 15:
            is_boss = True

    if is_boss:
        update_player(user_id, {"step_in_cycle": 0})
        return ("boss", None, f"🌑 **SELAMAT DATANG DI NERAKA YANG KAU CIPTAKAN.**\nDi ujung {current_loc}, layar ini retak. Sang Penjaga telah tiba!")

    # Update state langkah
    update_player(user_id, {"step_in_cycle": steps, "step_counter": player.get("step_counter", 0) + 1})

    # ==========================================
    # === THE JOURNEY DRIVER (ALUR DINAMIS) ===
    # ==========================================
    
    # FASE 1: PARANOIA (Langkah 1 - 15)
    if steps <= 15:
        roll = random.random()
        if roll < 0.10: # 10% Ketemu Kuburan
            return ("grave", None, "🪦 **NISAN KOSONG.** Liang lahat ini ukurannya sangat pas dengan tubuhmu. Cobalah berbaring.")
        elif roll < 0.15: # 5% Ketemu NPC Lore
            return ("npc_lore", None, "👤 **GEMA KETAKUTAN.** Bayangan yang menyerupai dirimu duduk meringkuk. Ia menangis tanpa suara.")
        elif roll < 0.35: # 20% Monster Lemah
            return ("monster", None, f"👾 {random.choice(MONSTER_WARNINGS)}")
        else: # 65% Jalan Paranoid
            teks = random.choice(NARRATIVES["safe"])
            if just_moved: teks = f"🗺️ **KAU TERJEBAK DI: {current_loc}**\n\n" + teks
            return ("safe", None, teks)

    # FASE 2: STALKING (Langkah 16 - 18)
    elif 16 <= steps <= 18:
        roll = random.random()
        if roll < 0.30:
            return ("monster", None, f"⚔️ {random.choice(MONSTER_WARNINGS)}")
        return ("safe", None, random.choice(NARRATIVES["transition"]))

    # FASE 3: DESPAIR / BAHAYA (Langkah 19 - 30)
    elif 19 <= steps <= 30:
        roll = random.random()
        hazard_type = "GELAP" if "Abyss" in current_loc else "RACUN" if "Mire" in current_loc else "DINGIN"
        
        # Sinyal Hazard Lingkungan setiap 4 langkah di zona bahaya
        if steps % 4 == 0:
            return ("hazard", {"type": hazard_type}, NARRATIVES["danger_start"][hazard_type])
            
        if roll < 0.20: # 20% Trap / Jebakan
            trap_type = random.choice(["tripwire", "acid", "siphon"])
            return ("trap", {"type": trap_type}, "⚠️ **KAU MENGINJAKNYA!** Dinding di sekitarmu tertawa saat rasa sakit itu datang!")
        
        elif roll < 0.35: # 15% Peti Harta
            chest_type = random.choices(["wood", "iron", "sealed"], weights=[60, 30, 10])[0]
            return ("treasure_chest", {"type": chest_type}, f"📦 **HARAPAN PALSU.** Sebuah peti {chest_type} tergeletak. Setiap hadiah di sini dibayar dengan kewarasan.")
        
        elif roll < 0.45: # 10% Patung
            return ("idol", None, "🗿 **BERHALA MATI.** Patung ini tidak punya mata, tapi kau merasa ia sedang menghitung kedipan matamu.")
            
        elif roll < 0.75: # 30% Monster Kuat
            return ("monster", None, f"⚔️ **PENYERGAPAN.** {random.choice(MONSTER_WARNINGS)}")
            
        else: # 25% Teror Bayangan
            return ("safe", None, "Jalanan kosong. Tapi layar ini berdenyut. Ia tahu kau ketakutan.")

    # FASE 4: KLIMAKS (Langkah 31 - 35)
    elif 31 <= steps <= 35:
        has_slain_miniboss = player.get('miniboss_slain_cycle', False)
        if steps == 34 and not has_slain_miniboss:
            update_player(user_id, {"miniboss_slain_cycle": True})
            miniboss_name = get_random_mini_boss()
            return ("miniboss", {"name": miniboss_name}, f"🚨 **PINTU TERTUTUP.**\n{miniboss_name} menghalangimu. Buktikan kau layak hidup!")
            
        roll = random.random()
        if roll < 0.40:
            return ("trap", {"type": "tripwire"}, "🏹 **KAU TIDAK BISA LARI!** Jebakan penghabisan terpicu di bawah kakimu!")
        return ("safe", None, "Cahaya api di kejauhan. Seret kakimu. Jangan menyerah sekarang.")

    # FASE 5: RELIEF / REST AREA (Langkah 36)
    else:
        update_player(user_id, {'step_in_cycle': 0, 'miniboss_slain_cycle': False})
        return ("rest_area", None, "🏕️ **CAMPFIRE.** Kau rubuh di dekat api unggun. Untuk sementara waktu... kau selamat dari dirimu sendiri.")
