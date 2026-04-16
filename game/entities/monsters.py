# game/entities/monsters.py

import random
from game.data import MONSTER_POOL, MINI_BOSS_POOL, MAIN_BOSS_POOL

def get_random_monster(tier=1, cycle=1):
    pool = MONSTER_POOL.get(tier, MONSTER_POOL.get(1))
    if not pool: return None
    monster = random.choice(pool).copy()
    # Scaling HP sederhana
    monster['base_hp'] = int(monster['base_hp'] * (1 + (cycle - 1) * 0.1))
    return monster

def get_random_mini_boss():
    if not MINI_BOSS_POOL: return None
    return random.choice(MINI_BOSS_POOL).copy()

def get_random_main_boss():
    if not MAIN_BOSS_POOL: return None
    return random.choice(MAIN_BOSS_POOL).copy()
