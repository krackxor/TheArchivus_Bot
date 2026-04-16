# game/data/miniboss_data.py

"""
DATABASE MINI-BOS - The Archivus (RPG ADVANCED EDITION)
Ancaman level menengah. Lebih kuat dari monster biasa, namun belum setara Dewa.
"""

MINI_BOSS_POOL = [
    {
        "name": "Shadow Sentinel", "element": "dark", "weakness": "light", "race": "undead", "attack_type": "physical",
        "base_hp": 2800, "p_atk": 130, "m_atk": 40, "p_def": 60, "m_def": 40, "speed": 6, "dodge_chance": 0.15, "crit_chance": 0.2, "crit_damage": 2.0,
        "status_resistance": {"blind": 1.0, "fear": 1.0}, "ai_behavior": "aggressive", "exp": 2500, "gold": 1200,
        "skill": {"name": "Abyssal Slash", "type": "blind", "chance": 0.3}, "drops": [{"id": "shadow_core", "chance": 1.0}, {"id": "potion_max_heal", "chance": 0.5}],
        "entry_narration": "Ruangan mendadak dingin. Sesosok ksatria bayangan bangkit dari lantai, membawa pedang yang menyerap cahaya.",
        "death_narration": "Ksatria itu hancur menjadi kabut hitam, meninggalkan keheningan yang mencekam."
    },
    {
        "name": "Ink Lieutenant", "element": "poison", "weakness": "fire", "race": "slime", "attack_type": "magic",
        "base_hp": 3200, "p_atk": 50, "m_atk": 140, "p_def": 45, "m_def": 70, "speed": 4, "dodge_chance": 0.05, "crit_chance": 0.15, "crit_damage": 1.5,
        "status_resistance": {"poison": 1.0, "bleed": 1.0}, "ai_behavior": "trickster", "exp": 2600, "gold": 1300,
        "skill": {"name": "Toxic Spill", "type": "poison", "chance": 0.45}, "drops": [{"id": "ink_gland", "chance": 1.0}, {"id": "resin_fire", "chance": 0.4}],
        "entry_narration": "Tinta pekat berbau busuk mengalir dari langit-langit, membentuk sosok militer tanpa wajah.",
        "death_narration": "Sosok itu meleleh menjadi genangan tinta asam yang mendidih."
    },
    {
        "name": "Frost Revenant", "element": "ice", "weakness": "fire", "race": "undead", "attack_type": "magic",
        "base_hp": 2500, "p_atk": 80, "m_atk": 145, "p_def": 50, "m_def": 80, "speed": 7, "dodge_chance": 0.2, "crit_chance": 0.25, "crit_damage": 2.2,
        "status_resistance": {"freeze": 1.0, "burn": 0.5}, "ai_behavior": "aggressive", "exp": 2700, "gold": 1400,
        "skill": {"name": "Absolute Zero", "type": "stun", "chance": 0.3}, "drops": [{"id": "frozen_tear", "chance": 1.0}, {"id": "ice_blade_fragment", "chance": 0.3}],
        "entry_narration": "Napasmu seketika membeku. Roh penasaran yang terbungkus es abadi melayang ke arahmu.",
        "death_narration": "Tubuhnya pecah menjadi ribuan serpihan es tajam yang melukai wajahmu."
    },
    {
        "name": "Crimson Scout", "element": "blood", "weakness": "lightning", "race": "demon", "attack_type": "physical",
        "base_hp": 3000, "p_atk": 150, "m_atk": 20, "p_def": 55, "m_def": 45, "speed": 9, "dodge_chance": 0.25, "crit_chance": 0.3, "crit_damage": 2.5,
        "status_resistance": {"bleed": 1.0}, "ai_behavior": "berserk", "exp": 2800, "gold": 1500,
        "skill": {"name": "Blood Siphon", "type": "drain_hp", "chance": 0.4}, "drops": [{"id": "blood_crystal", "chance": 1.0}, {"id": "vampiric_ring", "chance": 0.1}],
        "entry_narration": "Makhluk gesit berkulit merah darah mengendus udara. Ia mencium detak jantungmu.",
        "death_narration": "Ia meledak, menghujanimu dengan darah hangat yang terasa lengket."
    },
    {
        "name": "Volt Lurker", "element": "lightning", "weakness": "earth", "race": "anomaly", "attack_type": "magic",
        "base_hp": 2600, "p_atk": 40, "m_atk": 140, "p_def": 40, "m_def": 60, "speed": 10, "dodge_chance": 0.3, "crit_chance": 0.25, "crit_damage": 1.8,
        "status_resistance": {"paralyze": 1.0}, "ai_behavior": "trickster", "exp": 2550, "gold": 1250,
        "skill": {"name": "Static Discharge", "type": "paralyze", "chance": 0.35}, "drops": [{"id": "spark_plug", "chance": 1.0}],
        "entry_narration": "Percikan listrik menyambar-nyambar di udara kosong, perlahan membentuk siluet humanoid.",
        "death_narration": "Ledakan listrik membutakan matamu sejenak sebelum makhluk itu sirna."
    }
]
