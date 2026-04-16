# game/entities/npcs.py
from game.data import NPC_DATA

def get_npc(npc_id):
    return NPC_DATA.get(npc_id)
