# game/systems/exploration.py

"""
Sistem Eksplorasi (Exploration System) - ALUR DINAMIS & PSYCHO DREAD
Menangani logika pergerakan pemain dengan The Journey Driver.
Struktur: Satu pintu untuk Monster & Boss.
"""

import random
import time

# Panggilan ke database (Pastikan file database.py ada di root atau folder yang benar)
from database import get_player, update_player, add_history

# Panggilan ke sistem Entitas (Sesuai struktur baru: Satu Pintu)
from game.entities.monsters import get_random_monster, get_random_mini_boss
from game.entities.npcs import get_random_npc_event, get_random_lore

# Ambil data narasi dari pusat data
from game.data import NARRATIVES, MONSTER_WARNINGS

try:
    from database import LOCATIONS
except ImportError:
    LOCATIONS = [
        "The Whispering Hall", "The Forsaken Mire", "The Abyssal Depth", 
        "The Frozen Purgatory", "The Crimson Throne"
    ]

def update_location_if_needed(player):
    """Merotasi lokasi berdasarkan jumlah kill. Semakin tinggi, semakin dalam."""
    kills = player.get('kills', 0)
    current_loc = player.get('location', LOCATIONS[0])
    
    loc_idx = min(kills // 5, len(LOCATIONS) - 1)
    new_location = LOCATIONS[loc_idx]
    
    if new_location != current_loc:
        update_player(player['user_id'], {"location": new_location})
        add_history(player['user_id'], f"Menembus batas kewarasan dan memasuki {new_location}.")
        return new_location, True 
        
    return current_loc, False

def apply_trap_or_hazard(player, event_type, hazard_type=""):
    """Fungsi cerdas: Otomatis memotong HP atau memberi status jika kena jebakan."""
    updates = {}
    current_hp = player.get('hp', 100)
    debuffs = player.get('debuffs', [])

    if event_type == "trap":
        dmg = random.randint(10, 25)
        updates["hp"] = max(0, current_hp - dmg)
        
    elif event_type == "hazard":
        if hazard_type == "RACUN" and "poisoned" not in debuffs:
            debuffs.append("poisoned")
            updates["debuffs"] = debuffs
        elif hazard_type == "DINGIN":
            updates["energy"] = max(0, player.get('energy', 100) - 10)
        elif hazard_type == "GELAP" and "dizzy" not in debuffs:
            debuffs.append("dizzy")
            updates["debuffs"] = debuffs

    if updates:
        update_player(player['user_id'], updates)


def process_move(user_id):
    player = get_player(user_id)
    kills = player.get("kills", 0)
    cycle = player.get("cycle", 1)
    
    steps = player.get('step_in_cycle', 0) + 1
    current_loc, just_moved = update_location_if_needed(player)
    
    # 1. TRIGGER MISI AWAL (Tutorial/Lore Start)
    if player.get("step_counter", 0) == 0 and kills == 0 and cycle == 1:
        update_player(user_id, {"step_counter": 1, "step_in_cycle": 1})
        return ("npc_mission", {"identity": "The Last Chronicler"}, "✨ Teks di dinding perlahan membentuk wajah yang hancur...")

    # 2. TRIGGER BOSS UTAMA (Main Boss)
    is_boss = False
    if kills > 20: is_boss = True 
    elif kills >= 15 and random.randint(1, 100) <= (kills - 14) * 15: is_boss = True

    if is_boss:
        update_player(user_id, {"step_in_cycle": 0})
        return ("boss", None, f"🌑 **SELAMAT DATANG DI NERAKA YANG KAU CIPTAKAN.**\nSang Penjaga telah tiba!")

    # Update step counter pemain
    update_player(user_id, {"step_in_cycle": steps, "step_counter": player.get("step_counter", 0) + 1})
    
    # FASE 1: PARANOIA (Langkah 1 - 15)
    if steps <= 15:
        roll = random.random()
        if roll < 0.10: 
            return ("grave", None, "🪦 **NISAN KOSONG.** Liang lahat ini pas dengan tubuhmu.")
        elif roll < 0.15: 
            npc = get_random_npc_event()
            return ("npc", npc, f"👤 **KONTAK.** {npc['name']} muncul dari kegelapan.")
        elif roll < 0.35: 
            return ("monster", None, f"👾 {random.choice(MONSTER_WARNINGS)}")
        else: 
            teks = random.choice(NARRATIVES["safe"])
            if just_moved: teks = f"🗺️ **KAU TERJEBAK DI: {current_loc}**\n\n" + teks
            return ("safe", None, teks)

    # FASE 2: STALKING (Langkah 16 - 18)
    elif 16 <= steps <= 18:
        if random.random() < 0.30: 
            return ("monster", None, f"⚔️ {random.choice(MONSTER_WARNINGS)}")
        return ("safe", None, random.choice(NARRATIVES["transition"]))

    # FASE 3: DESPAIR / BAHAYA (Langkah 19 - 30)
    elif 19 <= steps <= 30:
        roll = random.random()
        hazard_type = "GELAP" if "Abyss" in current_loc else "RACUN" if "Mire" in current_loc else "DINGIN"
        
        if steps % 4 == 0:
            apply_trap_or_hazard(player, "hazard", hazard_type)
            return ("hazard", {"type": hazard_type}, NARRATIVES["danger_start"][hazard_type])
            
        if roll < 0.20:
            apply_trap_or_hazard(player, "trap")
            return ("trap", {"type": random.choice(["tripwire", "acid", "siphon"])}, "⚠️ **KAU MENGINJAKNYA!** Dinding tertawa saat rasa sakit merobek kulitmu! (-HP)")
        elif roll < 0.35:
            chest = random.choices(["wood", "iron", "sealed"], weights=[60, 30, 10])[0]
            return ("treasure_chest", {"type": chest}, f"📦 **HARAPAN PALSU.** Sebuah peti {chest} tergeletak.")
        elif roll < 0.45: 
            return ("idol", None, "🗿 **BERHALA MATI.** Patung ini sedang menghitung kedipan matamu.")
        elif roll < 0.75: 
            return ("monster", None, f"⚔️ **PENYERGAPAN.** {random.choice(MONSTER_WARNINGS)}")
        else: 
            return ("safe", None, "Jalanan kosong. Tapi layar ini berdenyut. Ia tahu kau ketakutan.")

    # FASE 4: KLIMAKS (Langkah 31 - 35)
    elif 31 <= steps <= 35:
        if steps == 34 and not player.get('miniboss_slain_cycle', False):
            # Penting: Mengambil dari monsters.py bukan bosses/ folder
            mb = get_random_mini_boss()
            mb_name = mb.get("name", "Elite Enemy") if isinstance(mb, dict) else "Mini Boss"
            return ("miniboss", {"data": mb}, f"🚨 **PINTU TERTUTUP.**\n{mb_name} menghalangimu!")
            
        if random.random() < 0.40:
            apply_trap_or_hazard(player, "trap")
            return ("trap", {"type": "tripwire"}, "🏹 **KAU TIDAK BISA LARI!** Jebakan terpicu di bawah kakimu! (-HP)")
            
        return ("safe", None, "Cahaya api di kejauhan. Seret kakimu. Jangan menyerah sekarang.")

    # FASE 5: RELIEF (36+)
    else:
        update_player(user_id, {'step_in_cycle': 0, 'miniboss_slain_cycle': False})
        return ("rest_area", None, "🏕️ **CAMPFIRE.** Kau rubuh di dekat api unggun. Untuk sementara waktu... kau selamat.")
