# game/items/consumables/utility.py

UTILITIES = {
    # --- STATUS CLEANSERS (Pembersih Status Efek) ---
    "cure_poison": {
        "id": "cure_poison", 
        "name": "Antidote", 
        "type": "consumable",
        "effect_type": "clear_poison", 
        "value": 0, 
        "tier": 2,
        "description": "Ramuan herbal pahit yang menetralkan segala jenis racun di dalam tubuh."
    },
    "warmth_pack": {
        "id": "warmth_pack", 
        "name": "Warmth Pack", 
        "type": "consumable",
        "effect_type": "clear_chill", 
        "value": 0, 
        "tier": 2,
        "description": "Kantong penghangat instan untuk menghilangkan efek 'Chill' atau membeku."
    },
    "sacred_water": {
        "id": "sacred_water", 
        "name": "Sacred Water", 
        "type": "consumable",
        "effect_type": "clear_all_debuffs", 
        "value": 0, 
        "tier": 4,
        "description": "Air suci yang diberkati. Menghapus semua status efek negatif (debuff) seketika."
    },

    # --- REPAIR KITS (Pemeliharaan Durabilitas) ---
    "repair_kit_minor": {
        "id": "repair_kit_minor", 
        "name": "Minor Repair Kit", 
        "type": "consumable",
        "effect_type": "repair_gear", 
        "value": 25, 
        "tier": 2,
        "description": "Alat perkakas sederhana untuk memulihkan 25 Durabilitas pada gear yang sedang dipakai."
    },
    "repair_kit_master": {
        "id": "repair_kit_master", 
        "name": "Master Repair Kit", 
        "type": "consumable",
        "effect_type": "repair_gear", 
        "value": 100, 
        "tier": 4,
        "description": "Peralatan pandai besi lengkap. Mengembalikan durabilitas seluruh gear ke kondisi maksimal."
    },

    # --- EXPLORATION UTILITY (Alat Bantu Jelajah) ---
    "smoke_bomb": {
        "id": "smoke_bomb", 
        "name": "Smoke Bomb", 
        "type": "consumable",
        "effect_type": "escape_battle", 
        "value": 0, 
        "tier": 3,
        "description": "Bom asap untuk melarikan diri dari pertarungan monster secara instan (100% sukses)."
    },
    "monster_lure": {
        "id": "monster_lure", 
        "name": "Monster Lure", 
        "type": "consumable",
        "effect_type": "increase_encounter", 
        "value": 5, 
        "tier": 3,
        "description": "Umpan berbau tajam yang meningkatkan peluang bertemu monster untuk 5 langkah ke depan."
    },
    "warding_incense": {
        "id": "warding_incense", 
        "name": "Warding Incense", 
        "type": "consumable",
        "effect_type": "decrease_encounter", 
        "value": 10, 
        "tier": 3,
        "description": "Dupa pelindung yang menjauhkan monster lemah selama 10 langkah ke depan."
    },

    # --- TELEPORTATION (Transportasi instan) ---
    "recall_scroll": {
        "id": "recall_scroll", 
        "name": "Recall Scroll", 
        "type": "consumable",
        "effect_type": "teleport_town", 
        "value": 0, 
        "tier": 3,
        "description": "Gulungan sihir yang membawamu kembali ke area aman (Rest Area) terdekat seketika."
    }
}
