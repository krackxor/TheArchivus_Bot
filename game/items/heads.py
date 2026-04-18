# game/items/heads.py

"""
DATABASE HEADS (Helm & Penutup Kepala)
Memberikan perlindungan defensif utama, sering kali memiliki bobot (weight) yang
berpengaruh pada speed/dodge pemain, atau memberikan bonus magic.
"""

HEADS = {
    # ==========================================
    # --- STARTER / BASIC HEADS (TIER 1-2) ---
    # ==========================================
    "cloth_cap": {
        "id": "cloth_cap", "name": "Peasant's Cloth Cap", "type": "head", "tier": 1,
        "p_def": 3, "m_def": 2, "weight": 1,
        "description": "Topi kain sederhana. Setidaknya melindungimu dari terik matahari."
    },
    "leather_cap": {
        "id": "leather_cap", "name": "Sturdy Leather Cap", "type": "head", "tier": 1,
        "p_def": 6, "m_def": 3, "weight": 2,
        "description": "Topi kulit yang dijahit kasar. Cukup menahan goresan."
    },
    "copper_helm": {
        "id": "copper_helm", "name": "Dented Copper Helm", "type": "head", "tier": 1,
        "p_def": 10, "m_def": 0, "speed": -1, "weight": 4,
        "description": "Helm tembaga penyok peninggalan prajurit yang gugur."
    },
    "apprentice_hat": {
        "id": "apprentice_hat", "name": "Apprentice's Pointy Hat", "type": "head", "tier": 1,
        "p_def": 2, "m_def": 8, "weight": 1,
        "description": "Topi kerucut khas pelajar sihir. Agak memalukan untuk dipakai."
    },
    "iron_skullcap": {
        "id": "iron_skullcap", "name": "Iron Skullcap", "type": "head", "tier": 2,
        "p_def": 15, "m_def": 2, "speed": -1, "weight": 5,
        "description": "Pelindung kepala dari besi utuh. Menahan pukulan tumpul dengan baik."
    },
    "ranger_hood": {
        "id": "ranger_hood", "name": "Ranger's Green Hood", "type": "head", "tier": 2,
        "p_def": 8, "m_def": 6, "speed": 2, "weight": 2,
        "description": "Penutup kepala dari kain tebal yang menyatu dengan alam."
    },
    "acolyte_cowl": {
        "id": "acolyte_cowl", "name": "Acolyte's White Cowl", "type": "head", "tier": 2,
        "p_def": 4, "m_def": 12, "weight": 1,
        "description": "Kudung putih bersih milik pelayan kuil."
    },

    # ==========================================
    # --- INTERMEDIATE HEADS (TIER 3) ---
    # ==========================================
    "steel_helmet": {
        "id": "steel_helmet", "name": "Knight's Steel Helmet", "type": "head", "tier": 3,
        "p_def": 25, "m_def": 5, "speed": -2, "weight": 8,
        "description": "Helm baja standar prajurit elit. Sangat kokoh."
    },
    "iron_helm": {
        "id": "iron_helm", "name": "Dread Iron Helm", "type": "head", "tier": 3,
        "p_def": 28, "m_def": 5, "weight": 10,
        "description": "Helm baja tertutup yang memberikan rasa aman semu. (Syarat Dread Knight)."
    },
    "leather_hood": {
        "id": "leather_hood", "name": "Scout's Leather Hood", "type": "head", "tier": 3,
        "p_def": 12, "m_def": 10, "speed": 5, "weight": 2,
        "description": "Penutup kepala ringan untuk menjaga penglihatan tetap tajam. (Syarat Phantom Archer)."
    },
    "sage_circlet": {
        "id": "sage_circlet", "name": "Circlet of the Sage", "type": "head", "tier": 3,
        "m_atk": 10, "p_def": 5, "m_def": 20, "weight": 1,
        "description": "Mahkota kecil yang memusatkan energi mental."
    },
    "hunter_trapper_hat": {
        "id": "hunter_trapper_hat", "name": "Beast-Trapper Hat", "type": "head", "tier": 3,
        "p_def": 15, "m_def": 8, "speed": 2, "weight": 3,
        "description": "Topi tebal dari kulit beruang. Hangat dan tangguh."
    },
    "gladiator_helm": {
        "id": "gladiator_helm", "name": "Arena Gladiator Helm", "type": "head", "tier": 3,
        "p_atk": 5, "p_def": 20, "m_def": 2, "speed": 1, "weight": 6,
        "description": "Helm berhias bulu merah, dirancang untuk mengintimidasi."
    },

    # ==========================================
    # --- HIGH-TIER / JOB-SPECIFIC (TIER 4) ---
    # ==========================================
    "circlet_of_north": {
        "id": "circlet_of_north", "name": "Circlet of the North", "type": "head", "tier": 4,
        "m_atk": 15, "p_def": 8, "m_def": 25, "weight": 2,
        "description": "Mahkota kristal yang memancarkan aura dingin abadi. (Syarat Blizzard Sovereign)."
    },
    "weaver_hood": {
        "id": "weaver_hood", "name": "Oracle's Veil", "type": "head", "tier": 4,
        "m_atk": 10, "p_def": 10, "m_def": 30, "weight": 1,
        "description": "Kain sutra yang diberkati untuk para pendeta es. (Syarat Void Sage)."
    },
    "paladin_greathelm": {
        "id": "paladin_greathelm", "name": "Paladin's Greathelm", "type": "head", "tier": 4,
        "p_def": 35, "m_def": 15, "speed": -3, "weight": 12,
        "description": "Helm suci yang diberkati. Sangat berat tapi menolak ilmu hitam."
    },
    "shadow_crown": {
        "id": "shadow_crown", "name": "Crown of Shadows", "type": "head", "tier": 4,
        "p_atk": 10, "m_atk": 10, "p_def": 12, "m_def": 12, "speed": 3, "weight": 2,
        "description": "Mahkota bergerigi yang terbuat dari bayangan padat."
    },
    "valkyrie_tiara": {
        "id": "valkyrie_tiara", "name": "Valkyrie's Winged Tiara", "type": "head", "tier": 4,
        "m_atk": 12, "p_def": 15, "m_def": 20, "speed": 8, "weight": 2,
        "description": "Hiasan kepala bersayap yang memberikan kecepatan luar biasa."
    },
    "golem_core_helm": {
        "id": "golem_core_helm", "name": "Earth-Core Helm", "type": "head", "tier": 4,
        "p_def": 40, "m_def": 5, "speed": -5, "weight": 15,
        "description": "Sebongkah batu ajaib yang diukir menjadi helm."
    },
    "blood_moon_cowl": {
        "id": "blood_moon_cowl", "name": "Cowl of the Blood Moon", "type": "head", "tier": 4,
        "p_atk": 15, "p_def": 18, "m_def": 18, "weight": 3,
        "description": "Tudung merah pekat yang membangkitkan haus darah penggunanya."
    },

    # ==========================================
    # --- LEGENDARY / MYTHICAL HEADS (TIER 5) ---
    # ==========================================
    "crown_of_the_abyss": {
        "id": "crown_of_the_abyss", "name": "Crown of the Abyss", "type": "head", "tier": 5,
        "p_atk": 15, "m_atk": 30, "p_def": 20, "m_def": 40, "weight": 3,
        "description": "Mahkota hitam berdenyut yang menyimpan kekuatan kehampaan."
    },
    "dragon_scale_helm": {
        "id": "dragon_scale_helm", "name": "Dragon Scale Helm", "type": "head", "tier": 5,
        "p_atk": 20, "p_def": 50, "m_def": 25, "speed": -2, "weight": 14,
        "description": "Helm maha kuat yang ditempa dari tengkorak dan sisik naga merah."
    },
    "halo_of_the_seraph": {
        "id": "halo_of_the_seraph", "name": "Halo of the Seraph", "type": "head", "tier": 5,
        "m_atk": 25, "p_def": 25, "m_def": 50, "speed": 5, "weight": 0,
        "description": "Lingkaran cahaya murni yang melayang di atas kepala pemakainya."
    },
    "tempest_crown": {
        "id": "tempest_crown", "name": "Crown of the Tempest", "type": "head", "tier": 5,
        "p_atk": 10, "m_atk": 20, "p_def": 20, "m_def": 20, "speed": 15, "weight": 1,
        "description": "Angin topan miniatur berputar abadi di sekitar mahkota ini."
    },
    "kings_fallen_crown": {
        "id": "kings_fallen_crown", "name": "The Fallen King's Crown", "type": "head", "tier": 5,
        "p_atk": 30, "m_atk": 30, "p_def": -10, "m_def": -10, "weight": 5,
        "description": "Mahkota raja gila. Mengorbankan pertahanan demi kekuatan penghancur absolut."
    }
}
