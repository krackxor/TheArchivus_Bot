# game/logic/states.py

from aiogram.fsm.state import State, StatesGroup

class GameState(StatesGroup):
    """
    Sistem State Terpusat (Finite State Machine)
    Mengatur alur kontrol agar input user diproses oleh handler yang tepat.
    """
    
    # --- EKSPLORASI & PERJALANAN ---
    exploring = State()        # State utama saat menjelajah jalan normal
    traveling = State()        # State transisi atau misi manual (NPC Quest)
    
    # --- COMBAT & SKILL ---
    in_combat = State()        # State saat bertarung melawan monster/bos
    casting_skill = State()    # State saat pemain sedang memilih/menggunakan skill aktif
    
    # --- INTERAKSI & EVENT ---
    in_event = State()         # State interaksi objek (peti, kuburan, patung)
    in_gamble = State()        # State khusus saat berurusan dengan The Void Gambler (Judi)
    in_quiz = State()          # State saat menjawab tantangan Scholar/Lore
    in_npc_talk = State()      # State saat berdialog dengan NPC (Misi/Cerita)
    
    # --- AREA AMAN & MENU ---
    in_rest_area = State()     # State saat di kemah/api unggun
    in_shop = State()          # State khusus saat sedang bertransaksi dengan Merchant
    
    # --- PENGELOLAAN KARAKTER ---
    in_inventory = State()     # State saat sedang mengatur tas/peralatan (Equip/Unequip)
    allocating_stats = State() # State saat sedang membelanjakan Stat Points (SP)
