# game/systems/exploration.py

"""
Sistem Eksplorasi (Exploration System) - ALUR DINAMIS & ENVIRONMENT HAZARDS
Menangani logika pergerakan pemain, trigger event NPC, Puzzle, dan Bahaya Lingkungan.
Terintegrasi dengan sistem Luck (Loot) dan Intelligence (Event detection).
"""

import random
from database import get_player, update_player, add_history

# Panggilan ke sistem Data & Lingkungan
from game.data import NARRATIVES, MONSTER_WARNINGS
from game.data.environment import hazards, deadly, landmarks

# --- KONFIGURASI LOKASI ---
LOCATIONS = [
    "The Whispering Hall", "The Forsaken Mire", "The Abyssal Depth", 
    "The Frozen Purgatory", "The Crimson Throne"
]

def update_location_if_needed(player):
    """Merotasi lokasi berdasarkan jumlah kill."""
    kills = player.get('kills', 0)
    current_loc = player.get('location', LOCATIONS[0])
    
    # Ganti area setiap 10 kills
    loc_idx = min(kills // 10, len(LOCATIONS) - 1)
    new_location = LOCATIONS[loc_idx]
    
    if new_location != current_loc:
        update_player(player['user_id'], {"location": new_location})
        add_history(player['user_id'], f"Menembus batas kewarasan dan memasuki {new_location}.")
        return new_location, True 
        
    return current_loc, False

def check_environment_protection(player, hazard_id):
    """Logika Survival: Cek item pelindung di Tas atau Equipment."""
    h_data = hazards.get_hazard_data(hazard_id)
    if not h_data: return True

    req_item = h_data.get('required_item')
    inventory = player.get('inventory', [])
    equipped = list(player.get('equipped', {}).values())
    
    return req_item in inventory or req_item in equipped

def apply_hazard_penalty(player, hazard_id):
    """Memproses dampak negatif dari lingkungan."""
    h_data = hazards.get_hazard_data(hazard_id)
    if not h_data: return {}
        
    penalty = h_data.get('penalty', {})
    updates = {}
    
    if 'hp_loss' in penalty:
        updates['hp'] = max(0, player.get('hp', 100) - penalty['hp_loss'])
    
    if 'energy_loss' in penalty:
        updates['energy'] = max(0, player.get('energy', 100) - penalty['energy_loss'])
        
    if 'status_effect' in penalty:
        effects = player.get('active_effects', [])
        eff_type = penalty['status_effect']
        if not any(e.get('type') == eff_type for e in effects):
            effects.append({
                "type": eff_type, 
                "value": penalty.get('effect_val', 5), 
                "duration": 3,
                "icon": "🤢" if eff_type == "poison" else "❄️"
            })
            updates['active_effects'] = effects
            
    if updates:
        update_player(player['user_id'], updates)
    return updates

def process_move(user_id, **kwargs):
    """
    The Journey Driver: Mengatur probabilitas event.
    Menerima luck dan intel dari main.py melalui **kwargs.
    """
    player = get_player(user_id)
    luck = kwargs.get('luck', 0)
    intel = kwargs.get('intel', 10)
    
    kills = player.get("kills", 0)
    steps = player.get('step_in_cycle', 0) + 1
    current_loc, just_moved = update_location_if_needed(player)
    
    # 1. TRIGGER BOSS (Threshold Kills)
    if kills > 0 and kills % 25 == 0 and steps > 5:
        update_player(user_id, {"step_in_cycle": 0})
        return ("boss", None, f"🌑 **DOMINION OF {current_loc.upper()}**\nSang Penjaga dimensi ini telah bangkit!")

    # Update step counter
    update_player(user_id, {
        "step_in_cycle": steps, 
        "step_counter": player.get("step_counter", 0) + 1
    })
    
    # Tentukan hazard berdasarkan lokasi
    loc_hazard = "GELAP" if any(x in current_loc for x in ["Abyss", "Hall"]) else "RACUN" if "Mire" in current_loc else "DINGIN"

    # Penyesuaian Roll dengan Luck (Luck memperkecil peluang hazard, memperbesar peluang landmark/rest)
    roll = random.random() - (luck * 0.005) # Luck 10 = -0.05 roll
    
    # --- PENENTUAN EVENT ---

    # A. REST AREA (Threshold Dinamis berdasarkan Intel)
    # Semakin tinggi intel, semakin cepat menemukan jalan ke Rest Area
    rest_threshold = max(20, 35 - (intel // 5))
    if steps >= rest_threshold:
        update_player(user_id, {'step_in_cycle': 0})
        return ("rest_area", None, "🏕️ **CAMPFIRE.** Kau menemukan tempat perlindungan. Energi dan jiwamu pulih.")

    # B. HAZARD LINGKUNGAN (Peluang 15%)
    if roll < 0.15:
        protected = check_environment_protection(player, loc_hazard)
        h_data = hazards.get_hazard_data(loc_hazard)
        if h_data:
            if not protected:
                apply_hazard_penalty(player, loc_hazard)
                return ("hazard", {"id": loc_hazard, "safe": False}, f"⚠️ **{h_data['name']}**\n{h_data['danger_msg']}")
            else:
                return ("hazard", {"id": loc_hazard, "safe": True}, f"🛡️ **{h_data['name']}**\n{h_data['safe_msg']}")

    # C. DEADLY EVENTS / TRAPS (Peluang 10%)
    if roll < 0.25 and steps > 8:
        event_id = random.choice(list(deadly.DEADLY_EVENTS.keys()))
        ev = deadly.get_deadly_data(event_id)
        return ("deadly", {"id": event_id}, f"💀 **{ev['name']}**\n{ev['desc']}")

    # D. LANDMARKS / SECRET ROOMS (Peluang dipengaruhi Intel)
    # Intel tinggi memudahkan deteksi Landmark
    landmark_chance = 0.35 + (intel * 0.002)
    if roll < landmark_chance:
        lm_id = random.choice(list(landmarks.LANDMARKS.keys()))
        lm = landmarks.get_landmark_data(lm_id)
        return ("landmark", {"id": lm_id}, f"🏛️ **{lm['name']}**\n{lm['desc']}")

    # E. NPC / STORY (Peluang 15%)
    if roll < 0.55:
        npc_cat = random.choice(["story", "guide", "quiz"])
        # Jika intel tinggi, lebih sering dapat Quiz (untuk nambah intel lagi)
        if intel > 25: npc_cat = random.choice(["quiz", "story"])
        
        msg = "👤 Seseorang berdiri di antara kabut..."
        if npc_cat == "story": msg = "📖 Seorang pencerita tua memanggilmu."
        elif npc_cat == "quiz": msg = "📜 Kau menemukan gulungan teka-teki kuno."
        return ("npc", {"category": npc_cat}, msg)

    # F. MONSTER ENCOUNTER (Peluang Utama 30%)
    if roll < 0.85:
        return ("monster", None, f"⚔️ **PERNYERGAPAN!** {random.choice(MONSTER_WARNINGS)}")

    # G. SAFE TRAVEL (Narasi Saja)
    safe_narration = "Langkahmu bergema di lorong sunyi."
    if NARRATIVES.get("safe"):
        safe_narration = random.choice(NARRATIVES["safe"])
        
    return ("safe", None, safe_narration)
