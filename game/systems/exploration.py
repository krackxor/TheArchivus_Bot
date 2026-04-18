# game/systems/exploration.py

"""
Sistem Eksplorasi (Exploration System) - ALUR DINAMIS & ENVIRONMENT HAZARDS
Menangani logika pergerakan pemain, trigger event NPC, Puzzle, dan Bahaya Lingkungan.
Terintegrasi dengan sistem Quest, Narasi Despair, dan Stalking Mode.
"""

import random
from database import get_player, update_player, add_history

# --- INCLUDE DATA MASTER & LOGIKA MODULAR ---
from game.data.script import DESPAIR_STEPS, NARRATIVES, STALKING_MESSAGES, MONSTER_WARNINGS
from game.data.environment import hazards, deadly, landmarks
from game.data.quests import update_quest_progress

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

def process_move(user_id, **kwargs):
    """
    The Journey Driver: Mengatur probabilitas event dan narasi.
    Menghubungkan Quest Tracker, Script Despair, dan Stalking Mode.
    """
    player = get_player(user_id)
    luck = kwargs.get('luck', 0)
    intel = kwargs.get('intel', 10)
    
    # 1. UPDATE QUEST PROGRESS (Misi Melangkah)
    # Setiap kali fungsi ini dipanggil (pemain melangkah), progres quest bertambah.
    player, quest_msgs = update_quest_progress(player, "move_steps")
    
    # 2. UPDATE STEP COUNTER & NARRATIVE
    steps = player.get('step_in_cycle', 0) + 1
    total_steps = player.get("step_counter", 0) + 1
    current_loc, just_moved = update_location_if_needed(player)
    
    # Ambil narasi psikologis berdasarkan langkah (Despair System)
    # Mengambil pesan unik dari DESPAIR_STEPS berdasarkan total_steps.
    despair_msg = DESPAIR_STEPS.get(total_steps, random.choice(NARRATIVES["safe"]))

    # 3. TRIGGER STALKING MODE (Peluang Paranoid 5%)
    if random.random() < 0.05:
        despair_msg += f"\n\n👁️ _{random.choice(STALKING_MESSAGES)}_"

    # Simpan status langkah terbaru
    update_player(user_id, {
        "step_in_cycle": steps, 
        "step_counter": total_steps,
        "active_quests": player['active_quests'] # Update data quest yang baru saja diproses
    })

    # 4. TRIGGER BOSS (Threshold Kills)
    kills = player.get("kills", 0)
    if kills > 0 and kills % 25 == 0 and steps > 5:
        update_player(user_id, {"step_in_cycle": 0})
        return ("boss", None, f"🌑 **DOMINION OF {current_loc.upper()}**\nSang Penjaga dimensi ini telah bangkit!")

    # 5. PENENTUAN HAZARD BERDASARKAN LOKASI
    loc_hazard = "GELAP" if any(x in current_loc for x in ["Abyss", "Hall"]) else "RACUN" if "Mire" in current_loc else "DINGIN"
    
    # Penyesuaian Roll dengan Luck
    roll = random.random() - (luck * 0.005)

    # --- PENENTUAN EVENT ---

    # A. REST AREA (Berdasarkan Intel)
    rest_threshold = max(20, 35 - (intel // 5))
    if steps >= rest_threshold:
        update_player(user_id, {'step_in_cycle': 0})
        return ("rest_area", None, "🏕️ **CAMPFIRE.** Kau menemukan perlindungan. Energi pulih.")

    # B. HAZARD LINGKUNGAN (Peluang 15%)
    if roll < 0.15:
        # Menggunakan logika modular dari hazards.py.
        safe, h_msg = hazards.process_hazard_interaction(player, loc_hazard)
        update_player(user_id, player) # Simpan dampak penalti jika tidak aman
        return ("hazard", {"id": loc_hazard, "safe": safe}, h_msg)

    # C. DEADLY EVENTS / TRAPS (Peluang 10%)
    if roll < 0.25 and steps > 8:
        event_id = random.choice(list(deadly.DEADLY_EVENTS.keys()))
        ev = deadly.get_deadly_data(event_id)
        return ("deadly", {"id": event_id}, f"💀 **{ev['name']}**\n{ev['desc']}")

    # D. LANDMARKS (Peluang dipengaruhi Intel)
    landmark_chance = 0.35 + (intel * 0.002)
    if roll < landmark_chance:
        lm_id = random.choice(list(landmarks.LANDMARKS.keys()))
        lm = landmarks.get_landmark_data(lm_id)
        return ("landmark", {"id": lm_id}, f"🏛️ **{lm['name']}**\n{lm['desc']}")

    # E. NPC POOL INTERACTION (Peluang 15%)
    if roll < 0.55:
        npc_cat = random.choice(["healer", "trickster", "guide", "scholar", "lore_keeper", "wanderer"])
        # Intel tinggi meningkatkan peluang bertemu Scholar/Lore Keeper
        if intel > 25: npc_cat = random.choice(["scholar", "lore_keeper", "pact"])
        
        return ("npc", {"category": npc_cat}, f"👤 {despair_msg}")

    # F. MONSTER ENCOUNTER (Peluang Utama 30%)
    if roll < 0.85:
        # Mengambil peringatan sergapan dari script.py.
        return ("monster", None, f"⚔️ **{random.choice(MONSTER_WARNINGS)}**")

    # G. SAFE TRAVEL (Despair Narrative + Quest Info)
    final_msg = despair_msg
    if quest_msgs:
        final_msg += "\n\n" + "\n".join(quest_msgs)
        
    return ("safe", None, final_msg)
