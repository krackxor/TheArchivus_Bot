# game/items/consumables/hp.py

HP_POTIONS = {
    # --- TIER 1: STARTER ---
    "potion_heal": {
        "id": "potion_heal", 
        "name": "Minor HP Potion", 
        "type": "consumable",
        "effect_type": "heal_hp", 
        "value": 30, 
        "tier": 1,
        "description": "Ramuan merah standar untuk memulihkan 30 HP."
    },
    "dried_herbs": {
        "id": "dried_herbs", 
        "name": "Dried Herbs", 
        "type": "consumable",
        "effect_type": "heal_hp", 
        "value": 15, 
        "tier": 1,
        "description": "Tanaman obat kering. Pahit, tapi bisa menutup luka kecil."
    },

    # --- TIER 2: AMATEUR ---
    "potion_heal_average": {
        "id": "potion_heal_average", 
        "name": "Standard HP Potion", 
        "type": "consumable",
        "effect_type": "heal_hp", 
        "value": 55, 
        "tier": 2,
        "description": "Ramuan merah jernih yang umum digunakan oleh para petualang berpengalaman."
    },

    # --- TIER 3: PROFESSIONAL ---
    "potion_heal_major": {
        "id": "potion_heal_major", 
        "name": "Major HP Potion", 
        "type": "consumable",
        "effect_type": "heal_hp", 
        "value": 100, 
        "tier": 3,
        "description": "Ramuan merah pekat dengan konsentrasi tinggi untuk memulihkan 100 HP."
    },
    "vampiric_extract": {
        "id": "vampiric_extract", 
        "name": "Vampiric Extract", 
        "type": "consumable",
        "effect_type": "heal_hp", 
        "value": 85, 
        "tier": 3,
        "description": "Ekstrak darah monster yang diolah. Memulihkan HP sekaligus memberikan sensasi haus darah."
    },

    # --- TIER 4: EXPERT ---
    "potion_heal_grand": {
        "id": "potion_heal_grand", 
        "name": "Grand Master Potion", 
        "type": "consumable",
        "effect_type": "heal_hp", 
        "value": 250, 
        "tier": 4,
        "description": "Hanya sedikit alkemis yang bisa meramu ini. Memulihkan HP dalam jumlah masif."
    },

    # --- TIER 5: MYTHICAL ---
    "elixir_life": {
        "id": "elixir_life", 
        "name": "Elixir of Life", 
        "type": "consumable",
        "effect_type": "heal_hp", 
        "value": 500, 
        "tier": 5,
        "description": "Cairan suci yang memancarkan cahaya. Memulihkan hampir seluruh luka fatal."
    },
    "phoenix_tear": {
        "id": "phoenix_tear", 
        "name": "Phoenix Tear", 
        "type": "consumable",
        "effect_type": "heal_hp", 
        "value": 999, 
        "tier": 5,
        "description": "Air mata burung Phoenix. Legenda mengatakan ini dapat membangkitkan orang dari ambang kematian."
    }
}
