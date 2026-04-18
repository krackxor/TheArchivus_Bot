# game/systems/exploration.py

"""
Sistem Eksplorasi (Exploration System) - ALUR DINAMIS & ENVIRONMENT HAZARDS
Menangani logika pergerakan pemain, trigger event NPC, Puzzle, dan Bahaya Lingkungan.
"""

import random
import time

# Panggilan ke database
from database import get_player, update_player, add_history

# Panggilan ke sistem Data & Lingkungan
from game.entities.monsters import get_random_mini_boss
from game.data import NARRATIVES, MONSTER_WARNINGS
from game.data.environment import hazards, deadly, landmarks
from game.data.npcs import functional, storytellers, guides, requesters

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
    
    # Ganti area setiap 5-10 kills
    loc_idx = min(kills // 10, len(LOCATIONS) - 1)
    new_location = LOCATIONS[loc_idx]
    
    if new_location != current_loc:
        update_player(player['user_id'], {"location": new_location})
        add_history(player['user_id'], f"Menembus batas kewarasan dan memasuki {new_location}.")
        return new_location, True 
        
    return current_loc, False

def check_environment_protection(player, hazard_id):
    """
    Logika Survival: Mengecek apakah pemain punya item pelindung untuk hazard tertentu.
    """
    hazard_data = hazards.get_hazard_data(hazard_id)
    if not hazard_data:
        return True

    required_item = hazard_data.get('required_item')
    inventory = player.get('inventory', [])
    equipped = list(player.get('equipped', {}).values())
    
    return required_item in inventory or required_item in equipped

def apply_hazard_penalty(player, hazard_id):
    """Fungsi Penalti: Memproses dampak negatif dari lingkungan (dengan Durasi)."""
    hazard_data = hazards.get_hazard_data(hazard_id)
    if not hazard_data:
        return {}
        
    penalty = hazard_data.get('penalty', {})
    updates = {}
    
    # 1. HP Loss
    if 'hp_loss' in penalty:
        updates['hp'] = max(0, player.get('hp', 100) - penalty['hp_loss'])
    
    # 2. Energy Loss
    if 'energy_loss' in penalty:
        updates['energy'] = max(0, player.get('energy', 100) - penalty['energy_loss'])
        
    # 3. Status Effects (Poison, etc) dengan durasi 3 putaran
    if 'status_effect' in penalty:
        effects = player.get('active_effects', [])
        eff_type = penalty['status_effect']
        if not any(e.get('type') == eff_type for e in effects):
            effects.append({
                "type": eff_type, 
                "value": penalty.get('effect_val', 5), 
                "duration": 3, # Durasi 3 giliran agar tidak bocor selamanya
                "icon": "🤢" if eff_type == "poison" else "❄️"
            })
            updates['active_effects'] = effects
            
    if updates:
        update_player(player['user_id'], updates)
    return updates

def process_move(user_id):
    """
    The Journey Driver: Mengatur probabilitas event berdasarkan langkah (Step).
    """
    player = get_player(user_id)
    kills = player.get("kills", 0)
    steps = player.get('step_in_cycle', 0) + 1
    current_loc, just_moved = update_location_if_needed(player)
    
    # 1. TRIGGER BOSS UTAMA (Threshold Kills)
    if kills >= 25 and steps > 5:
        update_player(user_id, {"step_in_cycle": 0})
        return ("boss", None, f"🌑 **DOMINION OF {current_loc.upper()}**\nSang Penjaga dimensi ini telah bangkit!")

    # Update step counter
    update_player(user_id, {"step_in_cycle": steps, "step_counter": player.get("step_counter", 0) + 1})
    
    # Tentukan hazard berdasarkan lokasi
    loc_hazard = "GELAP" if "Abyss" in current_loc or "Hall" in current_loc else "RACUN" if "Mire" in current_loc else "DINGIN"

    roll = random.random()

    # --- PENENTUAN EVENT ---

    # A. AREA AMAN / REST AREA (Setelah perjalanan panjang)
    if steps >= 35:
        update_player(user_id, {'step_in_cycle': 0, 'min_boss_slain': False})
        return ("rest_area", None, "🏕️ **CAMPFIRE.** Kau menemukan tempat perlindungan. Energi dan jiwamu perlahan pulih.")

    # B. HAZARD LINGKUNGAN (Peluang muncul saat eksplorasi)
    if roll < 0.15:
        protected = check_environment_protection(player, loc_hazard)
        h_data = hazards.get_hazard_data(loc_hazard)
        if h_data:
            if not protected:
                apply_hazard_penalty(player, loc_hazard)
                return ("hazard", {"id": loc_hazard, "safe": False}, f"⚠️ **{h_data['name']}**\n{h_data['danger_msg']}")
            else:
                return ("hazard", {"id": loc_hazard, "safe": True}, f"🛡️ **{h_data['name']}**\n{h_data['safe_msg']}")

    # C. DEADLY EVENTS (Jebakan Maut / Stat Check)
    if roll < 0.25 and steps > 10:
        event_id = random.choice(list(deadly.DEADLY_EVENTS.keys()))
        ev = deadly.get_deadly_data(event_id)
        if ev:
            return ("deadly", {"id": event_id}, f"💀 **{ev['name']}**\n{ev['desc']}")

    # D. LANDMARKS (Lokasi Interaktif)
    if roll < 0.35:
        lm_id = random.choice(list(landmarks.LANDMARKS.keys()))
        lm = landmarks.get_landmark_data(lm_id)
        if lm:
            return ("landmark", {"id": lm_id}, f"🏛️ **{lm['name']}**\n{lm['desc']}")

    # E. NPC INTERACTIONS
    if roll < 0.50:
        # Acak kategori NPC
        npc_cat = random.choice(["story", "guide", "gamble", "quiz"])
        msg = "👤 Seseorang berdiri di antara kabut..."
        if npc_cat == "story": msg = "📖 Seorang pencerita tua memanggilmu."
        elif npc_cat == "gamble": msg = "🎲 Kau mendengar suara koin berdenting."
        return ("npc", {"category": npc_cat}, msg)

    # F. MONSTER ENCOUNTER (Default Encounter)
    if roll < 0.85:
        return ("monster", None, f"⚔️ **PERNYERGAPAN!** {random.choice(MONSTER_WARNINGS)}")

    # G. SAFE TRAVEL (Narasi Saja)
    safe_narration = "Langkahmu bergema di lorong sunyi."
    if NARRATIVES and "safe" in NARRATIVES and NARRATIVES["safe"]:
        safe_narration = random.choice(NARRATIVES["safe"])
        
    return ("safe", None, safe_narration)
