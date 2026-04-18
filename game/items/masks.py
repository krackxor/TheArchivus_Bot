# game/items/masks.py

"""
DATABASE MASKS (Topeng & Penutup Wajah)
Bagian penting dari 8-Slot Equipment. Sering kali memberikan stat unik
seperti Dodge, Speed, Magic Defense, atau menjadi syarat khusus (Requirement)
untuk membuka Job/Class tingkat tinggi.
"""

MASKS = {
    # ==========================================
    # --- STARTER / BASIC MASKS (TIER 1-2) ---
    # ==========================================
    "cloth_mask": {
        "id": "cloth_mask", "name": "Bandit's Cloth Mask", "type": "mask", "tier": 1,
        "p_def": 2, "m_def": 1, "speed": 2, "weight": 0, "dodge": 0.01,
        "description": "Kain usang penutup wajah untuk menghindari debu dan menyembunyikan identitas."
    },
    "leather_half_mask": {
        "id": "leather_half_mask", "name": "Leather Half-Mask", "type": "mask", "tier": 1,
        "p_def": 4, "m_def": 2, "speed": 1, "weight": 1,
        "description": "Topeng kulit separuh wajah. Standar untuk prajurit bayaran."
    },
    "wooden_mask": {
        "id": "wooden_mask", "name": "Tribal Wooden Mask", "type": "mask", "tier": 1,
        "p_def": 3, "m_def": 5, "weight": 1,
        "description": "Topeng kayu ukiran suku kuno. Dipercaya bisa mengusir roh jahat."
    },
    "iron_visor": {
        "id": "iron_visor", "name": "Iron Visor", "type": "mask", "tier": 2,
        "p_def": 8, "m_def": 2, "speed": -1, "weight": 3,
        "description": "Penutup wajah besi. Kokoh tapi sedikit membatasi pandangan."
    },
    "silk_veil": {
        "id": "silk_veil", "name": "Enchanted Silk Veil", "type": "mask", "tier": 2,
        "p_def": 1, "m_def": 8, "dodge": 0.02, "weight": 0,
        "description": "Kain sutra tipis yang ditenun dengan sihir pelindung ringan."
    },
    "bandit_bandana": {
        "id": "bandit_bandana", "name": "Red Bandit Bandana", "type": "mask", "tier": 2,
        "p_def": 3, "m_def": 2, "speed": 3, "weight": 0,
        "description": "Ikat kepala merah yang biasa dipakai oleh penyamun padang pasir."
    },

    # ==========================================
    # --- INTERMEDIATE MASKS (TIER 3) ---
    # ==========================================
    "steel_faceplate": {
        "id": "steel_faceplate", "name": "Steel Faceplate", "type": "mask", "tier": 3,
        "p_def": 15, "m_def": 5, "speed": -2, "weight": 4,
        "description": "Pelat baja tebal yang dipasang di wajah. Sangat berat."
    },
    "assassin_cowl": {
        "id": "assassin_cowl", "name": "Shadow Assassin Cowl", "type": "mask", "tier": 3,
        "p_def": 5, "m_def": 6, "speed": 5, "dodge": 0.05, "weight": 1,
        "description": "Penutup wajah para pembunuh. Melarutkan wajahmu ke dalam bayangan."
    },
    "mage_veil": {
        "id": "mage_veil", "name": "Veil of the Magi", "type": "mask", "tier": 3,
        "p_atk": 0, "m_atk": 8, "p_def": 2, "m_def": 15, "weight": 1,
        "description": "Membantu pemakainya fokus menyalurkan energi mana."
    },
    "bone_mask": {
        "id": "bone_mask", "name": "Hollow Bone Mask", "type": "mask", "tier": 3,
        "p_atk": 4, "p_def": 8, "m_def": 10, "weight": 2,
        "description": "Terbuat dari tengkorak monster tak dikenal. Mengintimidasi lawan."
    },
    "noble_masquerade": {
        "id": "noble_masquerade", "name": "Noble's Masquerade", "type": "mask", "tier": 3,
        "p_def": 4, "m_def": 12, "dodge": 0.03, "weight": 1,
        "description": "Topeng pesta para bangsawan. Diberkati sihir ilusi."
    },

    # ==========================================
    # --- JOB-SPECIFIC & HIGH-TIER MASKS (TIER 4) ---
    # ==========================================
    "frozen_visage": {
        "id": "frozen_visage", "name": "Frozen Visage", "type": "mask", "tier": 4,
        "m_atk": 10, "p_def": 10, "m_def": 25, "weight": 2,
        "description": "Topeng es yang membekukan emosi pemakainya. (Syarat Blizzard Sovereign)."
    },
    "eagle_eye_monocle": {
        "id": "eagle_eye_monocle", "name": "Eagle-Eye Monocle", "type": "mask", "tier": 4,
        "p_def": 2, "m_def": 8, "speed": 10, "dodge": 0.05, "weight": 0,
        "description": "Lensa presisi tinggi untuk membidik titik fatal. (Syarat Phantom Archer)."
    },
    "plague_doctor_mask": {
        "id": "plague_doctor_mask", "name": "Plague Doctor Mask", "type": "mask", "tier": 4,
        "p_def": 12, "m_def": 22, "speed": 2, "weight": 2,
        "description": "Paruh burung berisi rempah penolak wabah. (Syarat Blood Reaper)."
    },
    "holy_visor": {
        "id": "holy_visor", "name": "Radiant Holy Visor", "type": "mask", "tier": 4,
        "p_def": 18, "m_def": 18, "weight": 3,
        "description": "Penutup wajah para ksatria suci yang bersinar dalam gelap. (Syarat Holy Templar)."
    },
    "demon_jaw": {
        "id": "demon_jaw", "name": "Crimson Demon Jaw", "type": "mask", "tier": 4,
        "p_atk": 12, "p_def": 14, "m_def": 5, "weight": 3,
        "description": "Topeng pelindung rahang berbentuk iblis mengamuk."
    },
    "kitsune_mask": {
        "id": "kitsune_mask", "name": "Spirit Kitsune Mask", "type": "mask", "tier": 4,
        "m_atk": 5, "p_def": 5, "m_def": 15, "speed": 8, "dodge": 0.08, "weight": 1,
        "description": "Topeng rubah ekor sembilan. Membuat gerakan pemakainya sangat lincah."
    },
    "golem_visage": {
        "id": "golem_visage", "name": "Earth-Golem Visage", "type": "mask", "tier": 4,
        "p_def": 25, "m_def": 15, "speed": -5, "weight": 6,
        "description": "Topeng batu padat. Sangat berat tapi tidak bisa ditembus anak panah."
    },
    "phantom_opera_mask": {
        "id": "phantom_opera_mask", "name": "Phantom Opera Mask", "type": "mask", "tier": 4,
        "m_atk": 15, "m_def": 18, "dodge": 0.04, "weight": 1,
        "description": "Setengah wajahmu tertutup, menambah aura misteri dan sihir."
    },

    # ==========================================
    # --- LEGENDARY / MYTHICAL MASKS (TIER 5) ---
    # ==========================================
    "ancient_mask": {
        "id": "ancient_mask", "name": "The Ancient Mask", "type": "mask", "tier": 5,
        "p_atk": 8, "m_atk": 8, "p_def": 20, "m_def": 20, "speed": 5, "weight": 2,
        "description": "Topeng tanpa wajah. (Syarat The Faceless, Void Sage & Dread Knight)."
    },
    "abyssal_veil": {
        "id": "abyssal_veil", "name": "Veil of the Abyss", "type": "mask", "tier": 5,
        "p_def": 15, "m_def": 35, "dodge": 0.05, "weight": 1,
        "description": "Kain penutup dari dimensi void. Menyerap semua sihir yang diarahkan ke wajahmu."
    },
    "dragon_priest_mask": {
        "id": "dragon_priest_mask", "name": "Dragon Priest Mask", "type": "mask", "tier": 5,
        "p_atk": 15, "m_atk": 15, "p_def": 22, "m_def": 22, "weight": 3,
        "description": "Topeng emas para pemuja naga kuno. Memancarkan panas yang luar biasa."
    },
    "blindfold_of_sight": {
        "id": "blindfold_of_sight", "name": "Blindfold of True Sight", "type": "mask", "tier": 5,
        "p_def": 5, "m_def": 30, "speed": 15, "dodge": 0.15, "weight": 0,
        "description": "Menutup mata jasmani untuk membuka mata batin. Hindaran meningkat drastis."
    },
    "crown_of_thorns": {
        "id": "crown_of_thorns", "name": "Martyr's Crown of Thorns", "type": "mask", "tier": 5,
        "p_atk": 25, "m_atk": 25, "p_def": -10, "m_def": -10, "weight": 1,
        "description": "Mahkota berduri yang melukai pemakainya, namun memberi kekuatan serangan yang mengerikan."
    },
    "celestial_halo": {
        "id": "celestial_halo", "name": "Celestial Halo Visor", "type": "mask", "tier": 5,
        "m_atk": 20, "p_def": 25, "m_def": 30, "weight": 2,
        "description": "Cahaya suci yang melingkari kepala, menolak segala bentuk kutukan."
    }
}
