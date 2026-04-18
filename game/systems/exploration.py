# game/systems/exploration.py

"""
Sistem Eksplorasi (Exploration System) - ALUR DINAMIS & ENVIRONMENT HAZARDS
Menangani logika pergerakan pemain, trigger event NPC, Puzzle, dan Bahaya Lingkungan.
"""

import random
import time

# Panggilan ke database
from database import get_player, update_player, add_history

# Panggilan ke sistem Entitas & Data
from game.entities.monsters import get_random_mini_boss
from game.entities.npcs import get_random_npc_event
from game.data import NARRATIVES, MONSTER_WARNINGS

# --- KONFIGURASI LOKASI ---
try:
    from database import LOCATIONS
except ImportError:
    LOCATIONS = [
        "The Whispering Hall", "The Forsaken Mire", "The Abyssal Depth", 
        "The Frozen Purgatory", "The Crimson Throne"
    ]

def update_location_if_needed(player):
    """Merotasi lokasi berdasarkan jumlah kill."""
    kills = player.get('kills', 0)
    current_loc = player.get('location', LOCATIONS[0])
    
    loc_idx = min(kills // 5, len(LOCATIONS) - 1)
    new_location = LOCATIONS[loc_idx]
    
    if new_location != current_loc:
        update_player(player['user_id'], {"location": new_location})
        add_history(player['user_id'], f"Menembus batas kewarasan dan memasuki {new_location}.")
        return new_location, True 
        
    return current_loc, False

def check_environment_protection(player, hazard_type):
    """
    Logika Survival: Mengecek apakah pemain punya item pelindung untuk hazard tertentu.
    """
    inventory = player.get('inventory', [])
    equipped = list(player.get('equipped', {}).values())
    all_items = inventory + equipped

    protection_map = {
        "RACUN": "item_masker_gas",
        "DINGIN": "item_mantel_bulu",
        "GELAP": "item_lentera_jiwa"
    }

    required_item = protection_map.get(hazard_type)
    if not required_item:
        return True # Tidak butuh item pelindung khusus
        
    return required_item in all_items

def apply_trap_or_hazard(player, event_type, hazard_type=""):
    """Fungsi Penalti: Memotong HP/Energy jika terkena hazard tanpa pelindung."""
    updates = {}
    current_hp = player.get('hp', 100)
    
    if event_type == "trap":
        dmg = random.randint(10, 25)
        updates["hp"] = max(0, current_hp - dmg)
        
    elif event_type == "hazard":
        # Cek apakah selamat karena punya item pelindung
        if not check_environment_protection(player, hazard_type):
            if hazard_type == "RACUN":
                # Tambahkan status poisoned ke active_effects (Logic combat akan memproses)
                effects = player.get('active_effects', [])
                if not any(e['type'] == 'poison' for e in effects):
                    effects.append({"type": "poison", "value": 5, "icon": "🤢"})
                    updates["active_effects"] = effects
                updates["hp"] = max(0, current_hp - 15)
            elif hazard_type == "DINGIN":
                updates["energy"] = max(0, player.get('energy', 100) - 20)
                updates["hp"] = max(0, current_hp - 5)
            elif hazard_type == "GELAP":
                # Kegelapan menguras kewarasan (MP)
                updates["mp"] = max(0, player.get('mp', 0) - 15)

    if updates:
        update_player(player['user_id'], updates)
    
    return updates

def process_move(user_id):
    """
    The Journey Driver: Mengatur probabilitas event berdasarkan langkah (Step).
    Jalur dipisahkan: Monster, NPC (Fungsional), Puzzle (Chest/Shrine), Environment.
    """
    player = get_player(user_id)
    kills = player.get("kills", 0)
    cycle = player.get("cycle", 1)
    steps = player.get('step_in_cycle', 0) + 1
    current_loc, just_moved = update_location_if_needed(player)
    
    # 1. TRIGGER BOSS UTAMA
    is_boss = False
    if kills > 20: is_boss = True 
    elif kills >= 15 and random.randint(1, 100) <= (kills - 14) * 15: is_boss = True

    if is_boss:
        update_player(user_id, {"step_in_cycle": 0})
        return ("boss", None, f"🌑 **DOMINION OF {current_loc.upper()}**\nSang Penjaga dimensi ini telah bangkit!")

    # Update step counter
    update_player(user_id, {"step_in_cycle": steps, "step_counter": player.get("step_counter", 0) + 1})
    
    # Tentukan hazard berdasarkan lokasi
    loc_hazard = "GELAP" if "Abyss" in current_loc or "Hall" in current_loc else "RACUN" if "Mire" in current_loc else "DINGIN"

    # --- PENENTUAN EVENT BERDASARKAN PROBABILITAS (ROLL) ---
    roll = random.random()

    # FASE 1: PENGENALAN (Langkah 1-10)
    if steps <= 10:
        if roll < 0.15: return ("npc", get_random_npc_event(), "👤 Seseorang berdiri di antara kabut...")
        if roll < 0.40: return ("monster", None, f"👾 {random.choice(MONSTER_WARNINGS)}")
        return ("safe", None, random.choice(NARRATIVES["safe"]))

    # FASE 2: DESPAIR & HAZARDS (Langkah 11-25)
    elif 11 <= steps <= 25:
        # Pengecekan Hazard Lingkungan (Setiap 5 langkah)
        if steps % 5 == 0:
            penalty_applied = apply_trap_or_hazard(player, "hazard", loc_hazard)
            protected = check_environment_protection(player, loc_hazard)
            
            if protected:
                return ("hazard", {"type": loc_hazard, "safe": True}, f"🛡️ Berkat perlengkapanmu, kamu berhasil melewati area {loc_hazard} dengan aman.")
            else:
                return ("hazard", {"type": loc_hazard, "safe": False}, f"⚠️ {NARRATIVES['danger_start'].get(loc_hazard, 'Lingkungan terasa mematikan!')}")

        if roll < 0.15: 
            # EVENT PUZZLE (Chest/Shrine)
            target = random.choice(["chest", "shrine", "monolith"])
            return (target, None, f"✨ Di depanmu terdapat sebuah **{target.upper()}** kuno yang tersegel.")
        
        if roll < 0.35: 
            # TRAP (Jebakan Maut)
            apply_trap_or_hazard(player, "trap")
            return ("deadly", {"type": "trap"}, "🏹 **JEBAKAN!** Mekanisme kuno terpicu saat kau melangkah! (-HP)")
            
        if roll < 0.65: return ("monster", None, f"⚔️ **PENYERGAPAN.** {random.choice(MONSTER_WARNINGS)}")
        
        return ("safe", None, "Lantai bergetar, namun tidak ada yang muncul. Untuk sekarang.")

    # FASE 3: KLIMAKS & MINI BOSS (Langkah 26-30)
    elif 26 <= steps <= 30:
        if steps == 29 and not player.get('miniboss_slain_cycle', False):
            mb = get_random_mini_boss()
            return ("miniboss", {"data": mb}, f"🚨 **PINTU TERKUNCI.**\n{mb['name']} menjaganya dengan nyawa!")
        
        if roll < 0.40: return ("monster", None, "⚔️ Musuh berdatangan tanpa henti!")
        return ("safe", None, "Pintu gerbang terlihat di kejauhan...")

    # FASE 4: REST AREA (31+)
    else:
        update_player(user_id, {'step_in_cycle': 0, 'miniboss_slain_cycle': False})
        return ("rest_area", None, "🏕️ **CAMPFIRE.** Kau rubuh di dekat api unggun. Energi dan jiwamu perlahan pulih.")
