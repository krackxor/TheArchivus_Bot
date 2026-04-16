# game/data/monster_data.py

"""
DATABASE MONSTER - The Archivus (RPG ADVANCED EDITION)
Total: 100 Monster Detail (20 Monster per Tier untuk Tier 1-5)
Mencakup: Element, Weakness, Race, Physical/Magic Stats, Speed, Crit, Dodge, AI Behavior, dan Drops.

Daftar Elemen: "fire", "water", "ice", "lightning", "earth", "dark", "light", "void", "blood", "poison", "none"
Daftar Ras: "undead", "beast", "cosmic", "construct", "demon", "humanoid", "slime", "anomaly"
Daftar AI: "aggressive", "defensive", "trickster", "berserk"
"""

MONSTER_POOL = {
    # =========================================================================
    # TIER 1 (Hama Dimensi & Pecahan Memori)
    # =========================================================================
    1: [
        {
            "name": "The Weeping Shadow", "element": "dark", "weakness": "light", "race": "undead", "attack_type": "magic",
            "base_hp": 30, "p_atk": 2, "m_atk": 8, "p_def": 1, "m_def": 4, "speed": 4, "dodge_chance": 0.15, "crit_chance": 0.05, "crit_damage": 1.5,
            "status_resistance": {"blind": 0.8}, "ai_behavior": "trickster", "exp": 10, "gold": 5,
            "skill": {"name": "Tears of Despair", "type": "blind", "chance": 0.2}, "drops": [{"id": "potion_minor_heal", "chance": 0.1}],
            "entry_narration": "Bayangan di dindingmu merayap turun. Ia menangis menggunakan suaramu.", "death_narration": "Bayangan itu memudar, tapi kau merasa sebagian dari dirimu ikut hilang."
        },
        {
            "name": "The Forgotten Child", "element": "none", "weakness": "dark", "race": "undead", "attack_type": "physical",
            "base_hp": 25, "p_atk": 8, "m_atk": 2, "p_def": 2, "m_def": 2, "speed": 5, "dodge_chance": 0.2, "crit_chance": 0.15, "crit_damage": 1.8,
            "status_resistance": {"fear": 1.0}, "ai_behavior": "aggressive", "exp": 12, "gold": 8,
            "skill": {"name": "Ankle Bite", "type": "critical", "chance": 0.15}, "drops": [{"id": "candy_wrapper", "chance": 0.05}],
            "entry_narration": "Sesuatu kecil dan dingin menarik ujung bajumu dari arah bawah tempat tidur.", "death_narration": "Ia hancur menjadi debu abu-abu yang berbau seperti rumah masa kecilmu."
        },
        {
            "name": "Static Glitch", "element": "lightning", "weakness": "earth", "race": "anomaly", "attack_type": "magic",
            "base_hp": 20, "p_atk": 3, "m_atk": 10, "p_def": 1, "m_def": 5, "speed": 7, "dodge_chance": 0.25, "crit_chance": 0.1, "crit_damage": 2.0,
            "status_resistance": {"stun": 1.0, "paralyze": 1.0}, "ai_behavior": "trickster", "exp": 15, "gold": 10,
            "skill": {"name": "Screen Tearing", "type": "stun", "chance": 0.2}, "drops": [{"id": "glitch_dust", "chance": 0.2}],
            "entry_narration": "Teks di layar ini bergetar. Sesuatu mencoba merangkak keluar dari balik huruf-huruf ini.", "death_narration": "Teks kembali normal, tapi baterai HP-mu terasa lebih panas."
        },
        {
            "name": "Blind Whisper", "element": "void", "weakness": "light", "race": "cosmic", "attack_type": "magic",
            "base_hp": 35, "p_atk": 1, "m_atk": 9, "p_def": 1, "m_def": 6, "speed": 3, "dodge_chance": 0.1, "crit_chance": 0.05, "crit_damage": 1.5,
            "status_resistance": {"blind": 1.0}, "ai_behavior": "defensive", "exp": 8, "gold": 4,
            "skill": {"name": "Madness Murmur", "type": "drain_mp", "chance": 0.25}, "drops": [{"id": "potion_minor_mp", "chance": 0.15}],
            "entry_narration": "Kau tidak melihat apa-apa, tapi ada napas basah di telinga kirimu.", "death_narration": "Napas itu berhenti. Keheningan ini justru lebih mengerikan."
        },
        {
            "name": "Dust Mite", "element": "earth", "weakness": "fire", "race": "beast", "attack_type": "physical",
            "base_hp": 40, "p_atk": 6, "m_atk": 1, "p_def": 4, "m_def": 2, "speed": 2, "dodge_chance": 0.05, "crit_chance": 0.05, "crit_damage": 1.2,
            "status_resistance": {"poison": 0.5}, "ai_behavior": "defensive", "exp": 10, "gold": 5,
            "skill": {"name": "Choking Hazard", "type": "poison", "chance": 0.2}, "drops": [],
            "entry_narration": "Gumpalan debu seukuran anjing menatapmu dengan lusinan mata bayi.", "death_narration": "Debu itu pecah, masuk ke pori-pori kulitmu."
        },
        {
            "name": "Crawling Ink", "element": "poison", "weakness": "fire", "race": "slime", "attack_type": "magic",
            "base_hp": 25, "p_atk": 3, "m_atk": 7, "p_def": 2, "m_def": 3, "speed": 4, "dodge_chance": 0.1, "crit_chance": 0.05, "crit_damage": 1.5,
            "status_resistance": {"poison": 1.0}, "ai_behavior": "aggressive", "exp": 12, "gold": 6,
            "skill": {"name": "Toxic Splatter", "type": "poison", "chance": 0.25}, "drops": [{"id": "ink_vial", "chance": 0.3}],
            "entry_narration": "Tinta dari kalimat ini menetes ke bawah, membentuk cakar yang meraih jarimu.", "death_narration": "Tinta itu mengering dan membekas di nadimu."
        },
        {
            "name": "The Guilt Fragment", "element": "blood", "weakness": "lightning", "race": "undead", "attack_type": "magic",
            "base_hp": 45, "p_atk": 2, "m_atk": 8, "p_def": 2, "m_def": 5, "speed": 3, "dodge_chance": 0.05, "crit_chance": 0.05, "crit_damage": 1.5,
            "status_resistance": {"fear": 0.8}, "ai_behavior": "defensive", "exp": 14, "gold": 12,
            "skill": {"name": "Heavy Heart", "type": "drain_energy", "chance": 0.3}, "drops": [{"id": "teardrop_gem", "chance": 0.05}],
            "entry_narration": "Makhluk ini berwajah seperti orang yang pernah kau sakiti di masa lalu.", "death_narration": "Ia tersenyum saat kau membunuhnya. Kau akan mengingat senyum itu selamanya."
        },
        {
            "name": "Hollow Rat", "element": "poison", "weakness": "fire", "race": "beast", "attack_type": "physical",
            "base_hp": 20, "p_atk": 8, "m_atk": 1, "p_def": 1, "m_def": 1, "speed": 6, "dodge_chance": 0.2, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"poison": 0.5}, "ai_behavior": "aggressive", "exp": 8, "gold": 3,
            "skill": {"name": "Infectious Bite", "type": "poison", "chance": 0.2}, "drops": [{"id": "rat_tail", "chance": 0.4}],
            "entry_narration": "Tikus tanpa kulit merangkak mendekat. Terdengar detak jantungnya yang berisik.", "death_narration": "Tikus itu meledak menjadi cipratan darah hitam."
        },
        {
            "name": "Pale Slime", "element": "water", "weakness": "lightning", "race": "slime", "attack_type": "physical",
            "base_hp": 50, "p_atk": 5, "m_atk": 3, "p_def": 3, "m_def": 3, "speed": 2, "dodge_chance": 0.0, "crit_chance": 0.05, "crit_damage": 1.2,
            "status_resistance": {"burn": 0.5}, "ai_behavior": "defensive", "exp": 15, "gold": 5,
            "skill": {"name": "Acidic Embrace", "type": "armor_break", "chance": 0.15}, "drops": [{"id": "pale_mucus", "chance": 0.5}],
            "entry_narration": "Gumpalan lendir pucat yang bentuknya menyerupai organ dalam manusia bergetar pelan.", "death_narration": "Lendir itu mencair, meninggalkan bau busuk di hidungmu."
        },
        {
            "name": "The Peeping Eye", "element": "light", "weakness": "dark", "race": "anomaly", "attack_type": "magic",
            "base_hp": 15, "p_atk": 1, "m_atk": 12, "p_def": 1, "m_def": 2, "speed": 8, "dodge_chance": 0.3, "crit_chance": 0.2, "crit_damage": 2.0,
            "status_resistance": {"blind": 1.0}, "ai_behavior": "trickster", "exp": 18, "gold": 15,
            "skill": {"name": "Stare of the Abyss", "type": "stun", "chance": 0.3}, "drops": [{"id": "glass_eye", "chance": 0.1}],
            "entry_narration": "Satu bola mata raksasa melayang. Ia berkedip bersamaan dengan matamu.", "death_narration": "Mata itu pecah. Kau merasa matamu sendiri perih."
        },
        {
            "name": "Rust Crawler", "element": "earth", "weakness": "water", "race": "construct", "attack_type": "physical",
            "base_hp": 30, "p_atk": 7, "m_atk": 0, "p_def": 5, "m_def": 1, "speed": 3, "dodge_chance": 0.05, "crit_chance": 0.05, "crit_damage": 1.5,
            "status_resistance": {"poison": 1.0, "bleed": 1.0}, "ai_behavior": "aggressive", "exp": 11, "gold": 6,
            "skill": {"name": "Tetanus Scratch", "type": "poison", "chance": 0.2}, "drops": [{"id": "iron_scrap", "chance": 0.3}],
            "entry_narration": "Kutu raksasa berkarat merayap di langit-langit, menjatuhkan serpihan karat ke rambutmu.", "death_narration": "Kutu itu hancur berkeping-keping layaknya besi tua yang rapuh."
        },
        {
            "name": "Ash Whisper", "element": "fire", "weakness": "water", "race": "undead", "attack_type": "magic",
            "base_hp": 22, "p_atk": 2, "m_atk": 9, "p_def": 1, "m_def": 4, "speed": 5, "dodge_chance": 0.2, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"burn": 1.0}, "ai_behavior": "trickster", "exp": 13, "gold": 7,
            "skill": {"name": "Choking Ash", "type": "blind", "chance": 0.25}, "drops": [{"id": "ash_pile", "chance": 0.2}],
            "entry_narration": "Gumpalan abu yang masih menyimpan bara api melayang mendekat, membisikkan doa kematian.", "death_narration": "Abunya tertiup angin yang tak terlihat, hilang tanpa bekas."
        },
        {
            "name": "Fog Wisp", "element": "water", "weakness": "lightning", "race": "anomaly", "attack_type": "magic",
            "base_hp": 35, "p_atk": 1, "m_atk": 6, "p_def": 1, "m_def": 6, "speed": 6, "dodge_chance": 0.25, "crit_chance": 0.05, "crit_damage": 1.5,
            "status_resistance": {"freeze": 0.5}, "ai_behavior": "defensive", "exp": 9, "gold": 4,
            "skill": {"name": "Damp Chill", "type": "drain_energy", "chance": 0.2}, "drops": [{"id": "mist_essence", "chance": 0.15}],
            "entry_narration": "Kabut tebal berbentuk seperti tangan manusia mencoba mencekik lehermu.", "death_narration": "Kabut itu mengembun menjadi air yang menetes ke lantai."
        },
        {
            "name": "Blood Bat", "element": "blood", "weakness": "ice", "race": "beast", "attack_type": "physical",
            "base_hp": 18, "p_atk": 10, "m_atk": 2, "p_def": 1, "m_def": 1, "speed": 8, "dodge_chance": 0.2, "crit_chance": 0.15, "crit_damage": 1.5,
            "status_resistance": {"bleed": 1.0}, "ai_behavior": "aggressive", "exp": 14, "gold": 9,
            "skill": {"name": "Leech Fang", "type": "drain_hp", "chance": 0.3}, "drops": [{"id": "bat_wing", "chance": 0.25}],
            "entry_narration": "Kelelawar merah tanpa bulu meneteskan darah dari taringnya yang panjang.", "death_narration": "Kelelawar itu meledak kecil layaknya balon berisi darah."
        },
        {
            "name": "Hollow Mite", "element": "void", "weakness": "light", "race": "cosmic", "attack_type": "magic",
            "base_hp": 40, "p_atk": 1, "m_atk": 7, "p_def": 2, "m_def": 5, "speed": 5, "dodge_chance": 0.15, "crit_chance": 0.05, "crit_damage": 1.5,
            "status_resistance": {"blind": 0.5}, "ai_behavior": "trickster", "exp": 10, "gold": 5,
            "skill": {"name": "Empty Bite", "type": "drain_mp", "chance": 0.2}, "drops": [{"id": "void_dust", "chance": 0.1}],
            "entry_narration": "Serangga tak kasat mata menggigit kakimu. Kau hanya bisa melihat bekas gigitannya yang menghitam.", "death_narration": "Rasa gatal dan sakitnya lenyap seketika bersama kematiannya."
        },
        {
            "name": "Mirror Shard", "element": "light", "weakness": "dark", "race": "construct", "attack_type": "magic",
            "base_hp": 25, "p_atk": 2, "m_atk": 9, "p_def": 5, "m_def": 1, "speed": 4, "dodge_chance": 0.1, "crit_chance": 0.1, "crit_damage": 2.0,
            "status_resistance": {"blind": 1.0, "bleed": 1.0}, "ai_behavior": "defensive", "exp": 12, "gold": 8,
            "skill": {"name": "Reflect Agony", "type": "copy_atk", "chance": 0.25}, "drops": [{"id": "broken_mirror", "chance": 0.2}],
            "entry_narration": "Pecahan kaca melayang, menampilkan pantulan wajahmu yang sedang menjerit.", "death_narration": "Kaca itu pecah berkeping-keping. Pantulan menjerit itu terdiam."
        },
        {
            "name": "Decay Grub", "element": "poison", "weakness": "fire", "race": "beast", "attack_type": "physical",
            "base_hp": 45, "p_atk": 5, "m_atk": 2, "p_def": 2, "m_def": 3, "speed": 1, "dodge_chance": 0.0, "crit_chance": 0.05, "crit_damage": 1.2,
            "status_resistance": {"poison": 1.0}, "ai_behavior": "defensive", "exp": 16, "gold": 7,
            "skill": {"name": "Putrid Stench", "type": "poison", "chance": 0.3}, "drops": [{"id": "grub_meat", "chance": 0.4}],
            "entry_narration": "Ulat seukuran lengan orang dewasa merayap pelan, meninggalkan lendir berbau bangkai.", "death_narration": "Ulat itu mengering dan keriput dalam hitungan detik."
        },
        {
            "name": "Frost Centipede", "element": "ice", "weakness": "fire", "race": "beast", "attack_type": "physical",
            "base_hp": 30, "p_atk": 7, "m_atk": 4, "p_def": 2, "m_def": 3, "speed": 6, "dodge_chance": 0.15, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"freeze": 1.0}, "ai_behavior": "aggressive", "exp": 15, "gold": 10,
            "skill": {"name": "Numbing Bite", "type": "paralyze", "chance": 0.25}, "drops": [{"id": "frost_leg", "chance": 0.3}],
            "entry_narration": "Kelabang putih transparan merayap di sepatumu. Suhu sekitarnya turun drastis.", "death_narration": "Kelabang itu hancur menjadi serpihan es."
        },
        {
            "name": "Spark Fly", "element": "lightning", "weakness": "water", "race": "beast", "attack_type": "magic",
            "base_hp": 15, "p_atk": 1, "m_atk": 12, "p_def": 1, "m_def": 2, "speed": 9, "dodge_chance": 0.3, "crit_chance": 0.2, "crit_damage": 1.5,
            "status_resistance": {"paralyze": 1.0, "stun": 0.5}, "ai_behavior": "trickster", "exp": 17, "gold": 12,
            "skill": {"name": "Jolt", "type": "stun", "chance": 0.2}, "drops": [{"id": "spark_plug", "chance": 0.1}],
            "entry_narration": "Serangga bercahaya menyetrum udara dengan suara bising yang menusuk telinga.", "death_narration": "Lampu kecil di perutnya padam selamanya setelah kilatan terakhir."
        },
        {
            "name": "Mud Leech", "element": "earth", "weakness": "ice", "race": "slime", "attack_type": "physical",
            "base_hp": 38, "p_atk": 6, "m_atk": 1, "p_def": 3, "m_def": 2, "speed": 2, "dodge_chance": 0.05, "crit_chance": 0.05, "crit_damage": 1.2,
            "status_resistance": {"poison": 0.5}, "ai_behavior": "berserk", "exp": 12, "gold": 6,
            "skill": {"name": "Suck Dry", "type": "drain_hp", "chance": 0.35}, "drops": [{"id": "mud_clump", "chance": 0.5}],
            "entry_narration": "Lintah raksasa berlapis lumpur tebal menempel di dinding, mencari kehangatan tubuhmu.", "death_narration": "Lintah itu mengeras menjadi tanah liat tak bernyawa."
        }
    ],

    # =========================================================================
    # TIER 2 (Prajurit Jatuh & Bekas Weaver)
    # =========================================================================
    2: [
        {
            "name": "Faceless Scribe", "element": "dark", "weakness": "light", "race": "humanoid", "attack_type": "magic",
            "base_hp": 60, "p_atk": 4, "m_atk": 18, "p_def": 3, "m_def": 6, "speed": 5, "dodge_chance": 0.1, "crit_chance": 0.15, "crit_damage": 2.0,
            "status_resistance": {"blind": 0.8}, "ai_behavior": "trickster", "exp": 30, "gold": 25,
            "skill": {"name": "Death Sentence", "type": "critical", "chance": 0.2}, "drops": [{"id": "potion_minor_mp", "chance": 0.2}],
            "entry_narration": "Makhluk berjubah tanpa wajah memegang pena yang terbuat dari tulang iga.", "death_narration": "Jubahnya runtuh. Tidak ada tubuh di dalamnya."
        },
        {
            "name": "Memory Parasite", "element": "void", "weakness": "lightning", "race": "anomaly", "attack_type": "magic",
            "base_hp": 50, "p_atk": 5, "m_atk": 16, "p_def": 2, "m_def": 8, "speed": 6, "dodge_chance": 0.2, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"stun": 0.5}, "ai_behavior": "aggressive", "exp": 35, "gold": 20,
            "skill": {"name": "Brain Leach", "type": "drain_mp", "chance": 0.3}, "drops": [{"id": "memory_shard", "chance": 0.15}],
            "entry_narration": "Cacing berduri melesat masuk ke telingamu, mencoba memakan ingatan bahagiamu.", "death_narration": "Kau memuntahkan cacing itu. Sayangnya, memori bahagiamu sudah tertelan."
        },
        {
            "name": "Shattered Knight", "element": "earth", "weakness": "water", "race": "undead", "attack_type": "physical",
            "base_hp": 80, "p_atk": 15, "m_atk": 0, "p_def": 10, "m_def": 2, "speed": 3, "dodge_chance": 0.0, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"bleed": 1.0, "poison": 1.0}, "ai_behavior": "berserk", "exp": 40, "gold": 35,
            "skill": {"name": "Rusty Cleave", "type": "bleed", "chance": 0.25}, "drops": [{"id": "iron_scrap", "chance": 0.4}],
            "entry_narration": "Armor berkarat berjalan terseok-seok. Darah terus mengalir dari celah helmnya.", "death_narration": "Armor itu hancur menjadi serpihan logam tajam."
        },
        {
            "name": "The Hanged Weaver", "element": "dark", "weakness": "fire", "race": "undead", "attack_type": "physical",
            "base_hp": 40, "p_atk": 22, "m_atk": 5, "p_def": 3, "m_def": 4, "speed": 7, "dodge_chance": 0.15, "crit_chance": 0.2, "crit_damage": 1.8,
            "status_resistance": {"fear": 1.0, "stun": 0.5}, "ai_behavior": "aggressive", "exp": 35, "gold": 15,
            "skill": {"name": "Desperate Thrash", "type": "multi_hit", "chance": 0.25}, "drops": [{"id": "hangman_rope", "chance": 0.1}],
            "entry_narration": "Mayat Weaver tergantung di langit-langit. Lehernya patah, tapi tangannya memegang pedang.", "death_narration": "Talinya putus. Ia akhirnya beristirahat."
        },
        {
            "name": "Echo Phantom", "element": "ice", "weakness": "fire", "race": "undead", "attack_type": "magic",
            "base_hp": 45, "p_atk": 2, "m_atk": 17, "p_def": 1, "m_def": 8, "speed": 6, "dodge_chance": 0.25, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"freeze": 1.0, "bleed": 1.0}, "ai_behavior": "trickster", "exp": 30, "gold": 30,
            "skill": {"name": "Frost Scream", "type": "stun", "chance": 0.2}, "drops": [{"id": "potion_minor_heal", "chance": 0.2}],
            "entry_narration": "Hantu es ini terus mengulang kata terakhir yang kau ketik di chat telegram ini.", "death_narration": "Suaramu sendiri menjerit saat ia mencair."
        },
        {
            "name": "Corrupted Marionette", "element": "earth", "weakness": "fire", "race": "construct", "attack_type": "physical",
            "base_hp": 70, "p_atk": 14, "m_atk": 5, "p_def": 6, "m_def": 4, "speed": 4, "dodge_chance": 0.1, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"poison": 1.0, "bleed": 1.0}, "ai_behavior": "defensive", "exp": 45, "gold": 25,
            "skill": {"name": "Tangled Strings", "type": "bind", "chance": 0.25}, "drops": [{"id": "cursed_wood", "chance": 0.3}],
            "entry_narration": "Boneka kayu seukuran manusia bergerak dengan sendi yang patah. 'Peluk aku...' bisiknya.", "death_narration": "Kayunya terbakar menjadi abu hitam."
        },
        {
            "name": "Glitch Zombie", "element": "lightning", "weakness": "earth", "race": "anomaly", "attack_type": "physical",
            "base_hp": 55, "p_atk": 16, "m_atk": 8, "p_def": 4, "m_def": 5, "speed": 5, "dodge_chance": 0.2, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"paralyze": 1.0}, "ai_behavior": "berserk", "exp": 50, "gold": 40,
            "skill": {"name": "Data Corruption", "type": "drain_hp", "chance": 0.3}, "drops": [{"id": "glitch_dust", "chance": 0.4}],
            "entry_narration": "Tubuhnya berkedip antara mayat membusuk dan sekumpulan kode error biner.", "death_narration": "Ia terhapus (deleted) dari eksistensi, meninggalkan bau ozon."
        },
        {
            "name": "Blood Hound", "element": "blood", "weakness": "lightning", "race": "beast", "attack_type": "physical",
            "base_hp": 65, "p_atk": 18, "m_atk": 2, "p_def": 3, "m_def": 3, "speed": 8, "dodge_chance": 0.15, "crit_chance": 0.2, "crit_damage": 1.8,
            "status_resistance": {"bleed": 0.5}, "ai_behavior": "aggressive", "exp": 40, "gold": 20,
            "skill": {"name": "Rabid Bite", "type": "bleed", "chance": 0.35}, "drops": [{"id": "hound_fang", "chance": 0.25}],
            "entry_narration": "Anjing liar tanpa kulit mengendus ketakutanmu. Air liurnya adalah asam.", "death_narration": "Ia melolong panjang sebelum hancur menjadi genangan darah."
        },
        {
            "name": "Blind Swordsman", "element": "none", "weakness": "poison", "race": "humanoid", "attack_type": "physical",
            "base_hp": 75, "p_atk": 20, "m_atk": 0, "p_def": 5, "m_def": 5, "speed": 6, "dodge_chance": 0.2, "crit_chance": 0.25, "crit_damage": 2.5,
            "status_resistance": {"blind": 1.0}, "ai_behavior": "defensive", "exp": 60, "gold": 50,
            "skill": {"name": "Iaijutsu", "type": "critical", "chance": 0.25}, "drops": [{"id": "broken_blade", "chance": 0.2}],
            "entry_narration": "Matanya dijahit rapat, namun pedangnya mengarah tepat ke lehermu dengan presisi mutlak.", "death_narration": "Pedangnya patah, ia tersungkur dan berubah menjadi debu."
        },
        {
            "name": "The Observer's Hand", "element": "void", "weakness": "light", "race": "anomaly", "attack_type": "physical",
            "base_hp": 90, "p_atk": 12, "m_atk": 6, "p_def": 6, "m_def": 4, "speed": 3, "dodge_chance": 0.05, "crit_chance": 0.05, "crit_damage": 1.5,
            "status_resistance": {"stun": 0.8}, "ai_behavior": "aggressive", "exp": 55, "gold": 45,
            "skill": {"name": "Crushing Grip", "type": "stun", "chance": 0.2}, "drops": [{"id": "buy_key_iron", "chance": 0.05}],
            "entry_narration": "Satu tangan raksasa merangkak dari kegelapan, mencoba meremas paru-parumu.", "death_narration": "Tangan itu meleleh seperti lilin."
        },
        {
            "name": "Rust Golem", "element": "earth", "weakness": "water", "race": "construct", "attack_type": "physical",
            "base_hp": 85, "p_atk": 14, "m_atk": 0, "p_def": 12, "m_def": 2, "speed": 2, "dodge_chance": 0.0, "crit_chance": 0.05, "crit_damage": 1.5,
            "status_resistance": {"poison": 1.0, "bleed": 1.0, "blind": 1.0}, "ai_behavior": "defensive", "exp": 45, "gold": 30,
            "skill": {"name": "Iron Smash", "type": "armor_break", "chance": 0.3}, "drops": [{"id": "iron_scrap", "chance": 0.5}],
            "entry_narration": "Tumpukan perlengkapan zirah rongsok membentuk tubuh manusia tanpa daging.", "death_narration": "Baut-bautnya lepas, menyisakan gundukan besi rongsok."
        },
        {
            "name": "Plague Doctor", "element": "poison", "weakness": "fire", "race": "humanoid", "attack_type": "magic",
            "base_hp": 55, "p_atk": 5, "m_atk": 15, "p_def": 3, "m_def": 8, "speed": 5, "dodge_chance": 0.15, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"poison": 1.0}, "ai_behavior": "trickster", "exp": 48, "gold": 35,
            "skill": {"name": "Miasma Flask", "type": "poison", "chance": 0.4}, "drops": [{"id": "poison_vial", "chance": 0.3}],
            "entry_narration": "Sosok bertopeng gagak mengamatimu. 'Pasien ini tidak bisa diselamatkan,' gumamnya pelan.", "death_narration": "Topengnya pecah, tidak ada wajah di baliknya."
        },
        {
            "name": "Ash Walker", "element": "fire", "weakness": "water", "race": "undead", "attack_type": "physical",
            "base_hp": 50, "p_atk": 16, "m_atk": 8, "p_def": 2, "m_def": 3, "speed": 6, "dodge_chance": 0.1, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"burn": 1.0}, "ai_behavior": "aggressive", "exp": 55, "gold": 25,
            "skill": {"name": "Burning Touch", "type": "burn", "chance": 0.3}, "drops": [{"id": "ash_pile", "chance": 0.4}],
            "entry_narration": "Manusia yang sekujur tubuhnya terbakar api abadi. Tercium bau daging gosong.", "death_narration": "Ia rubuh, hancur menjadi arang hitam yang rapuh."
        },
        {
            "name": "Drowned Corpse", "element": "water", "weakness": "lightning", "race": "undead", "attack_type": "physical",
            "base_hp": 70, "p_atk": 13, "m_atk": 5, "p_def": 4, "m_def": 4, "speed": 3, "dodge_chance": 0.05, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"bleed": 1.0}, "ai_behavior": "defensive", "exp": 42, "gold": 28,
            "skill": {"name": "Suffocate", "type": "drain_energy", "chance": 0.35}, "drops": [{"id": "water_essence", "chance": 0.2}],
            "entry_narration": "Mayat bengkak dipenuhi air meneteskan cairan amis ke lantai.", "death_narration": "Tubuhnya pecah seperti kantung air yang ditusuk jarum."
        },
        {
            "name": "Frostbite Ghoul", "element": "ice", "weakness": "fire", "race": "undead", "attack_type": "physical",
            "base_hp": 65, "p_atk": 14, "m_atk": 6, "p_def": 3, "m_def": 5, "speed": 5, "dodge_chance": 0.1, "crit_chance": 0.15, "crit_damage": 1.5,
            "status_resistance": {"freeze": 1.0}, "ai_behavior": "berserk", "exp": 44, "gold": 32,
            "skill": {"name": "Chilling Bite", "type": "paralyze", "chance": 0.25}, "drops": [{"id": "frozen_tear", "chance": 0.25}],
            "entry_narration": "Ghoul biru dengan tubuh membeku menatapmu lapar. Hawa dingin memancar dari kulitnya.", "death_narration": "Ia membeku sepenuhnya dan hancur berkeping-keping."
        },
        {
            "name": "Void Specter", "element": "void", "weakness": "light", "race": "cosmic", "attack_type": "magic",
            "base_hp": 48, "p_atk": 2, "m_atk": 18, "p_def": 2, "m_def": 8, "speed": 6, "dodge_chance": 0.2, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"blind": 0.8}, "ai_behavior": "trickster", "exp": 52, "gold": 38,
            "skill": {"name": "Soul Drain", "type": "drain_hp", "chance": 0.3}, "drops": [{"id": "void_dust", "chance": 0.3}],
            "entry_narration": "Sosok astral tanpa kaki melayang. Ia menyerap sisa cahaya di ruanganmu.", "death_narration": "Ia ditarik paksa ke dalam ketiadaan dimensi."
        },
        {
            "name": "Radiant Zealot", "element": "light", "weakness": "dark", "race": "humanoid", "attack_type": "physical",
            "base_hp": 62, "p_atk": 16, "m_atk": 10, "p_def": 5, "m_def": 5, "speed": 5, "dodge_chance": 0.1, "crit_chance": 0.15, "crit_damage": 1.5,
            "status_resistance": {"fear": 1.0}, "ai_behavior": "aggressive", "exp": 58, "gold": 45,
            "skill": {"name": "Blinding Judgment", "type": "blind", "chance": 0.3}, "drops": [{"id": "radiant_gem", "chance": 0.2}],
            "entry_narration": "Prajurit bercahaya fanatik ini menganggapmu sebagai iblis yang harus dihabisi.", "death_narration": "Cahayanya padam, meninggalkan mayat pendeta biasa."
        },
        {
            "name": "Bleeding Statue", "element": "blood", "weakness": "ice", "race": "construct", "attack_type": "physical",
            "base_hp": 85, "p_atk": 12, "m_atk": 4, "p_def": 8, "m_def": 4, "speed": 2, "dodge_chance": 0.0, "crit_chance": 0.05, "crit_damage": 1.5,
            "status_resistance": {"bleed": 1.0, "poison": 1.0}, "ai_behavior": "defensive", "exp": 46, "gold": 22,
            "skill": {"name": "Blood Curse", "type": "bleed", "chance": 0.4}, "drops": [{"id": "blood_vial", "chance": 0.3}],
            "entry_narration": "Patung batu pualam yang menangis dan berkeringat darah segar mulai berjalan mendekatimu.", "death_narration": "Patung itu runtuh, menumpahkan darah busuk ke lantai."
        },
        {
            "name": "Toxic Sludge", "element": "poison", "weakness": "fire", "race": "slime", "attack_type": "magic",
            "base_hp": 75, "p_atk": 8, "m_atk": 14, "p_def": 4, "m_def": 6, "speed": 3, "dodge_chance": 0.05, "crit_chance": 0.05, "crit_damage": 1.2,
            "status_resistance": {"poison": 1.0}, "ai_behavior": "defensive", "exp": 38, "gold": 18,
            "skill": {"name": "Acid Spray", "type": "armor_break", "chance": 0.25}, "drops": [{"id": "poison_vial", "chance": 0.4}],
            "entry_narration": "Genangan racun bergerak seperti cacing raksasa, mengikis lantai pijakannya.", "death_narration": "Lendir itu menguap menjadi gas bau yang tidak berbahaya."
        },
        {
            "name": "Static Anomaly", "element": "lightning", "weakness": "earth", "race": "anomaly", "attack_type": "magic",
            "base_hp": 40, "p_atk": 2, "m_atk": 22, "p_def": 2, "m_def": 8, "speed": 8, "dodge_chance": 0.25, "crit_chance": 0.15, "crit_damage": 1.8,
            "status_resistance": {"paralyze": 1.0, "stun": 0.5}, "ai_behavior": "berserk", "exp": 60, "gold": 42,
            "skill": {"name": "Shockwave", "type": "stun", "chance": 0.35}, "drops": [{"id": "spark_plug", "chance": 0.35}],
            "entry_narration": "Distorsi ruang memunculkan petir yang bergerak tak terkendali di ruangan.", "death_narration": "Kilatan besar terjadi, lalu ruangan kembali hening."
        }
    ],

    # =========================================================================
    # TIER 3 (Predator Dimensi & Sorcerer)
    # =========================================================================
    3: [
        {
            "name": "The Soul Butcher", "element": "blood", "weakness": "light", "race": "demon", "attack_type": "physical",
            "base_hp": 120, "p_atk": 30, "m_atk": 5, "p_def": 8, "m_def": 6, "speed": 4, "dodge_chance": 0.05, "crit_chance": 0.15, "crit_damage": 2.0,
            "status_resistance": {"fear": 1.0}, "ai_behavior": "aggressive", "exp": 100, "gold": 80,
            "skill": {"name": "Mince Meat", "type": "bleed", "chance": 0.35}, "drops": [{"id": "blood_crystal", "chance": 0.1}],
            "entry_narration": "Makhluk gempal dengan kapak jagal menatapmu. 'Daging Weaver selalu yang paling manis.'", "death_narration": "Tubuhnya meledak menjadi hujan daging busuk."
        },
        {
            "name": "Crimson Wraith", "element": "blood", "weakness": "ice", "race": "undead", "attack_type": "magic",
            "base_hp": 90, "p_atk": 5, "m_atk": 35, "p_def": 3, "m_def": 12, "speed": 7, "dodge_chance": 0.2, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"bleed": 1.0}, "ai_behavior": "trickster", "exp": 110, "gold": 90,
            "skill": {"name": "Blood Boil", "type": "burn", "chance": 0.3}, "drops": [{"id": "blood_vial", "chance": 0.4}],
            "entry_narration": "Sosok melayang yang terbuat sepenuhnya dari darah yang mendidih.", "death_narration": "Darahnya menguap, meninggalkan noda merah di layarmu."
        },
        {
            "name": "The Grief Lurker", "element": "void", "weakness": "light", "race": "anomaly", "attack_type": "magic",
            "base_hp": 150, "p_atk": 8, "m_atk": 25, "p_def": 5, "m_def": 10, "speed": 3, "dodge_chance": 0.1, "crit_chance": 0.05, "crit_damage": 1.5,
            "status_resistance": {"blind": 0.5}, "ai_behavior": "defensive", "exp": 120, "gold": 70,
            "skill": {"name": "Sorrow's Weight", "type": "drain_energy", "chance": 0.4}, "drops": [{"id": "void_stone", "chance": 0.1}],
            "entry_narration": "Ia tidak memiliki mata, hanya mulut yang memuntahkan penyesalan terdalammu.", "death_narration": "Mulutnya tertutup rapat. Ia mencekik dirinya sendiri."
        },
        {
            "name": "Memory Weaver", "element": "dark", "weakness": "fire", "race": "beast", "attack_type": "physical",
            "base_hp": 110, "p_atk": 28, "m_atk": 15, "p_def": 6, "m_def": 6, "speed": 6, "dodge_chance": 0.15, "crit_chance": 0.2, "crit_damage": 1.8,
            "status_resistance": {"bind": 1.0}, "ai_behavior": "trickster", "exp": 130, "gold": 100,
            "skill": {"name": "Nerve Strike", "type": "paralyze", "chance": 0.25}, "drops": [{"id": "spider_silk", "chance": 0.3}],
            "entry_narration": "Sosok laba-laba raksasa bertenun menggunakan saraf tulang belakang manusia.", "death_narration": "Saraf itu putus, laba-laba itu hancur menjadi debu tulang."
        },
        {
            "name": "Hexed Gargoyle", "element": "earth", "weakness": "water", "race": "construct", "attack_type": "physical",
            "base_hp": 180, "p_atk": 22, "m_atk": 8, "p_def": 15, "m_def": 5, "speed": 3, "dodge_chance": 0.05, "crit_chance": 0.05, "crit_damage": 1.5,
            "status_resistance": {"poison": 1.0, "bleed": 1.0}, "ai_behavior": "defensive", "exp": 140, "gold": 110,
            "skill": {"name": "Stone Gaze", "type": "stun", "chance": 0.2}, "drops": [{"id": "gargoyle_stone", "chance": 0.5}],
            "entry_narration": "Patung batu merobek kulit batunya sendiri, memperlihatkan otot merah di dalamnya.", "death_narration": "Ia kembali membatu, tapi wajahnya kini menyerupai wajahmu."
        },
        {
            "name": "Tormented Illusion", "element": "light", "weakness": "dark", "race": "anomaly", "attack_type": "magic",
            "base_hp": 80, "p_atk": 5, "m_atk": 40, "p_def": 2, "m_def": 12, "speed": 7, "dodge_chance": 0.25, "crit_chance": 0.15, "crit_damage": 2.0,
            "status_resistance": {"blind": 1.0}, "ai_behavior": "trickster", "exp": 150, "gold": 120,
            "skill": {"name": "Mirror Strike", "type": "copy_atk", "chance": 0.35}, "drops": [{"id": "broken_mirror", "chance": 0.2}],
            "entry_narration": "Cermin pecah muncul di udara. Pantulanmu sendiri keluar dan mencoba mencekikmu.", "death_narration": "Cermin itu hancur. Kau takkan pernah bisa melihat pantulanmu dengan tenang lagi."
        },
        {
            "name": "Tomb Banshee", "element": "dark", "weakness": "light", "race": "undead", "attack_type": "magic",
            "base_hp": 100, "p_atk": 4, "m_atk": 32, "p_def": 3, "m_def": 10, "speed": 6, "dodge_chance": 0.2, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"fear": 1.0}, "ai_behavior": "aggressive", "exp": 115, "gold": 85,
            "skill": {"name": "Death Wail", "type": "drain_mp", "chance": 0.4}, "drops": [{"id": "banshee_tear", "chance": 0.2}],
            "entry_narration": "Jeritannya menembus speaker HP-mu, membuat telingamu berdenging secara fisik.", "death_narration": "Jeritannya berubah menjadi tawa kecil sebelum ia menghilang."
        },
        {
            "name": "Shadow Sorcerer", "element": "dark", "weakness": "light", "race": "humanoid", "attack_type": "magic",
            "base_hp": 95, "p_atk": 8, "m_atk": 38, "p_def": 4, "m_def": 15, "speed": 5, "dodge_chance": 0.15, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"blind": 0.5}, "ai_behavior": "defensive", "exp": 160, "gold": 130,
            "skill": {"name": "Dark Void", "type": "blind", "chance": 0.3}, "drops": [{"id": "sorcerer_cloak", "chance": 0.05}],
            "entry_narration": "Penyihir berjubah kegelapan mengutuk namamu mundur, merusak kewarasanmu.", "death_narration": "Ia tersedot ke dalam lubang bayangannya sendiri."
        },
        {
            "name": "The Skin Stealer", "element": "blood", "weakness": "fire", "race": "demon", "attack_type": "physical",
            "base_hp": 130, "p_atk": 25, "m_atk": 5, "p_def": 6, "m_def": 5, "speed": 6, "dodge_chance": 0.1, "crit_chance": 0.2, "crit_damage": 1.8,
            "status_resistance": {"bleed": 0.5}, "ai_behavior": "aggressive", "exp": 125, "gold": 95,
            "skill": {"name": "Flay", "type": "bleed", "chance": 0.35}, "drops": [{"id": "potion_max_heal", "chance": 0.1}],
            "entry_narration": "Ia berjalan telanjang. 'Kulitmu sangat pas ukurannya denganku... berikan.'", "death_narration": "Ia mengelupas dan hancur seperti kertas basah."
        },
        {
            "name": "Phantom Executioner", "element": "dark", "weakness": "light", "race": "undead", "attack_type": "physical",
            "base_hp": 160, "p_atk": 35, "m_atk": 0, "p_def": 10, "m_def": 8, "speed": 3, "dodge_chance": 0.05, "crit_chance": 0.25, "crit_damage": 2.5,
            "status_resistance": {"stun": 0.5}, "ai_behavior": "berserk", "exp": 180, "gold": 150,
            "skill": {"name": "Guillotine Drop", "type": "critical", "chance": 0.2}, "drops": [{"id": "executioner_axe", "chance": 0.05}],
            "entry_narration": "Hantu raksasa membawa *Guillotine* di punggungnya.", "death_narration": "Pisau pancung itu jatuh mengenai lehernya sendiri."
        },
        {
            "name": "Magma Behemoth", "element": "fire", "weakness": "water", "race": "demon", "attack_type": "physical",
            "base_hp": 190, "p_atk": 28, "m_atk": 15, "p_def": 12, "m_def": 6, "speed": 2, "dodge_chance": 0.0, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"burn": 1.0, "poison": 1.0}, "ai_behavior": "aggressive", "exp": 155, "gold": 115,
            "skill": {"name": "Eruption", "type": "burn", "chance": 0.35}, "drops": [{"id": "ember_core", "chance": 0.2}],
            "entry_narration": "Batu cair panas membentuk gorila raksasa yang siap memanggang tubuhmu.", "death_narration": "Magma itu mendingin dan mengeras menjadi obsidian rapuh."
        },
        {
            "name": "Abyssal Crawler", "element": "water", "weakness": "lightning", "race": "beast", "attack_type": "physical",
            "base_hp": 140, "p_atk": 32, "m_atk": 10, "p_def": 14, "m_def": 8, "speed": 4, "dodge_chance": 0.05, "crit_chance": 0.15, "crit_damage": 1.5,
            "status_resistance": {"freeze": 0.5}, "ai_behavior": "defensive", "exp": 135, "gold": 105,
            "skill": {"name": "Deep Crush", "type": "armor_break", "chance": 0.3}, "drops": [{"id": "abyssal_pearl", "chance": 0.15}],
            "entry_narration": "Kepiting laut dalam raksasa merayap keluar dari genangan air gelap di lantai.", "death_narration": "Cangkangnya retak, memuntahkan air asin hitam."
        },
        {
            "name": "Glacial Predator", "element": "ice", "weakness": "fire", "race": "beast", "attack_type": "physical",
            "base_hp": 130, "p_atk": 35, "m_atk": 12, "p_def": 6, "m_def": 10, "speed": 8, "dodge_chance": 0.2, "crit_chance": 0.2, "crit_damage": 2.0,
            "status_resistance": {"freeze": 1.0}, "ai_behavior": "aggressive", "exp": 145, "gold": 125,
            "skill": {"name": "Frostbite", "type": "paralyze", "chance": 0.35}, "drops": [{"id": "ice_blade_fragment", "chance": 0.15}],
            "entry_narration": "Singa es dengan taring memanjang berlari kencang tanpa mengeluarkan suara.", "death_narration": "Singa itu pecah menjadi butiran salju yang menusuk."
        },
        {
            "name": "Storm Caller", "element": "lightning", "weakness": "earth", "race": "humanoid", "attack_type": "magic",
            "base_hp": 110, "p_atk": 10, "m_atk": 42, "p_def": 4, "m_def": 12, "speed": 6, "dodge_chance": 0.15, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"paralyze": 1.0}, "ai_behavior": "trickster", "exp": 165, "gold": 140,
            "skill": {"name": "Thunder Strike", "type": "stun", "chance": 0.25}, "drops": [{"id": "spark_plug", "chance": 0.4}],
            "entry_narration": "Dukun dengan mata bercahaya putih memanggil petir langsung ke dalam ruangan ini.", "death_narration": "Petirnya menyambar dirinya sendiri, mengubahnya menjadi abu."
        },
        {
            "name": "Toxic Hydra", "element": "poison", "weakness": "fire", "race": "beast", "attack_type": "physical",
            "base_hp": 170, "p_atk": 28, "m_atk": 15, "p_def": 8, "m_def": 8, "speed": 4, "dodge_chance": 0.05, "crit_chance": 0.15, "crit_damage": 1.5,
            "status_resistance": {"poison": 1.0}, "ai_behavior": "berserk", "exp": 175, "gold": 160,
            "skill": {"name": "Venom Fangs", "type": "poison", "chance": 0.45}, "drops": [{"id": "poison_vial", "chance": 0.5}],
            "entry_narration": "Ular berkepala tiga yang tersusun dari lendir hijau meneteskan bisa ke lantai.", "death_narration": "Ketiga kepalanya saling memakan hingga habis."
        },
        {
            "name": "Void Stalker", "element": "void", "weakness": "light", "race": "cosmic", "attack_type": "physical",
            "base_hp": 125, "p_atk": 36, "m_atk": 14, "p_def": 5, "m_def": 10, "speed": 9, "dodge_chance": 0.3, "crit_chance": 0.25, "crit_damage": 2.0,
            "status_resistance": {"blind": 0.5}, "ai_behavior": "trickster", "exp": 150, "gold": 130,
            "skill": {"name": "Phase Shift", "type": "blind", "chance": 0.3}, "drops": [{"id": "void_dust", "chance": 0.3}],
            "entry_narration": "Sosok ramping setinggi langit-langit berteleportasi di antara kedipan matamu.", "death_narration": "Ia berhenti berkedip dan lenyap terhapus dari eksistensi."
        },
        {
            "name": "Blood Mage", "element": "blood", "weakness": "light", "race": "humanoid", "attack_type": "magic",
            "base_hp": 105, "p_atk": 5, "m_atk": 45, "p_def": 3, "m_def": 14, "speed": 5, "dodge_chance": 0.1, "crit_chance": 0.15, "crit_damage": 1.5,
            "status_resistance": {"bleed": 1.0}, "ai_behavior": "aggressive", "exp": 170, "gold": 145,
            "skill": {"name": "Sanguine Drain", "type": "drain_hp", "chance": 0.35}, "drops": [{"id": "blood_crystal", "chance": 0.1}],
            "entry_narration": "Penyihir ini melukai pergelangan tangannya untuk menggunakan darahnya sebagai cambuk.", "death_narration": "Ia kehabisan darah dan mati tersenyum."
        },
        {
            "name": "Sandstorm Djinn", "element": "earth", "weakness": "water", "race": "demon", "attack_type": "magic",
            "base_hp": 165, "p_atk": 15, "m_atk": 30, "p_def": 10, "m_def": 12, "speed": 6, "dodge_chance": 0.2, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"blind": 1.0}, "ai_behavior": "trickster", "exp": 155, "gold": 135,
            "skill": {"name": "Blinding Sand", "type": "blind", "chance": 0.35}, "drops": [{"id": "chronos_sand", "chance": 0.05}],
            "entry_narration": "Badai pasir mini di dalam ruangan membentuk sosok raksasa bermata merah.", "death_narration": "Pasir itu jatuh ke lantai bagai tumpukan tanah biasa."
        },
        {
            "name": "Echoing Nightmare", "element": "dark", "weakness": "light", "race": "anomaly", "attack_type": "magic",
            "base_hp": 115, "p_atk": 10, "m_atk": 38, "p_def": 5, "m_def": 15, "speed": 7, "dodge_chance": 0.15, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"fear": 1.0}, "ai_behavior": "defensive", "exp": 160, "gold": 150,
            "skill": {"name": "Mind Rend", "type": "drain_mp", "chance": 0.4}, "drops": [{"id": "nightmare_essence", "chance": 0.05}],
            "entry_narration": "Makhluk ini menampilkan wajah keluargamu yang sedang berteriak marah padamu.", "death_narration": "Wajah itu meleleh, mengubah raut marah menjadi sedih."
        },
        {
            "name": "Radiant Punisher", "element": "light", "weakness": "dark", "race": "cosmic", "attack_type": "physical",
            "base_hp": 145, "p_atk": 38, "m_atk": 15, "p_def": 10, "m_def": 10, "speed": 5, "dodge_chance": 0.1, "crit_chance": 0.2, "crit_damage": 2.2,
            "status_resistance": {"blind": 1.0}, "ai_behavior": "aggressive", "exp": 165, "gold": 155,
            "skill": {"name": "Smite Evil", "type": "critical", "chance": 0.25}, "drops": [{"id": "radiant_gem", "chance": 0.3}],
            "entry_narration": "Malaikat berbaju zirah suci menghunuskan tombaknya. 'Dosa-dosamu terlalu berat.'", "death_narration": "Sayapnya patah. Ia jatuh seperti manusia fana lainnya."
        }
    ],

    # =========================================================================
    # TIER 4 (Kosmik & Dimensi Terdistorsi)
    # =========================================================================
    4: [
        {
            "name": "Time Devourer", "element": "void", "weakness": "light", "race": "cosmic", "attack_type": "magic",
            "base_hp": 250, "p_atk": 10, "m_atk": 50, "p_def": 8, "m_def": 18, "speed": 10, "dodge_chance": 0.25, "crit_chance": 0.15, "crit_damage": 1.5,
            "status_resistance": {"stun": 1.0, "paralyze": 1.0}, "ai_behavior": "trickster", "exp": 300, "gold": 250,
            "skill": {"name": "Time Stop", "type": "stun", "chance": 0.3}, "drops": [{"id": "hourglass_shard", "chance": 0.15}],
            "entry_narration": "Makhluk ini menelan jam pasir. Kau menyadari jam di dunia nyatamu serasa berhenti berdetak.", "death_narration": "Waktu kembali berjalan, namun kau kehilangan sisa umurmu."
        },
        {
            "name": "Glitch Archon", "element": "lightning", "weakness": "earth", "race": "anomaly", "attack_type": "magic",
            "base_hp": 200, "p_atk": 15, "m_atk": 55, "p_def": 10, "m_def": 15, "speed": 8, "dodge_chance": 0.3, "crit_chance": 0.2, "crit_damage": 2.0,
            "status_resistance": {"paralyze": 1.0, "blind": 0.5}, "ai_behavior": "aggressive", "exp": 350, "gold": 300,
            "skill": {"name": "Fatal Error", "type": "drain_hp", "chance": 0.35}, "drops": [{"id": "corrupted_core", "chance": 0.1}],
            "entry_narration": "E̵R̶R̸O̷R̸:̶ ̸E̵N̶T̶I̵T̷Y̶ ̸N̷O̷T̸ ̵F̸O̷U̶N̸D̵. Sesuatu meretas layar pertempuranmu secara paksa!", "death_narration": "Sistem reboot. Layar perlahan kembali bersih dari darah digital."
        },
        {
            "name": "Void Behemoth", "element": "void", "weakness": "light", "race": "cosmic", "attack_type": "physical",
            "base_hp": 400, "p_atk": 45, "m_atk": 20, "p_def": 15, "m_def": 15, "speed": 3, "dodge_chance": 0.0, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"stun": 0.5, "fear": 1.0}, "ai_behavior": "defensive", "exp": 320, "gold": 200,
            "skill": {"name": "Black Hole", "type": "drain_mp", "chance": 0.4}, "drops": [{"id": "void_stone", "chance": 0.2}],
            "entry_narration": "Lubang hitam mini terbuka di dadanya. Semua cahaya dan harapan tersedot ke sana.", "death_narration": "Ia runtuh ke dalam dirinya sendiri hingga menjadi titik ketiadaan."
        },
        {
            "name": "Chaos Oracle", "element": "dark", "weakness": "light", "race": "demon", "attack_type": "magic",
            "base_hp": 220, "p_atk": 10, "m_atk": 58, "p_def": 8, "m_def": 20, "speed": 6, "dodge_chance": 0.15, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"blind": 1.0, "fear": 1.0}, "ai_behavior": "trickster", "exp": 330, "gold": 280,
            "skill": {"name": "Whispers of Doom", "type": "confuse", "chance": 0.3}, "drops": [{"id": "oracle_eye", "chance": 0.1}],
            "entry_narration": "Mulutnya ada lusinan. Semuanya membisikkan dosa-dosa yang belum kau lakukan.", "death_narration": "Semua mulut itu menjerit dan dijahit paksa oleh kekuatan tak terlihat."
        },
        {
            "name": "Reality Shredder", "element": "none", "weakness": "blood", "race": "anomaly", "attack_type": "physical",
            "base_hp": 280, "p_atk": 50, "m_atk": 15, "p_def": 12, "m_def": 10, "speed": 7, "dodge_chance": 0.2, "crit_chance": 0.2, "crit_damage": 2.2,
            "status_resistance": {"stun": 0.8}, "ai_behavior": "aggressive", "exp": 340, "gold": 260,
            "skill": {"name": "Dimension Slash", "type": "armor_break", "chance": 0.3}, "drops": [{"id": "reality_shard", "chance": 0.2}],
            "entry_narration": "Ubin lantai dan dinding hancur berantakan. Ia memutarbalikkan gravitasi ruangan ini.", "death_narration": "Realitas kembali datar. Kau jatuh ke lantai dengan keras."
        },
        {
            "name": "The System Purger", "element": "lightning", "weakness": "water", "race": "construct", "attack_type": "magic",
            "base_hp": 180, "p_atk": 15, "m_atk": 65, "p_def": 10, "m_def": 25, "speed": 8, "dodge_chance": 0.1, "crit_chance": 0.15, "crit_damage": 1.8,
            "status_resistance": {"poison": 1.0, "bleed": 1.0}, "ai_behavior": "trickster", "exp": 400, "gold": 350,
            "skill": {"name": "Format Drive", "type": "drain_energy", "chance": 0.35}, "drops": [{"id": "buy_key_magic", "chance": 0.05}],
            "entry_narration": "Mata makhluk ini memindai 'Database' hidupmu. Ia tahu kau hanya seonggok data di matanya.", "death_narration": "Koneksinya terputus. Ia gagal menghapus eksistensimu."
        },
        {
            "name": "Dimension Ripper", "element": "void", "weakness": "light", "race": "demon", "attack_type": "physical",
            "base_hp": 300, "p_atk": 55, "m_atk": 10, "p_def": 12, "m_def": 12, "speed": 7, "dodge_chance": 0.15, "crit_chance": 0.25, "crit_damage": 2.5,
            "status_resistance": {"bleed": 0.5}, "ai_behavior": "berserk", "exp": 360, "gold": 290,
            "skill": {"name": "Tear Fabric", "type": "bleed", "chance": 0.3}, "drops": [{"id": "ripper_claw", "chance": 0.15}],
            "entry_narration": "Ia merobek latar belakang teks ini dengan cakar raksasa, memperlihatkan kekosongan putih.", "death_narration": "Robekan itu menutup, menyegelnya di dimensi mati."
        },
        {
            "name": "Eclipse Titan", "element": "fire", "weakness": "water", "race": "cosmic", "attack_type": "magic",
            "base_hp": 350, "p_atk": 20, "m_atk": 50, "p_def": 15, "m_def": 20, "speed": 4, "dodge_chance": 0.05, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"burn": 1.0, "blind": 1.0}, "ai_behavior": "defensive", "exp": 380, "gold": 310,
            "skill": {"name": "Solar Flare", "type": "burn", "chance": 0.35}, "drops": [{"id": "eclipse_fragment", "chance": 0.1}],
            "entry_narration": "Matahari hitam muncul di atasnya. Kegelapan mutlak mengaburkan pandanganmu.", "death_narration": "Matahari hitam pecah menjadi pecahan cahaya dingin."
        },
        {
            "name": "The Unwritten", "element": "dark", "weakness": "light", "race": "anomaly", "attack_type": "magic",
            "base_hp": 240, "p_atk": 5, "m_atk": 62, "p_def": 8, "m_def": 22, "speed": 6, "dodge_chance": 0.2, "crit_chance": 0.15, "crit_damage": 1.5,
            "status_resistance": {"blind": 1.0, "fear": 1.0}, "ai_behavior": "trickster", "exp": 420, "gold": 400,
            "skill": {"name": "Amnesia", "type": "blind", "chance": 0.4}, "drops": [{"id": "blank_page", "chance": 0.2}],
            "entry_narration": "Makhluk ini tidak memiliki deskripsi. Kehadirannya menghapus ingatan jangka pendekmu.", "death_narration": "Ia dilupakan seketika setelah kau membunuhnya."
        },
        {
            "name": "Astral Colossus", "element": "light", "weakness": "dark", "race": "cosmic", "attack_type": "physical",
            "base_hp": 500, "p_atk": 48, "m_atk": 25, "p_def": 20, "m_def": 15, "speed": 2, "dodge_chance": 0.0, "crit_chance": 0.15, "crit_damage": 2.0,
            "status_resistance": {"stun": 0.8}, "ai_behavior": "aggressive", "exp": 450, "gold": 300,
            "skill": {"name": "Meteor Strike", "type": "critical", "chance": 0.2}, "drops": [{"id": "celestial_core", "chance": 0.1}],
            "entry_narration": "Raksasa berbintang yang langkahnya membuat HP-mu bergetar hebat.", "death_narration": "Bintang-bintang di tubuhnya meledak seperti supernova kecil."
        },
        {
            "name": "Blood Moon Prophet", "element": "blood", "weakness": "ice", "race": "humanoid", "attack_type": "magic",
            "base_hp": 310, "p_atk": 15, "m_atk": 52, "p_def": 10, "m_def": 18, "speed": 5, "dodge_chance": 0.1, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"bleed": 1.0}, "ai_behavior": "defensive", "exp": 410, "gold": 330,
            "skill": {"name": "Crimson Tidal", "type": "bleed", "chance": 0.35}, "drops": [{"id": "blood_crystal", "chance": 0.2}],
            "entry_narration": "Ia menyembah bulan purnana yang merah. Ia mengorbankan dirinya untuk memanggil bulan itu turun.", "death_narration": "Ia tertimpa ilusi bulannya sendiri."
        },
        {
            "name": "Abyssal Leviathan Jr", "element": "water", "weakness": "lightning", "race": "beast", "attack_type": "physical",
            "base_hp": 480, "p_atk": 42, "m_atk": 20, "p_def": 18, "m_def": 12, "speed": 4, "dodge_chance": 0.05, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"freeze": 1.0}, "ai_behavior": "berserk", "exp": 430, "gold": 280,
            "skill": {"name": "Crushing Depth", "type": "armor_break", "chance": 0.3}, "drops": [{"id": "abyssal_pearl", "chance": 0.15}],
            "entry_narration": "Anak ikan paus kosmik berenang melintasi udara seolah itu adalah lautan.", "death_narration": "Ikan paus kosmik ini hancur menjadi tetesan air asin."
        },
        {
            "name": "Frostbound Warlord", "element": "ice", "weakness": "fire", "race": "undead", "attack_type": "physical",
            "base_hp": 380, "p_atk": 55, "m_atk": 15, "p_def": 16, "m_def": 10, "speed": 5, "dodge_chance": 0.1, "crit_chance": 0.2, "crit_damage": 2.0,
            "status_resistance": {"freeze": 1.0, "bleed": 1.0}, "ai_behavior": "aggressive", "exp": 400, "gold": 320,
            "skill": {"name": "Avalanche", "type": "paralyze", "chance": 0.25}, "drops": [{"id": "ice_blade_fragment", "chance": 0.2}],
            "entry_narration": "Raja dari musim dingin abadi memandangmu dari atas kuda esnya.", "death_narration": "Kudanya meleleh, dan ia patah lehernya saat jatuh."
        },
        {
            "name": "Toxic Hivemind", "element": "poison", "weakness": "fire", "race": "anomaly", "attack_type": "magic",
            "base_hp": 290, "p_atk": 5, "m_atk": 60, "p_def": 8, "m_def": 16, "speed": 6, "dodge_chance": 0.15, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"poison": 1.0, "blind": 0.5}, "ai_behavior": "trickster", "exp": 370, "gold": 340,
            "skill": {"name": "Neural Toxin", "type": "poison", "chance": 0.4}, "drops": [{"id": "ink_gland", "chance": 0.1}],
            "entry_narration": "Gumpalan otak raksasa yang melayang ini menyuntikkan racun langsung ke dalam benakmu.", "death_narration": "Otaknya meledak, menyebarkan isi pikiran yang bukan milikmu."
        },
        {
            "name": "Earthquake Bringer", "element": "earth", "weakness": "water", "race": "construct", "attack_type": "physical",
            "base_hp": 450, "p_atk": 48, "m_atk": 10, "p_def": 22, "m_def": 8, "speed": 2, "dodge_chance": 0.0, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"stun": 1.0, "poison": 1.0}, "ai_behavior": "defensive", "exp": 390, "gold": 290,
            "skill": {"name": "Tectonic Shift", "type": "stun", "chance": 0.3}, "drops": [{"id": "golem_heart", "chance": 0.1}],
            "entry_narration": "Makhluk batu raksasa meninju tanah, membuat kakimu mati rasa akibat getarannya.", "death_narration": "Tubuhnya retak terbelah dua seperti tebing yang longsor."
        },
        {
            "name": "Meteorite Golem", "element": "fire", "weakness": "water", "race": "construct", "attack_type": "physical",
            "base_hp": 420, "p_atk": 52, "m_atk": 20, "p_def": 18, "m_def": 10, "speed": 3, "dodge_chance": 0.0, "crit_chance": 0.15, "crit_damage": 1.8,
            "status_resistance": {"burn": 1.0, "bleed": 1.0}, "ai_behavior": "aggressive", "exp": 440, "gold": 350,
            "skill": {"name": "Impact Crater", "type": "burn", "chance": 0.35}, "drops": [{"id": "ember_core", "chance": 0.15}],
            "entry_narration": "Batu meteorit yang jatuh dari langit membentuk golem yang masih terbakar hebat.", "death_narration": "Cahaya intinya meredup, menyisakan batu angkasa biasa."
        },
        {
            "name": "The Silent King", "element": "dark", "weakness": "light", "race": "undead", "attack_type": "magic",
            "base_hp": 330, "p_atk": 15, "m_atk": 58, "p_def": 10, "m_def": 20, "speed": 5, "dodge_chance": 0.15, "crit_chance": 0.15, "crit_damage": 2.0,
            "status_resistance": {"fear": 1.0, "blind": 0.8}, "ai_behavior": "trickster", "exp": 460, "gold": 380,
            "skill": {"name": "Royal Silence", "type": "drain_energy", "chance": 0.35}, "drops": [{"id": "shadow_core", "chance": 0.2}],
            "entry_narration": "Raja tengkorak ini menempelkan jari ke bibirnya. Jika kau bersuara, kau akan mati.", "death_narration": "Tulangnya hancur dalam keheningan mutlak."
        },
        {
            "name": "Radiant Archangel", "element": "light", "weakness": "dark", "race": "cosmic", "attack_type": "magic",
            "base_hp": 360, "p_atk": 25, "m_atk": 55, "p_def": 12, "m_def": 18, "speed": 7, "dodge_chance": 0.2, "crit_chance": 0.2, "crit_damage": 2.2,
            "status_resistance": {"blind": 1.0}, "ai_behavior": "aggressive", "exp": 470, "gold": 360,
            "skill": {"name": "Heaven's Fury", "type": "blind", "chance": 0.3}, "drops": [{"id": "radiant_gem", "chance": 0.25}],
            "entry_narration": "Malaikat agung dengan enam sayap cahaya turun untuk menghapuskan pendosamu.", "death_narration": "Sayapnya terbakar menjadi hitam pekat sebelum ia jatuh."
        },
        {
            "name": "Singularity Core", "element": "void", "weakness": "light", "race": "anomaly", "attack_type": "magic",
            "base_hp": 260, "p_atk": 0, "m_atk": 70, "p_def": 20, "m_def": 25, "speed": 1, "dodge_chance": 0.0, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"stun": 1.0, "paralyze": 1.0}, "ai_behavior": "defensive", "exp": 490, "gold": 410,
            "skill": {"name": "Event Horizon", "type": "drain_all", "chance": 0.25}, "drops": [{"id": "void_stone", "chance": 0.2}],
            "entry_narration": "Sebuah inti energi hitam murni yang menyerap warna dari ruangan ini.", "death_narration": "Inti itu kolaps, meninggalkan bintik buta di matamu."
        },
        {
            "name": "Nullifier", "element": "none", "weakness": "void", "race": "construct", "attack_type": "physical",
            "base_hp": 300, "p_atk": 60, "m_atk": 0, "p_def": 15, "m_def": 30, "speed": 6, "dodge_chance": 0.1, "crit_chance": 0.25, "crit_damage": 2.0,
            "status_resistance": {"poison": 1.0, "burn": 1.0, "freeze": 1.0}, "ai_behavior": "berserk", "exp": 410, "gold": 370,
            "skill": {"name": "Bypass Armor", "type": "armor_break", "chance": 0.45}, "drops": [{"id": "iron_scrap", "chance": 0.8}],
            "entry_narration": "Entitas ini menetralisir semua energi magis di sekitarnya. Ini pertarungan murni.", "death_narration": "Ia lenyap dan sihir di udara kembali terasa."
        }
    ],

    # =========================================================================
    # TIER 5 (Bos, Entitas Kuno, Dewa)
    # =========================================================================
    5: [
        {
            "name": "The Final Paradox", "element": "void", "weakness": "light", "race": "anomaly", "attack_type": "magic",
            "base_hp": 1000, "p_atk": 30, "m_atk": 85, "p_def": 20, "m_def": 35, "speed": 8, "dodge_chance": 0.25, "crit_chance": 0.2, "crit_damage": 2.0,
            "status_resistance": {"stun": 1.0, "paralyze": 1.0, "blind": 1.0}, "ai_behavior": "trickster", "exp": 1500, "gold": 1000,
            "skill": {"name": "Logic Break", "type": "drain_all", "chance": 0.3}, "drops": [{"id": "paradox_core", "chance": 1.0}],
            "entry_narration": "KAU SEHARUSNYA TIDAK BERADA DI SINI. Makhluk ini adalah perwujudan dari bug semesta.", "death_narration": "Paradoks itu pecah. Akal sehatmu hampir ikut hancur bersamanya."
        },
        {
            "name": "Orion, The First Scribe", "element": "light", "weakness": "dark", "race": "humanoid", "attack_type": "magic",
            "base_hp": 850, "p_atk": 40, "m_atk": 90, "p_def": 15, "m_def": 40, "speed": 7, "dodge_chance": 0.2, "crit_chance": 0.15, "crit_damage": 1.8,
            "status_resistance": {"fear": 1.0}, "ai_behavior": "defensive", "exp": 1800, "gold": 1200,
            "skill": {"name": "Rewrite Fate", "type": "heal_self", "chance": 0.2}, "drops": [{"id": "orion_quill", "chance": 1.0}],
            "entry_narration": "Pencipta dimensi ini menatapmu. 'Anakku yang gagal. Biar kuhapus kau dari naskahku.'", "death_narration": "Orion meneteskan air mata tinta. 'Akhirnya... aku bisa tidur.'"
        },
        {
            "name": "Void Leviathan", "element": "void", "weakness": "light", "race": "cosmic", "attack_type": "physical",
            "base_hp": 1200, "p_atk": 80, "m_atk": 40, "p_def": 30, "m_def": 20, "speed": 4, "dodge_chance": 0.05, "crit_chance": 0.25, "crit_damage": 2.5,
            "status_resistance": {"stun": 0.8}, "ai_behavior": "aggressive", "exp": 1600, "gold": 1100,
            "skill": {"name": "Abyssal Maw", "type": "drain_hp", "chance": 0.35}, "drops": [{"id": "leviathan_scale", "chance": 1.0}],
            "entry_narration": "Naga raksasa yang berenang melintasi lautan ruang hampa. Mulutnya bisa menelan bulan.", "death_narration": "Paus kosmik ini meraung terakhir kali, sebelum hancur menjadi debu bintang."
        },
        {
            "name": "The Sleeping God", "element": "none", "weakness": "dark", "race": "cosmic", "attack_type": "magic",
            "base_hp": 999, "p_atk": 10, "m_atk": 100, "p_def": 25, "m_def": 45, "speed": 1, "dodge_chance": 0.0, "crit_chance": 0.1, "crit_damage": 3.0,
            "status_resistance": {"all": 0.5}, "ai_behavior": "defensive", "exp": 2000, "gold": 1500,
            "skill": {"name": "Lucid Nightmare", "type": "stun", "chance": 0.4}, "drops": [{"id": "god_tear", "chance": 1.0}],
            "entry_narration": "Dewa ini bahkan tidak membuka matanya. Kehadirannya saja membuat kulitmu terkelupas perlahan.", "death_narration": "Dewa ini mendengkur, lalu perlahan memudar ke alam mimpi yang lebih dalam."
        },
        {
            "name": "Eternal Nightmare", "element": "dark", "weakness": "light", "race": "demon", "attack_type": "magic",
            "base_hp": 800, "p_atk": 25, "m_atk": 95, "p_def": 10, "m_def": 35, "speed": 9, "dodge_chance": 0.3, "crit_chance": 0.2, "crit_damage": 2.0,
            "status_resistance": {"fear": 1.0, "blind": 1.0}, "ai_behavior": "trickster", "exp": 1700, "gold": 1300,
            "skill": {"name": "Terror Resonance", "type": "confuse", "chance": 0.45}, "drops": [{"id": "nightmare_essence", "chance": 1.0}],
            "entry_narration": "Rasa takut paling murnimu berbentuk fisik. Ia memakan harapanmu.", "death_narration": "Kau terbangun dari mimpi buruk ini. Napasmu tersengal-sengal."
        },
        {
            "name": "The Nameless Sovereign", "element": "blood", "weakness": "ice", "race": "undead", "attack_type": "physical",
            "base_hp": 1500, "p_atk": 75, "m_atk": 30, "p_def": 35, "m_def": 25, "speed": 5, "dodge_chance": 0.1, "crit_chance": 0.2, "crit_damage": 1.8,
            "status_resistance": {"bleed": 1.0}, "ai_behavior": "aggressive", "exp": 1400, "gold": 1800,
            "skill": {"name": "Royal Decree", "type": "armor_break", "chance": 0.3}, "drops": [{"id": "sovereign_crown", "chance": 1.0}],
            "entry_narration": "Raja tanpa kerajaan. Ia duduk di atas takhta yang terbuat dari ribuan HP Weaver yang gugur.", "death_narration": "Takhtanya runtuh. Sang Raja jatuh tanpa suara."
        },
        {
            "name": "Alpha and Omega", "element": "light", "weakness": "dark", "race": "cosmic", "attack_type": "magic",
            "base_hp": 1111, "p_atk": 50, "m_atk": 85, "p_def": 22, "m_def": 33, "speed": 7, "dodge_chance": 0.15, "crit_chance": 0.3, "crit_damage": 2.5,
            "status_resistance": {"blind": 1.0, "stun": 0.5}, "ai_behavior": "berserk", "exp": 2500, "gold": 2000,
            "skill": {"name": "Genesis Ray", "type": "critical", "chance": 0.35}, "drops": [{"id": "omega_particle", "chance": 1.0}],
            "entry_narration": "Awal dan akhir dari segalanya berpadu dalam satu bentuk menyilaukan. Kau merasa tidak pantas menatapnya.", "death_narration": "Dunia ter-reset sejenak sebelum ia lenyap sepenuhnya."
        },
        {
            "name": "The Weaver of Fate", "element": "dark", "weakness": "fire", "race": "humanoid", "attack_type": "magic",
            "base_hp": 900, "p_atk": 20, "m_atk": 90, "p_def": 15, "m_def": 30, "speed": 8, "dodge_chance": 0.25, "crit_chance": 0.15, "crit_damage": 2.0,
            "status_resistance": {"bind": 1.0}, "ai_behavior": "trickster", "exp": 1900, "gold": 1400,
            "skill": {"name": "Sever Thread", "type": "bleed", "chance": 0.4}, "drops": [{"id": "fate_spindle", "chance": 1.0}],
            "entry_narration": "Ia memegang benang merah kehidupanmu. Satu tarikan, dan nadimu akan putus.", "death_narration": "Benang merahmu terlepas dari genggamannya. Kau bebas."
        },
        {
            "name": "Reality's Cancer", "element": "poison", "weakness": "fire", "race": "anomaly", "attack_type": "magic",
            "base_hp": 1300, "p_atk": 15, "m_atk": 75, "p_def": 25, "m_def": 25, "speed": 3, "dodge_chance": 0.05, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"poison": 1.0, "bleed": 1.0}, "ai_behavior": "defensive", "exp": 1650, "gold": 1250,
            "skill": {"name": "Metastasis", "type": "poison", "chance": 0.5}, "drops": [{"id": "tumor_core", "chance": 1.0}],
            "entry_narration": "Tumor kosmik raksasa yang terus membesar, menghisap warna dari lingkungan sekitar.", "death_narration": "Tumor ini mengering, melepaskan miasma penyembuh yang aneh."
        },
        {
            "name": "The Architect of Despair", "element": "earth", "weakness": "water", "race": "humanoid", "attack_type": "physical",
            "base_hp": 950, "p_atk": 85, "m_atk": 40, "p_def": 40, "m_def": 20, "speed": 5, "dodge_chance": 0.1, "crit_chance": 0.2, "crit_damage": 2.2,
            "status_resistance": {"stun": 1.0}, "ai_behavior": "aggressive", "exp": 2200, "gold": 1600,
            "skill": {"name": "Collapse", "type": "drain_all", "chance": 0.2}, "drops": [{"id": "architect_blueprint", "chance": 1.0}],
            "entry_narration": "Arsitek bangunan labirin Archivus ini tersenyum. 'Kau suka permainanku, tikus kecil?'", "death_narration": "Ia tertawa saat mati. 'Game over... untukku.'"
        },
        {
            "name": "Sun Eater", "element": "fire", "weakness": "water", "race": "cosmic", "attack_type": "magic",
            "base_hp": 1400, "p_atk": 50, "m_atk": 80, "p_def": 25, "m_def": 30, "speed": 6, "dodge_chance": 0.1, "crit_chance": 0.25, "crit_damage": 1.8,
            "status_resistance": {"burn": 1.0, "blind": 1.0}, "ai_behavior": "berserk", "exp": 2100, "gold": 1700,
            "skill": {"name": "Solar Devour", "type": "burn", "chance": 0.4}, "drops": [{"id": "ember_core", "chance": 1.0}],
            "entry_narration": "Entitas pemakan bintang yang perutnya berisi jutaan matahari yang telah ditelannya.", "death_narration": "Perutnya pecah, menyebarkan percikan galaksi kecil yang indah."
        },
        {
            "name": "Ocean's Grave", "element": "water", "weakness": "lightning", "race": "anomaly", "attack_type": "magic",
            "base_hp": 1600, "p_atk": 30, "m_atk": 70, "p_def": 30, "m_def": 35, "speed": 4, "dodge_chance": 0.05, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"freeze": 0.8}, "ai_behavior": "defensive", "exp": 1750, "gold": 1350,
            "skill": {"name": "Abyssal Pressure", "type": "stun", "chance": 0.3}, "drops": [{"id": "abyssal_pearl", "chance": 1.0}],
            "entry_narration": "Laut berdarah yang memiliki kesadaran. Ia siap menenggelamkanmu dalam keputusasaan.", "death_narration": "Lautan itu mengering menjadi padang garam putih."
        },
        {
            "name": "Absolute Zero", "element": "ice", "weakness": "fire", "race": "demon", "attack_type": "magic",
            "base_hp": 1100, "p_atk": 40, "m_atk": 90, "p_def": 20, "m_def": 40, "speed": 7, "dodge_chance": 0.2, "crit_chance": 0.2, "crit_damage": 2.0,
            "status_resistance": {"freeze": 1.0, "burn": 0.5}, "ai_behavior": "trickster", "exp": 1850, "gold": 1450,
            "skill": {"name": "Flash Freeze", "type": "paralyze", "chance": 0.45}, "drops": [{"id": "frozen_tear", "chance": 1.0}],
            "entry_narration": "Suhu ruangan turun drastis hingga molekul udara berhenti. Dewa Es telah tiba.", "death_narration": "Ia mencair, memberikan kehangatan pertama yang kau rasakan di ruangan ini."
        },
        {
            "name": "Storm God", "element": "lightning", "weakness": "earth", "race": "cosmic", "attack_type": "physical",
            "base_hp": 950, "p_atk": 100, "m_atk": 60, "p_def": 25, "m_def": 25, "speed": 9, "dodge_chance": 0.15, "crit_chance": 0.3, "crit_damage": 2.5,
            "status_resistance": {"paralyze": 1.0}, "ai_behavior": "aggressive", "exp": 2300, "gold": 1800,
            "skill": {"name": "Wrath of Heavens", "type": "critical", "chance": 0.3}, "drops": [{"id": "storm_crystal", "chance": 1.0}],
            "entry_narration": "Dewa badai dengan palu petir yang menghancurkan langit-langit Archivus.", "death_narration": "Petir terakhirnya menyambar dadanya sendiri."
        },
        {
            "name": "Plague Incarnate", "element": "poison", "weakness": "fire", "race": "demon", "attack_type": "magic",
            "base_hp": 1250, "p_atk": 25, "m_atk": 75, "p_def": 20, "m_def": 30, "speed": 5, "dodge_chance": 0.1, "crit_chance": 0.15, "crit_damage": 1.5,
            "status_resistance": {"poison": 1.0}, "ai_behavior": "berserk", "exp": 1950, "gold": 1550,
            "skill": {"name": "Pandemic", "type": "poison", "chance": 0.6}, "drops": [{"id": "plague_sample", "chance": 1.0}],
            "entry_narration": "Wujud fisik dari semua penyakit yang pernah membunuh umat manusia merayap kepadamu.", "death_narration": "Ia terbatuk darah hitam dan membusuk dari dalam."
        },
        {
            "name": "Blood Sea Emperor", "element": "blood", "weakness": "light", "race": "undead", "attack_type": "magic",
            "base_hp": 1450, "p_atk": 50, "m_atk": 85, "p_def": 25, "m_def": 25, "speed": 6, "dodge_chance": 0.15, "crit_chance": 0.2, "crit_damage": 1.8,
            "status_resistance": {"bleed": 1.0}, "ai_behavior": "aggressive", "exp": 2400, "gold": 1900,
            "skill": {"name": "Sanguine Tsunami", "type": "drain_hp", "chance": 0.4}, "drops": [{"id": "blood_crown", "chance": 1.0}],
            "entry_narration": "Kaisar lalim yang meminum darah rakyatnya untuk mencapai keabadian. Ia haus akan darahmu.", "death_narration": "Ia mati kekeringan, menyadari keabadiannya adalah kutukan."
        },
        {
            "name": "The Cosmic Eradicator", "element": "void", "weakness": "light", "race": "construct", "attack_type": "physical",
            "base_hp": 2000, "p_atk": 95, "m_atk": 50, "p_def": 45, "m_def": 40, "speed": 3, "dodge_chance": 0.0, "crit_chance": 0.15, "crit_damage": 2.0,
            "status_resistance": {"stun": 1.0, "poison": 1.0, "bleed": 1.0}, "ai_behavior": "defensive", "exp": 3000, "gold": 2500,
            "skill": {"name": "Delete Existence", "type": "drain_all", "chance": 0.3}, "drops": [{"id": "void_stone", "chance": 1.0}],
            "entry_narration": "Mesin raksasa kosmik yang bertugas menghapus galaksi cacat. Matanya tertuju padamu.", "death_narration": "Mesin itu mati. Sistem pendinginnya bocor dan hancur."
        },
        {
            "name": "The Golden Idol", "element": "light", "weakness": "dark", "race": "construct", "attack_type": "magic",
            "base_hp": 1050, "p_atk": 40, "m_atk": 88, "p_def": 35, "m_def": 35, "speed": 5, "dodge_chance": 0.05, "crit_chance": 0.25, "crit_damage": 2.5,
            "status_resistance": {"blind": 1.0, "burn": 0.5}, "ai_behavior": "trickster", "exp": 2150, "gold": 3000,
            "skill": {"name": "Greed's Punishment", "type": "armor_break", "chance": 0.4}, "drops": [{"id": "radiant_gem", "chance": 1.0}, {"id": "gambler_coin", "chance": 1.0}],
            "entry_narration": "Patung emas raksasa yang hidup karena keserakahan manusia. Ia menyilaukan dan mematikan.", "death_narration": "Emasnya meleleh, mengungkapkan lumpur kotor di baliknya."
        },
        {
            "name": "The World Serpent", "element": "earth", "weakness": "ice", "race": "beast", "attack_type": "physical",
            "base_hp": 1800, "p_atk": 75, "m_atk": 25, "p_def": 30, "m_def": 20, "speed": 6, "dodge_chance": 0.1, "crit_chance": 0.2, "crit_damage": 1.5,
            "status_resistance": {"poison": 1.0}, "ai_behavior": "aggressive", "exp": 2200, "gold": 1600,
            "skill": {"name": "Constrict", "type": "bind", "chance": 0.35}, "drops": [{"id": "serpent_scale", "chance": 1.0}],
            "entry_narration": "Ular raksasa yang tubuhnya melingkari seluruh Archivus. Mulutnya muncul tepat di depanmu.", "death_narration": "Ular ini menelan ekornya sendiri dan lenyap."
        },
        {
            "name": "The Empty Throne", "element": "dark", "weakness": "light", "race": "anomaly", "attack_type": "magic",
            "base_hp": 1350, "p_atk": 10, "m_atk": 95, "p_def": 25, "m_def": 40, "speed": 2, "dodge_chance": 0.0, "crit_chance": 0.1, "crit_damage": 1.5,
            "status_resistance": {"fear": 1.0, "stun": 1.0}, "ai_behavior": "defensive", "exp": 2600, "gold": 1750,
            "skill": {"name": "Aura of Domination", "type": "drain_energy", "chance": 0.5}, "drops": [{"id": "throne_fragment", "chance": 1.0}],
            "entry_narration": "Takhta kosong yang memancarkan aura dominasi yang luar biasa. Takhta ini yang mengendalikanmu.", "death_narration": "Takhtanya hancur. Kau akhirnya menjadi penguasa nasibmu sendiri."
        }
    ]
}
