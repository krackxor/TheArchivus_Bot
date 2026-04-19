# game/items/cloaks.py

"""
====================================================================
DATABASE CLOAKS (Jubah & Mantel) - The Archivus
====================================================================
File ini menyimpan seluruh data item untuk slot 'Cloak' (Jubah).
Jubah berfungsi sebagai pelindung sekunder yang sangat krusial.

FOKUS STATUS JUBAH:
- m_def (Magic Defense): Jubah adalah penahan sihir terbaik.
- speed & dodge: Karena ringan, jubah sering kali menambah kelincahan.
- weight: Umumnya memiliki bobot rendah (0 hingga 2), kecuali jubah 
  baja khusus tipe ksatria.

SINKRONISASI HAZARDS:
Beberapa item di sini (berawalan 'item_') adalah pelindung mutlak 
dari bahaya lingkungan (Suhu ekstrem, Cuaca) di file hazards.py.
====================================================================
"""

CLOAKS = {
    # ==========================================
    # --- STARTER / BASIC CLOAKS (TIER 1-2) ---
    # ==========================================
    "traveler_cloak": {
        "id": "traveler_cloak", "name": "Tattered Traveler Cloak", "type": "cloak", "tier": 1,
        "p_def": 1, "m_def": 2, "weight": 1,
        "description": "Jubah usang penjelajah. Cukup hangat untuk malam yang dingin."
    },
    "ragged_cape": {
        "id": "ragged_cape", "name": "Ragged Cape", "type": "cloak", "tier": 1,
        "dodge": 0.01, "weight": 0,
        "description": "Kain robek yang berkibar tertiup angin. Tidak memberikan banyak pertahanan."
    },
    "hunter_cloak": {
        "id": "hunter_cloak", "name": "Hunter's Camo Cloak", "type": "cloak", "tier": 1,
        "p_def": 2, "m_def": 3, "speed": 1, "weight": 1,
        "description": "Jubah hijau kecoklatan untuk menyamar di dalam hutan."
    },
    "apprentice_cape": {
        "id": "apprentice_cape", "name": "Apprentice Cape", "type": "cloak", "tier": 1,
        "m_def": 5, "weight": 1,
        "description": "Jubah pendek standar pelajar akademi sihir."
    },
    "heavy_wool_cloak": {
        "id": "heavy_wool_cloak", "name": "Heavy Wool Cloak", "type": "cloak", "tier": 2,
        "p_def": 4, "m_def": 6, "weight": 3,
        "description": "Jubah wol yang sangat tebal. Nyaman tapi sedikit membebani."
    },
    "scout_cape": {
        "id": "scout_cape", "name": "Scout's Swift Cape", "type": "cloak", "tier": 2,
        "p_def": 2, "m_def": 4, "speed": 3, "dodge": 0.02, "weight": 1,
        "description": "Dirancang agar tidak menghalangi pergerakan kaki saat berlari."
    },
    "acolyte_mantle": {
        "id": "acolyte_mantle", "name": "Acolyte's Mantle", "type": "cloak", "tier": 2,
        "m_def": 10, "m_atk": 2, "weight": 1,
        "description": "Mantel seremonial yang membantu mencerahkan pikiran."
    },
    "mercenary_cloak": {
        "id": "mercenary_cloak", "name": "Mercenary's Black Cloak", "type": "cloak", "tier": 2,
        "p_def": 5, "m_def": 5, "weight": 2,
        "description": "Jubah hitam tebal yang menyembunyikan noda darah dengan baik."
    },

    # ==========================================
    # --- HAZARD PROTECTION CLOAKS (TIER 3) ---
    # ==========================================
    # 1. Pelindung DINGIN (Suhu Sub-Zero)
    "item_mantel_bulu": {
        "id": "item_mantel_bulu", "name": "Mantel Bulu Tebal", "type": "cloak", "tier": 3,
        "p_def": 6, "m_def": 8, "speed": -1, "weight": 3,
        "description": "Mantel berlapis bulu beruang. Menjagamu tetap hidup di Suhu Sub-Zero."
    },
    # 2. Pelindung PANAS (Lautan Api Hitam)
    "item_jubah_asbes": {
        "id": "item_jubah_asbes", "name": "Jubah Asbes Hitam", "type": "cloak", "tier": 3,
        "p_def": 4, "m_def": 15, "weight": 2,
        "description": "Ditenun dengan serat khusus yang mustahil terbakar. Melindungimu dari Lautan Api Hitam."
    },

    # ==========================================
    # --- INTERMEDIATE CLOAKS (TIER 3) ---
    # ==========================================
    "knight_cape": {
        "id": "knight_cape", "name": "Knight's Heraldic Cape", "type": "cloak", "tier": 3,
        "p_def": 8, "m_def": 8, "weight": 2,
        "description": "Jubah dengan lambang kerajaan. Kainnya ditenun bersama benang baja."
    },
    "assassin_cloak": {
        "id": "assassin_cloak", "name": "Shadow Assassin Cloak", "type": "cloak", "tier": 3,
        "p_def": 3, "m_def": 10, "speed": 5, "dodge": 0.06, "weight": 1,
        "description": "Jubah yang seolah menyerap cahaya di sekitarnya."
    },
    "sage_mantle": {
        "id": "sage_mantle", "name": "Mantle of the Sage", "type": "cloak", "tier": 3,
        "m_atk": 5, "m_def": 15, "weight": 1,
        "description": "Diberkati dengan sihir pengusir kutukan."
    },
    "crimson_cloak": {
        "id": "crimson_cloak", "name": "Crimson Battle Cloak", "type": "cloak", "tier": 3,
        "p_atk": 5, "p_def": 6, "m_def": 6, "weight": 2,
        "description": "Jubah merah menyala yang membangkitkan semangat bertarung."
    },
    "elven_cloak": {
        "id": "elven_cloak", "name": "Elven Leaf Cloak", "type": "cloak", "tier": 3,
        "m_def": 12, "speed": 8, "dodge": 0.05, "weight": 0,
        "description": "Sangat ringan hingga terasa seperti tidak memakai apa-apa."
    },
    "cleric_shroud": {
        "id": "cleric_shroud", "name": "Shroud of Mercy", "type": "cloak", "tier": 3,
        "m_atk": 8, "p_def": 4, "m_def": 14, "weight": 2,
        "description": "Kain kafan suci yang memancarkan aura kehidupan."
    },

    # ==========================================
    # --- HIGH-TIER / JOB-SPECIFIC (TIER 4) ---
    # ==========================================
    "frost_cloak": {
        "id": "frost_cloak", "name": "Frost-Woven Cloak", "type": "cloak", "tier": 4,
        "p_def": 8, "m_def": 25, "weight": 4,
        "description": "Jubah tebal yang mampu menahan badai salju paling ekstrem. (Syarat Job: Blizzard Sovereign & Dread Knight)."
    },
    "mist_weaver_cloak": {
        "id": "mist_weaver_cloak", "name": "Mist-Weaver Cloak", "type": "cloak", "tier": 4,
        "m_def": 15, "speed": 10, "dodge": 0.12, "weight": 1,
        "description": "Membuat siluet pemakainya tampak kabur seperti uap es. (Syarat Job: Phantom Archer)."
    },
    "radiant_cloak": {
        "id": "radiant_cloak", "name": "Radiant Templar Cloak", "type": "cloak", "tier": 4,
        "p_def": 15, "m_def": 30, "weight": 3,
        "description": "Jubah emas yang membiaskan sihir gelap. (Syarat Job: Holy Templar)."
    },
    "shadow_shroud": {
        "id": "shadow_shroud", "name": "Shroud of Shadows", "type": "cloak", "tier": 4,
        "m_atk": 10, "m_def": 20, "dodge": 0.08, "weight": 1,
        "description": "Jubah yang ditenun dari bayangan murni."
    },
    "golem_cape": {
        "id": "golem_cape", "name": "Earth-Bound Cape", "type": "cloak", "tier": 4,
        "p_def": 25, "m_def": 10, "speed": -3, "weight": 8,
        "description": "Bukan sekadar kain, melainkan rangkaian lempengan batu ajaib."
    },
    "blood_weave_cloak": {
        "id": "blood_weave_cloak", "name": "Blood-Weave Cloak", "type": "cloak", "tier": 4,
        "p_atk": 12, "p_def": 10, "m_def": 15, "weight": 2,
        "description": "Benangnya terbuat dari pembuluh darah monster raksasa."
    },

    # ==========================================
    # --- LEGENDARY / MYTHICAL CLOAKS (TIER 5) ---
    # ==========================================
    "void_mantle": {
        "id": "void_mantle", "name": "Mantle of the Void", "type": "cloak", "tier": 5,
        "m_def": 40, "dodge": 0.15, "weight": 3,
        "description": "Jubah yang terbuat dari kegelapan murni. Sangat sulit disentuh sihir. (Syarat Job: Void Sage & The Faceless)."
    },
    "dragon_wing_cloak": {
        "id": "dragon_wing_cloak", "name": "Dragon Wing Cloak", "type": "cloak", "tier": 5,
        "p_atk": 15, "p_def": 20, "m_def": 30, "weight": 5,
        "description": "Terbuat dari membran sayap naga kuno. Tahan terhadap api neraka."
    },
    "celestial_mantle": {
        "id": "celestial_mantle", "name": "Mantle of the Celestial", "type": "cloak", "tier": 5,
        "m_atk": 25, "p_def": 15, "m_def": 45, "weight": 2,
        "description": "Jubah surgawi yang seolah memancarkan starlight."
    },
    "abyssal_shroud": {
        "id": "abyssal_shroud", "name": "Abyssal Shroud", "type": "cloak", "tier": 5,
        "p_def": 25, "m_def": 35, "dodge": 0.10, "weight": 4,
        "description": "Kain basah dan berat yang berasal dari palung lautan terdalam."
    },
    "kings_velvet_cape": {
        "id": "kings_velvet_cape", "name": "The Fallen King's Cape", "type": "cloak", "tier": 5,
        "p_atk": 20, "m_atk": 20, "p_def": 30, "m_def": 30, "speed": -5, "weight": 10,
        "description": "Sangat mewah, sangat berat. Membawa aura penaklukan."
    }
}
