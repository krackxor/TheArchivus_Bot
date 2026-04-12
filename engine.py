import random
from database import get_player, update_player
from generators import generate_npc

def process_move(user_id):
    player = get_player(user_id)
    new_steps = player.get("step_counter", 0) + 1
    trigger_event = False
    
    if new_steps >= 3:
        chance = (new_steps / 15.0) * 100 
        if random.randint(1, 100) <= chance or new_steps >= 15:
            trigger_event = True

    if trigger_event:
        update_player(user_id, {"step_counter": 0})
        event_roll = random.random()
        
        if event_roll < 0.35: 
            return ("npc_baik", generate_npc(is_liar=False), f"Langkahmu terhenti di langkah ke-{new_steps}.")
        elif event_roll < 0.70: 
            return ("npc_jahat", generate_npc(is_liar=True), f"Langkahmu terhenti di langkah ke-{new_steps}.")
        else: 
            return ("monster", None, f"Udara mendadak dingin di langkah ke-{new_steps}...")

    else:
        update_player(user_id, {"step_counter": new_steps})
        return ("safe", None, f"Kamu melangkah dalam sunyi... (Langkah: {new_steps}/15)")
