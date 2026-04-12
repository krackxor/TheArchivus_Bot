import random
from database import get_player, update_player
from generators import generate_npc

def process_move(user_id):
    """
    Fungsi penentu nasib pemain di setiap langkahnya.
    Mengembalikan tuple: (Tipe_Kejadian, Data_Kejadian, Teks_Info)
    """
    player = get_player(user_id)
    current_steps = player.get("step_counter", 0)
    
    new_steps = current_steps + 1
    
    # --- LOGIKA KETEGANGAN 3 SAMPAI 15 LANGKAH ---
    trigger_event = False
    
    if new_steps >= 3:
        # Semakin mendekati langkah ke-15, peluang kena event semakin besar (mendekati 100%)
        chance = (new_steps / 15.0) * 100 
        
        # Melempar dadu persentase
        if random.randint(1, 100) <= chance or new_steps >= 15:
            trigger_event = True

    # --- JIKA TERKENA EVENT ---
    if trigger_event:
        update_player(user_id, {"step_counter": 0}) # Reset langkah ke 0
        
        # Lempar dadu untuk menentukan nasib (Gacha Event)
        event_roll = random.random()
        
        if event_roll < 0.35: 
            # 35% Peluang bertemu NPC Jujur
            npc = generate_npc(is_liar=False)
            return ("npc_baik", npc, f"Langkahmu terhenti di langkah ke-{new_steps}.")
            
        elif event_roll < 0.70: 
            # 35% Peluang bertemu NPC Penipu
            npc = generate_npc(is_liar=True)
            return ("npc_jahat", npc, f"Langkahmu terhenti di langkah ke-{new_steps}.")
            
        else: 
            # 30% Peluang bertemu Monster
            # (Untuk monster, kita buat data sederhana dulu untuk test)
            monster = {"name": "Corrupted Glitch", "hp": 50, "type": "Anagram"}
            return ("monster", monster, f"Udara mendadak dingin di langkah ke-{new_steps}...")

    # --- JIKA AMAN ---
    else:
        update_player(user_id, {"step_counter": new_steps})
        return ("safe", None, f"Kamu melangkah dalam sunyi... (Total langkah: {new_steps})")
