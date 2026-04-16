# game/entities/bosses.py

"""
Sistem Entitas Bos (Router Edition)
Hanya berisi logika pemanggil. Data dan perakitan stat ditarik 
langsung dari file generator di folder game/data/
"""

# Import factory function dari file data yang sudah kita pisah
from game.data.miniboss_data import generate_mini_boss
from game.data.mainboss_data import generate_main_boss

def get_random_mini_boss():
    """
    Memanggil dan mengembalikan data dictionary Mini-Bos secara dinamis.
    """
    try:
        return generate_mini_boss()
    except Exception as e:
        # Fallback aman jika terjadi error saat generate
        return _fallback_boss("mini")

def get_random_boss():
    """
    Memanggil dan mengembalikan data dictionary Bos Utama secara dinamis.
    """
    try:
        return generate_main_boss()
    except Exception as e:
        # Fallback aman jika terjadi error saat generate
        return _fallback_boss("main")

def _fallback_boss(boss_type):
    """Fallback darurat agar bot tidak crash jika file data bermasalah"""
    if boss_type == "mini":
        return {
            "name": "Corrupted Guardian (Mini-Boss)", "element": "void", "weakness": "light", 
            "race": "anomaly", "attack_type": "physical", "base_hp": 3000, 
            "p_atk": 100, "m_atk": 50, "p_def": 50, "m_def": 50, "speed": 5, 
            "dodge_chance": 0.1, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {}, "ai_behavior": "aggressive", "exp": 1000, "gold": 500,
            "skill": {"name": "Slam", "type": "stun", "chance": 0.2}, "drops": [],
            "entry_narration": "Penjaga darurat terkorupsi muncul.", "death_narration": "Penjaga hancur."
        }
    else:
        return {
            "name": "SYSTEM OVERLORD (Main Boss)", "element": "void", "weakness": "light", 
            "race": "cosmic", "attack_type": "magic", "base_hp": 8000, 
            "p_atk": 150, "m_atk": 200, "p_def": 100, "m_def": 100, "speed": 8, 
            "dodge_chance": 0.2, "crit_chance": 0.2, "crit_damage": 2.0,
            "status_resistance": {"all": 0.5}, "ai_behavior": "trickster", "exp": 5000, "gold": 2500,
            "skill": {"name": "Fatal Exception", "type": "drain_all", "chance": 0.3}, "drops": [],
            "entry_narration": "CRITICAL ERROR: Entitas Induk menghapus ruang.", "death_narration": "Sistem di-override."
        }
