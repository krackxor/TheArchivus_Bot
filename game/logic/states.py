# game/logic/states.py

from aiogram.fsm.state import State, StatesGroup

class GameState(StatesGroup):
    """
    Sistem State Terpusat (Refactored) - The Archivus
    Disederhanakan menjadi 5 Core States untuk mencegah memory leak,
    race condition, dan tumpang tindih input.
    
    State ini mengontrol validitas tombol yang ditekan pemain di berbagai folder handlers/.
    """
    
    # --- 1. EXPLORING (Penjelajahan) ---
    # State default saat pemain berjalan di Desa, Hutan, atau Kota.
    # Memungkinkan akses ke tombol navigasi arah dan Menu Profil/Tas.
    exploring = State()

    # --- 2. IN_COMBAT (Pertarungan) ---
    # Terkunci saat menghadapi Monster, Miniboss, atau Boss (Castile).
    # Tombol navigasi arah dimatikan secara sistem (FSM Filter).
    in_combat = State()

    # --- 3. IN_EVENT (Interaksi & Teka-teki) ---
    # Digunakan saat berinteraksi dengan:
    # - NPC (Storytellers di Cafe, Peramal di Kuburan)
    # - Puzzle (Membuka peti, membaca pesan berdarah)
    # - Landmark (Altar Ibadah)
    in_event = State()

    # --- 4. IN_REST_AREA (Area Aman & Fasilitas) ---
    # Digunakan saat berada di Penginapan (Inn), Rest Area (Campfire), atau Toko.
    # Memungkinkan fitur Shop dan Repair tanpa risiko diserang musuh.
    in_rest_area = State()

    # --- 5. DEAD (Kematian) ---
    # State saat HP mencapai 0. 
    # Mengunci seluruh fungsi permainan hingga pemain melakukan Respawn.
    dead = State()
