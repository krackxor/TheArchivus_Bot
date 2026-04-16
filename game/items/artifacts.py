# game/items/artifacts.py

ARTIFACT_DB = {
    # --- DEFENSIVE / SHIELDS (Untuk Job Melee/Tank) ---
    "shield_of_light": {
        "id": "shield_of_light",
        "name": "Aegis of the Saint",
        "tier": 4,
        "p_def": 30,
        "m_def": 15,
        "special": "Block: Peluang 15% meniadakan damage fisik.",
        "price": 1100,
        "description": "Perisai suci yang bersinar redup. Wajib untuk Paladin."
    },
    "mountain_wall": {
        "id": "mountain_wall",
        "name": "Great Mountain Wall",
        "tier": 4,
        "p_def": 45,
        "weight": 20,
        "special": "Heavy: Mengurangi Speed musuh saat memukulmu.",
        "price": 1300,
        "description": "Sangat berat, tapi tak tergoyahkan. Cocok untuk Dread Knight."
    },

    # --- MAGIC FOCUS / ORBS (Untuk Job Mage/Ice) ---
    "everfrost_shard": {
        "id": "everfrost_shard",
        "name": "Everfrost Crystal Shard",
        "tier": 4,
        "m_atk": 20,
        "bonus_mp": 50,
        "special": "Deep Chill: Efek Freeze bertahan 1 turn lebih lama.",
        "price": 1500,
        "description": "Inti es yang tidak pernah membeku sepenuhnya. Syarat Blizzard Sovereign."
    },
    "void_orb": {
        "id": "void_orb",
        "name": "Orb of the Abyss",
        "tier": 5,
        "m_atk": 35,
        "special": "Void Echo: Peluang 10% serangan sihir keluar 2x.",
        "price": 2500,
        "description": "Bola hitam yang menghisap cahaya di sekitarnya. Syarat Void Sage."
    },
    "soul_jar": {
        "id": "soul_jar",
        "name": "Ancient Soul Jar",
        "tier": 3,
        "m_atk": 15,
        "special": "Soul Harvest: Pulihkan 5 MP setiap musuh mati.",
        "price": 900,
        "description": "Guci tua untuk menampung sisa-sisa jiwa. Syarat Soul Eater."
    },

    # --- UTILITY / CHARMS (Untuk Job Archer/Support) ---
    "quiver_of_wind": {
        "id": "quiver_of_wind",
        "name": "Quiver of Whispering Wind",
        "tier": 3,
        "speed": 10,
        "accuracy": 15,
        "special": "Tailwind: Serangan Archer selalu menyerang pertama.",
        "price": 850,
        "description": "Tempat anak panah yang membuat panah terasa ringan. Syarat Phantom Archer."
    },
    "blood_gem": {
        "id": "blood_gem",
        "name": "Heart of the Abyss",
        "tier": 5,
        "p_atk": 25,
        "special": "Life Link: Lifesteal meningkat sebesar 15%.",
        "price": 2200,
        "description": "Permata yang berdetak seperti jantung manusia. Syarat Blood Reaper."
    },
    "talisman_of_tundra": {
        "id": "talisman_of_tundra",
        "name": "Talisman of Tundra",
        "tier": 4,
        "m_def": 25,
        "hp_regen": 5,
        "special": "Healing Grace: Efek Heal meningkat 20%.",
        "price": 1200,
        "description": "Jimat dari kutub utara yang menenangkan jiwa. Syarat Arctic Oracle."
    },
    "shadow_pendant": {
        "id": "shadow_pendant",
        "name": "Living Shadow Pendant",
        "tier": 4,
        "dodge": 12,
        "special": "Stealth: Mengurangi kemungkinan diserang musuh.",
        "price": 1400,
        "description": "Kalung yang bisa membiaskan bayangan pemakainya. Syarat Necromancer."
    },
    "toxic_vial": {
        "id": "toxic_vial",
        "name": "Alchemist's Master Vial",
        "tier": 4,
        "special": "Infection: Racun menyebar ke musuh di sekitarnya.",
        "price": 1050,
        "description": "Botol berisi cairan hijau pekat yang bergejolak. Syarat Plague Alchemist."
    }
    # ... (Dan seterusnya untuk melengkapi 20 job)
}
