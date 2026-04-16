"""
Sistem Entitas Monster (RPG ADVANCED EDITION)
Menghubungkan generator encounter dengan database monster lengkap.
Mencakup: Elemen, Kelemahan, HP, ATK, EXP, Gold, Skill, Drops, dan Narasi Horor.
"""

import random
# KITA IMPORT DATA DARI FILE BARU
from game.data.monster_data import MONSTER_POOL

def get_random_monster(tier):
    """
    Mengambil satu set data monster lengkap (Dictionary) berdasarkan tier.
    Return struktur Ultimate:
    {
        "name": str,
        "element": str,
        "weakness": str,
        "race": str,
        "attack_type": str,
        "base_hp": int,
        "p_atk": int,
        "m_atk": int,
        "p_def": int,
        "m_def": int,
        "speed": int,
        "dodge_chance": float,
        "crit_chance": float,
        "crit_damage": float,
        "status_resistance": dict,
        "ai_behavior": str,
        "exp": int,
        "gold": int,
        "drops": [{"id": str, "chance": float}],
        "skill": {"name": str, "type": str, "chance": float},
        "entry_narration": str,
        "death_narration": str
    }
    """
    # Mengamankan input tier agar tidak error jika melebihi batas 1-5
    safe_tier = max(1, min(tier, 5))
    
    # Pastikan tier ada di POOL untuk mencegah KeyError
    if safe_tier not in MONSTER_POOL or not MONSTER_POOL[safe_tier]:
        # Fallback Darurat jika data kosong
        return {
            "name": "Glitch Entity", "element": "void", "weakness": "light",
            "race": "cosmic", "attack_type": "magic",
            "base_hp": 50, "p_atk": 5, "m_atk": 15, "p_def": 5, "m_def": 20,
            "speed": 5, "dodge_chance": 0.2, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"poison": 1.0}, "ai_behavior": "trickster",
            "exp": 10, "gold": 5, "drops": [], "skill": {"name": "Error", "type": "stun", "chance": 0.1},
            "entry_narration": "Sistem gagal memuat entitas.", "death_narration": "Kode rusak dihapus."
        }
    
    # Mengambil random monster dictionary dari POOL
    monster_data = random.choice(MONSTER_POOL[safe_tier])
    
    return monster_data
