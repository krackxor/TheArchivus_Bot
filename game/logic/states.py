# game/logic/states.py

from aiogram.fsm.state import State, StatesGroup

class GameState(StatesGroup):
    """
    Sistem State Terpusat (Refactored)
    Disederhanakan menjadi 5 Core States untuk mencegah memory leak,
    race condition, dan tumpang tindih input.
    """
    
    # --- 1. EXPLORING (Penjelajahan) ---
    # State utama saat pemain berjalan (Utara, Selatan, dll).
    # Digunakan juga saat pemain membuka Profil/Tas di luar pertempuran.
    exploring = State()

    # --- 2. IN_COMBAT (Pertarungan) ---
    # State terkunci saat melawan Monster, Miniboss, atau Boss Utama.
    # Selama state ini, navigasi arah (Utara/Selatan) dimatikan.
    in_combat = State()

    # --- 3. IN_EVENT (Interaksi Objek, NPC & Lingkungan) ---
    # Digunakan untuk semua interaksi non-combat:
    # - Dialog NPC (Storyteller, Guide, Requester)
    # - Mini-game (Gambler)
    # - Teka-teki (Quiz, Chest, Landmark)
    # - Bahaya Lingkungan yang butuh Stat Check (Jurang/Deadly)
    in_event = State()

    # --- 4. IN_REST_AREA (Area Aman) ---
    # State saat berada di Campfire atau Kota.
    # Memungkinkan transaksi Shop, Repair, dan pemulihan HP/MP tanpa gangguan monster.
    in_rest_area = State()

    # --- 5. DEAD (Kematian) ---
    # State saat HP mencapai 0. 
    # Mengunci semua fungsi kecuali tombol Respawn.
    dead = State()
