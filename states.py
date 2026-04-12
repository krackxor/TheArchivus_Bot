from aiogram.fsm.state import StatesGroup, State

class GameState(StatesGroup):
    exploring = State()    # Mode jelajah normal (Navigasi bebas)
    in_combat = State()    # Mode pertarungan (Waktu terbatas, input jawaban)
    traveling = State()    # Mode navigasi misi (Wajib mengikuti arah NPC 5x)
