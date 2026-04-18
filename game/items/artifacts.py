# game/items/artifacts.py

"""
DATABASE ARTIFACTS (Offhand & Relics)
Berfungsi sebagai Tangan Kiri (Shield/Orb) atau Jimat Pasif.
Sangat krusial untuk melengkapi Sinergi Job.
"""

ARTIFACTS = {
    # ==========================================
    # --- DEFENSIVE / SHIELDS (Tank & Melee) ---
    # ==========================================
    "wooden_shield": {
        "id": "wooden_shield", "name": "Crude Wooden Shield", "type": "offhand", "tier": 1,
        "p_def": 10, "weight": 5, "dodge": -0.02,
        "description": "Papan kayu yang diikat tali. Setidaknya bisa menahan gigitan serigala."
    },
    "iron_buckler": {
        "id": "iron_buckler", "name": "Iron Buckler", "type": "offhand", "tier": 2,
        "p_def": 18, "weight": 7, "dodge": -0.01,
        "description": "Perisai besi kecil yang ringan dan efektif untuk tangkisan cepat."
    },
    "shield_of_light": {
        "id": "shield_of_light", "name": "Aegis of the Saint", "type": "offhand", "tier": 4,
        "p_def": 30, "m_def": 20, "weight": 10,
        "description": "Perisai suci yang bersinar redup. (Syarat Holy Templar)."
    },
    "mountain_wall": {
        "id": "mountain_wall", "name": "Great Mountain Wall", "type": "offhand", "tier": 4,
        "p_def": 45, "m_def": 10, "weight": 20, "speed": -5,
        "description": "Sangat berat, tapi tak tergoyahkan. (Syarat Dread Knight)."
    },
    "dragon_scale_greatshield": {
        "id": "dragon_scale_greatshield", "name": "Dragon-Scale Greatshield", "type": "offhand", "tier": 5,
        "p_def": 55, "m_def": 25, "weight": 18,
        "description": "Dibuat dari sisik naga purba, mampu menahan api neraka sekalipun."
    },

    # ==========================================
    # --- MAGIC FOCUS / ORBS (Mage & Elemental) ---
    # ==========================================
    "glass_orb": {
        "id": "glass_orb", "name": "Cloudy Glass Orb", "type": "artifact", "tier": 1,
        "m_atk": 5, "m_def": 2, "weight": 1,
        "description": "Bola kaca buram yang sedikit bergetar saat ada mana di dekatnya."
    },
    "everfrost_shard": {
        "id": "everfrost_shard", "name": "Everfrost Crystal Shard", "type": "artifact", "tier": 4,
        "m_atk": 22, "m_def": 15, "weight": 2,
        "description": "Inti es yang tidak pernah membeku sepenuhnya. (Syarat Blizzard Sovereign)."
    },
    "void_orb": {
        "id": "void_orb", "name": "Orb of the Abyss", "type": "artifact", "tier": 5,
        "m_atk": 35, "m_def": 20, "weight": 2,
        "description": "Bola hitam yang menghisap cahaya di sekitarnya. (Syarat Void Sage & The Faceless)."
    },
    "soul_jar": {
        "id": "soul_jar", "name": "Ancient Soul Jar", "type": "artifact", "tier": 3,
        "m_atk": 15, "m_def": 10, "weight": 3,
        "description": "Guci tua untuk menampung sisa-sisa jiwa. (Syarat Blood Reaper)."
    },
    "phoenix_egg_relic": {
        "id": "phoenix_egg_relic", "name": "Dormant Phoenix Egg", "type": "artifact", "tier": 5,
        "m_atk": 25, "p_atk": 10, "m_def": 20,
        "description": "Terasa sangat panas. Memberikan energi kehidupan yang tak terbatas."
    },

    # ==========================================
    # --- UTILITY / CHARMS (Archer & Assassin) ---
    # ==========================================
    "quiver_of_wind": {
        "id": "quiver_of_wind", "name": "Quiver of Whispering Wind", "type": "artifact", "tier": 3,
        "speed": 10, "dodge": 0.05, "weight": 2,
        "description": "Tempat anak panah yang membuat panah terasa ringan. (Syarat Phantom Archer)."
    },
    "blood_gem": {
        "id": "blood_gem", "name": "Heart of the Abyss", "type": "artifact", "tier": 5,
        "p_atk": 20, "p_def": 10, "weight": 1,
        "description": "Permata yang berdetak seperti jantung manusia. (Syarat Blood Reaper)."
    },
    "shadow_pendant": {
        "id": "shadow_pendant", "name": "Living Shadow Pendant", "type": "artifact", "tier": 4,
        "dodge": 0.12, "speed": 5, "weight": 0,
        "description": "Kalung yang bisa membiaskan bayangan pemakainya."
    },
    "thief_tools": {
        "id": "thief_tools", "name": "Master Thief's Tools", "type": "artifact", "tier": 3,
        "speed": 8, "dodge": 0.08, "weight": 2,
        "description": "Kumpulan kunci dan kawat untuk membongkar rahasia Archivus."
    },
    "lucky_charm": {
        "id": "lucky_charm", "name": "Weaver's Lucky Charm", "type": "artifact", "tier": 2,
        "dodge": 0.05, "speed": 2,
        "description": "Jimat keberuntungan sederhana yang terbuat dari benang takdir."
    },

    # ==========================================
    # --- ALCHEMY & SPECIAL (Support & Craft) ---
    # ==========================================
    "toxic_vial": {
        "id": "toxic_vial", "name": "Alchemist's Master Vial", "type": "artifact", "tier": 4,
        "m_atk": 15, "p_atk": 5, "m_def": 10,
        "description": "Botol berisi cairan hijau pekat yang bergejolak. Menambah daya hancur racun."
    },
    "talisman_of_tundra": {
        "id": "talisman_of_tundra", "name": "Talisman of Tundra", "type": "artifact", "tier": 4,
        "m_def": 25, "m_atk": 10, "weight": 1,
        "description": "Jimat dari kutub utara yang menenangkan jiwa."
    },
    "sacred_tome": {
        "id": "sacred_tome", "name": "Sacred Tome of Grace", "type": "artifact", "tier": 4,
        "m_atk": 15, "m_def": 25, "weight": 3,
        "description": "Kitab suci berisi rapalan doa penyembuhan. (Syarat Holy Templar)."
    },
    "cursed_skull": {
        "id": "cursed_skull", "name": "Skull of the Betrayer", "type": "artifact", "tier": 4,
        "m_atk": 30, "p_def": -10, "m_def": -10,
        "description": "Tengkorak yang terus berbisik. Kekuatan besar dengan bayaran pertahanan."
    },
    "magnifying_glass": {
        "id": "magnifying_glass", "name": "Scholar's Lens", "type": "artifact", "tier": 2,
        "m_atk": 8, "speed": 2,
        "description": "Kaca pembesar untuk meneliti artefak kuno dan kelemahan musuh."
    },

    # ==========================================
    # --- MYTHICAL / ENDGAME (Legendary) ---
    # ==========================================
    "chronos_watch": {
        "id": "chronos_watch", "name": "Shattered Chronos Watch", "type": "artifact", "tier": 5,
        "speed": 25, "dodge": 0.10, "weight": 1,
        "description": "Jam saku yang jarumnya berputar ke belakang. Mengendalikan sedikit aliran waktu."
    },
    "eye_of_beholder": {
        "id": "eye_of_beholder", "name": "Eye of the Beholder", "type": "artifact", "tier": 5,
        "m_atk": 40, "m_def": 30, "weight": 2,
        "description": "Mata yang masih berkedip, memberikan penglihatan menembus dimensi."
    },
    "world_tree_seed": {
        "id": "world_tree_seed", "name": "Seed of the World Tree", "type": "artifact", "tier": 5,
        "m_def": 50, "speed": 10, "weight": 1,
        "description": "Benih kecil yang memancarkan energi kehidupan murni."
    },
    "void_harvester_core": {
        "id": "void_harvester_core", "name": "Void Harvester Core", "type": "artifact", "tier": 5,
        "p_atk": 25, "m_atk": 25, "speed": 10,
        "description": "Inti mesin dari dimensi lain yang haus akan energi."
    },
    "kings_seal": {
        "id": "kings_seal", "name": "Seal of the Fallen King", "type": "artifact", "tier": 5,
        "p_atk": 20, "m_atk": 20, "p_def": 20, "m_def": 20, "weight": 5,
        "description": "Cincin stempel kerajaan yang hancur. Memberikan otoritas mutlak pada pemakainya."
    }
}
