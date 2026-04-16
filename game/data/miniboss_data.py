# game/data/miniboss_data.py

"""
DATABASE MINI-BOS - The Archivus (RPG ADVANCED EDITION)
Ancaman level menengah. Lebih kuat dari monster biasa, namun belum setara Dewa.
Masing-masing mewakili satu dari 10 elemen utama.
"""

MINI_BOSS_POOL = [
    # 1. ELEMENT: DARK | RACE: UNDEAD
    {
        "name": "Shadow Sentinel", "element": "dark", "weakness": "light", "race": "undead", "attack_type": "physical",
        "base_hp": 2800, "p_atk": 130, "m_atk": 40, "p_def": 60, "m_def": 40, "speed": 6, "dodge_chance": 0.15, "crit_chance": 0.2, "crit_damage": 2.0,
        "status_resistance": {"blind": 1.0, "fear": 1.0}, "ai_behavior": "aggressive", "exp": 2500, "gold": 1200,
        "skill": {"name": "Abyssal Slash", "type": "blind", "chance": 0.3}, "drops": [{"id": "shadow_core", "chance": 1.0}, {"id": "potion_max_heal", "chance": 0.5}],
        "entry_narration": "🌑 Ruangan mendadak dingin. Sesosok ksatria bayangan bangkit dari lantai, membawa pedang yang menyerap cahaya.",
        "death_narration": "Ksatria itu hancur menjadi kabut hitam, meninggalkan keheningan yang mencekam."
    },
    
    # 2. ELEMENT: POISON | RACE: SLIME
    {
        "name": "Ink Lieutenant", "element": "poison", "weakness": "fire", "race": "slime", "attack_type": "magic",
        "base_hp": 3200, "p_atk": 50, "m_atk": 140, "p_def": 45, "m_def": 70, "speed": 4, "dodge_chance": 0.05, "crit_chance": 0.15, "crit_damage": 1.5,
        "status_resistance": {"poison": 1.0, "bleed": 1.0}, "ai_behavior": "trickster", "exp": 2600, "gold": 1300,
        "skill": {"name": "Toxic Spill", "type": "poison", "chance": 0.45}, "drops": [{"id": "ink_gland", "chance": 1.0}, {"id": "resin_fire", "chance": 0.4}],
        "entry_narration": "🦠 Tinta pekat berbau busuk mengalir dari langit-langit, membentuk sosok militer tanpa wajah.",
        "death_narration": "Sosok itu meleleh menjadi genangan tinta asam yang mendidih."
    },
    
    # 3. ELEMENT: ICE | RACE: UNDEAD
    {
        "name": "Frost Revenant", "element": "ice", "weakness": "fire", "race": "undead", "attack_type": "magic",
        "base_hp": 2500, "p_atk": 80, "m_atk": 145, "p_def": 50, "m_def": 80, "speed": 7, "dodge_chance": 0.2, "crit_chance": 0.25, "crit_damage": 2.2,
        "status_resistance": {"freeze": 1.0, "burn": 0.5}, "ai_behavior": "aggressive", "exp": 2700, "gold": 1400,
        "skill": {"name": "Absolute Zero", "type": "stun", "chance": 0.3}, "drops": [{"id": "frozen_tear", "chance": 1.0}, {"id": "ice_blade_fragment", "chance": 0.3}],
        "entry_narration": "❄️ Napasmu seketika membeku. Roh penasaran yang terbungkus es abadi melayang ke arahmu.",
        "death_narration": "Tubuhnya pecah menjadi ribuan serpihan es tajam yang melukai wajahmu."
    },
    
    # 4. ELEMENT: BLOOD | RACE: DEMON
    {
        "name": "Crimson Scout", "element": "blood", "weakness": "lightning", "race": "demon", "attack_type": "physical",
        "base_hp": 3000, "p_atk": 150, "m_atk": 20, "p_def": 55, "m_def": 45, "speed": 9, "dodge_chance": 0.25, "crit_chance": 0.3, "crit_damage": 2.5,
        "status_resistance": {"bleed": 1.0}, "ai_behavior": "berserk", "exp": 2800, "gold": 1500,
        "skill": {"name": "Blood Siphon", "type": "drain_hp", "chance": 0.4}, "drops": [{"id": "blood_crystal", "chance": 1.0}, {"id": "vampiric_ring", "chance": 0.1}],
        "entry_narration": "🩸 Makhluk gesit berkulit merah darah mengendus udara. Ia mencium detak jantungmu.",
        "death_narration": "Ia meledak, menghujanimu dengan darah hangat yang terasa lengket."
    },
    
    # 5. ELEMENT: LIGHTNING | RACE: ANOMALY
    {
        "name": "Volt Lurker", "element": "lightning", "weakness": "earth", "race": "anomaly", "attack_type": "magic",
        "base_hp": 2600, "p_atk": 40, "m_atk": 140, "p_def": 40, "m_def": 60, "speed": 10, "dodge_chance": 0.3, "crit_chance": 0.25, "crit_damage": 1.8,
        "status_resistance": {"paralyze": 1.0}, "ai_behavior": "trickster", "exp": 2550, "gold": 1250,
        "skill": {"name": "Static Discharge", "type": "paralyze", "chance": 0.35}, "drops": [{"id": "spark_plug", "chance": 1.0}],
        "entry_narration": "⚡ Percikan listrik menyambar-nyambar di udara kosong, perlahan membentuk siluet humanoid.",
        "death_narration": "Ledakan listrik membutakan matamu sejenak sebelum makhluk itu sirna."
    },

    # 6. ELEMENT: FIRE | RACE: DEMON
    {
        "name": "Pyre Walker", "element": "fire", "weakness": "water", "race": "demon", "attack_type": "physical",
        "base_hp": 2900, "p_atk": 160, "m_atk": 60, "p_def": 50, "m_def": 40, "speed": 7, "dodge_chance": 0.1, "crit_chance": 0.25, "crit_damage": 2.0,
        "status_resistance": {"burn": 1.0}, "ai_behavior": "aggressive", "exp": 2650, "gold": 1350,
        "skill": {"name": "Hellfire", "type": "burn", "chance": 0.35}, "drops": [{"id": "ember_core", "chance": 1.0}, {"id": "resin_fire", "chance": 0.3}],
        "entry_narration": "🔥 Udara menjadi sangat panas hingga paru-parumu terbakar. Tengkorak berapi berjalan menembus dinding.",
        "death_narration": "Apinya padam, hanya menyisakan tulang hangus yang rapuh."
    },

    # 7. ELEMENT: EARTH | RACE: CONSTRUCT
    {
        "name": "Flesh Golem", "element": "earth", "weakness": "ice", "race": "construct", "attack_type": "physical",
        "base_hp": 4500, "p_atk": 135, "m_atk": 10, "p_def": 85, "m_def": 30, "speed": 2, "dodge_chance": 0.0, "crit_chance": 0.1, "crit_damage": 1.5,
        "status_resistance": {"poison": 1.0, "stun": 0.8}, "ai_behavior": "defensive", "exp": 3000, "gold": 1600,
        "skill": {"name": "Earthquake Slam", "type": "armor_break", "chance": 0.35}, "drops": [{"id": "golem_heart", "chance": 1.0}, {"id": "heavy_plating", "chance": 0.2}],
        "entry_narration": "🪨 Raksasa yang dijahit dari ratusan potongan tubuh manusia dan batu melangkah berat menghampirimu.",
        "death_narration": "Jahitannya putus. Golem itu runtuh menjadi tumpukan daging dan debu yang menjijikkan."
    },

    # 8. ELEMENT: WATER | RACE: BEAST
    {
        "name": "Tidal Wraith", "element": "water", "weakness": "lightning", "race": "beast", "attack_type": "magic",
        "base_hp": 3100, "p_atk": 30, "m_atk": 150, "p_def": 55, "m_def": 75, "speed": 5, "dodge_chance": 0.2, "crit_chance": 0.15, "crit_damage": 1.8,
        "status_resistance": {"bleed": 1.0, "burn": 0.5}, "ai_behavior": "defensive", "exp": 2600, "gold": 1300,
        "skill": {"name": "Drowning Tide", "type": "drain_energy", "chance": 0.4}, "drops": [{"id": "abyssal_pearl", "chance": 1.0}, {"id": "water_essence", "chance": 0.5}],
        "entry_narration": "🌊 Lantai tiba-tiba banjir. Sesosok wanita yang terbuat dari air gelap bangkit dari genangan.",
        "death_narration": "Ia menjerit sebelum airnya surut, meninggalkan bau amis laut."
    },

    # 9. ELEMENT: LIGHT | RACE: HUMANOID
    {
        "name": "Radiant Inquisitor", "element": "light", "weakness": "dark", "race": "humanoid", "attack_type": "physical",
        "base_hp": 2700, "p_atk": 140, "m_atk": 90, "p_def": 65, "m_def": 65, "speed": 6, "dodge_chance": 0.15, "crit_chance": 0.2, "crit_damage": 2.2,
        "status_resistance": {"blind": 1.0, "fear": 1.0}, "ai_behavior": "aggressive", "exp": 2900, "gold": 1450,
        "skill": {"name": "Holy Smite", "type": "blind", "chance": 0.3}, "drops": [{"id": "radiant_gem", "chance": 1.0}, {"id": "purifying_scroll", "chance": 0.2}],
        "entry_narration": "✨ Cahaya suci yang menyilaukan turun dari atas. Ia datang bukan untuk menyelamatkan, tapi untuk menghukum.",
        "death_narration": "Cahayanya meredup dan mati, membuktikan bahwa bahkan malaikat bisa dibunuh."
    },

    # 10. ELEMENT: VOID | RACE: COSMIC
    {
        "name": "Void Assassin", "element": "void", "weakness": "light", "race": "cosmic", "attack_type": "physical",
        "base_hp": 2900, "p_atk": 145, "m_atk": 60, "p_def": 50, "m_def": 50, "speed": 8, "dodge_chance": 0.35, "crit_chance": 0.4, "crit_damage": 2.5,
        "status_resistance": {"blind": 1.0, "fear": 1.0, "paralyze": 0.5}, "ai_behavior": "trickster", "exp": 3200, "gold": 1800,
        "skill": {"name": "Dimension Strike", "type": "critical", "chance": 0.4}, "drops": [{"id": "void_dagger", "chance": 0.15}, {"id": "void_dust", "chance": 1.0}],
        "entry_narration": "🌀 Ruang di sekitarmu terdistorsi. Sesuatu yang tidak memiliki bentuk menempelkan bilah dingin di lehermu.",
        "death_narration": "Ia tertelan kembali ke dalam dimensi ketiadaan."
    }
]
