# game/consumables/items.py

"""
====================================================================
DATABASE MISCELLANEOUS & CAMPING ITEMS - The Archivus
====================================================================
File ini menyimpan barang-barang yang tidak bisa dipakai di badan 
(Non-Equip). Mencakup perlengkapan kemah (Rest Area) dan perkakas 
umum (Misc) yang digunakan sebagai syarat interaksi di Landmark.
====================================================================
"""

# ==========================================
# --- CAMPING GEARS (Alat Perkemahan) ---
# ==========================================
CAMPING_ITEMS = {
    "tenda": {
        "id": "tenda",
        "name": "Tenda Kemah",
        "type": "consumable",        # Tetap 'consumable' agar muncul di tas ramuan/item
        "effect_type": "camp_gear",  # Identitas unik untuk Rest Area
        "description": "Tenda portabel penahan dingin. Hanya bisa dipasang di Rest Area untuk memulihkan 100% HP, MP, dan Energi.",
        "price": 300,
        "tier": 1
    }
}

# ==========================================
# --- LANDMARK TOOLS & MISC (Perkakas Umum) ---
# ==========================================
MISC_ITEMS = {
    # --- Perkakas Eksplorasi ---
    "item_sekop": {
        "id": "item_sekop", "name": "Sekop Penggali Kubur", "type": "misc", "tier": 1,
        "description": "Sekop berkarat dengan gagang kayu yang kuat. Digunakan untuk menggali gundukan tanah."
    },
    "item_beliung_tambang": {
        "id": "item_beliung_tambang", "name": "Beliung Tambang Besi", "type": "misc", "tier": 2,
        "description": "Alat berat untuk menghancurkan bebatuan keras dan mengekstrak kristal dari dinding gua."
    },
    "item_linggis": {
        "id": "item_linggis", "name": "Linggis Baja", "type": "misc", "tier": 1,
        "description": "Besi panjang dengan ujung melengkung. Sangat cocok untuk mencongkel peti kayu yang terkunci."
    },
    "item_tali_panjat": {
        "id": "item_tali_panjat", "name": "Tali Panjat Tebal", "type": "misc", "tier": 2,
        "description": "Tali sepanjang 50 meter yang sangat kuat. Memungkinkanmu turun ke jurang yang dalam."
    },
    "item_palu_godam": {
        "id": "item_palu_godam", "name": "Palu Godam Raksasa", "type": "misc", "tier": 2,
        "description": "Palu yang sangat berat. Bisa digunakan untuk membunyikan lonceng raksasa yang berkarat."
    },
    "item_kain_pembersih_kaca": {
        "id": "item_kain_pembersih_kaca", "name": "Kain Pembersih Halus", "type": "misc", "tier": 1,
        "description": "Kain berbahan mikrofiber kuno. Digunakan untuk membersihkan debu tanpa menggores lensa."
    },

    # --- Barang Ritual & Supranatural ---
    "item_pisau_ritual": {
        "id": "item_pisau_ritual", "name": "Pisau Ritual Pengorbanan", "type": "misc", "tier": 3,
        "description": "Pisau bergelombang yang digunakan khusus untuk menumpahkan darah di altar kutukan."
    },
    "item_benang_merah": {
        "id": "item_benang_merah", "name": "Gulungan Benang Merah", "type": "misc", "tier": 2,
        "description": "Benang takdir. Sering diikatkan ke dahan pohon untuk mengirimkan memori kepada orang yang sudah mati."
    },
    "item_kaca_pantul": {
        "id": "item_kaca_pantul", "name": "Pecahan Kaca Pantul", "type": "misc", "tier": 2,
        "description": "Pecahan cermin ajaib yang tidak memantulkan bayangan, melainkan menyerap sihir di sekitarnya."
    },
    "item_cawan_suci": {
        "id": "item_cawan_suci", "name": "Cawan Perak Kuno", "type": "misc", "tier": 3,
        "description": "Gelas dari perak murni. Mampu menampung cairan paling mematikan atau korup tanpa ikut hancur."
    },

    # --- Barang Keseharian ---
    "item_handuk_kering": {
        "id": "item_handuk_kering", "name": "Handuk Katun Kering", "type": "misc", "tier": 1,
        "description": "Handuk bersih. Sangat dibutuhkan setelah berendam di mata air panas agar tubuh tidak kedinginan."
    },
    "item_kayu_bakar": {
        "id": "item_kayu_bakar", "name": "Ikatan Kayu Bakar", "type": "misc", "tier": 1,
        "description": "Kayu pinus kering yang mudah terbakar. Penting untuk menyalakan api unggun di area gelap."
    },
    "item_botol_kosong": {
        "id": "item_botol_kosong", "name": "Botol Kaca Kosong", "type": "misc", "tier": 1,
        "description": "Botol kecil dengan sumbat gabus. Bisa digunakan untuk menampung air mistik dari danau."
    },
    "item_koin_emas": {
        "id": "item_koin_emas", "name": "Koin Emas Kerajaan", "type": "misc", "tier": 2,
        "description": "Koin kuno yang sangat berat. Memiliki ukiran raja yang telah lama mati. Digunakan sebagai upeti."
    },
    "item_palu_tempa": {
        "id": "item_palu_tempa", "name": "Palu Tempa Blacksmith", "type": "misc", "tier": 3,
        "description": "Palu khusus penempa besi. Dibutuhkan jika kau ingin memanfaatkan tungku peleburan kuno."
    },
    "item_pisau_bedah": {
        "id": "item_pisau_bedah", "name": "Pisau Bedah Tajam", "type": "misc", "tier": 2,
        "description": "Pisau medis dengan presisi tinggi. Berguna untuk memotong bagian jamur atau spesimen beracun tanpa merusaknya."
    },
    
    # --- Loot (Hasil dari Interaksi Landmark) ---
    "item_old_relic": {
        "id": "item_old_relic", "name": "Relik Kuno Berdebu", "type": "misc", "tier": 2,
        "description": "Barang antik yang usianya ratusan tahun. Bisa dijual mahal ke Merchant."
    },
    "item_mana_crystal": {
        "id": "item_mana_crystal", "name": "Bongkahan Kristal Mana", "type": "misc", "tier": 3,
        "description": "Batu permata yang memancarkan energi magis. Hasil tambang murni."
    },
    "item_peta_usang": {
        "id": "item_peta_usang", "name": "Peta Wilayah Usang", "type": "misc", "tier": 3,
        "description": "Peta yang membantumu melihat arah jalan yang benar. Meningkatkan keselamatan eksplorasi."
    }
}

# ==========================================
# --- LOGIKA PENGAMBILAN DATA (GETTER) ---
# ==========================================

# Menggabungkan kedua dictionary secara virtual agar get_item() lebih efisien
ALL_ITEMS = {**CAMPING_ITEMS, **MISC_ITEMS}

def get_item(item_id):
    """
    Mengambil data item dari database perkemahan maupun perkakas/misc.
    """
    return ALL_ITEMS.get(item_id)
