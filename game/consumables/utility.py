# game/consumables/utility.py

"""
====================================================================
DATABASE UTILITIES (Barang Bawaan & Konsumsi Spesial) - The Archivus
====================================================================
File ini menyimpan seluruh data item bertipe 'consumable' (sekali pakai)
yang memberikan efek utilitas di luar penyembuhan HP/MP murni.

Kategori di dalam file ini meliputi:
1. Hazard Protectors -> Item pelindung lingkungan yang sifatnya
   dibawa di tas (Inventory), tidak butuh slot Equip (Weapon/Armor).
2. Status Cleansers -> Menghapus efek racun, beku, dll.
3. Repair Kits -> Memulihkan durabilitas perlengkapan pemain.
4. Exploration -> Bom asap, umpan monster, transportasi instan.

SINKRONISASI HAZARDS:
Item berawalan 'item_' (seperti Salep dan Pelarut) adalah syarat 
untuk selamat dari anomali lingkungan di sistem hazards.py. 
Pemain cukup memilikinya di dalam tas (Inventory) agar otomatis 
terhindar dari penalti area.
====================================================================
"""

UTILITIES = {
    # ==========================================
    # --- HAZARD PROTECTION (Alat Lingkungan) ---
    # ==========================================
    # 1. Pelindung PARASIT (Hutan Spora Parasit)
    "item_salep_belerang": {
        "id": "item_salep_belerang", 
        "name": "Salep Belerang", 
        "type": "consumable",
        "effect_type": "hazard_protection", 
        "value": 0, 
        "tier": 3,
        "description": "Salep berbau menyengat. Membawanya dan mengoleskannya ke kulit mencegah spora parasit menempel di tubuhmu."
    },
    # 2. Pelindung LEKAP (Lendir Daging Menempel)
    "item_pelarut_lendir": {
        "id": "item_pelarut_lendir", 
        "name": "Cairan Pelarut Lendir", 
        "type": "consumable",
        "effect_type": "hazard_protection", 
        "value": 0, 
        "tier": 3,
        "description": "Zat kimia keras pembakar jaringan organik. Digunakan untuk melepaskan langkah kaki dari jebakan lendir monster."
    },

    # ==========================================
    # --- STATUS CLEANSERS (Pembersih Efek) ---
    # ==========================================
    "cure_poison": {
        "id": "cure_poison", 
        "name": "Antidote", 
        "type": "consumable",
        "effect_type": "clear_poison", 
        "value": 0, 
        "tier": 2,
        "description": "Ramuan herbal pahit yang menetralkan segala jenis racun di dalam darah."
    },
    "warmth_pack": {
        "id": "warmth_pack", 
        "name": "Warmth Pack", 
        "type": "consumable",
        "effect_type": "clear_chill", 
        "value": 0, 
        "tier": 2,
        "description": "Kantong penghangat instan untuk menghentikan efek 'Freeze' atau kedinginan ekstrem."
    },
    "sacred_water": {
        "id": "sacred_water", 
        "name": "Sacred Water", 
        "type": "consumable",
        "effect_type": "clear_all_debuffs", 
        "value": 0, 
        "tier": 4,
        "description": "Air suci yang diberkati. Menghapus semua status efek negatif (debuff) dan kutukan seketika."
    },

    # ==========================================
    # --- REPAIR KITS (Pemeliharaan Durabilitas) ---
    # ==========================================
    "repair_kit_minor": {
        "id": "repair_kit_minor", 
        "name": "Minor Repair Kit", 
        "type": "consumable",
        "effect_type": "repair_gear", 
        "value": 25, 
        "tier": 2,
        "description": "Alat perkakas sederhana. Memulihkan 25 Poin Durabilitas pada perlengkapan yang sedang dipakai."
    },
    "repair_kit_master": {
        "id": "repair_kit_master", 
        "name": "Master Repair Kit", 
        "type": "consumable",
        "effect_type": "repair_gear", 
        "value": 100, 
        "tier": 4,
        "description": "Peralatan pandai besi lengkap. Mengembalikan durabilitas seluruh perlengkapanmu ke kondisi 100% maksimal."
    },

    # ==========================================
    # --- EXPLORATION UTILITY (Alat Bantu Jelajah) ---
    # ==========================================
    "smoke_bomb": {
        "id": "smoke_bomb", 
        "name": "Smoke Bomb", 
        "type": "consumable",
        "effect_type": "escape_battle", 
        "value": 0, 
        "tier": 3,
        "description": "Bom asap pekat. Memungkinkanmu melarikan diri dari pertarungan monster secara instan dengan peluang sukses 100%."
    },
    "monster_lure": {
        "id": "monster_lure", 
        "name": "Monster Lure", 
        "type": "consumable",
        "effect_type": "increase_encounter", 
        "value": 5, 
        "tier": 3,
        "description": "Umpan daging berbau tajam. Sangat cocok untuk *grinding*, meningkatkan peluang bertemu monster selama 5 langkah."
    },
    "warding_incense": {
        "id": "warding_incense", 
        "name": "Warding Incense", 
        "type": "consumable",
        "effect_type": "decrease_encounter", 
        "value": 10, 
        "tier": 3,
        "description": "Dupa wangi yang dibenci oleh makhluk kegelapan. Menurunkan peluang diserang musuh selama 10 langkah ke depan."
    },

    # ==========================================
    # --- TELEPORTATION (Transportasi Instan) ---
    # ==========================================
    "recall_scroll": {
        "id": "recall_scroll", 
        "name": "Recall Scroll", 
        "type": "consumable",
        "effect_type": "teleport_town", 
        "value": 0, 
        "tier": 3,
        "description": "Gulungan sihir yang mengoyak ruang. Membawamu kembali ke area aman (Rest Area / Kota) seketika."
    }
}
