# game/entities/monsters.py
import random
from game.data import MONSTER_POOL, MINI_BOSS_POOL, BOSS_DATA

def get_random_monster(tier=1):
    return random.choice(MONSTER_POOL.get(tier, MONSTER_POOL[1])).copy()

def get_random_mini_boss():
    return random.choice(MINI_BOSS_POOL).copy()

def get_random_main_boss():
    return random.choice(BOSS_DATA).copy()
