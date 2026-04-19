# game/items/armors.py

"""
====================================================================
DATABASE ARMORS (Baju Zirah & Jubah Utama) - The Archivus
====================================================================
File ini menyimpan seluruh data item untuk slot 'Armor' (Badan).
Slot ini adalah penyumbang terbesar untuk Physical Defense (P_DEF).

ATURAN BALANCE (KESEIMBANGAN):
- Armor Berat (Plate/Cuirass) memberikan P_DEF maksimal namun 
  memiliki penalti Weight yang paling tinggi di game. Hal ini akan 
  mengurangi Speed secara drastis (Minus Speed).
- Armor Tipe Kain (Robe/Tunic) fokus pada Magic Defense (M_DEF)
  dan memiliki beban yang jauh lebih ringan.

SINKRONISASI HAZARDS:
Item berawalan 'item_' di bawah ini adalah syarat mutlak (Requirement)
agar pemain bisa selamat melintasi anomali udara tajam (Angin Silet)
pada sistem hazards.py.
====================================================================
"""

ARMORS = {
    # ==========================================
    # --- STARTER / BASIC ARMORS (TIER 1-2) ---
    # ==========================================
    "cloth_tunic": {
        "id": "cloth_tunic", "name": "Peasant's Cloth Tunic", "type": "armor", "tier": 1,
        "p_def": 5, "m_def": 2, "weight": 2,
        "description": "Pakaian kain biasa yang kasar. Memberikan perlindungan minimal."
    },
    "leather_armor": {
        "id": "leather_armor", "name": "Hardened Leather Armor", "type": "armor", "tier": 1,
        "p_def": 12, "m_def": 5, "weight": 6,
        "description": "Baju dari kulit binatang yang dikeraskan. Standar untuk petualang baru."
    },
    "padded_vest": {
        "id": "padded_vest", "name": "Padded Gambit Vest", "type": "armor", "tier": 1,
        "p_def": 8, "m_def": 8, "weight": 4,
        "description": "Rompi berlapis kain tebal, cukup ringan dan nyaman."
    },
    "iron_cuirass": {
        "id": "iron_cuirass", "name": "Militia Iron Cuirass", "type": "armor", "tier": 2,
        "p_def": 25, "m_def": 2, "weight": 15,
        "description": "Lempengan besi pelindung dada. Cukup berat untuk pemula."
    },
    "enchanted_robes": {
        "id": "enchanted_robes", "name": "Enchanted Weaver Robes", "type": "armor", "tier": 2,
        "p_def": 5, "m_def": 18, "weight": 3,
        "description": "Jubah sutra yang ditenun dengan sedikit energi mana."
    },
    "studded_leather": {
        "id": "studded_leather", "name": "Studded Leather Armor", "type": "armor", "tier": 2,
        "p_def": 18, "m_def": 8, "weight": 8,
        "description": "Armor kulit yang diperkuat dengan paku-paku besi."
    },

    # ==========================================
    # --- HAZARD PROTECTION ARMORS (TIER 3) ---
    # ==========================================
    # 1. Pelindung PISAU (Lorong Angin Silet)
    "item_zirah_rantai_perak": {
        "id": "item_zirah_rantai_perak", "name": "Zirah Rantai Perak (Chainmail)", "type": "armor", "tier": 3,
        "p_def": 25, "m_def": 15, "speed": -2, "weight": 12,
        "description": "Rantai baja murni yang dilapisi perak. Sanggup memercikkan dan menahan sayatan angin silet yang mematikan."
    },

    # ==========================================
    # --- INTERMEDIATE ARMORS (TIER 3) ---
    # ==========================================
    "steel_plate": {
        "id": "steel_plate", "name": "Knight's Steel Plate", "type": "armor", "tier": 3,
        "p_def": 40, "m_def": 10, "weight": 25,
        "description": "Zirah baja standar ksatria kerajaan. Memberikan pertahanan fisik yang solid."
    },
    "assassin_garb": {
        "id": "assassin_garb", "name": "Shadow-Step Tunic", "type": "armor", "tier": 3,
        "p_def": 15, "m_def": 12, "speed": 10, "dodge": 0.05, "weight": 4,
        "description": "Pakaian ringan untuk bergerak dalam gelap. (Syarat Job: Phantom Archer & Blood Reaper)."
    },
    "sage_robe": {
        "id": "sage_robe", "name": "Robe of the Arch-Sage", "type": "armor", "tier": 3,
        "p_def": 8, "m_def": 35, "m_atk": 10, "weight": 5,
        "description": "Jubah megah yang bergetar karena energi sihir yang kuat."
    },
    "brigandine": {
        "id": "brigandine", "name": "Veteran's Brigandine", "type": "armor", "tier": 3,
        "p_def": 32, "m_def": 15, "weight": 18,
        "description": "Kombinasi kulit tebal dan lempengan besi di dalamnya."
    },
    "ranger_tunic": {
        "id": "ranger_tunic", "name": "Wilderness Ranger Tunic", "type": "armor", "tier": 3,
        "p_def": 20, "m_def": 15, "speed": 5, "dodge": 0.03, "weight": 7,
        "description": "Armor tangguh yang tidak membatasi mobilitas di alam liar."
    },

    # ==========================================
    # --- HIGH-TIER / JOB-SPECIFIC (TIER 4) ---
    # ==========================================
    "glacier_plate": {
        "id": "glacier_plate", "name": "Glacier Plate Mail", "type": "armor", "tier": 4,
        "p_def": 55, "m_def": 20, "weight": 28, "element": "ice",
        "description": "Zirah berat dari es abadi. (Syarat Job: The Faceless)."
    },
    "blizzard_robe": {
        "id": "blizzard_robe", "name": "Blizzard Weaver Robe", "type": "armor", "tier": 4,
        "p_def": 12, "m_def": 50, "m_atk": 15, "weight": 5, "element": "ice",
        "description": "Jubah tipis yang memancarkan hawa dingin. (Syarat Job: Blizzard Sovereign & Void Sage)."
    },
    "full_plate_mail": {
        "id": "full_plate_mail", "name": "Dread Emperor Plate", "type": "armor", "tier": 4,
        "p_def": 70, "m_def": 10, "weight": 35, "element": "earth",
        "description": "Zirah hitam legam yang sangat berat. (Syarat Job: Dread Knight)."
    },
    "templar_plate": {
        "id": "templar_plate", "name": "Holy Templar Plate", "type": "armor", "tier": 4,
        "p_def": 60, "m_def": 30, "weight": 30, "element": "light",
        "description": "Zirah perak bercahaya yang diberkati. (Syarat Job: Holy Templar)."
    },
    "dragon_hide_armor": {
        "id": "dragon_hide_armor", "name": "Dragon Hide Armor", "type": "armor", "tier": 4,
        "p_def": 45, "m_def": 25, "weight": 12, "element": "fire",
        "description": "Dibuat dari kulit naga muda. Sangat tahan terhadap panas."
    },
    "storm_chaser_mail": {
        "id": "storm_chaser_mail", "name": "Storm Chaser Mail", "type": "armor", "tier": 4,
        "p_def": 35, "m_def": 20, "speed": 15, "weight": 10, "element": "lightning",
        "description": "Rantai besi ringan yang dialiri energi kinetik badai."
    },

    # ==========================================
    # --- LEGENDARY / MYTHICAL ARMORS (TIER 5) ---
    # ==========================================
    "abyssal_plate": {
        "id": "abyssal_plate", "name": "Cataclysm Abyssal Plate", "type": "armor", "tier": 5,
        "p_def": 85, "m_def": 30, "weight": 40,
        "description": "Zirah yang ditempa di inti bumi. Hampir mustahil ditembus senjata biasa."
    },
    "void_raiment": {
        "id": "void_raiment", "name": "Raiment of the Void", "type": "armor", "tier": 5,
        "p_def": 20, "m_def": 75, "dodge": 0.10, "weight": 4,
        "description": "Pakaian yang terbuat dari ketiadaan. Serangan sihir seolah melewati tubuhmu."
    },
    "celestial_armor": {
        "id": "celestial_armor", "name": "Celestial Sun-Plate", "type": "armor", "tier": 5,
        "p_def": 65, "m_def": 50, "m_atk": 20, "weight": 20,
        "description": "Zirah emas para dewa yang bersinar seterang matahari siang hari."
    },
    "blood_god_regalia": {
        "id": "blood_god_regalia", "name": "Regalia of the Blood God", "type": "armor", "tier": 5,
        "p_atk": 25, "p_def": 50, "m_def": 20, "weight": 15,
        "description": "Armor merah tua yang terus haus akan darah musuh."
    },
    "titan_exoskeleton": {
        "id": "titan_exoskeleton", "name": "Titan Exoskeleton", "type": "armor", "tier": 5,
        "p_def": 100, "m_def": 5, "speed": -15, "weight": 50,
        "description": "Kerangka luar raksasa purba. Membuatmu menjadi benteng berjalan yang lamban."
    },
    "wind_god_garb": {
        "id": "wind_god_garb", "name": "Garb of the Wind God", "type": "armor", "tier": 5,
        "p_def": 30, "m_def": 30, "speed": 30, "dodge": 0.20, "weight": 2,
        "description": "Sangat ringan hingga pemakainya bisa bergerak secepat kilat."
    }
}
