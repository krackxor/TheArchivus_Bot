# game/entities/minibosses.py

import random
from game.data.miniboss_data import MINI_BOSS_POOL

def get_random_mini_boss():
    """
    Mengambil satu set data Mini-Bos dari database.
    """
    if not MINI_BOSS_POOL:
        return _fallback_mini_boss()
        
    return random.choice(MINI_BOSS_POOL)

def _fallback_mini_boss():
    """Fallback darurat jika database miniboss_data.py kosong"""
    return {
        "name": "Corrupted Guard", "element": "void", "weakness": "light", "race": "anomaly", "attack_type": "physical",
        "base_hp": 2000, "p_atk": 100, "m_atk": 50, "p_def": 50, "m_def": 50, "speed": 5, "dodge_chance": 0.1, "crit_chance": 0.1, "crit_damage": 1.5,
        "status_resistance": {}, "ai_behavior": "aggressive", "exp": 1000, "gold": 500,
        "skill": {"name": "Slam", "type": "stun", "chance": 0.2}, "drops": [],
        "entry_narration": "Sistem memanggil penjaga darurat yang terkorupsi.", "death_narration": "Penjaga darurat hancur."
    }
