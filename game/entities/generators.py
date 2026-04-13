"""
Sistem Generator Entitas (Entity Generators)
Berisi fungsi-fungsi untuk merakit data dasar entitas, seperti nama acak NPC dan dialog dasar.
"""

import random

# --- KUMPULAN KOSA KATA NAMA NPC ---
PREFIXES = [
    "The Blind", "The Hollow", "The Wandering", "The Forgotten", 
    "The Faceless", "The Cursed", "The Broken", "The Exiled"
]
NOUNS = [
    "Seer", "Scribe", "Thief", "Weaver", "Archivist", 
    "Merchant", "Oracle", "Knight", "Scholar", "Beggar"
]

def generate_npc_name():
    """
    Menghasilkan kombinasi nama unik untuk NPC.
    Contoh output: 'The Hollow Scribe', 'The Blind Oracle'
    """
    return f"{random.choice(PREFIXES)} {random.choice(NOUNS)}"

def generate_npc(player_gold=0, is_liar=False):
    """
    Menghasilkan data dasar NPC (Identitas, Dialog, dan Syarat/Cost).
    (Fungsi ini tetap dipertahankan agar file-file lama yang memanggilnya tidak error).
    """
    identity = generate_npc_name()
    
    # Menentukan dialog berdasarkan sifat NPC (Jahat/Penipu vs Baik)
    if is_liar:
        dialogs = [
            "'Hehehe... Kau terlihat lelah. Mau menukar sedikit nyawamu dengan emas?'",
            "'Peti ini berat sekali... Berikan aku sebagian koinmu, dan isinya jadi milikmu!'",
            "'Ayo bertaruh dengan takdir! Serahkan koinmu, dan lihat apa yang terjadi!'"
        ]
        # NPC pembohong/penipu biasanya memberi harga "murah" di awal untuk memancing pemain
        cost = random.randint(10, 30)
    else:
        dialogs = [
            "'Luka-lukamu bercerita banyak, Weaver... Berikan sedikit koin, dan aku akan menyembuhkanmu.'",
            "'Jalan di depan sangat gelap. Ambillah ramuan ini dariku.'",
            "'Bahkan seorang Weaver butuh bantuan. Kau butuh sesuatu?'"
        ]
        # NPC baik/jujur memberikan harga yang standar
        cost = random.randint(20, 50)
        
    # Skala dinamis: Jika pemain sedang kaya (Gold banyak), NPC akan menaikkan harga
    if player_gold > 200:
        cost += random.randint(10, 40)

    return {
        "identity": identity,
        "dialog": random.choice(dialogs),
        "requirement": {"type": "gold", "amount": cost},
        "is_liar": is_liar
    }
