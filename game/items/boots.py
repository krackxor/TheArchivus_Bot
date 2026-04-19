# game/items/boots.py

"""
====================================================================
DATABASE BOOTS (Sepatu & Greaves) - The Archivus
====================================================================
File ini menyimpan seluruh data item untuk slot 'Boots' (Sepatu).
Fokus utama pada slot ini adalah menentukan mobilitas karakter
melalui penambahan kelincahan (Speed) dan peluang menghindar (Dodge).

ATURAN BALANCE (KESEIMBANGAN):
- Sepatu zirah (Sabatons/Greaves) memberikan Physical Defense (P_DEF) 
  tinggi, tapi membebani berat (Weight) pemain. Hal ini berujung pada 
  pengurangan Speed secara keseluruhan (minus speed).
- Sepatu dari bahan ringan (kain, kulit, bayangan) memberikan bonus
  Speed dan Dodge, tetapi sangat rentan terhadap tebasan senjata fisik.

SINKRONISASI HAZARDS:
Item berawalan 'item_' di bawah ini adalah syarat mutlak (Requirement)
agar pemain bisa selamat melintasi anomali tanah seperti Rawa Lumpur, 
Genangan Asam, dan Lantai Berduri pada sistem hazards.py.
====================================================================
"""

BOOTS = {
    # ==========================================
    # --- STARTER / BASIC BOOTS (TIER 1-2) ---
    # ==========================================
    "cloth_shoes": {
        "id": "cloth_shoes", "name": "Peasant's Cloth Shoes", "type": "boots", "tier": 1,
        "p_def": 1, "speed": 2, "weight": 0,
        "description": "Sepatu kain tipis. Nyaman, tapi kakimu akan basah jika menginjak genangan."
    },
    "leather_boots": {
        "id": "leather_boots", "name": "Worn Leather Boots", "type": "boots", "tier": 1,
        "p_def": 3, "speed": 1, "weight": 1,
        "description": "Sepatu bot kulit usang milik para pengembara."
    },
    "heavy_work_boots": {
        "id": "heavy_work_boots", "name": "Heavy Work Boots", "type": "boots", "tier": 1,
        "p_def": 5, "speed": -1, "weight": 3,
        "description": "Sepatu pekerja tambang dengan ujung besi pelindung jari."
    },
    "apprentice_shoes": {
        "id": "apprentice_shoes", "name": "Apprentice Shoes", "type": "boots", "tier": 1,
        "m_def": 3, "speed": 1, "weight": 0,
        "description": "Sepatu pantofel rapi seragam pelajar akademi."
    },
    "iron_greaves": {
        "id": "iron_greaves", "name": "Militia Iron Greaves", "type": "boots", "tier": 2,
        "p_def": 8, "speed": -2, "weight": 5,
        "description": "Pelindung tulang kering dari pelat besi."
    },
    "ranger_boots": {
        "id": "ranger_boots", "name": "Ranger's Swift Boots", "type": "boots", "tier": 2,
        "p_def": 4, "speed": 5, "dodge": 0.02, "weight": 1,
        "description": "Dirancang untuk bermanuver cepat di dalam hutan."
    },
    "acolyte_sandals": {
        "id": "acolyte_sandals", "name": "Acolyte Sandals", "type": "boots", "tier": 2,
        "m_def": 5, "speed": 3, "weight": 0,
        "description": "Sandal terbuka yang ringan. Tidak disarankan untuk area bersalju."
    },

    # ==========================================
    # --- HAZARD PROTECTION BOOTS (TIER 3) ---
    # ==========================================
    # 1. Pelindung RAWA (Lumpur Penghisap)
    "item_boots_heavy": {
        "id": "item_boots_heavy", "name": "Heavy Gravity Boots", "type": "boots", "tier": 3,
        "p_def": 8, "speed": -3, "weight": 6,
        "description": "Sepatu dengan sol pemberat yang dirancang khusus untuk memijak kuat di atas lumpur hidup."
    },
    # 2. Pelindung ASAM (Genangan Asam Pelebur)
    "item_sepatu_karet_tebal": {
        "id": "item_sepatu_karet_tebal", "name": "Sepatu Karet Alkimia", "type": "boots", "tier": 3,
        "p_def": 4, "m_def": 12, "speed": -1, "weight": 2,
        "description": "Terbuat dari getah pohon iblis, sepatu ini sama sekali tidak bisa dilelehkan oleh genangan asam."
    },
    # 3. Pelindung DURI (Lantai Kaca Berduri)
    "item_pelindung_kaki_baja": {
        "id": "item_pelindung_kaki_baja", "name": "Pelindung Kaki Baja Solid", "type": "boots", "tier": 3,
        "p_def": 18, "m_def": 2, "speed": -4, "weight": 8,
        "description": "Telapak baja tebal ini akan meremukkan kaca tajam dan duri karatan menjadi debu saat diinjak."
    },

    # ==========================================
    # --- INTERMEDIATE BOOTS (TIER 3) ---
    # ==========================================
    "steel_sabatons": {
        "id": "steel_sabatons", "name": "Knight's Steel Sabatons", "type": "boots", "tier": 3,
        "p_def": 12, "speed": -3, "weight": 7,
        "description": "Sepatu zirah baja utuh. Sulit dipakai berlari, namun sangat kokoh."
    },
    "scout_boots": {
        "id": "scout_boots", "name": "Silent Scout Boots", "type": "boots", "tier": 3,
        "p_def": 5, "m_def": 5, "speed": 10, "dodge": 0.05, "weight": 2,
        "description": "Dibuat dari kulit hewan langka, tidak bersuara saat melangkah. (Syarat Job: Phantom Archer, Void Sage, Blood Reaper)."
    },
    "sage_shoes": {
        "id": "sage_shoes", "name": "Shoes of the Sage", "type": "boots", "tier": 3,
        "m_atk": 5, "m_def": 10, "speed": 2, "weight": 1,
        "description": "Sol sepatunya dipenuhi rajahan rune pemulih energi."
    },
    "assassin_striders": {
        "id": "assassin_striders", "name": "Shadow Assassin Striders", "type": "boots", "tier": 3,
        "p_def": 4, "speed": 12, "dodge": 0.08, "weight": 1,
        "description": "Sepatu pembunuh bayaran. Membantu melompat dari atap ke atap."
    },
    "gladiator_sandals": {
        "id": "gladiator_sandals", "name": "Arena Gladiator Sandals", "type": "boots", "tier": 3,
        "p_atk": 3, "p_def": 6, "speed": 4, "weight": 2,
        "description": "Sandal kulit tebal berbalut tembaga khas petarung Colosseum."
    },

    # ==========================================
    # --- HIGH-TIER / JOB-SPECIFIC (TIER 4) ---
    # ==========================================
    "permafrost_treads": {
        "id": "permafrost_treads", "name": "Permafrost Treads", "type": "boots", "tier": 4,
        "m_def": 10, "speed": 8, "dodge": 0.05, "weight": 4,
        "description": "Langkah yang meninggalkan jejak es. (Syarat Job: Blizzard Sovereign & The Faceless)."
    },
    "steadfast_boots": {
        "id": "steadfast_boots", "name": "Iron-Shod Steadfast Boots", "type": "boots", "tier": 4,
        "p_def": 20, "m_def": 5, "speed": -5, "weight": 12,
        "description": "Sangat berat, membuatmu tidak mudah goyah. (Syarat Job: Dread Knight & Holy Templar)."
    },
    "wind_dashers": {
        "id": "wind_dashers", "name": "Wind Dasher Boots", "type": "boots", "tier": 4,
        "p_def": 6, "speed": 18, "dodge": 0.10, "weight": 1,
        "description": "Angin topan miniatur berputar di sekitar tumitnya."
    },
    "blood_treads": {
        "id": "blood_treads", "name": "Crimson Blood Treads", "type": "boots", "tier": 4,
        "p_atk": 10, "p_def": 10, "speed": 8, "weight": 3,
        "description": "Meninggalkan jejak darah kemanapun pemakainya melangkah."
    },
    "golem_greaves": {
        "id": "golem_greaves", "name": "Earth-Core Greaves", "type": "boots", "tier": 4,
        "p_def": 25, "m_def": 8, "speed": -6, "weight": 14,
        "description": "Kaki batu raksasa. Menapakkan benda ini akan membuat bumi bergetar."
    },
    "spectral_shoes": {
        "id": "spectral_shoes", "name": "Spectral Hover Shoes", "type": "boots", "tier": 4,
        "m_atk": 8, "m_def": 15, "speed": 10, "dodge": 0.12, "weight": 0,
        "description": "Membuat kakimu sedikit melayang dari tanah."
    },

    # ==========================================
    # --- LEGENDARY / MYTHICAL BOOTS (TIER 5) ---
    # ==========================================
    "abyssal_striders": {
        "id": "abyssal_striders", "name": "Striders of the Abyss", "type": "boots", "tier": 5,
        "p_def": 15, "m_def": 25, "speed": 10, "dodge": 0.15, "weight": 2,
        "description": "Sepatu yang terbuat dari ketiadaan murni. Kakimu tidak bisa dilacak."
    },
    "dragon_scale_boots": {
        "id": "dragon_scale_boots", "name": "Dragon Scale Sabatons", "type": "boots", "tier": 5,
        "p_atk": 10, "p_def": 30, "m_def": 20, "speed": -2, "weight": 10,
        "description": "Sepatu baja berlapis sisik naga. Tahan menginjak lahar panas."
    },
    "celestial_steps": {
        "id": "celestial_steps", "name": "Steps of the Celestial", "type": "boots", "tier": 5,
        "m_atk": 15, "m_def": 30, "speed": 20, "dodge": 0.05, "weight": 1,
        "description": "Tiap langkahnya memunculkan pijakan cahaya. Bisa berjalan di atas udara."
    },
    "void_walkers": {
        "id": "void_walkers", "name": "Void Walker Boots", "type": "boots", "tier": 5,
        "p_atk": 15, "m_atk": 15, "speed": 25, "dodge": 0.18, "weight": 0,
        "description": "Dapat melipat jarak ruang sejenak saat pemakainya berlari."
    },
    "kings_heavy_sabatons": {
        "id": "kings_heavy_sabatons", "name": "The Fallen King's Sabatons", "type": "boots", "tier": 5,
        "p_atk": 20, "p_def": 40, "m_def": 20, "speed": -8, "weight": 18,
        "description": "Sangat lambat, namun memberimu kekuatan dan ketahanan layaknya benteng berjalan."
    }
}
