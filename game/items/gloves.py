# game/items/gloves.py

"""
DATABASE GLOVES (Sarung Tangan & Gauntlet)
Memberikan perlindungan pada lengan, bonus serangan (P.ATK / M.ATK), 
serta mempengaruhi kecepatan (Speed) dan hindaran (Dodge).
"""

GLOVES = {
    # ==========================================
    # --- STARTER / BASIC GLOVES (TIER 1-2) ---
    # ==========================================
    "cloth_gloves": {
        "id": "cloth_gloves", "name": "Tattered Cloth Gloves", "type": "gloves", "tier": 1,
        "p_def": 1, "m_def": 1, "speed": 1, "weight": 0,
        "description": "Sarung tangan kain tipis yang sudah robek di bagian jari."
    },
    "leather_gloves": {
        "id": "leather_gloves", "name": "Worker's Leather Gloves", "type": "gloves", "tier": 1,
        "p_def": 3, "p_atk": 1, "weight": 1,
        "description": "Sarung tangan kulit kasar yang biasa dipakai pekerja tambang."
    },
    "copper_gauntlets": {
        "id": "copper_gauntlets", "name": "Copper Gauntlets", "type": "gloves", "tier": 1,
        "p_def": 5, "speed": -1, "weight": 3,
        "description": "Pelindung tangan dari tembaga yang membatasi pergerakan jari."
    },
    "apprentice_gloves": {
        "id": "apprentice_gloves", "name": "Apprentice Magician Gloves", "type": "gloves", "tier": 1,
        "m_atk": 3, "m_def": 3, "weight": 0,
        "description": "Sarung tangan rajut dengan sedikit sisa-sisa energi mana."
    },
    "iron_gauntlets": {
        "id": "iron_gauntlets", "name": "Militia Iron Gauntlets", "type": "gloves", "tier": 2,
        "p_def": 8, "p_atk": 3, "speed": -1, "weight": 4,
        "description": "Gauntlet besi standar prajurit penjaga kota."
    },
    "hunter_gloves": {
        "id": "hunter_gloves", "name": "Hunter's Fingerless Gloves", "type": "gloves", "tier": 2,
        "p_atk": 2, "p_def": 4, "speed": 3, "weight": 1,
        "description": "Sarung tangan tanpa jari untuk memudahkan menarik tali busur."
    },
    "acolyte_wraps": {
        "id": "acolyte_wraps", "name": "Acolyte Hand Wraps", "type": "gloves", "tier": 2,
        "m_atk": 5, "m_def": 5, "speed": 2, "weight": 0,
        "description": "Perban kain yang diberkati dengan doa ringan."
    },

    # ==========================================
    # --- INTERMEDIATE GLOVES (TIER 3) ---
    # ==========================================
    "steel_gauntlets": {
        "id": "steel_gauntlets", "name": "Knight's Steel Gauntlets", "type": "gloves", "tier": 3,
        "p_def": 12, "p_atk": 5, "weight": 6,
        "description": "Gauntlet baja tebal. Melindungi tangan dari tebasan pedang lawan."
    },
    "heavy_gauntlets": {
        "id": "heavy_gauntlets", "name": "Titan Steel Gauntlets", "type": "gloves", "tier": 3,
        "p_atk": 10, "p_def": 15, "weight": 8,
        "description": "Genggaman sekuat baja untuk pengguna senjata berat. (Syarat Dread Knight / Templar)."
    },
    "assassin_gloves": {
        "id": "assassin_gloves", "name": "Shadow Assassin Gloves", "type": "gloves", "tier": 3,
        "p_atk": 8, "speed": 5, "dodge": 0.03, "weight": 1,
        "description": "Kain hitam kelam yang meredam suara pergerakan sendi."
    },
    "sage_gloves": {
        "id": "sage_gloves", "name": "Gloves of the Sage", "type": "gloves", "tier": 3,
        "m_atk": 10, "m_def": 10, "weight": 1,
        "description": "Berhiaskan rune emas yang mempercepat rapalan sihir."
    },
    "brawler_wraps": {
        "id": "brawler_wraps", "name": "Pit Brawler Wraps", "type": "gloves", "tier": 3,
        "p_atk": 12, "speed": 4, "p_def": 2, "weight": 1,
        "description": "Perban petarung jalanan yang dilumuri darah kering."
    },
    "thief_grips": {
        "id": "thief_grips", "name": "Burglar's Grip", "type": "gloves", "tier": 3,
        "speed": 8, "dodge": 0.05, "weight": 0,
        "description": "Membantumu memanjat dinding dan mencopet dalam diam."
    },

    # ==========================================
    # --- HIGH-TIER / JOB-SPECIFIC (TIER 4) ---
    # ==========================================
    "archers_cold_grip": {
        "id": "archers_cold_grip", "name": "Archer's Cold Grip", "type": "gloves", "tier": 4,
        "p_atk": 8, "speed": 10, "dodge": 0.05, "weight": 2,
        "description": "Sarung tangan yang menjaga tangan tetap stabil saat membeku. (Syarat Phantom Archer)."
    },
    "weaver_mits": {
        "id": "weaver_mits", "name": "Mana-Weave Mits", "type": "gloves", "tier": 4,
        "m_atk": 18, "m_def": 15, "weight": 1,
        "description": "Sarung tangan sutra yang membantu mengalirkan mana murni. (Syarat Void Sage)."
    },
    "paladin_gauntlets": {
        "id": "paladin_gauntlets", "name": "Holy Paladin Gauntlets", "type": "gloves", "tier": 4,
        "p_atk": 12, "p_def": 20, "m_def": 15, "weight": 7,
        "description": "Baja putih bercahaya yang tidak bisa dinodai oleh kejahatan."
    },
    "blood_claws": {
        "id": "blood_claws", "name": "Vampiric Blood Claws", "type": "gloves", "tier": 4,
        "p_atk": 18, "speed": 6, "m_atk": 10, "weight": 3,
        "description": "Sarung tangan berduri yang mengoyak daging di setiap genggaman."
    },
    "golem_fists": {
        "id": "golem_fists", "name": "Earth-Core Fists", "type": "gloves", "tier": 4,
        "p_atk": 15, "p_def": 25, "speed": -4, "weight": 10,
        "description": "Tinju batu raksasa. Meninju musuh dengan benda ini sama dengan melempar batu besar."
    },
    "storm_bracers": {
        "id": "storm_bracers", "name": "Bracers of the Storm", "type": "gloves", "tier": 4,
        "m_atk": 15, "speed": 12, "weight": 2,
        "description": "Meninggalkan percikan listrik setiap kali tangan digerakkan."
    },

    # ==========================================
    # --- LEGENDARY / MYTHICAL GLOVES (TIER 5) ---
    # ==========================================
    "abyssal_grasps": {
        "id": "abyssal_grasps", "name": "Grasps of the Abyss", "type": "gloves", "tier": 5,
        "m_atk": 25, "p_def": 15, "m_def": 25, "weight": 2,
        "description": "Sarung tangan yang seolah terbuat dari ketiadaan ruang. Benda yang digenggamnya terasa hampa."
    },
    "dragon_scale_gauntlets": {
        "id": "dragon_scale_gauntlets", "name": "Dragon Scale Gauntlets", "type": "gloves", "tier": 5,
        "p_atk": 25, "p_def": 30, "m_def": 15, "weight": 9,
        "description": "Gauntlet dari sisik naga. Sangat panas di bagian luarnya."
    },
    "celestial_hands": {
        "id": "celestial_hands", "name": "Hands of the Celestial", "type": "gloves", "tier": 5,
        "m_atk": 30, "m_def": 30, "speed": 5, "weight": 1,
        "description": "Sarung tangan putih tanpa cela yang memancarkan aura kehidupan."
    },
    "windwalker_wraps": {
        "id": "windwalker_wraps", "name": "Wraps of the Windwalker", "type": "gloves", "tier": 5,
        "p_atk": 15, "speed": 20, "dodge": 0.10, "weight": 0,
        "description": "Begitu ringan hingga tangan pemakainya hampir tidak terlihat saat bergerak."
    },
    "kings_iron_fist": {
        "id": "kings_iron_fist", "name": "The Fallen King's Iron Fist", "type": "gloves", "tier": 5,
        "p_atk": 35, "p_def": 35, "speed": -5, "weight": 12,
        "description": "Pernah menghancurkan kerajaan hanya dengan satu kepalan."
    }
}
