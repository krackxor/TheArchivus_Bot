import random

# --- DATABASE NAMA (15 Karakter) ---
NPC_NAMES = [
    "The Wanderer", "Hollow Sentinel", "Echo of Silence", "Pale Weaver", "Blind Scholar",
    "Broken Vessel", "Shadow Weaver", "Lost Archivist", "Dust Walker", "Cursed Scribe",
    "Void Merchant", "Fallen Keeper", "Grim Penitent", "Silent Observer", "The Nameless"
]

# --- DATABASE 50 KARAKTER (Berdasarkan List Kamu) ---
TRAITS_DB = {
    "POSITIF": [
        "Empatik", "Jujur", "Bertanggung Jawab", "Dewasa", "Sabar", 
        "Setia", "Rendah Hati", "Disiplin", "Konsisten", "Optimis", 
        "Pemaaf", "Supportif", "Bijaksana", "Mandiri", "Tulus"
    ],
    "NETRAL": [
        "Ambivert", "Perfeksionis", "Realistis", "Ambisius", "Kompetitif", 
        "Sensitif", "Idealistis", "Overthinker", "Spontan", "Santai"
    ],
    "NEGATIF": [
        "Egois", "Pemalas", "Pemarah", "Pendendam", "Sombong", 
        "Iri", "Munafik", "Posesif", "Drama Queen", "Pengeluh"
    ],
    "BERBAHAYA": [
        "Manipulator", "Gaslighter", "Narsistik", "Opportunist", "Backstabber", 
        "Two-faced", "Dominan", "Pasif-Agresif", "Playing Victim", "Love Bomber"
    ],
    "EKSTREM": [
        "Psikopat", "Sociopath", "Obsesif", "Paranoid", "Nihilist"
    ]
}

# --- KONFIGURASI ITEM ---
ITEM_POOL = [
    {"id": "item_pedang", "name": "Pedang Karat"},
    {"id": "item_batu", "name": "Batu Jiwa"},
    {"id": "item_emas", "name": "Batangan Emas"},
    {"id": "item_buku", "name": "Lembaran Kosong"}
]

def generate_npc():
    """
    Menghasilkan NPC secara acak. 
    Bisa menjadi penipu (is_liar) atau jujur dengan kepribadian yang kompleks.
    """
    # 1. Tentukan Niat (50% Peluang Jahat/Liar)
    is_liar = random.choice([True, False])
    
    # 2. Pilih Kategori & Sifat (Trait)
    if is_liar:
        # Penipu mengambil sifat dari kategori Manipulatif, Negatif, atau Ekstrem
        cat_key = random.choice(["BERBAHAYA", "NEGATIF", "EKSTREM"])
    else:
        # Penolong mengambil sifat dari kategori Positif atau Netral
        cat_key = random.choice(["POSITIF", "NETRAL"])
    
    trait = random.choice(TRAITS_DB[cat_key])
    name = random.choice(NPC_NAMES)
    
    # 3. Tentukan Permintaan (Requirement)
    if random.random() > 0.5:
        req = {"type": "gold", "amount": random.randint(15, 60), "name": "Gold"}
    else:
        selected_item = random.choice(ITEM_POOL)
        req = {"type": "item", "amount": 1, "id": selected_item['id'], "name": selected_item['name']}

    # 4. Logika Dialog Berdasarkan Kategori (Psikologi Terbalik)
    if cat_key == "BERBAHAYA":
        # NPC Jahat yang manipulatif (Bicara sangat manis/Love Bomber)
        dialogs = [
            f"Aku melihat jiwa yang murni dalam dirimu. Berikan {req['name']} itu, biar aku menjagamu dari kegelapan.",
            f"Hanya kau yang bisa membantuku. Setelah kau beri {req['name']}, aku akan memberikan seluruh hartaku padamu.",
            f"Jangan takut, Weaver. Aku di sini untuk menolongmu. Cukup sedikit {req['name']} sebagai tanda persahabatan."
        ]
    elif cat_key == "EKSTREM":
        # NPC Dingin/Antisosial
        dialogs = [
            f"Hidup ini tak berarti. Berikan {req['name']}-mu, atau biarkan ia membusuk bersamamu.",
            f"Aku mendengar bisikan bahwa kau akan mati. Berikan {req['name']} itu sekarang jika ingin kutunda ajalmu."
        ]
    elif cat_key == "POSITIF":
        # NPC Baik tapi bisa bicara kasar (Tulus tapi Marah/Disiplin)
        dialogs = [
            f"Jangan bodoh! Cepat berikan {req['name']} itu jika kau tidak ingin hancur di langkah berikutnya!",
            f"Berikan padaku! Archivus tidak butuh Weaver yang lamban. Aku akan memperkuat lenteramu dengan ini!",
            f"Kau membawa {req['name']} itu seperti beban. Sini, biar kuurus dan kuberikan kau perlindungan!"
        ]
    elif cat_key == "NEGATIF":
        # NPC Jahat yang terang-terangan (Sombong/Egois)
        dialogs = [
            f"Heh, Weaver payah. Berikan {req['name']}-mu sebagai upeti karena telah mengganggu jalanku!",
            f"Aku butuh {req['name']}. Berikan atau aku akan memastikan monster di depan mencabikmu!"
        ]
    else: # NETRAL
        dialogs = [
            f"Mari bicara realistis. Aku butuh {req['name']}, dan kau butuh selamat. Setuju?",
            f"Secara logika, pertukaran ini menguntungkanmu. Berikan {req['name']}-nya."
        ]

    return {
        "identity": f"{name} ({trait})",
        "trait": trait,
        "category": cat_key,
        "is_liar": is_liar,
        "dialog": random.choice(dialogs),
        "requirement": req
    }

def get_death_message(cause):
    death_notes = [
        "Tinta habis. Ceritamu terhenti di tengah kalimat.",
        "Namamu perlahan memudar dari halaman Archivus.",
        "Kegelapan menelan Weaver terakhir. Cahaya itu kini padam.",
        "Nihilist benar, pada akhirnya tidak ada yang tersisa darimu."
    ]
    return random.choice(death_notes)
