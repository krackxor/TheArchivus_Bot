"""
Sistem Generator Entitas (Entity Generators)
Berisi fungsi-fungsi untuk merakit data dasar entitas, seperti nama acak NPC dan dialog dasar.
[DEPRECATED / LEGACY SUPPORT] - Sangat disarankan untuk menggunakan game.entities.npcs mulai sekarang.
Fungsi ini dipertahankan dan disesuaikan strukturnya agar modul lama yang memanggilnya tidak crash.
"""

import random

# --- KUMPULAN KOSA KATA NAMA NPC (Diperluas) ---
PREFIXES = [
    "The Blind", "The Hollow", "The Wandering", "The Forgotten", 
    "The Faceless", "The Cursed", "The Broken", "The Exiled",
    "The Crimson", "The Ashen", "The Silent", "The Weeping"
]
NOUNS = [
    "Seer", "Scribe", "Thief", "Weaver", "Archivist", 
    "Merchant", "Oracle", "Knight", "Scholar", "Beggar",
    "Specter", "Phantom", "Wanderer"
]

def generate_npc_name():
    """
    Menghasilkan kombinasi nama unik untuk NPC.
    Contoh output: 'The Hollow Scribe', 'The Weeping Oracle'
    """
    return f"{random.choice(PREFIXES)} {random.choice(NOUNS)}"

def generate_npc(player_gold=0, is_liar=False):
    """
    Menghasilkan data dasar NPC (Identitas, Dialog, dan Syarat/Cost).
    Struktur telah diperbarui dengan 'choices' untuk mencegah KeyError jika dipanggil oleh UI baru.
    """
    identity = generate_npc_name()
    
    # Menentukan dialog berdasarkan sifat NPC (Penipu vs Baik)
    if is_liar:
        dialogs = [
            "'Hehehe... Kau terlihat lelah. Mau menukar sedikit nyawamu dengan emas?'",
            "'Peti ini berat sekali... Berikan aku sebagian koinmu, dan isinya jadi milikmu!'",
            "'Ayo bertaruh dengan takdir! Serahkan koinmu, dan lihat apa yang terjadi!'",
            "'Psst... Penjaga di depan buta terhadap emas. Beri aku koin, kuajarkan cara melewatinya.'"
        ]
        # NPC pembohong/penipu biasanya memberi harga "murah" di awal untuk memancing pemain
        cost = random.randint(10, 30)
    else:
        dialogs = [
            "'Luka-lukamu bercerita banyak, Weaver... Berikan sedikit koin, dan aku akan menyembuhkanmu.'",
            "'Jalan di depan sangat gelap. Ambillah ramuan ini dariku.'",
            "'Bahkan seorang Weaver butuh bantuan. Kau butuh sesuatu?'",
            "'Istirahatlah sejenak. Serahkan sedikit koinmu untuk perbekalan, dan aku akan menjagamu.'"
        ]
        # NPC baik/jujur memberikan harga yang standar
        cost = random.randint(20, 50)
        
    # Skala dinamis: Jika pemain sedang kaya (Gold banyak), NPC akan "memalak" lebih mahal
    if player_gold > 500:
        cost += random.randint(30, 70)
    elif player_gold > 200:
        cost += random.randint(10, 40)

    # --- PERBAIKAN BENTROK MINOR ---
    # Menambahkan array 'choices' agar UI di main.py tetap bisa memproses tombol (Inline Keyboard)
    return {
        "identity": identity,
        "dialog": random.choice(dialogs),
        "requirement": {"type": "gold", "amount": cost},
        "is_liar": is_liar,
        "choices": [
            {"text": f"Bayar {cost} Gold", "action": "pay_gold", "value": cost},
            {"text": "Abaikan", "action": "ignore", "value": 0}
        ]
    }
