# game/entities/npcs.py

import random
from game.data import NPC_POOL, LORE_STORIES

def get_npc_by_category(category):
    category_list = NPC_POOL.get(category)
    if not category_list: return None
    npc = random.choice(category_list).copy()
    npc['category'] = category
    return npc

def get_random_npc_event():
    category = random.choice(list(NPC_POOL.keys()))
    return get_npc_by_category(category)

def get_random_lore():
    return random.choice(LORE_STORIES)
