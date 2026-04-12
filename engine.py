import random
from database import get_player, update_player
from generators import generate_npc

def process_move(user_id):
    player = get_player(user_id)
    new_steps = player.get("step_counter", 0) + 1
    trigger_event = False
    
    # Logika tetap berjalan dari langkah 3 hingga 15
    if new_steps >= 3:
        chance = (new_steps / 15.0) * 100 
        if random.randint(1, 100) <= chance or new_steps >= 15:
            trigger_event = True

    if trigger_event:
        update_player(user_id, {"step_counter": 0})
        event_roll = random.random()
        
        # Narasi diubah: Angka langkah dihapus sepenuhnya
        if event_roll < 0.35: 
            return ("npc_baik", generate_npc(is_liar=False), "Sesuatu membuat langkahmu terhenti.")
        elif event_roll < 0.70: 
            return ("npc_jahat", generate_npc(is_liar=True), "Sesuatu membuat langkahmu terhenti.")
        else: 
            return ("monster", None, "Udara di sekitarmu mendadak menjadi sangat dingin...")

    else:
        update_player(user_id, {"step_counter": new_steps})
        # Narasi aman diubah: Angka langkah dihapus
        return ("safe", None, "Kamu melangkah ke depan dalam sunyi...")
