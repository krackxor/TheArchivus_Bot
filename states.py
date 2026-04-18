# game/logic/states.py

from aiogram.fsm.state import State, StatesGroup

class GameState(StatesGroup):
    """
    Sistem State Terpusat (Refactored)
    Disederhanakan menjadi 5 Core States untuk mencegah memory leak,
    race condition, dan overlapping input.
    """
    
    # --- 1. IDLE / MENU (Area Aman) ---
    # Digunakan saat di Kota, Rest Area, atau saat membuka menu utama (Profil/Inventory).
    # Input yang diterima: Navigasi Menu, Equip, Shop, Repair.
    idle = State()

    # --- 2. EXPLORING (Penjelajahan) ---
    # State aktif saat pemain berjalan (Utara, Selatan, dll).
    # Input yang diterima: Tombol Arah & Navigasi Profil.
    exploring = State()

    # --- 3. IN_COMBAT (Pertarungan) ---
    # State terkunci saat melawan Monster/Boss.
    # Input yang diterima: Stance (Serang, Skill, Block, Dodge, Item, Run).
    # TIDAK BISA berjalan atau buka menu lain sampai pertarungan selesai.
    in_combat = State()

    # --- 4. IN_EVENT (Interaksi Objek & NPC) ---
    # State untuk interaksi Narasi/Puzzle: Peti (Chest), Altar, Jurang, 
    # Quiz NPC, Gambler, atau Dialog Story.
    # Input yang diterima: Jawaban Teka-teki (Anagram/Lore/Math) atau Pilihan Dialog.
    in_event = State()

    # --- 5. DEAD (Kematian) ---
    # State saat HP mencapai 0. 
    # Input yang diterima: Hanya tombol Respawn / Reset.
    dead = State()
