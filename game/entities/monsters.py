# game/entities/monsters.py

import random
# Mengambil data dari folder data (Integrated Data Layer)
from game.data import MONSTER_POOL, MINI_BOSS_POOL, MAIN_BOSS_POOL

def get_random_monster(tier=1):
    """Mengambil satu monster biasa berdasarkan tier (1-3)"""
    # Mencari pool berdasarkan tier, jika tidak ada gunakan tier 1
    pool = MONSTER_POOL.get(tier, MONSTER_POOL.get(1))
    if not pool:
        return None
    return random.choice(pool).copy()

def get_random_mini_boss():
    """Mengambil satu mini-boss acak dari database"""
    if not MINI_BOSS_POOL:
        return None
    return random.choice(MINI_BOSS_POOL).copy()

def get_random_main_boss():
    """Mengambil satu boss utama (Main Boss) dari database"""
    if not MAIN_BOSS_POOL:
        return None
    return random.choice(MAIN_BOSS_POOL).copy()
