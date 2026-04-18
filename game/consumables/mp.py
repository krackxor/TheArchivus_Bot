# game/items/consumables/mp.py

MP_POTIONS = {
    # --- TIER 1: STARTER ---
    "mana_dust": {
        "id": "mana_dust", 
        "name": "Mana Dust", 
        "type": "consumable",
        "effect_type": "restore_mp", 
        "value": 15, 
        "tier": 1,
        "description": "Serbuk biru halus. Memberikan sedikit percikan memori untuk sihir kecil."
    },
    "potion_mana_minor": {
        "id": "potion_mana_minor", 
        "name": "Minor Mana Potion", 
        "type": "consumable",
        "effect_type": "restore_mp", 
        "value": 25, 
        "tier": 1,
        "description": "Ramuan biru muda yang memulihkan sedikit energi mental."
    },

    # --- TIER 2: AMATEUR ---
    "potion_mana": {
        "id": "potion_mana", 
        "name": "Tetesan Memori", 
        "type": "consumable",
        "effect_type": "restore_mp", 
        "value": 45, 
        "tier": 2,
        "description": "Cairan biru bening yang memulihkan 45 MP. Sangat populer di kalangan penyihir."
    },

    # --- TIER 3: PROFESSIONAL ---
    "potion_mana_major": {
        "id": "potion_mana_major", 
        "name": "Major Mana Potion", 
        "type": "consumable",
        "effect_type": "restore_mp", 
        "value": 80, 
        "tier": 3,
        "description": "Esensi memori yang kental, mampu memulihkan kapasitas sihir dalam jumlah besar."
    },
    "concentrated_mist": {
        "id": "concentrated_mist", 
        "name": "Concentrated Mist", 
        "type": "consumable",
        "effect_type": "restore_mp", 
        "value": 110, 
        "tier": 3,
        "description": "Kabut sihir yang dikompres ke dalam botol. Terasa dingin saat diminum."
    },

    # --- TIER 4: EXPERT ---
    "elixir_mana": {
        "id": "elixir_mana", 
        "name": "Elixir Mana", 
        "type": "consumable",
        "effect_type": "restore_mp", 
        "value": 200, 
        "tier": 4,
        "description": "Esensi sihir murni. Memulihkan 200 MP dengan sangat cepat."
    },
    "sage_brew": {
        "id": "sage_brew", 
        "name": "Sage's Secret Brew", 
        "type": "consumable",
        "effect_type": "restore_mp", 
        "value": 350, 
        "tier": 4,
        "description": "Racikan rahasia para petua. Pikiranmu akan menjadi sangat jernih seketika."
    },

    # --- TIER 5: MYTHICAL ---
    "essence_of_archivus": {
        "id": "essence_of_archivus", 
        "name": "Essence of Archivus", 
        "type": "consumable",
        "effect_type": "restore_mp", 
        "value": 600, 
        "tier": 5,
        "description": "Serpihan energi dari dimensi Archivus itu sendiri. Memulihkan hampir seluruh MP."
    },
    "stellar_tears": {
        "id": "stellar_tears", 
        "name": "Stellar Tears", 
        "type": "consumable",
        "effect_type": "restore_mp", 
        "value": 999, 
        "tier": 5,
        "description": "Air mata bintang yang jatuh ke bumi. Memenuhi seluruh cadangan Mana hingga meluap."
    }
}
