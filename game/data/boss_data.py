# game/data/mainboss_data.py

"""
DATABASE MAIN BOSS - The Archivus (RPG ADVANCED EDITION)
Ancaman level Dewa, Kosmik, dan Entitas Absolut pemegang kunci dimensi.
Masing-masing mewakili satu dari 10 elemen utama.
"""

MAIN_BOSS_POOL = [
    # 1. ELEMENT: VOID | RACE: COSMIC
    {
        "name": "THE KEEPER", "element": "void", "weakness": "light", "race": "cosmic", "attack_type": "magic",
        "base_hp": 8500, "p_atk": 120, "m_atk": 220, "p_def": 90, "m_def": 120, "speed": 8, "dodge_chance": 0.2, "crit_chance": 0.25, "crit_damage": 2.0,
        "status_resistance": {"all": 0.5, "stun": 1.0, "paralyze": 1.0}, "ai_behavior": "trickster", "exp": 10000, "gold": 5000,
        "skill": {"name": "Absolute Eradication", "type": "drain_all", "chance": 0.35}, "drops": [{"id": "keeper_crown", "chance": 1.0}, {"id": "void_grimoire", "chance": 0.5}],
        "entry_narration": "🌑 **KEGELAPAN MUTLAK.**\nPenjaga The Archivus telah bangkit. Matanya adalah dua lubang hitam yang menelan cahaya lentera milikmu. 'Tidak ada yang boleh keluar dari sini.'",
        "death_narration": "Tubuh raksasanya retak seperti kaca. 'Kau... telah merusak... perpustakaan ini...' The Keeper hancur menjadi serpihan bintang mati."
    },
    
    # 2. ELEMENT: WATER | RACE: BEAST
    {
        "name": "ABYSSAL LEVIATHAN", "element": "water", "weakness": "lightning", "race": "beast", "attack_type": "physical",
        "base_hp": 12000, "p_atk": 240, "m_atk": 150, "p_def": 150, "m_def": 100, "speed": 4, "dodge_chance": 0.05, "crit_chance": 0.15, "crit_damage": 2.5,
        "status_resistance": {"freeze": 1.0, "bleed": 1.0}, "ai_behavior": "aggressive", "exp": 12000, "gold": 6000,
        "skill": {"name": "Tsunami of Despair", "type": "stun", "chance": 0.4}, "drops": [{"id": "leviathan_scale", "chance": 1.0}, {"id": "oceanic_trident", "chance": 0.3}],
        "entry_narration": "🌊 **BANJIR DARAH.**\nLantai Archivus hancur, digantikan oleh lautan tak berdasar. Paus kosmik raksasa muncul, membuka rahangnya yang siap menelan duniamu.",
        "death_narration": "Jeritan monster itu memekakkan telinga sebelum ia perlahan tenggelam ke dasar kegelapan abadi."
    },
    
    # 3. ELEMENT: FIRE | RACE: UNDEAD
    {
        "name": "THE ASHEN LORD", "element": "fire", "weakness": "water", "race": "undead", "attack_type": "magic",
        "base_hp": 7500, "p_atk": 160, "m_atk": 230, "p_def": 110, "m_def": 90, "speed": 7, "dodge_chance": 0.15, "crit_chance": 0.3, "crit_damage": 2.2,
        "status_resistance": {"burn": 1.0, "poison": 1.0}, "ai_behavior": "berserk", "exp": 11000, "gold": 5500,
        "skill": {"name": "Incinerate", "type": "burn", "chance": 0.5}, "drops": [{"id": "ashen_heart", "chance": 1.0}, {"id": "hellfire_blade", "chance": 0.4}],
        "entry_narration": "🔥 **NERAKA BOCOR.**\nRaja yang terbakar abadi ini melangkah keluar dari abu. Setiap langkahnya melelehkan batu di sekitarnya.",
        "death_narration": "Ia tertawa di tengah kobaran api. 'Setidaknya... aku merasa hangat...' Api itu akhirnya padam."
    },
    
    # 4. ELEMENT: EARTH | RACE: ANOMALY
    {
        "name": "CHRONOS DEVOURER", "element": "earth", "weakness": "ice", "race": "anomaly", "attack_type": "physical",
        "base_hp": 9000, "p_atk": 210, "m_atk": 100, "p_def": 180, "m_def": 150, "speed": 10, "dodge_chance": 0.25, "crit_chance": 0.2, "crit_damage": 1.8,
        "status_resistance": {"stun": 1.0, "paralyze": 1.0, "blind": 1.0}, "ai_behavior": "defensive", "exp": 13000, "gold": 7000,
        "skill": {"name": "Time Fracture", "type": "confuse", "chance": 0.35}, "drops": [{"id": "chronos_sand", "chance": 1.0}, {"id": "time_bender_ring", "chance": 0.25}],
        "entry_narration": "⏳ **WAKTU BERHENTI.**\nCacing tanah berlapis emas raksasa yang menelan jam pasir dimensi. Pergerakanmu terasa sangat melambat.",
        "death_narration": "Tubuhnya retak dan waktu melesat maju dengan cepat. Ia menua jutaan tahun dalam sedetik lalu hancur."
    },
    
    # 5. ELEMENT: LIGHT | RACE: HUMANOID
    {
        "name": "THE FIRST WEAVER", "element": "light", "weakness": "dark", "race": "humanoid", "attack_type": "magic",
        "base_hp": 10000, "p_atk": 190, "m_atk": 250, "p_def": 130, "m_def": 160, "speed": 9, "dodge_chance": 0.3, "crit_chance": 0.3, "crit_damage": 2.5,
        "status_resistance": {"all": 0.8}, "ai_behavior": "trickster", "exp": 20000, "gold": 10000,
        "skill": {"name": "Erase Reality", "type": "drain_all", "chance": 0.4}, "drops": [{"id": "first_weaver_soul", "chance": 1.0}, {"id": "the_archivus_key", "chance": 1.0}],
        "entry_narration": "📜 **SANG PENCIPTA.**\nPemain pertama yang terjebak di game ini. Ia telah kehilangan kemanusiaannya. 'Kau tidak akan bisa menyelesaikan apa yang kumulai.'",
        "death_narration": "'Akhirnya... giliranku untuk log out...' Tubuhnya hancur menjadi barisan kode program hijau."
    },

    # ========================== TAMBAHAN BARU ==========================

    # 6. ELEMENT: POISON | RACE: SLIME
    {
        "name": "JAMES MARCUS ECHO", "element": "poison", "weakness": "fire", "race": "slime", "attack_type": "magic",
        "base_hp": 8200, "p_atk": 140, "m_atk": 240, "p_def": 100, "m_def": 150, "speed": 5, "dodge_chance": 0.1, "crit_chance": 0.2, "crit_damage": 1.8,
        "status_resistance": {"poison": 1.0, "bleed": 1.0, "blind": 0.5}, "ai_behavior": "defensive", "exp": 10500, "gold": 5200,
        "skill": {"name": "Progenitor Strain", "type": "poison", "chance": 0.55}, "drops": [{"id": "t_virus_vial", "chance": 1.0}, {"id": "leech_charm", "chance": 0.4}],
        "entry_narration": "🦠 **BIOLOGICAL HORROR.**\nRatusan lintah raksasa bergabung membentuk seorang pria berbaju putih. 'Dunia ini butuh tatanan evolusi baru!'",
        "death_narration": "Lintah-lintah itu meledak, menyisakan cairan asam yang berbau sangat menyengat."
    },

    # 7. ELEMENT: BLOOD | RACE: DEMON
    {
        "name": "ORPHAN OF THE ARCHIVES", "element": "blood", "weakness": "lightning", "race": "demon", "attack_type": "physical",
        "base_hp": 6800, "p_atk": 260, "m_atk": 100, "p_def": 120, "m_def": 80, "speed": 9, "dodge_chance": 0.35, "crit_chance": 0.4, "crit_damage": 3.0,
        "status_resistance": {"bleed": 1.0, "fear": 1.0}, "ai_behavior": "berserk", "exp": 11500, "gold": 5800,
        "skill": {"name": "Placenta Slam", "type": "bleed", "chance": 0.45}, "drops": [{"id": "orphan_umbilical_cord", "chance": 1.0}, {"id": "kos_parasite", "chance": 0.2}],
        "entry_narration": "🩸 **JERITAN BAYI.**\nBayi kosmik yang cacat merangkak lambat ke arahmu, menyeret senjata berdaging. Ia menangis memanggil ibunya.",
        "death_narration": "Ia kembali ke posisi janin, menangis pelan sebelum akhirnya terdiam selamanya."
    },

    # 8. ELEMENT: DARK | RACE: ANOMALY
    {
        "name": "NIGHTMARE INCARNATE", "element": "dark", "weakness": "light", "race": "anomaly", "attack_type": "magic",
        "base_hp": 7800, "p_atk": 90, "m_atk": 260, "p_def": 140, "m_def": 180, "speed": 8, "dodge_chance": 0.4, "crit_chance": 0.15, "crit_damage": 1.5,
        "status_resistance": {"fear": 1.0, "blind": 1.0, "stun": 0.5}, "ai_behavior": "trickster", "exp": 12500, "gold": 6500,
        "skill": {"name": "Sleep Paralysis", "type": "paralyze", "chance": 0.5}, "drops": [{"id": "nightmare_essence", "chance": 1.0}, {"id": "dreamcatcher_amulet", "chance": 0.35}],
        "entry_narration": "👁️ **TEROR PIKIRAN.**\nWujudnya terus berubah, mengambil bentuk trauma terdalam dan ketakutan terburuk yang pernah kau rasakan.",
        "death_narration": "Mimpi buruk itu memudar bagai asap, meninggalkan keringat dingin di tubuhmu."
    },

    # 9. ELEMENT: LIGHTNING | RACE: CONSTRUCT
    {
        "name": "CLOCKWORK LEVIATHAN", "element": "lightning", "weakness": "earth", "race": "construct", "attack_type": "physical",
        "base_hp": 11000, "p_atk": 220, "m_atk": 180, "p_def": 200, "m_def": 110, "speed": 3, "dodge_chance": 0.0, "crit_chance": 0.2, "crit_damage": 2.0,
        "status_resistance": {"poison": 1.0, "bleed": 1.0, "paralyze": 1.0}, "ai_behavior": "defensive", "exp": 14000, "gold": 7500,
        "skill": {"name": "Overcharge Protocol", "type": "armor_break", "chance": 0.4}, "drops": [{"id": "leviathan_gear", "chance": 1.0}, {"id": "tesla_coil", "chance": 0.4}],
        "entry_narration": "⚡ **MESIN KIAMAT.**\nNaga mekanik raksasa merobek dinding dimensi. Tubuhnya mengalirkan listrik jutaan volt yang membuat rambutmu berdiri.",
        "death_narration": "Roda giginya berhenti berputar. Naga itu meledak dalam kilatan cahaya biru yang membutakan."
    },

    # 10. ELEMENT: ICE | RACE: GOD
    {
        "name": "ECLIPSE SOVEREIGN", "element": "ice", "weakness": "fire", "race": "god", "attack_type": "magic",
        "base_hp": 9500, "p_atk": 150, "m_atk": 270, "p_def": 160, "m_def": 200, "speed": 6, "dodge_chance": 0.2, "crit_chance": 0.3, "crit_damage": 2.5,
        "status_resistance": {"freeze": 1.0, "burn": 0.5, "fear": 1.0}, "ai_behavior": "aggressive", "exp": 16000, "gold": 8000,
        "skill": {"name": "Absolute Zero Eclipse", "type": "freeze", "chance": 0.45}, "drops": [{"id": "sovereign_crown", "chance": 1.0}, {"id": "frozen_galaxy", "chance": 0.25}],
        "entry_narration": "❄️ **ZAMAN ES KOSMIK.**\nMatahari hitam bersinar dingin di atas kepalanya. Entitas ini tidak bernapas, namun auranya membekukan aliran darahmu.",
        "death_narration": "Mahkotanya hancur. Suhu ruangan kembali normal seiring memudarnya sang penguasa."
    }
]
