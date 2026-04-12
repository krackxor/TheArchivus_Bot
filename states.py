from aiogram.fsm.state import StatesGroup, State

class GameState(StatesGroup):
    exploring = State()    # Mode aman (Muncul tombol arah)
    in_combat = State()    # Mode tarung (Tombol hilang, harus ngetik)
