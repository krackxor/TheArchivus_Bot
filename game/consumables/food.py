# game/items/consumables/food.py

FOODS = {
    # --- TIER 1: BASIC (Survival Dasar) ---
    "food_ration": {
        "id": "food_ration", 
        "name": "Roti Kering", 
        "type": "consumable",
        "effect_type": "restore_energy", 
        "value": 30, 
        "tier": 1,
        "description": "Cukup untuk mengganjal perut dan menambah 30 Energi. Rasanya hambar namun mengenyangkan."
    },
    "wild_berries": {
        "id": "wild_berries", 
        "name": "Wild Berries", 
        "type": "consumable",
        "effect_type": "restore_energy", 
        "value": 15, 
        "tier": 1,
        "description": "Buah berry hutan yang asam. Memberikan sedikit asupan energi instan."
    },

    # --- TIER 2: COOKED (Makanan Olahan) ---
    "food_meat": {
        "id": "food_meat", 
        "name": "Daging Panggang", 
        "type": "consumable",
        "effect_type": "restore_energy", 
        "value": 60, 
        "tier": 2,
        "description": "Daging lezat yang dibakar dengan api unggun. Memulihkan 60 Energi."
    },
    "vegetable_stew": {
        "id": "vegetable_stew", 
        "name": "Rebusan Sayur", 
        "type": "consumable",
        "effect_type": "restore_energy", 
        "value": 50, 
        "tier": 2,
        "description": "Sup hangat yang menyehatkan, memulihkan energi dan memberikan rasa nyaman."
    },

    # --- TIER 3: FEAST (Hidangan Lengkap) ---
    "smoked_ribs": {
        "id": "smoked_ribs", 
        "name": "Smoked Ribs", 
        "type": "consumable",
        "effect_type": "restore_energy", 
        "value": 100, 
        "tier": 3,
        "description": "Iga asap bumbu rempah. Sangat padat energi, cocok sebelum pertempuran besar."
    },
    "honey_glaze_ham": {
        "id": "honey_glaze_ham", 
        "name": "Honey Glaze Ham", 
        "type": "consumable",
        "effect_type": "restore_energy", 
        "value": 125, 
        "tier": 3,
        "description": "Daging paha bumbu madu. Memberikan ledakan energi yang bertahan lama."
    },

    # --- TIER 4: GOURMET (Masakan Master) ---
    "monster_curry": {
        "id": "monster_curry", 
        "name": "Monster Curry", 
        "type": "consumable",
        "effect_type": "restore_energy", 
        "value": 200, 
        "tier": 4,
        "description": "Kari pedas dari bagian tubuh monster langka. Membakar semangat dan energi hingga 200 unit."
    },

    # --- TIER 5: LEGENDARY (Hidangan Dewa) ---
    "dragon_steak": {
        "id": "dragon_steak", 
        "name": "Steak Naga Unggul", 
        "type": "consumable",
        "effect_type": "restore_energy", 
        "value": 500, 
        "tier": 5,
        "description": "Potongan daging naga purba yang sangat langka. Memulihkan seluruh energi dan rasa lelah seketika."
    },
    "ambrosia_nectar": {
        "id": "ambrosia_nectar", 
        "name": "Ambrosia Nectar", 
        "type": "consumable",
        "effect_type": "restore_energy", 
        "value": 999, 
        "tier": 5,
        "description": "Minuman para dewa. Menghilangkan segala rasa lapar dan lelah untuk waktu yang sangat lama."
    }
}
