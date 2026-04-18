# game/items/weapons.py

WEAPONS = {
    # ==========================================
    # --- STARTER / BASIC WEAPONS (TIER 1-2) ---
    # ==========================================
    "iron_sword": {
        "id": "iron_sword", "name": "Rusty Iron Sword", "tier": 1, "grip": "1H", "element": "none",
        "p_atk": 15, "m_atk": 0, "durability": 50, "max_durability": 50, "sockets": 0, "installed_shards": [],
        "description": "Pedang besi berkarat. Setidaknya sisi tajamnya masih bisa memotong."
    },
    "novice_staff": {
        "id": "novice_staff", "name": "Novice Wooden Staff", "tier": 1, "grip": "2H", "element": "none",
        "p_atk": 5, "m_atk": 20, "durability": 40, "max_durability": 40, "sockets": 0, "installed_shards": [],
        "description": "Tongkat kayu ek sederhana untuk pemula sihir."
    },
    "hunting_bow": {
        "id": "hunting_bow", "name": "Old Hunting Bow", "tier": 1, "grip": "2H", "element": "none",
        "p_atk": 18, "m_atk": 0, "durability": 45, "max_durability": 45, "sockets": 0, "installed_shards": [],
        "description": "Busur tua yang digunakan untuk berburu kelinci."
    },
    "iron_dagger": {
        "id": "iron_dagger", "name": "Thief's Iron Dagger", "tier": 1, "grip": "1H", "element": "none",
        "p_atk": 12, "m_atk": 0, "durability": 35, "max_durability": 35, "sockets": 0, "installed_shards": [],
        "description": "Belati pendek. Ringan dan mematikan dalam jarak dekat."
    },
    "wooden_club": {
        "id": "wooden_club", "name": "Heavy Wooden Club", "tier": 1, "grip": "1H", "element": "earth",
        "p_atk": 22, "m_atk": 0, "durability": 60, "max_durability": 60, "sockets": 0, "installed_shards": [],
        "description": "Gada kayu berat. Sederhana, tapi pukulannya meremukkan tulang."
    },
    "copper_blade": {
        "id": "copper_blade", "name": "Copper Blade", "tier": 1, "grip": "1H", "element": "none",
        "p_atk": 17, "m_atk": 0, "durability": 55, "max_durability": 55, "sockets": 0, "installed_shards": [],
        "description": "Pedang tembaga yang rapuh namun cukup tajam."
    },
    "apprentice_wand": {
        "id": "apprentice_wand", "name": "Apprentice Wand", "tier": 1, "grip": "1H", "element": "none",
        "p_atk": 2, "m_atk": 18, "durability": 40, "max_durability": 40, "sockets": 0, "installed_shards": [],
        "description": "Tongkat sihir pendek dengan batu kaca murahan di ujungnya."
    },
    "militia_spear": {
        "id": "militia_spear", "name": "Militia Spear", "tier": 1, "grip": "2H", "element": "none",
        "p_atk": 20, "m_atk": 0, "durability": 50, "max_durability": 50, "sockets": 0, "installed_shards": [],
        "description": "Tombak standar milik prajurit sipil kota bawah."
    },
    "stone_axe": {
        "id": "stone_axe", "name": "Crude Stone Axe", "tier": 1, "grip": "1H", "element": "earth",
        "p_atk": 25, "m_atk": 0, "durability": 45, "max_durability": 45, "sockets": 0, "installed_shards": [],
        "description": "Kapak batu kasar, sangat berat namun mematikan."
    },
    "slingshot": {
        "id": "slingshot", "name": "Leather Slingshot", "tier": 1, "grip": "1H", "element": "none",
        "p_atk": 10, "m_atk": 0, "durability": 30, "max_durability": 30, "sockets": 0, "installed_shards": [],
        "description": "Ketapel kulit untuk melempar kerikil tajam."
    },
    "steel_longsword": {
        "id": "steel_longsword", "name": "Steel Longsword", "tier": 2, "grip": "1H", "element": "none",
        "p_atk": 25, "m_atk": 0, "durability": 70, "max_durability": 70, "sockets": 1, "installed_shards": [],
        "description": "Pedang baja tempaan standar yang tahan lama."
    },
    "soldier_crossbow": {
        "id": "soldier_crossbow", "name": "Soldier Crossbow", "tier": 2, "grip": "2H", "element": "none",
        "p_atk": 30, "m_atk": 0, "durability": 60, "max_durability": 60, "sockets": 1, "installed_shards": [],
        "description": "Crossbow militer yang lambat namun punya daya tembus kuat."
    },
    "acolyte_staff": {
        "id": "acolyte_staff", "name": "Acolyte Crystal Staff", "tier": 2, "grip": "2H", "element": "light",
        "p_atk": 8, "m_atk": 30, "durability": 65, "max_durability": 65, "sockets": 1, "installed_shards": [],
        "description": "Tongkat bagi murid sihir tingkat lanjut."
    },
    "hunter_dirk": {
        "id": "hunter_dirk", "name": "Hunter's Dirk", "tier": 2, "grip": "1H", "element": "none",
        "p_atk": 20, "m_atk": 0, "durability": 50, "max_durability": 50, "sockets": 1, "installed_shards": [],
        "description": "Pisau berburu yang sangat tajam."
    },
    "reinforced_mace": {
        "id": "reinforced_mace", "name": "Reinforced Mace", "tier": 2, "grip": "1H", "element": "none",
        "p_atk": 32, "m_atk": 0, "durability": 80, "max_durability": 80, "sockets": 1, "installed_shards": [],
        "description": "Gada baja dengan duri-duri kecil di ujungnya."
    },

    # ==========================================
    # --- SWORDS & BLADES (1H) ---
    # ==========================================
    "silver_longsword": {
        "id": "silver_longsword", "name": "Silver Longsword", "tier": 3, "grip": "1H", "element": "light",
        "p_atk": 45, "m_atk": 20, "durability": 100, "max_durability": 100, "sockets": 1, "installed_shards": [],
        "description": "Pedang perak suci. (Diperlukan oleh Holy Templar)."
    },
    "blessed_sword": {
        "id": "blessed_sword", "name": "Blessed Silver Sword", "tier": 4, "grip": "1H", "element": "light",
        "p_atk": 50, "m_atk": 30, "durability": 180, "max_durability": 180, "sockets": 2, "installed_shards": [],
        "description": "Pedang suci yang benci akan kegelapan."
    },
    "flame_blade": {
        "id": "flame_blade", "name": "Searing Flame Blade", "tier": 3, "grip": "1H", "element": "fire",
        "p_atk": 40, "m_atk": 15, "durability": 90, "max_durability": 90, "sockets": 1, "installed_shards": [],
        "description": "Bilah pedangnya selalu terasa hangat."
    },
    "frost_edge": {
        "id": "frost_edge", "name": "Glacial Frost Edge", "tier": 3, "grip": "1H", "element": "ice",
        "p_atk": 38, "m_atk": 18, "durability": 95, "max_durability": 95, "sockets": 1, "installed_shards": [],
        "description": "Udara di sekitar pedang ini mengembun."
    },
    "venom_sword": {
        "id": "venom_sword", "name": "Viper's Kiss Sword", "tier": 3, "grip": "1H", "element": "poison",
        "p_atk": 35, "m_atk": 10, "durability": 85, "max_durability": 85, "sockets": 1, "installed_shards": [],
        "description": "Cairan hijau beracun menetes dari bilahnya."
    },
    "thunder_rapier": {
        "id": "thunder_rapier", "name": "Thunderclap Rapier", "tier": 4, "grip": "1H", "element": "lightning",
        "p_atk": 48, "m_atk": 25, "durability": 110, "max_durability": 110, "sockets": 2, "installed_shards": [],
        "description": "Pedang anggar ramping yang menyimpan energi petir."
    },
    "abyssal_blade": {
        "id": "abyssal_blade", "name": "Abyssal Dark Blade", "tier": 4, "grip": "1H", "element": "dark",
        "p_atk": 55, "m_atk": 20, "durability": 130, "max_durability": 130, "sockets": 2, "installed_shards": [],
        "description": "Pedang hitam pekat yang menyerap cahaya."
    },
    "blood_drinker": {
        "id": "blood_drinker", "name": "Blood Drinker Katana", "tier": 4, "grip": "1H", "element": "blood",
        "p_atk": 52, "m_atk": 10, "durability": 100, "max_durability": 100, "sockets": 2, "installed_shards": [],
        "description": "Katana melengkung berwarna merah darah."
    },
    "gale_scimitar": {
        "id": "gale_scimitar", "name": "Desert Gale Scimitar", "tier": 3, "grip": "1H", "element": "wind",
        "p_atk": 42, "m_atk": 5, "durability": 95, "max_durability": 95, "sockets": 1, "installed_shards": [],
        "description": "Sangat cepat saat diayunkan membelah udara."
    },
    "crystal_sword": {
        "id": "crystal_sword", "name": "Resonant Crystal Sword", "tier": 4, "grip": "1H", "element": "none",
        "p_atk": 35, "m_atk": 45, "durability": 80, "max_durability": 80, "sockets": 3, "installed_shards": [],
        "description": "Bilah kristal murni. Sangat kuat untuk magic attack."
    },
    "sunlight_blade": {
        "id": "sunlight_blade", "name": "Blade of the Dawn", "tier": 5, "grip": "1H", "element": "light",
        "p_atk": 65, "m_atk": 45, "durability": 200, "max_durability": 200, "sockets": 2, "installed_shards": [],
        "description": "Membawa kehangatan fajar pertama."
    },
    "void_edge": {
        "id": "void_edge", "name": "Edge of the Void", "tier": 5, "grip": "1H", "element": "void",
        "p_atk": 70, "m_atk": 50, "durability": 190, "max_durability": 190, "sockets": 2, "installed_shards": [],
        "description": "Bilahnya seperti robekan di ruang angkasa."
    },

    # ==========================================
    # --- GREATSWORDS & 2H BLADES ---
    # ==========================================
    "mountain_crusher": {
        "id": "mountain_crusher", "name": "Mountain Crusher Greatsword", "tier": 4, "grip": "2H", "element": "earth",
        "p_atk": 75, "m_atk": 0, "durability": 250, "max_durability": 250, "sockets": 1, "installed_shards": [],
        "description": "Satu tebasan yang mampu membelah bukit. (Diperlukan oleh Dread Knight)."
    },
    "dragon_blade": {
        "id": "dragon_blade", "name": "Dragon-Bone Greatblade", "tier": 5, "grip": "2H", "element": "fire",
        "p_atk": 95, "m_atk": 20, "durability": 300, "max_durability": 300, "sockets": 2, "installed_shards": [],
        "description": "Ditempa dari tulang naga purba."
    },
    "claymore": {
        "id": "claymore", "name": "Knight's Claymore", "tier": 3, "grip": "2H", "element": "none",
        "p_atk": 60, "m_atk": 0, "durability": 150, "max_durability": 150, "sockets": 1, "installed_shards": [],
        "description": "Pedang raksasa andalan ksatria kerajaan."
    },
    "executioner_sword": {
        "id": "executioner_sword", "name": "Executioner's Blade", "tier": 4, "grip": "2H", "element": "dark",
        "p_atk": 80, "m_atk": 0, "durability": 180, "max_durability": 180, "sockets": 2, "installed_shards": [],
        "description": "Ujungnya tumpul, difokuskan murni untuk memenggal."
    },
    "iceberg_greatsword": {
        "id": "iceberg_greatsword", "name": "Iceberg Colossus", "tier": 4, "grip": "2H", "element": "ice",
        "p_atk": 70, "m_atk": 25, "durability": 220, "max_durability": 220, "sockets": 1, "installed_shards": [],
        "description": "Sebuah gletser tajam yang diberi gagang."
    },
    "tempest_zweihander": {
        "id": "tempest_zweihander", "name": "Tempest Zweihander", "tier": 4, "grip": "2H", "element": "wind",
        "p_atk": 68, "m_atk": 15, "durability": 170, "max_durability": 170, "sockets": 2, "installed_shards": [],
        "description": "Pedang besar yang mengendalikan arus angin saat diayunkan."
    },
    "titan_slayer": {
        "id": "titan_slayer", "name": "Titan Slayer Greatsword", "tier": 5, "grip": "2H", "element": "earth",
        "p_atk": 105, "m_atk": 0, "durability": 350, "max_durability": 350, "sockets": 2, "installed_shards": [],
        "description": "Sangat berat hingga hanya orang terpilih yang bisa mengangkatnya."
    },

    # ==========================================
    # --- DUAL SWORDS ---
    # ==========================================
    "phantom_twin_blades": {
        "id": "phantom_twin_blades", "name": "Phantom Twin Blades", "tier": 4, "grip": "2H", "element": "wind",
        "p_atk": 60, "m_atk": 15, "durability": 120, "max_durability": 120, "sockets": 2, "installed_shards": [],
        "description": "Dua pedang melengkung yang sangat ringan bak angin."
    },
    "fire_ice_twins": {
        "id": "fire_ice_twins", "name": "Twin Blades of Frost & Flame", "tier": 5, "grip": "2H", "element": "water",
        "p_atk": 75, "m_atk": 40, "durability": 180, "max_durability": 180, "sockets": 2, "installed_shards": [],
        "description": "Satu bilah membakar, satu lagi membekukan."
    },
    "shadow_dancers": {
        "id": "shadow_dancers", "name": "Shadow Dancer Dual Swords", "tier": 4, "grip": "2H", "element": "dark",
        "p_atk": 65, "m_atk": 10, "durability": 130, "max_durability": 130, "sockets": 2, "installed_shards": [],
        "description": "Bilah ganda yang menyatu dengan bayangan penggunanya."
    },
    "blood_twins": {
        "id": "blood_twins", "name": "Crimson Twin Sabers", "tier": 3, "grip": "2H", "element": "blood",
        "p_atk": 50, "m_atk": 0, "durability": 100, "max_durability": 100, "sockets": 1, "installed_shards": [],
        "description": "Saber ganda untuk tarian darah mematikan."
    },

    # ==========================================
    # --- DAGGERS & ASSASSIN WEAPONS ---
    # ==========================================
    "soul_eater_dagger": {
        "id": "soul_eater_dagger", "name": "Cursed Soul-Eater Dagger", "tier": 3, "grip": "1H", "element": "dark",
        "p_atk": 35, "m_atk": 25, "durability": 70, "max_durability": 70, "sockets": 1, "installed_shards": [],
        "description": "Setiap tusukan merobek sedikit jiwa lawan."
    },
    "icicle_daggers": {
        "id": "icicle_daggers", "name": "Icicle Shard Daggers", "tier": 4, "grip": "1H", "element": "ice",
        "p_atk": 40, "m_atk": 20, "durability": 80, "max_durability": 80, "sockets": 2, "installed_shards": [],
        "description": "Belati kembar sedingin kematian."
    },
    "venom_fang_dagger": {
        "id": "venom_fang_dagger", "name": "Venom Fang Dagger", "tier": 3, "grip": "1H", "element": "poison",
        "p_atk": 30, "m_atk": 10, "durability": 65, "max_durability": 65, "sockets": 1, "installed_shards": [],
        "description": "Mata pisaunya selalu meneteskan racun mematikan."
    },
    "obsidian_kris": {
        "id": "obsidian_kris", "name": "Obsidian Kris", "tier": 4, "grip": "1H", "element": "earth",
        "p_atk": 48, "m_atk": 5, "durability": 90, "max_durability": 90, "sockets": 1, "installed_shards": [],
        "description": "Pisau bergelombang yang diukir dari kaca vulkanik."
    },
    "whispering_dagger": {
        "id": "whispering_dagger", "name": "Whispering Dagger", "tier": 5, "grip": "1H", "element": "void",
        "p_atk": 55, "m_atk": 40, "durability": 120, "max_durability": 120, "sockets": 2, "installed_shards": [],
        "description": "Kau bisa mendengar suara korbannya dari bilah ini."
    },
    "golden_stiletto": {
        "id": "golden_stiletto", "name": "Royal Golden Stiletto", "tier": 3, "grip": "1H", "element": "light",
        "p_atk": 32, "m_atk": 15, "durability": 60, "max_durability": 60, "sockets": 2, "installed_shards": [],
        "description": "Elegan, mahal, dan sangat tajam."
    },
    "shadow_shiv": {
        "id": "shadow_shiv", "name": "Shadow Shiv", "tier": 2, "grip": "1H", "element": "dark",
        "p_atk": 25, "m_atk": 5, "durability": 45, "max_durability": 45, "sockets": 1, "installed_shards": [],
        "description": "Senjata pembunuh bayaran jalanan."
    },

    # ==========================================
    # --- SCYTHES (2H) ---
    # ==========================================
    "crimson_hunger": {
        "id": "crimson_hunger", "name": "Crimson Hunger Scythe", "tier": 5, "grip": "2H", "element": "blood",
        "p_atk": 85, "m_atk": 40, "durability": 140, "max_durability": 140, "sockets": 2, "installed_shards": [],
        "description": "Sabit yang hanya akan berhenti jika sudah puas minum darah. (Diperlukan oleh Blood Reaper)."
    },
    "frozen_scythe": {
        "id": "frozen_scythe", "name": "Soul-Chill Scythe", "tier": 4, "grip": "2H", "element": "ice",
        "p_atk": 65, "m_atk": 30, "durability": 110, "max_durability": 110, "sockets": 2, "installed_shards": [],
        "description": "Sabit besar pemanen jiwa yang membeku."
    },
    "reaper_scythe": {
        "id": "reaper_scythe", "name": "Grim Reaper's Scythe", "tier": 3, "grip": "2H", "element": "dark",
        "p_atk": 55, "m_atk": 20, "durability": 100, "max_durability": 100, "sockets": 1, "installed_shards": [],
        "description": "Sabit standar penuai jiwa."
    },
    "emerald_scythe": {
        "id": "emerald_scythe", "name": "Emerald Wind Scythe", "tier": 4, "grip": "2H", "element": "wind",
        "p_atk": 60, "m_atk": 35, "durability": 130, "max_durability": 130, "sockets": 2, "installed_shards": [],
        "description": "Tebasannya memicu badai topan beracun."
    },
    "void_harvester": {
        "id": "void_harvester", "name": "Void Harvester Scythe", "tier": 5, "grip": "2H", "element": "void",
        "p_atk": 90, "m_atk": 60, "durability": 160, "max_durability": 160, "sockets": 3, "installed_shards": [],
        "description": "Sabit yang memotong ruang, bukan hanya daging."
    },

    # ==========================================
    # --- MAGIC STAFFS, WANDS & SCEPTERS ---
    # ==========================================
    "ice_staff": {
        "id": "ice_staff", "name": "Staff of Eternal Frost", "tier": 4, "grip": "2H", "element": "ice",
        "p_atk": 10, "m_atk": 75, "durability": 120, "max_durability": 120, "sockets": 2, "installed_shards": [],
        "description": "Tongkat es abadi. (Diperlukan oleh Blizzard Sovereign)."
    },
    "ice_scepter": {
        "id": "ice_scepter", "name": "Scepter of the Tundra", "tier": 4, "grip": "1H", "element": "ice",
        "p_atk": 5, "m_atk": 55, "durability": 100, "max_durability": 100, "sockets": 1, "installed_shards": [],
        "description": "Tongkat pendek untuk mengatur badai salju."
    },
    "void_grimoire": {
        "id": "void_grimoire", "name": "Archivist Grimoire", "tier": 5, "grip": "2H", "element": "void",
        "p_atk": 5, "m_atk": 95, "durability": 150, "max_durability": 150, "sockets": 3, "installed_shards": [],
        "description": "Buku yang berisi rahasia penciptaan dan kehancuran. (Diperlukan oleh Void Sage)."
    },
    "prism_staff": {
        "id": "prism_staff", "name": "Prismatic Prism Staff", "tier": 5, "grip": "2H", "element": "light",
        "p_atk": 15, "m_atk": 90, "durability": 180, "max_durability": 180, "sockets": 3, "installed_shards": [],
        "description": "Legenda yang membiaskan cahaya menjadi elemen."
    },
    "lich_rib": {
        "id": "lich_rib", "name": "Lich-King’s Rib Staff", "tier": 4, "grip": "2H", "element": "dark",
        "p_atk": 15, "m_atk": 70, "durability": 100, "max_durability": 100, "sockets": 2, "installed_shards": [],
        "description": "Memanggil kedinginan dari alam kubur."
    },
    "inferno_wand": {
        "id": "inferno_wand", "name": "Inferno Ember Wand", "tier": 3, "grip": "1H", "element": "fire",
        "p_atk": 5, "m_atk": 50, "durability": 80, "max_durability": 80, "sockets": 1, "installed_shards": [],
        "description": "Meskipun kecil, panas yang dikeluarkannya bisa melelehkan baja."
    },
    "golem_core_staff": {
        "id": "golem_core_staff", "name": "Earth Golem Staff", "tier": 3, "grip": "2H", "element": "earth",
        "p_atk": 30, "m_atk": 45, "durability": 160, "max_durability": 160, "sockets": 1, "installed_shards": [],
        "description": "Terbuat dari batu utuh dengan inti golem di atasnya."
    },
    "storm_caller_scepter": {
        "id": "storm_caller_scepter", "name": "Storm Caller Scepter", "tier": 4, "grip": "1H", "element": "lightning",
        "p_atk": 10, "m_atk": 65, "durability": 90, "max_durability": 90, "sockets": 2, "installed_shards": [],
        "description": "Petir menyambar-nyambar dari ujungnya."
    },
    "sage_wand": {
        "id": "sage_wand", "name": "Wand of the High Sage", "tier": 4, "grip": "1H", "element": "light",
        "p_atk": 5, "m_atk": 68, "durability": 100, "max_durability": 100, "sockets": 2, "installed_shards": [],
        "description": "Memancarkan aura kebijaksanaan dan penyembuhan."
    },
    "abyssal_grimoire": {
        "id": "abyssal_grimoire", "name": "Tome of the Deep", "tier": 4, "grip": "2H", "element": "water",
        "p_atk": 0, "m_atk": 75, "durability": 120, "max_durability": 120, "sockets": 2, "installed_shards": [],
        "description": "Buku sihir berisi misteri lautan dalam."
    },
    "nature_staff": {
        "id": "nature_staff", "name": "Staff of the Forest", "tier": 3, "grip": "2H", "element": "poison",
        "p_atk": 10, "m_atk": 55, "durability": 110, "max_durability": 110, "sockets": 1, "installed_shards": [],
        "description": "Akar yang melilit membentuk tongkat ajaib."
    },
    
    # ==========================================
    # --- BOWS & CROSSBOWS ---
    # ==========================================
    "oak_shortbow": {
        "id": "oak_shortbow", "name": "Oak-Heart Shortbow", "tier": 3, "grip": "2H", "element": "wind",
        "p_atk": 45, "m_atk": 0, "durability": 90, "max_durability": 90, "sockets": 1, "installed_shards": [],
        "description": "Sangat ringan dan cepat. (Diperlukan oleh Phantom Archer)."
    },
    "black_mamba_bow": {
        "id": "black_mamba_bow", "name": "Black-Mamba Longbow", "tier": 4, "grip": "2H", "element": "dark",
        "p_atk": 65, "m_atk": 10, "durability": 110, "max_durability": 110, "sockets": 2, "installed_shards": [],
        "description": "Panah yang mengejar mangsa dalam kegelapan."
    },
    "venom_crossbow": {
        "id": "venom_crossbow", "name": "Venom-Spit Crossbow", "tier": 4, "grip": "2H", "element": "poison",
        "p_atk": 55, "m_atk": 15, "durability": 100, "max_durability": 100, "sockets": 1, "installed_shards": [],
        "description": "Menghembuskan maut melalui racun."
    },
    "hailstorm_bow": {
        "id": "hailstorm_bow", "name": "Hailstorm Recurve", "tier": 4, "grip": "2H", "element": "ice",
        "p_atk": 50, "m_atk": 25, "durability": 100, "max_durability": 100, "sockets": 1, "installed_shards": [],
        "description": "Busur yang menembakkan serpihan es tajam."
    },
    "lightning_crossbow": {
        "id": "lightning_crossbow", "name": "Storm-Bolt Crossbow", "tier": 5, "grip": "2H", "element": "lightning",
        "p_atk": 85, "m_atk": 20, "durability": 130, "max_durability": 130, "sockets": 2, "installed_shards": [],
        "description": "Melesatkan baut petir lebih cepat dari kedipan mata."
    },
    "fire_bird_bow": {
        "id": "fire_bird_bow", "name": "Phoenix Feather Bow", "tier": 5, "grip": "2H", "element": "fire",
        "p_atk": 80, "m_atk": 40, "durability": 150, "max_durability": 150, "sockets": 2, "installed_shards": [],
        "description": "Anak panahnya terbakar seperti sayap phoenix."
    },
    "elven_longbow": {
        "id": "elven_longbow", "name": "Elven Longbow", "tier": 3, "grip": "2H", "element": "light",
        "p_atk": 50, "m_atk": 10, "durability": 100, "max_durability": 100, "sockets": 1, "installed_shards": [],
        "description": "Busur elegan dengan akurasi sempurna."
    },
    "golem_crossbow": {
        "id": "golem_crossbow", "name": "Heavy Golem Crossbow", "tier": 4, "grip": "2H", "element": "earth",
        "p_atk": 70, "m_atk": 0, "durability": 160, "max_durability": 160, "sockets": 1, "installed_shards": [],
        "description": "Crossbow raksasa yang menembakkan paku baja."
    },
    "abyssal_bow": {
        "id": "abyssal_bow", "name": "Bow of the Abyss", "tier": 5, "grip": "2H", "element": "void",
        "p_atk": 95, "m_atk": 30, "durability": 180, "max_durability": 180, "sockets": 3, "installed_shards": [],
        "description": "Menarik busur ini terasa seperti menarik ruang dan waktu."
    },
    "water_nymph_bow": {
        "id": "water_nymph_bow", "name": "Water Nymph Recurve", "tier": 3, "grip": "2H", "element": "water",
        "p_atk": 42, "m_atk": 25, "durability": 85, "max_durability": 85, "sockets": 1, "installed_shards": [],
        "description": "Sangat fleksibel seperti aliran air."
    },

    # ==========================================
    # --- BLUNT, MACES, HAMMERS & OTHERS ---
    # ==========================================
    "ice_mace": {
        "id": "ice_mace", "name": "Glacial Granite Mace", "tier": 4, "grip": "1H", "element": "ice",
        "p_atk": 55, "m_atk": 20, "durability": 150, "max_durability": 150, "sockets": 1, "installed_shards": [],
        "description": "Gada berat yang membekukan sendi lawan."
    },
    "frost_knuckles": {
        "id": "frost_knuckles", "name": "Frost-Bitten Knuckles", "tier": 4, "grip": "1H", "element": "ice",
        "p_atk": 50, "m_atk": 10, "durability": 200, "max_durability": 200, "sockets": 1, "installed_shards": [],
        "description": "Tinju yang mampu menghancurkan baja membeku."
    },
    "monk_staff": {
        "id": "monk_staff", "name": "Wandering Monk Staff", "tier": 3, "grip": "2H", "element": "wind",
        "p_atk": 45, "m_atk": 10, "durability": 150, "max_durability": 150, "sockets": 1, "installed_shards": [],
        "description": "Tongkat kayu yang fleksibel namun keras."
    },
    "hollow_husk": {
        "id": "hollow_husk", "name": "The Hollow Husk", "tier": 1, "grip": "1H", "element": "none",
        "p_atk": 1, "m_atk": 1, "durability": 999, "max_durability": 999, "sockets": 0, "installed_shards": [],
        "description": "Hanya sebuah cangkang kosong untuk yang tak berwajah. (Diperlukan oleh The Faceless)."
    },
    "thunder_hammer": {
        "id": "thunder_hammer", "name": "Hammer of the Storm", "tier": 5, "grip": "1H", "element": "lightning",
        "p_atk": 85, "m_atk": 35, "durability": 200, "max_durability": 200, "sockets": 2, "installed_shards": [],
        "description": "Gada bergemuruh yang menyimpan kekuatan badai."
    },
    "volcanic_hammer": {
        "id": "volcanic_hammer", "name": "Volcanic Magma Hammer", "tier": 4, "grip": "2H", "element": "fire",
        "p_atk": 80, "m_atk": 25, "durability": 220, "max_durability": 220, "sockets": 1, "installed_shards": [],
        "description": "Gada raksasa dengan lelehan magma di kepalanya."
    },
    "golden_mace": {
        "id": "golden_mace", "name": "Golden Paladin Mace", "tier": 3, "grip": "1H", "element": "light",
        "p_atk": 50, "m_atk": 15, "durability": 130, "max_durability": 130, "sockets": 1, "installed_shards": [],
        "description": "Simbol keadilan dan retaknya tulang tengkorak heretik."
    },
    "abyssal_anchor": {
        "id": "abyssal_anchor", "name": "Deep Sea Anchor", "tier": 5, "grip": "2H", "element": "water",
        "p_atk": 100, "m_atk": 0, "durability": 400, "max_durability": 400, "sockets": 1, "installed_shards": [],
        "description": "Sebuah jangkar raksasa berkarat dari kapal kutukan."
    },
    "shadow_whip": {
        "id": "shadow_whip", "name": "Shadow Spine Whip", "tier": 4, "grip": "1H", "element": "dark",
        "p_atk": 45, "m_atk": 30, "durability": 90, "max_durability": 90, "sockets": 2, "installed_shards": [],
        "description": "Pecut tajam yang terbuat dari tulang punggung monster kegelapan."
    },
    "meteor_flail": {
        "id": "meteor_flail", "name": "Meteor Star Flail", "tier": 5, "grip": "1H", "element": "earth",
        "p_atk": 90, "m_atk": 20, "durability": 180, "max_durability": 180, "sockets": 2, "installed_shards": [],
        "description": "Bola berduri yang terbuat dari inti meteorit."
    },
    "blood_fists": {
        "id": "blood_fists", "name": "Vampiric Fists", "tier": 3, "grip": "1H", "element": "blood",
        "p_atk": 42, "m_atk": 15, "durability": 120, "max_durability": 120, "sockets": 1, "installed_shards": [],
        "description": "Sarung tangan besi dengan duri penyedot darah."
    },
    
    # ==========================================
    # --- SPEARS, HALBERDS, & POLEARMS (2H) ---
    # ==========================================
    "steel_halberd": {
        "id": "steel_halberd", "name": "Steel Halberd", "tier": 2, "grip": "2H", "element": "none",
        "p_atk": 35, "m_atk": 0, "durability": 90, "max_durability": 90, "sockets": 1, "installed_shards": [],
        "description": "Senjata panjang untuk menjaga jarak dari monster."
    },
    "lightning_spear": {
        "id": "lightning_spear", "name": "Thunderclap Spear", "tier": 4, "grip": "2H", "element": "lightning",
        "p_atk": 65, "m_atk": 35, "durability": 130, "max_durability": 130, "sockets": 2, "installed_shards": [],
        "description": "Tombak panjang yang menusuk dengan kecepatan kilat."
    },
    "dragon_lance": {
        "id": "dragon_lance", "name": "Dragonslayer Lance", "tier": 5, "grip": "2H", "element": "fire",
        "p_atk": 95, "m_atk": 10, "durability": 160, "max_durability": 160, "sockets": 2, "installed_shards": [],
        "description": "Tombak raksasa yang dirancang menembus sisik naga."
    },
    "trident_of_depths": {
        "id": "trident_of_depths", "name": "Trident of the Depths", "tier": 4, "grip": "2H", "element": "water",
        "p_atk": 70, "m_atk": 40, "durability": 140, "max_durability": 140, "sockets": 2, "installed_shards": [],
        "description": "Trisula emas yang mengendalikan ombak."
    },
    "poison_pike": {
        "id": "poison_pike", "name": "Viper's Pike", "tier": 3, "grip": "2H", "element": "poison",
        "p_atk": 50, "m_atk": 15, "durability": 100, "max_durability": 100, "sockets": 1, "installed_shards": [],
        "description": "Ujung tombaknya dilapisi racun neurotoksin."
    }
}
