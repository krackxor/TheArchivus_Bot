from aiogram.fsm.state import State, StatesGroup

class GameState(StatesGroup):
    exploring = State()    # Jalan normal
    traveling = State()    # Misi manual 5 langkah dari NPC
    in_combat = State()    # Lawan Monster/Boss
    in_quiz = State()      # Sedang ditanya oleh NPC Quiz
