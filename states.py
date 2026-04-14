from aiogram.fsm.state import State, StatesGroup

class GameState(StatesGroup):
    exploring = State()       # State saat pemain sedang menjelajah jalan normal
    traveling = State()       # State untuk misi manual (misal: disuruh NPC jalan 5 langkah)
    in_combat = State()       # State saat pemain melawan monster/bos
    in_quiz = State()         # State saat ditanya oleh NPC Quiz/Scholar
    in_event = State()        # State untuk interaksi objek (peti harta, kuburan, patung, NPC judi)
    in_rest_area = State()    # State saat pemain sedang beristirahat di kemah / berbelanja
