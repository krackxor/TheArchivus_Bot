# game/data/boss_data.py

"""
DATABASE BOS & MINI-BOS - The Archivus (RPG ADVANCED EDITION)
Hierarki Stat Terjaga: Monster Biasa < Mini-Boss < Main Boss
Mencakup: Element, Weakness, Race, Physical/Magic Stats, Speed, Crit, Dodge, AI Behavior, dan Drops Langka.
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
        "name": "Flesh Golem", "element": "earth", "weakness": "fire", "race": "construct", "attack_type": "physical",
        "base_hp": 4500, "p_atk": 135, "m_atk": 10, "p_def": 85, "m_def": 30, "speed": 2, "dodge_chance": 0.0, "crit_chance": 0.1, "crit_damage": 1.5,
        "status_resistance": {"poison": 1.0, "stun": 0.8}, "ai_behavior": "defensive", "exp": 3000, "gold": 1600,
        "skill": {"name": "Earthquake Slam", "type": "armor_break", "chance": 0.35}, "drops": [{"id": "golem_heart", "chance": 1.0}, {"id": "heavy_plating", "chance": 0.2}],
        "entry_narration": "Raksasa yang dijahit dari ratusan potongan tubuh manusia dan batu melangkah berat menghampirimu.",
        "death_narration": "Jahitannya putus. Golem itu runtuh menjadi tumpukan daging dan debu yang menjijikkan."
    },
    {
        "name": "Volt Lurker", "element": "lightning", "weakness": "earth", "race": "anomaly", "attack_type": "magic",
        "base_hp": 2600, "p_atk": 40, "m_atk": 140, "p_def": 40, "m_def": 60, "speed": 10, "dodge_chance": 0.3, "crit_chance": 0.25, "crit_damage": 1.8,
        "status_resistance": {"paralyze": 1.0}, "ai_behavior": "trickster", "exp": 2550, "gold": 1250,
        "skill": {"name": "Static Discharge", "type": "paralyze", "chance": 0.35}, "drops": [{"id": "spark_plug", "chance": 1.0}],
        "entry_narration": "Percikan listrik menyambar-nyambar di udara kosong, perlahan membentuk siluet humanoid.",
        "death_narration": "Ledakan listrik membutakan matamu sejenak sebelum makhluk itu sirna."
    },
    {
        "name": "Void Assassin", "element": "void", "weakness": "light", "race": "cosmic", "attack_type": "physical",
        "base_hp": 2900, "p_atk": 145, "m_atk": 60, "p_def": 50, "m_def": 50, "speed": 8, "dodge_chance": 0.35, "crit_chance": 0.4, "crit_damage": 2.5,
        "status_resistance": {"blind": 1.0, "fear": 1.0}, "ai_behavior": "aggressive", "exp": 3200, "gold": 1800,
        "skill": {"name": "Dimension Strike", "type": "drain_all", "chance": 0.25}, "drops": [{"id": "void_dagger", "chance": 0.15}, {"id": "void_dust", "chance": 1.0}],
        "entry_narration": "Ruang di sekitarmu terdistorsi. Sesuatu yang tidak memiliki bentuk menempelkan bilah dingin di lehermu.",
        "death_narration": "Ia tertelan kembali ke dalam dimensi ketiadaan."
    }
]


MAIN_BOSS_POOL = [
    {
        "name": "THE KEEPER", "element": "void", "weakness": "light", "race": "cosmic", "attack_type": "magic",
        "base_hp": 8500, "p_atk": 120, "m_atk": 220, "p_def": 90, "m_def": 120, "speed": 8, "dodge_chance": 0.2, "crit_chance": 0.25, "crit_damage": 2.0,
        "status_resistance": {"all": 0.5, "stun": 1.0, "paralyze": 1.0}, "ai_behavior": "trickster", "exp": 10000, "gold": 5000,
        "skill": {"name": "Absolute Eradication", "type": "drain_all", "chance": 0.35}, "drops": [{"id": "keeper_crown", "chance": 1.0}, {"id": "void_grimoire", "chance": 0.5}],
        "entry_narration": "🌑 **KEGELAPAN MUTLAK.**\nPenjaga The Archivus telah bangkit. Matanya adalah dua lubang hitam yang menelan cahaya lentera milikmu. 'Tidak ada yang boleh keluar dari sini.'",
        "death_narration": "Tubuh raksasanya retak seperti kaca. 'Kau... telah merusak... perpustakaan ini...' The Keeper hancur menjadi serpihan bintang mati."
    },
    {
        "name": "ABYSSAL LEVIATHAN", "element": "water", "weakness": "lightning", "race": "beast", "attack_type": "physical",
        "base_hp": 12000, "p_atk": 240, "m_atk": 150, "p_def": 150, "m_def": 100, "speed": 4, "dodge_chance": 0.05, "crit_chance": 0.15, "crit_damage": 2.5,
        "status_resistance": {"freeze": 1.0, "bleed": 1.0}, "ai_behavior": "aggressive", "exp": 12000, "gold": 6000,
        "skill": {"name": "Tsunami of Despair", "type": "stun", "chance": 0.4}, "drops": [{"id": "leviathan_scale", "chance": 1.0}, {"id": "oceanic_trident", "chance": 0.3}],
        "entry_narration": "🌊 **BANJIR DARAH.**\nLantai Archivus hancur, digantikan oleh lautan tak berdasar. Paus kosmik raksasa muncul, membuka rahangnya yang siap menelan duniamu.",
        "death_narration": "Jeritan monster itu memekakkan telinga sebelum ia perlahan tenggelam ke dasar kegelapan abadi."
    },
    {
        "name": "THE ASHEN LORD", "element": "fire", "weakness": "water", "race": "undead", "attack_type": "magic",
        "base_hp": 7500, "p_atk": 160, "m_atk": 230, "p_def": 110, "m_def": 90, "speed": 7, "dodge_chance": 0.15, "crit_chance": 0.3, "crit_damage": 2.2,
        "status_resistance": {"burn": 1.0, "poison": 1.0}, "ai_behavior": "berserk", "exp": 11000, "gold": 5500,
        "skill": {"name": "Incinerate", "type": "burn", "chance": 0.5}, "drops": [{"id": "ashen_heart", "chance": 1.0}, {"id": "hellfire_blade", "chance": 0.4}],
        "entry_narration": "🔥 **NERAKA BOCOR.**\nRaja yang terbakar abadi ini melangkah keluar dari abu. Setiap langkahnya melelehkan batu di sekitarnya.",
        "death_narration": "Ia tertawa di tengah kobaran api. 'Setidaknya... aku merasa hangat...' Api itu akhirnya padam."
    },
    {
        "name": "CHRONOS DEVOURER", "element": "earth", "weakness": "ice", "race": "anomaly", "attack_type": "physical",
        "base_hp": 9000, "p_atk": 210, "m_atk": 100, "p_def": 180, "m_def": 150, "speed": 10, "dodge_chance": 0.25, "crit_chance": 0.2, "crit_damage": 1.8,
        "status_resistance": {"stun": 1.0, "paralyze": 1.0, "blind": 1.0}, "ai_behavior": "defensive", "exp": 13000, "gold": 7000,
        "skill": {"name": "Time Fracture", "type": "confuse", "chance": 0.35}, "drops": [{"id": "chronos_sand", "chance": 1.0}, {"id": "time_bender_ring", "chance": 0.25}],
        "entry_narration": "⏳ **WAKTU BERHENTI.**\nCacing tanah berlapis emas raksasa yang menelan jam pasir dimensi. Pergerakanmu terasa sangat melambat.",
        "death_narration": "Tubuhnya retak dan waktu melesat maju dengan cepat. Ia menua jutaan tahun dalam sedetik lalu hancur."
    },
    {
        "name": "THE FIRST WEAVER", "element": "light", "weakness": "dark", "race": "humanoid", "attack_type": "magic",
        "base_hp": 10000, "p_atk": 190, "m_atk": 250, "p_def": 130, "m_def": 160, "speed": 9, "dodge_chance": 0.3, "crit_chance": 0.3, "crit_damage": 2.5,
        "status_resistance": {"all": 0.8}, "ai_behavior": "trickster", "exp": 20000, "gold": 10000,
        "skill": {"name": "Erase Reality", "type": "drain_all", "chance": 0.4}, "drops": [{"id": "first_weaver_soul", "chance": 1.0}, {"id": "the_archivus_key", "chance": 1.0}],
        "entry_narration": "📜 **SANG PENCIPTA.**\nPemain pertama yang terjebak di game ini. Ia telah kehilangan kemanusiaannya. 'Kau tidak akan bisa menyelesaikan apa yang kumulai.'",
        "death_narration": "'Akhirnya... giliranku untuk log out...' Tubuhnya hancur menjadi barisan kode program hijau."
    }
]
