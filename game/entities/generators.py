import random

# --- 1. PROCEDURAL NPC NAMES (1000+ Kombinasi) ---
NPC_ADJECTIVES = [
    "Hollow", "Pale", "Blind", "Broken", "Shadow", "Lost", "Dust", "Cursed", 
    "Grim", "Silent", "Nameless", "Forgotten", "Abyssal", "Bleeding", "Crimson",
    "Weeping", "Iron", "Glass", "Shattered", "Void", "Astral", "Fading", "Ruined",
    "Veiled", "Eldritch", "Corrupted", "Gleaming", "Tattered", "Wandering", "Exiled",
    "Grieving", "Mad", "Doomed", "Eternal", "Frozen", "Burning", "Ashen", "Spectral"
]

NPC_NOUNS = [
    "Wanderer", "Sentinel", "Echo", "Weaver", "Scholar", "Vessel", "Archivist", 
    "Walker", "Scribe", "Merchant", "Keeper", "Penitent", "Observer", "Knight",
    "Oracle", "Mage", "Priest", "Beggar", "King", "Queen", "Jester", "Blacksmith",
    "Gravekeeper", "Alchemist", "Pilgrim", "Prophet", "Executioner", "Heretic",
    "Monk", "Thief", "Assassin", "Ghost", "Phantom", "Wraith", "Soul"
]

def generate_npc_name():
    """Menghasilkan lebih dari 1300 kombinasi nama NPC unik"""
    return f"The {random.choice(NPC_ADJECTIVES)} {random.choice(NPC_NOUNS)}"


# --- 2. KONFIGURASI ITEM ---
ITEM_POOL = [
    {"id": "item_pedang", "name": "Pedang Karat"},
    {"id": "item_batu", "name": "Batu Jiwa"},
    {"id": "item_emas", "name": "Batangan Emas"},
    {"id": "item_buku", "name": "Lembaran Kosong"}
]


# --- 3. BANK SOAL NPC QUIZ (LORE ARCHIVUS) ---
QUIZ_POOL = [
    {"q": "Siapa entitas pencatat memori di dimensi ini?", "a": "ARCHIVUS"},
    {"q": "Apa julukan untuk para penjelajah sepertimu?", "a": "WEAVER"},
    {"q": "Jawab dengan satu kata: Apakah kabut ini membawa kehidupan atau kematian?", "a": "KEMATIAN"},
    {"q": "Benda apa yang kau andalkan untuk membelah kegelapan Archivus?", "a": "LENTERA"},
    {"q": "Berapa banyak arah langkah yang bisa kau pilih di persimpangan?", "a": "4"}
]


# --- 4. FRAGMEN NARASI MODULAR (Pembuka & Penutup) ---
OPENERS_NEUTRAL = [
    "Langkahmu terdengar sangat berat, Weaver.",
    "Kabut ini menelan terlalu banyak nama hari ini...",
    "Mendekatlah, mataku sudah lama buta oleh kegelapan.",
    "Tintamu hampir habis... aku bisa menciumnya dari sini.",
    "Ada bayangan terdistorsi yang terus mengikutimu dari belakang.",
    "Dingin sekali... apakah kau membawa api dari dunia luar?",
    "Jangan menatap dinding itu terlalu lama. Mereka bernapas.",
    "Berapa banyak siklus yang sudah kau lalui hingga tiba di sini?"
]

CLOSERS_MYSTIC = [
    "Semoga Sang Penjaga tidak menyadari kehadiranmu.",
    "Ingat... Archivus tidak pernah lupa, ia hanya menyembunyikannya.",
    "Bergegaslah, sebelum struktur lorong ini kembali bergeser.",
    "Jangan percaya pada suara yang memanggil nama aslimu.",
    "Sejarahmu akan segera berakhir di sini, atau baru saja dimulai.",
    "Biarkan sisa-sisa debu ini menjadi saksi bisu perjalananmu.",
    "Waktuku sudah habis. Kegelapan ini memanggilku kembali.",
    "Jaga lenteramu. Begitu apinya mati, kau akan menjadi seperti kami."
]


# --- 5. EFEK INTERAKSI NPC (Game Consequences) ---
GOOD_EFFECTS = [
    {"type": "heal", "value": 30, "msg": "❤️ Luka-lukamu menutup perlahan. (+30 HP)"},
    {"type": "buff_mp", "value": 20, "msg": "🔮 Pikiranmu menjadi lebih jernih. (+20 MP)"},
    {"type": "give_item", "value": "item_buku", "msg": "📖 Kamu menerima 'Lembaran Kosong'."}
]

BAD_EFFECTS = [
    {"type": "damage", "value": 30, "msg": "💀 Pengkhianatan! Sosok itu menusukmu dari balik jubahnya. (-30 HP)"},
    {"type": "steal_gold", "value": 100, "msg": "❌ Ilusi! Sosok itu lenyap bersama koin di kantongmu. (-100 Gold)"},
    {"type": "curse_mp", "value": 50, "msg": "🌑 Menatap matanya menghancurkan kewarasanmu secara instan. (-50 MP)"},
    {"type": "fatal_trap", "value": 9999, "msg": "💀 **KUTUKAN KEMATIAN!**\nSaat tanganmu menyentuhnya, tubuhnya meledak menjadi kabut hitam pekat yang langsung menelan jiwamu. Nafasmu berhenti detik itu juga."}
]


# --- 6. FUNGSI MERAKIT DIALOG ---
def generate_dialog_early(direction, is_liar):
    opener = random.choice(OPENERS_NEUTRAL)
    closer = random.choice(CLOSERS_MYSTIC)
    
    if is_liar:
        cores = [
            f"Jalan menuju {direction} benar-benar kosong. Aku berani bersumpah demi sisa memori ini.",
            f"Aku baru saja lari dari jebakan mematikan, tapi lorong {direction} terlihat sangat aman.",
            f"Seseorang menjatuhkan banyak harta di jalur {direction}. Ambil sebelum entitas lain melihatnya.",
            f"Jika kau ingin selamat, berlari lurus ke {direction}. Abaikan suara geraman itu."
        ]
    else:
        cores = [
            f"Hawa dingin yang murni berhembus dari {direction}. Itu pertanda jalan itu belum terkorupsi.",
            f"Aku melihat jejak Weaver terdahulu mengarah ke {direction}. Ikuti takdir mereka.",
            f"Lorong selain {direction} dipenuhi anomali yang menganga. Pilihanmu sangat terbatas.",
            f"Tinta sejarah menuntun benangmu ke {direction}. Jangan menyimpang dari naskah."
        ]
    return f"{opener} {random.choice(cores)} {closer}"

def generate_dialog_mid(amount, is_liar):
    opener = random.choice(OPENERS_NEUTRAL)
    closer = random.choice(CLOSERS_MYSTIC)
    
    if is_liar:
        cores = [
            f"Beri aku {amount} Gold, dan aku akan membisikkan rahasia kelemahan Sang Penjaga padamu.",
            f"Tukarkan {amount} Gold denganku. Aku menyembunyikan peta jalan pintas di balik jubah ini.",
            f"Serahkan {amount} Gold, atau aku akan berteriak memanggil letnan kegelapan ke sini!"
        ]
    else:
        cores = [
            f"Tubuhku memudar... Aku hanya butuh {amount} Gold untuk menstabilkan jiwaku. Tolonglah.",
            f"Apakah kau punya {amount} Gold ekstra? Lentera tuaku hampir mati dan aku benci kegelapan.",
            f"Sumbangkan {amount} Gold untuk jiwa yang terlupakan ini, niscaya karma baik melindungimu."
        ]
    return f"{opener} {random.choice(cores)} {closer}"

def generate_dialog_late(req_name, is_liar):
    opener = random.choice(OPENERS_NEUTRAL)
    closer = random.choice(CLOSERS_MYSTIC)
    
    if is_liar:
        cores = [
            f"Harta itu membebani langkahmu. Serahkan {req_name} sekarang sebelum benda itu membunuhmu!",
            f"Kau tak akan selamat membawa {req_name}. Berikan padaku, aku akan menyimpannya."
        ]
    else:
        cores = [
            f"Untuk melewati gerbang berikutnya, kau harus mengorbankan {req_name}. Serahkan padaku.",
            f"Entitas penjaga meminta upeti. {req_name} adalah harga yang pantas untuk nyawamu."
        ]
    return f"{opener} {random.choice(cores)} {closer}"


# --- 7. FUNGSI UTAMA GENERATE NPC ---
def generate_npc(player_gold=0, is_liar=None, is_quiz=False):
    """
    Menghasilkan NPC dinamis dengan nama acak, dialog prosedural, 
    dan efek interaksi yang mengikat ke dalam sistem Game.
    """
    
    # 1. INTERSEPSI NPC QUIZ
    if is_quiz:
        quiz = random.choice(QUIZ_POOL)
        return {
            "identity": "The Memory Thief", 
            "is_liar": False,
            "is_quiz": True,
            "dialog": f"Berhenti, Weaver! Buktikan ingatanmu belum membusuk. Jawab pertanyaanku: *\"{quiz['q']}\"*",
            "requirement": {"type": "quiz", "question": quiz['q'], "answer": quiz['a']},
            "game_effect": None
        }

    # 2. LOGIKA NPC NORMAL (BAIK/JAHAT)
    if is_liar is None:
        is_liar = random.choice([True, False])
    
    name = generate_npc_name() # Generate nama 1000+ variasi
    req = None
    chosen_effect = random.choice(BAD_EFFECTS) if is_liar else random.choice(GOOD_EFFECTS)
    
    # --- FASE EARLY (Navigasi & Petunjuk Arah) ---
    if player_gold < 300:
        arah_pilihan = random.choice(["Utara", "Selatan", "Timur", "Barat"])
        # Dialog petunjuk arah ditambahkan efek "interaksi/bantuan opsional"
        # Supaya kalau pemain berinteraksi, masih ada efeknya
        req = {"type": "gold", "amount": 10, "name": "Gold"} if player_gold >= 10 else None
        dialog_final = generate_dialog_early(arah_pilihan, is_liar)
            
    # --- FASE MID (Transaksi Gold Skala Menengah) ---
    elif 300 <= player_gold < 800:
        amt = int(player_gold * 0.15)
        req = {"type": "gold", "amount": amt, "name": "Gold"}
        dialog_final = generate_dialog_mid(amt, is_liar)

    # --- FASE LATE (Pajak Besar & Pencurian Item) ---
    else:
        if random.random() > 0.5:
            amt = int(player_gold * 0.3)
            req = {"type": "gold", "amount": amt, "name": "Gold"}
            dialog_final = generate_dialog_late(f"{amt} Gold", is_liar)
        else:
            selected_item = random.choice(ITEM_POOL)
            req = {"type": "item", "amount": 1, "id": selected_item['id'], "name": selected_item['name']}
            dialog_final = generate_dialog_late(selected_item['name'], is_liar)

    return {
        "identity": name, 
        "is_liar": is_liar,
        "is_quiz": False,
        "dialog": dialog_final,
        "requirement": req,
        "game_effect": chosen_effect # Efek ini akan dieksekusi di main.py
    }


def get_death_message(cause):
    death_notes = [
        "Tinta habis. Ceritamu terhenti di tengah kalimat.",
        "Namamu memudar dari halaman Archivus.",
        "Kegelapan menelan Weaver terakhir.",
        "Nihilist benar, pada akhirnya tidak ada yang tersisa."
    ]
    return random.choice(death_notes)
