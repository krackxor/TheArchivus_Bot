import random

# --- DATABASE NAMA (15 Karakter Unik) ---
NPC_NAMES = [
    "The Wanderer", "Hollow Sentinel", "Echo of Silence", "Pale Weaver", "Blind Scholar",
    "Broken Vessel", "Shadow Weaver", "Lost Archivist", "Dust Walker", "Cursed Scribe",
    "Void Merchant", "Fallen Keeper", "Grim Penitent", "Silent Observer", "The Nameless"
]

# --- DATABASE 50 KARAKTER (Psikologi Terbagi 5 Kategori) ---
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

def generate_npc(player_gold=0, is_liar=None):
    """
    Menghasilkan NPC dinamis berdasarkan progres kekayaan pemain.
    """
    if is_liar is None:
        is_liar = random.choice([True, False])
    
    name = random.choice(NPC_NAMES)
    req = None
    
    # --- 1. FASE EARLY (Gold < 300) : Pemandu / Penyesat ---
    if player_gold < 300:
        trait = "Penyesat" if is_liar else "Pemandu"
        cat_key = "NEGATIF" if is_liar else "POSITIF"
        
        if is_liar:
            dialogs = [
                "Ke Utara saja, Weaver. Aku melihat cahaya pintu keluar di sana.",
                "Barat adalah jalan paling cepat menuju Toko. Jangan lewatkan itu.",
                "Aku bersumpah Timur sedang kosong. Monster-monster sedang tidur."
            ]
        else:
            dialogs = [
                "Hati-hati, aku mendengar geraman di Selatan. Putar baliklah.",
                "Gunakan jalan Barat jika ingin menghindari jebakan di lorong ini.",
                "Tetaplah di jalur Utara, Archivus sedang stabil di arah itu."
            ]
            
    # --- 2. FASE MID (300 <= Gold < 800) : Transaksi / Pemalak ---
    elif 300 <= player_gold < 800:
        cat_key = random.choice(["BERBAHAYA", "NEGATIF"]) if is_liar else random.choice(["NETRAL", "POSITIF"])
        trait = random.choice(TRAITS_DB[cat_key])
        
        # Minta 15% dari total Gold pemain (dibulatkan)
        amt = int(player_gold * 0.15)
        req = {"type": "gold", "amount": amt, "name": "Gold"}
        
        if is_liar:
            dialogs = [f"Beri aku {amt} Gold, dan aku akan membisikkan rahasia besar padamu."]
        else:
            dialogs = [f"Aku butuh {amt} Gold untuk menyalakan lentera ini kembali. Bantu aku?"]

    # --- 3. FASE LATE (Gold >= 800) : The Collector / Corrupted Soul ---
    else:
        cat_key = "EKSTREM" if is_liar else "POSITIF"
        trait = random.choice(TRAITS_DB[cat_key])
        
        # Minta 30% Gold atau satu Item acak
        if random.random() > 0.5:
            amt = int(player_gold * 0.3)
            req = {"type": "gold", "amount": amt, "name": "Gold (Pajak)"}
            dialogs = [f"Harta itu terlalu berat untukmu. Setor {amt} Gold padaku sekarang!"]
        else:
            selected_item = random.choice(ITEM_POOL)
            req = {"type": "item", "amount": 1, "id": selected_item['id'], "name": selected_item['name']}
            dialogs = [f"Berikan {selected_item['name']}-mu. Orang mati tidak butuh barang mewah."]

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
        "Namamu memudar dari halaman Archivus.",
        "Kegelapan menelan Weaver terakhir.",
        "Nihilist benar, pada akhirnya tidak ada yang tersisa."
    ]
    return random.choice(death_notes)
