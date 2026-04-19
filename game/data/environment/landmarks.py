# game/data/environment/landmarks.py

"""
====================================================================
DATABASE LANDMARKS (Lokasi Interaktif & Titik Istirahat) - The Archivus
====================================================================
File ini berisi 20 daftar lokasi permanen di peta (Environment).
Berbeda dengan 'Hazards' yang sifatnya merugikan, 'Landmarks' 
biasanya memberikan keuntungan (Buff, Heal, Hapus Kutukan, Item) 
atau memicu Puzzle/Teka-teki.

SISTEM INTERAKSI:
Setiap landmark bisa di-setting membutuhkan syarat item ('requirement').
Fungsi interaksinya sudah terintegrasi untuk membaca Inventory pemain
serta sistem Auto-Equip.
====================================================================
"""

import random

LANDMARKS = {
    # ==========================================
    # --- SHRINES & HEALING (Titik Pemulihan) ---
    # ==========================================
    "landmark_altar_cleansing": {
        "name": "Altar Pembersihan",
        "type": "landmark",
        "desc": "Sebuah altar marmer putih yang memancarkan aura suci. Air jernih mengalir dari celah-celahnya.",
        "interaction": "pray",
        "effect": "clear_debuffs",
        "msg": "✨ Kau membasuh wajahmu di altar. Semua rasa sakit, racun, dan kutukan dalam tubuhmu seketika sirna!",
        "requirement": None
    },
    "landmark_church_abandoned": {
        "name": "Rumah Ibadah Terbengkalai",
        "type": "landmark",
        "desc": "Atapnya sudah runtuh, namun patung dewi di tengahnya masih utuh, menatap kosong ke langit.",
        "interaction": "rest",
        "effect": "restore_mp",
        "msg": "🧘 Kedamaian di tempat ini memulihkan fokus mentalmu. Seluruh Mana (MP) milikmu terisi penuh.",
        "requirement": None
    },
    "landmark_hot_spring": {
        "name": "Mata Air Panas Belerang",
        "type": "landmark",
        "desc": "Kolam air panas alami di tengah bebatuan. Uapnya berbau belerang ringan yang menenangkan.",
        "interaction": "bathe",
        "effect": "restore_hp",
        "msg": "♨️ Kau berendam sejenak. Kehangatan airnya menutup semua luka luarmu. HP-mu pulih kembali.",
        "requirement": "item_handuk_kering"
    },
    "landmark_hermits_campfire": {
        "name": "Api Unggun Pengembara",
        "type": "landmark",
        "desc": "Sisa-sisa perapian yang ditinggalkan. Abunya masih hangat, hanya butuh kayu untuk dinyalakan.",
        "interaction": "ignite",
        "effect": "restore_energy",
        "msg": "🏕️ Kau menyalakan api dan beristirahat. Rasa lelahmu menguap. Stamina/Energy pulih sepenuhnya.",
        "requirement": "item_kayu_bakar"
    },
    "landmark_shattered_mirror": {
        "name": "Cermin Realitas Retak",
        "type": "landmark",
        "desc": "Sebuah cermin setinggi manusia. Pantulan di dalamnya tidak memiliki luka sepertimu.",
        "interaction": "touch",
        "effect": "clear_debuffs",
        "msg": "🪞 Kau menyentuh cermin itu dengan kaca pantulmu. Cermin menyerap semua kutukanmu lalu hancur berkeping-keping!",
        "requirement": "item_kaca_pantul"
    },

    # ==========================================
    # --- EXPLORATION & LOOT (Penggalian & Eksplorasi) ---
    # ==========================================
    "landmark_graveyard_ancient": {
        "name": "Kuburan Kuno",
        "type": "landmark",
        "desc": "Ribuan nisan berlumut berdiri di sini. Tanah terasa dingin dan berdenyut perlahan.",
        "interaction": "dig",
        "effect": "random_loot",
        "msg": "🪦 Kau menggali tanah yang gembur dan menemukan sebuah artefak tersembunyi!",
        "danger_chance": 0.4, # 40% Peluang Ambush
        "requirement": "item_sekop"
    },
    "landmark_mining_vein": {
        "name": "Urat Tambang Bercahaya",
        "type": "landmark",
        "desc": "Celah di dinding gua ini memperlihatkan bongkahan kristal biru yang belum ditambang.",
        "interaction": "mine",
        "effect": "random_loot_crystal",
        "msg": "💎 Percikan api keluar saat kau menghancurkan batu. Kau berhasil menambang kristal langka!",
        "danger_chance": 0.2, 
        "requirement": "item_beliung_tambang"
    },
    "landmark_abandoned_cart": {
        "name": "Kereta Pedagang Terlantar",
        "type": "landmark",
        "desc": "Kereta kuda yang hancur. Ada peti kayu kokoh yang terkunci rapat di bagian belakangnya.",
        "interaction": "pry_open",
        "effect": "random_loot",
        "msg": "📦 *KRAK!* Kau mencongkel peti itu secara paksa. Di dalamnya terdapat barang berharga!",
        "danger_chance": 0.6, # 60% Ambush karena berisik
        "requirement": "item_linggis"
    },
    "landmark_astral_telescope": {
        "name": "Teleskop Astral Rusak",
        "type": "landmark",
        "desc": "Alat kuno untuk meneropong bintang. Lensa utamanya tertutup debu abadi.",
        "interaction": "clean",
        "effect": "reveal_map",
        "msg": "🔭 Setelah membersihkannya, kau meneropong ke luar. Kau sekarang tahu peta wilayah ini secara keseluruhan.",
        "requirement": "item_kain_pembersih_kaca"
    },
    "landmark_whispering_chasm": {
        "name": "Jurang Berbisik",
        "type": "landmark",
        "desc": "Jurang vertikal yang sangat dalam. Dari bawah, kau bisa mendengar suara orang-orang yang kau kenal.",
        "interaction": "climb_down",
        "effect": "trigger_puzzle",
        "msg": "🧗 Kau turun menggunakan tali. Di tengah tebing, kau menemukan ukiran rahasia peninggalan masa lalu.",
        "requirement": "item_tali_panjat"
    },

    # ==========================================
    # --- MYSTERIES & PUZZLES (Teka-Teki Dunia) ---
    # ==========================================
    "landmark_statue_cipher": {
        "name": "Patung Bersandi",
        "type": "landmark",
        "desc": "Patung raksasa tanpa wajah yang memegang buku batu. Ada ukiran yang terus berubah di alasnya.",
        "interaction": "solve",
        "effect": "trigger_puzzle",
        "msg": "📜 Patung itu menuntut jawaban atas teka-tekinya sebelum membiarkanmu lewat.",
        "requirement": None
    },
    "landmark_silent_bell": {
        "name": "Menara Lonceng Bisu",
        "type": "landmark",
        "desc": "Lonceng perunggu raksasa berkarat yang sudah puluhan tahun tidak pernah dibunyikan.",
        "interaction": "strike",
        "effect": "buff_luck",
        "msg": "🔔 *DOOONG!* Getaran lonceng mengusir roh-roh jahat di sekitarmu. Keberuntunganmu meningkat drastis! (+10 Luck)",
        "requirement": "item_palu_godam"
    },
    "landmark_wishing_tree": {
        "name": "Pohon Harapan Korup",
        "type": "landmark",
        "desc": "Pohon tanpa daun. Dahannya dipenuhi benang merah pudar milik ribuan pengembara sebelummu.",
        "interaction": "tie_thread",
        "effect": "gain_exp",
        "msg": "🧶 Kau mengikat benang merah ke dahan. Sekilas, memori para pengembara masa lalu mengalir ke otakmu! (+150 EXP)",
        "requirement": "item_benang_merah"
    },

    # ==========================================
    # --- PERMANENT BUFFS (Peningkatan Status) ---
    # ==========================================
    "landmark_monolith_blood": {
        "name": "Monolit Darah",
        "type": "landmark",
        "desc": "Batu hitam raksasa yang menyerap semua cahaya. Ia seolah menunggumu mengorbankan sesuatu.",
        "interaction": "sacrifice",
        "effect": "buff_atk",
        "msg": "🩸 Kau menggores tanganmu. Kekuatan buas mengalir ke ototmu! (HP -10, P_ATK +15)",
        "requirement": "item_pisau_ritual"
    },
    "landmark_echoing_well": {
        "name": "Sumur Gema Kematian",
        "type": "landmark",
        "desc": "Sumur kering yang sangat dalam. Katanya, dasar sumur ini terhubung ke dunia arwah.",
        "interaction": "toss_coin",
        "effect": "buff_def",
        "msg": "🪙 Kau melempar koin ke dalam. Sebuah suara berbisik, 'Kami melindungimu.' (+10 M_DEF)",
        "requirement": "item_koin_emas"
    },
    "landmark_mystic_lake": {
        "name": "Danau Mistik Perak",
        "type": "landmark",
        "desc": "Air danau ini berwarna perak kebiruan. Kau bisa melihat pantulan masa depan di permukaannya.",
        "interaction": "drink",
        "effect": "buff_luck",
        "msg": "💧 Air danau terasa manis. Kau merasa hari ini keberuntungan akan sangat berpihak padamu! (+5 Luck)",
        "requirement": "item_botol_kosong"
    },
    "landmark_ancient_forge": {
        "name": "Tungku Tempa Dewa",
        "type": "landmark",
        "desc": "Tungku peleburan baja kuno. Apinya masih menyala biru berkat sihir abadi.",
        "interaction": "forge",
        "effect": "buff_atk",
        "msg": "⚒️ Kau memanaskan dan menimpa senjatamu. Bilahnya kini jauh lebih tajam dan mematikan! (+15 P_ATK)",
        "requirement": "item_palu_tempa"
    },
    "landmark_glowing_mushroom": {
        "name": "Jamur Vitalitas Raksasa",
        "type": "landmark",
        "desc": "Jamur aneh bercahaya ungu. Spora yang jatuh darinya membuat tanaman di sekitarnya tumbuh gila-gilaan.",
        "interaction": "slice_and_eat",
        "effect": "buff_max_hp",
        "msg": "🍄 Kau mengiris sepotong dan memakannya. Ototmu menebal, daya tahan tubuhmu berevolusi! (+10 Max HP)",
        "requirement": "item_pisau_bedah"
    },
    "landmark_shadow_pool": {
        "name": "Kolam Bayangan",
        "type": "landmark",
        "desc": "Bukan air, kolam ini berisi bayangan cair yang sangat dingin.",
        "interaction": "scoop",
        "effect": "buff_max_mp",
        "msg": "🫗 Kau menyendok bayangan itu dan meminumnya. Pikiranmu meluas menembus batas kewarasan! (+10 Max MP)",
        "requirement": "item_cawan_suci"
    },
    "landmark_fallen_king_statue": {
        "name": "Patung Raja Tumbang",
        "type": "landmark",
        "desc": "Patung raja tanpa kepala. Tangannya menengadah ke atas seperti meminta upeti.",
        "interaction": "offer",
        "effect": "buff_def",
        "msg": "👑 Kau meletakkan upeti. Aura pertahanan dari kerajaan yang runtuh menyelimuti tubuhmu. (+10 P_DEF)",
        "requirement": "item_koin_emas"
    }
}

# --- LOGIKA INTERAKSI LANDMARK ---

def process_landmark_interaction(player, landmark_id):
    """
    Logika untuk mengeksekusi efek dari landmark terhadap pemain.
    Sudah mengintegrasikan sistem Pengecekan Tas (Inventory) & Pengecekan Barang Dipakai (Equipped).
    Mengembalikan: (result_type, message)
    """
    landmark = LANDMARKS.get(landmark_id)
    if not landmark:
        return False, "❌ Landmark tidak ditemukan."

    req = landmark.get('requirement')
    inventory_items = player.get('inventory', [])
    equipped_items = list(player.get('equipped', {}).values())

    # 1. LOGIKA PENGECEKAN PERSYARATAN (REQUIREMENT)
    if req:
        if req in equipped_items:
            pass # Lanjut, item sudah dipakai (Aman)
        elif req in inventory_items:
            # Item ada di tas, tapi belum dipakai. Minta pemain untuk Auto-Equip via Handler.
            nama_item = req.replace('item_', '').replace('_', ' ').title()
            return "equip_needed", {
                "item_id": req,
                "msg": f"⚠️ Kau membutuhkan **{nama_item}** untuk ini.\nBarang tersebut ada di dalam tasmu, tetapi belum dipakai. Ingin memakainya sekarang?"
            }
        else:
            # Item benar-benar tidak dimiliki
            nama_item = req.replace('item_', '').replace('_', ' ').title()
            return "req_failed", f"❌ Kau membutuhkan **{nama_item}** untuk berinteraksi di sini."

    # 2. EKSEKUSI EFEK BERDASARKAN JENIS LANDMARK
    effect = landmark.get('effect')
    
    # --- EFEK PEMULIHAN (RESTORE) ---
    if effect == "clear_debuffs":
        player['active_effects'] = [] # Menghapus semua status efek negatif
        
    elif effect == "restore_mp":
        player['mp'] = player.get('max_mp', 100) # Memulihkan MP penuh
        
    elif effect == "restore_hp":
        player['hp'] = player.get('max_hp', 100) # Memulihkan HP penuh
        
    elif effect == "restore_energy":
        # Menghapus item konsumsi (kayu bakar) dari inventory
        if 'item_kayu_bakar' in player.get('inventory', []):
            player['inventory'].remove('item_kayu_bakar')
        player['energy'] = player.get('max_energy', 100) # Memulihkan Stamina/Energy

    # --- EFEK BUFF (PENINGKATAN STATUS) ---
    elif effect == "buff_luck":
        player['base_luck'] = player.get('base_luck', 0) + 5
        
    elif effect == "buff_atk":
        # Jika monolit darah, kurangi HP. Jika tungku tempa, biarkan aman.
        if landmark_id == "landmark_monolith_blood":
            player['hp'] = max(1, player.get('hp', 100) - 10) # Denda darah
        player['base_p_atk'] = player.get('base_p_atk', 10) + 15
        
    elif effect == "buff_def":
        # Hapus item koin emas sebagai tumbal/upeti
        if 'item_koin_emas' in player.get('inventory', []):
            player['inventory'].remove('item_koin_emas')
        # Jika patung raja (Physical Def), jika sumur (Magic Def)
        if landmark_id == "landmark_fallen_king_statue":
            player['base_p_def'] = player.get('base_p_def', 10) + 10
        else:
            player['base_m_def'] = player.get('base_m_def', 10) + 10

    elif effect == "buff_max_hp":
        # Ekspansi Max HP
        player['max_hp'] = player.get('max_hp', 100) + 10
        player['hp'] = min(player['max_hp'], player.get('hp', 100) + 10)
        
    elif effect == "buff_max_mp":
        # Ekspansi Max MP
        player['max_mp'] = player.get('max_mp', 50) + 10
        player['mp'] = min(player['max_mp'], player.get('mp', 50) + 10)

    # --- EFEK LAINNYA (LOOT, EXP, PUZZLE) ---
    elif effect == "gain_exp":
        player['exp'] = player.get('exp', 0) + 150
        
    elif effect == "reveal_map":
        player['inventory'].append("item_peta_usang")
        
    elif effect in ["random_loot", "random_loot_crystal"]:
        # Logika risiko kemunculan musuh (Ambush)
        if random.random() < landmark.get('danger_chance', 0):
            return "ambush", "⚠️ Sesuatu yang mengerikan bangkit dari sana! Persiapkan senjatamu!"
        
        # Berikan item acak
        loot_item = "item_old_relic" if effect == "random_loot" else "item_mana_crystal"
        player['inventory'].append(loot_item)
        
    elif effect == "trigger_puzzle":
        # Menandai bahwa pemain harus menghadapi kuis/puzzle khusus (Diurus oleh handler)
        return "puzzle", landmark['msg']

    # Jika sukses mengeksekusi efek, kembalikan nilai True dan pesannya
    return True, landmark['msg']

def get_landmark_data(landmark_id):
    """Mengambil data landmark berdasarkan ID."""
    return LANDMARKS.get(landmark_id)

def get_all_landmarks():
    """Mengambil seluruh daftar landmark."""
    return LANDMARKS
