# game/data/environment/hazards.py

"""
Hazards Database - The Archivus
Berisi daftar bahaya lingkungan yang memberikan penalti jika pemain
tidak menggunakan item pelindung (Masker, Mantel, Cincin, dll).
Telah mendukung pengecekan dari Tas (Inventory) maupun Item Terpakai (Equipped).
"""

HAZARDS = {
    # 1. RACUN
    "RACUN": {
        "name": "Miasma Beracun",
        "desc": "Kabut hijau pekat menyelimuti area ini. Udaranya terasa berat dan berbau busuk.",
        "required_item": "item_masker_gas",
        "safe_msg": "😷 **Masker Gas** milikmu menyaring udara kotor. Kau bisa bernapas dengan lega.",
        "danger_msg": "🤢 Paru-parumu terasa terbakar! Racun miasma mulai merusak tubuhmu.",
        "penalty": {"hp_loss": 15, "status_effect": "poison", "effect_val": 5}
    },
    
    # 2. DINGIN
    "DINGIN": {
        "name": "Suhu Sub-Zero",
        "desc": "Angin es berhembus kencang, membekukan apapun yang tidak bergerak.",
        "required_item": "item_mantel_bulu",
        "safe_msg": "🧥 **Mantel Bulu** yang tebal menjaga suhu tubuhmu tetap hangat.",
        "danger_msg": "❄️ Dingin yang ekstrem menusuk hingga ke tulang! Gerakanmu melambat.",
        "penalty": {"energy_loss": 20, "hp_loss": 5, "status_effect": "freeze"}
    },

    # 3. GELAP
    "GELAP": {
        "name": "Kegelapan Abyss",
        "desc": "Cahaya tidak mampu menembus area ini. Kau merasa diawasi oleh ribuan mata dari kegelapan.",
        "required_item": "item_lentera_jiwa",
        "safe_msg": "🕯️ Cahaya dari **Lentera Jiwa** mengusir bayangan jahat di sekitarmu.",
        "danger_msg": "🌑 Kegelapan mulai menggerogoti kewarasanmu. Kau merasa kehilangan arah.",
        "penalty": {"mp_loss": 20, "energy_loss": 10}
    },

    # 4. RAWA
    "RAWA": {
        "name": "Lumpur Penghisap",
        "desc": "Tanah di bawah kakimu tidak stabil dan mulai menarikmu ke bawah.",
        "required_item": "item_boots_heavy",
        "safe_msg": "🥾 **Heavy Boots** membuat pijakanmu tetap kokoh di atas lumpur.",
        "danger_msg": "⚠️ Kau terjebak dalam lumpur! Membutuhkan tenaga ekstra untuk melepaskan diri.",
        "penalty": {"energy_loss": 30}
    },

    # 5. PANAS
    "PANAS": {
        "name": "Lautan Api Hitam",
        "desc": "Lantai memancarkan suhu panas yang tidak wajar, api hitam menjilat-jilat udara.",
        "required_item": "item_jubah_asbes",
        "safe_msg": "🔥 **Jubah Asbes** menahan panas api hitam agar tidak memanggang kulitmu.",
        "danger_msg": "🔥 Kulitmu melepuh! Panas api hitam ini membakar hingga ke jiwamu.",
        "penalty": {"hp_loss": 20, "status_effect": "burn", "effect_val": 10}
    },

    # 6. ILUSI
    "ILUSI": {
        "name": "Cermin Distorsi",
        "desc": "Ruangan ini penuh dengan cermin yang memantulkan kengerian masa lalumu.",
        "required_item": "item_kacamata_kebenaran",
        "safe_msg": "👓 **Kacamata Kebenaran** membantumu melihat jalan keluar tanpa tertipu ilusi.",
        "danger_msg": "🌀 Kau terjebak dalam ilusi kengerian! Pikiranmu terkuras habis.",
        "penalty": {"mp_loss": 30, "energy_loss": 15}
    },

    # 7. KUTUKAN
    "KUTUKAN": {
        "name": "Bisikan Terkutuk",
        "desc": "Suara-suara gaib memenuhi lorong ini, mencoba merasuki pikiranmu untuk bunuh diri.",
        "required_item": "item_kalung_suci",
        "safe_msg": "📿 **Kalung Suci** memancarkan aura hangat, meredam bisikan gaib tersebut.",
        "danger_msg": "👿 Bisikan itu berhasil menembus pikiranmu, meninggalkan kutukan yang menyakitkan.",
        "penalty": {"hp_loss": 10, "mp_loss": 20, "status_effect": "curse"}
    },

    # 8. ASAM
    "ASAM": {
        "name": "Genangan Asam Pelebur",
        "desc": "Lantai tergenang cairan asam tebal yang mendesis saat menyentuh bebatuan.",
        "required_item": "item_sepatu_karet_tebal",
        "safe_msg": "🥾 **Sepatu Karet Tebal** melindungimu, kau melintasi genangan asam dengan aman.",
        "danger_msg": "🧪 Asam itu melelehkan sepatumu dan membakar daging kakimu!",
        "penalty": {"hp_loss": 25, "energy_loss": 10}
    },

    # 9. PETIR
    "PETIR": {
        "name": "Badai Petir Merah",
        "desc": "Ruangan tanpa atap dengan kilatan petir merah yang menyambar tak beraturan.",
        "required_item": "item_cincin_grounding",
        "safe_msg": "💍 **Cincin Grounding** menyerap aliran listrik yang menyambar di dekatmu.",
        "danger_msg": "⚡ Tubuhmu tersambar petir merah! Ototmu kejang dan sistem syarafmu rusak sementara.",
        "penalty": {"hp_loss": 20, "status_effect": "stun"}
    },

    # 10. ANGIN
    "ANGIN": {
        "name": "Angin Topan Tulang",
        "desc": "Angin kencang menerbangkan serpihan tulang tajam bak pisau cukur.",
        "required_item": "item_jangkar_besi",
        "safe_msg": "⚓ Dengan **Jangkar Besi**, kau bisa merangkak perlahan melawan badai tanpa terbawa angin.",
        "danger_msg": "🌪️ Kau terhempas angin! Serpihan tulang menyayat kulitmu saat kau berguling jatuh.",
        "penalty": {"hp_loss": 15, "energy_loss": 25, "status_effect": "bleed"}
    },

    # 11. BISING
    "BISING": {
        "name": "Jeritan Jiwa Tersiksa",
        "desc": "Gema jeritan dari ribuan jiwa terdengar sangat keras hingga membuat telinga berdarah.",
        "required_item": "item_penutup_telinga_lilin",
        "safe_msg": "🎧 **Penutup Telinga Lilin** menyumbat jeritan mematikan itu, menyisakan keheningan absolut.",
        "danger_msg": "🔊 Gendang telingamu pecah! Darah segar menetes dari hidung dan telingamu.",
        "penalty": {"hp_loss": 10, "mp_loss": 15, "energy_loss": 10}
    },

    # 12. TETESAN
    "TETESAN": {
        "name": "Hujan Darah Mendidih",
        "desc": "Tetesan darah mendidih jatuh dari langit-langit gua tanpa henti.",
        "required_item": "item_payung_kulit_naga",
        "safe_msg": "☂️ **Payung Kulit Naga** menahan tetesan darah mendidih dengan sempurna.",
        "danger_msg": "🩸 Darah mendidih menetes mengenai kulitmu, meninggalkan luka bakar yang mengerikan.",
        "penalty": {"hp_loss": 20}
    },

    # 13. DURI
    "DURI": {
        "name": "Lantai Kaca Berduri",
        "desc": "Lantai area ini tertutup oleh pecahan kaca dan duri besi berkarat.",
        "required_item": "item_pelindung_kaki_baja",
        "safe_msg": "🛡️ **Pelindung Kaki Baja** menghancurkan duri-duri itu tanpa melukaimu.",
        "danger_msg": "📌 Duri besi menusuk telapak kakimu! Kau kesulitan untuk berjalan tegak.",
        "penalty": {"energy_loss": 20, "hp_loss": 10, "status_effect": "bleed"}
    },

    # 14. KABUT_BUTA
    "KABUT_BUTA": {
        "name": "Kabut Pemakan Arah",
        "desc": "Kabut pekat berwarna putih susu, kau bahkan tidak bisa melihat tanganmu sendiri.",
        "required_item": "item_kompas_mata_darah",
        "safe_msg": "🧭 **Kompas Mata Darah** berkedut, menunjuk jalan keluar melalui kabut buta.",
        "danger_msg": "🌫️ Kau tersesat berjam-jam di dalam kabut, kelelahan dan hampir gila.",
        "penalty": {"energy_loss": 40, "mp_loss": 10}
    },

    # 15. PARASIT
    "PARASIT": {
        "name": "Hutan Spora Parasit",
        "desc": "Spora berterbangan mencari inang daging. Spora ini tumbuh dengan memakan darah.",
        "required_item": "item_salep_belerang",
        "safe_msg": "🧴 **Salep Belerang** yang kau oleskan di kulit membuat spora enggan menempel.",
        "danger_msg": "🍄 Spora menempel di kulitmu dan mulai berakar! Menyedot darah dari tubuhmu.",
        "penalty": {"hp_loss": 15, "status_effect": "poison"}
    },

    # 16. GRAVITASI
    "GRAVITASI": {
        "name": "Zona Anti-Gravitasi",
        "desc": "Hukum fisika rusak di sini. Benda-benda melayang dan tubuhmu terangkat secara paksa.",
        "required_item": "item_sabuk_pemberat",
        "safe_msg": "🪨 **Sabuk Pemberat** membuat kakimu tetap menapak erat ke lantai.",
        "danger_msg": "🌌 Kau terlempar ke udara dan menghantam langit-langit sebelum jatuh kembali!",
        "penalty": {"hp_loss": 25, "energy_loss": 15}
    },

    # 17. LEKAP
    "LEKAP": {
        "name": "Lendir Daging Menempel",
        "desc": "Lantai dan dinding dilapisi lendir hidup yang mencengkeram apa saja yang menyentuhnya.",
        "required_item": "item_pelarut_lendir",
        "safe_msg": "🧪 Kau menyiramkan **Pelarut Lendir** ke sepatumu, membuat lendir daging menyusut menjauh.",
        "danger_msg": "🕸️ Kakimu menempel kuat pada lantai! Butuh usaha besar untuk menariknya.",
        "penalty": {"energy_loss": 35}
    },

    # 18. PISAU
    "PISAU": {
        "name": "Lorong Angin Silet",
        "desc": "Arus angin memotong-motong udara dengan sangat kuat, tajam seperti ribuan pisau tak kasat mata.",
        "required_item": "item_zirah_rantai_perak",
        "safe_msg": "🛡️ Angin silet menghantam **Zirah Rantai Perak** dan memercikkan bunga api, kau aman.",
        "danger_msg": "🔪 Angin tajam menyayat-nyayat pakaian dan kulitmu!",
        "penalty": {"hp_loss": 30, "status_effect": "bleed"}
    },

    # 19. HALUSINASI
    "HALUSINASI": {
        "name": "Taman Jamur Halusinogen",
        "desc": "Bunga-bunga indah bercahaya memancarkan serbuk sari yang membelokkan realitas.",
        "required_item": "item_lonceng_kesadaran",
        "safe_msg": "🔔 Suara nyaring dari **Lonceng Kesadaran** menyentak otakmu agar tetap sadar.",
        "danger_msg": "😵 Kau kehilangan kendali pikiranmu dan bertingkah seperti orang gila selama beberapa waktu.",
        "penalty": {"mp_loss": 40, "energy_loss": 10}
    },

    # 20. MEMORI
    "MEMORI": {
        "name": "Zona Penyedot Ingatan",
        "desc": "Ruangan kosong tanpa warna. Berada di sini membuatmu lupa identitas dan kenanganmu.",
        "required_item": "item_ikat_kepala_timah",
        "safe_msg": "🤕 **Ikat Kepala Timah** melindungi aliran pikiranmu dari efek penyedot ingatan.",
        "danger_msg": "🧠 Kepalamu pusing hebat! Ingatan pentingmu seperti direnggut paksa dari dalam otak.",
        "penalty": {"mp_loss": 50, "status_effect": "amnesia"}
    }
}

# --- LOGIKA INTERAKSI HAZARD ---

def process_hazard_interaction(player, hazard_type):
    """
    Memproses dampak bahaya lingkungan terhadap pemain.
    Sudah terintegrasi dengan pengecekan Inventory & Equipped items.
    Mengembalikan: (is_safe, message)
    """
    hazard = HAZARDS.get(hazard_type)
    if not hazard:
        return True, "Area ini aman."

    required_item = hazard['required_item']
    
    # 1. Ambil data Tas (Inventory)
    inventory_items = player.get('inventory', [])
    
    # 2. Ambil data Barang Dipakai (Equipped)
    equipped_items = list(player.get('equipped', {}).values())
    
    # 3. Cek apakah pemain memiliki item pelindung di tas ATAU sedang dipakai
    if required_item in inventory_items or required_item in equipped_items:
        return True, hazard['safe_msg']
    
    # Jika tidak memiliki item pelindung, terapkan penalti
    penalty = hazard['penalty']
    
    # Terapkan pengurangan HP
    if 'hp_loss' in penalty:
        player['hp'] = max(0, player.get('hp', 0) - penalty['hp_loss'])
        
    # Terapkan pengurangan Energy
    if 'energy_loss' in penalty:
        player['energy'] = max(0, player.get('energy', 100) - penalty['energy_loss'])
        
    # Terapkan pengurangan MP
    if 'mp_loss' in penalty:
        player['mp'] = max(0, player.get('mp', 0) - penalty['mp_loss'])
        
    # Terapkan efek status
    if 'status_effect' in penalty:
        if 'active_effects' not in player:
            player['active_effects'] = []
            
        # Cek agar efek yang sama tidak double bertumpuk berulang kali
        existing_effects = [e.get('type') for e in player['active_effects']]
        eff_type = penalty['status_effect']
        
        if eff_type not in existing_effects:
            player['active_effects'].append({
                "type": eff_type, 
                "value": penalty.get('effect_val', 5), 
                "duration": 3 # Default durasi racun lingkungan adalah 3 turn/langkah
            })
        
    return False, hazard['danger_msg']

def get_hazard_data(hazard_type):
    """Mengambil data bahaya berdasarkan tipe (RACUN, DINGIN, dll)."""
    return HAZARDS.get(hazard_type)

def get_all_hazards():
    """Mengambil seluruh daftar bahaya lingkungan."""
    return HAZARDS
