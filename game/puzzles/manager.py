"""
Manager Puzzle (Smart Puzzle Engine)
Bertugas mengatur probabilitas dan mendistribusikan permintaan puzzle 
ke modul yang tepat (math, words, lore).
Dilengkapi dengan DDA (Dynamic Difficulty) dan Elemental Bias.
"""

import random

# Import semua fungsi pembuat puzzle dari file-file kategori
from .math import generate_math_puzzle, generate_sequence_puzzle
from .words import generate_linguistic_puzzle, generate_cipher_puzzle
from .lore import generate_lore_puzzle

def get_random_puzzle(tier, monster_element="Netral", win_streak=0):
    """
    Mengambil satu puzzle secara cerdas (Smart Selection).
    Mengembalikan tuple: (Pertanyaan_String, Jawaban_String)
    """
    
    # 1. DYNAMIC DIFFICULTY ADJUSTMENT (DDA)
    # Jika pemain menang 3x berturut-turut, tingkat kesulitan puzzle naik 1 tier!
    effective_tier = min(5, tier + (win_streak // 3))
    
    # 2. TENTUKAN BOBOT DASAR BERDASARKAN TIER EFEKTIF
    # Urutan Index: [0: math, 1: sequence, 2: linguistic, 3: cipher, 4: lore]
    if effective_tier <= 2:
        # Tier rendah: Fokus ke matematika dasar dan anagram
        weights = [0.35, 0.15, 0.30, 0.10, 0.10] 
    elif effective_tier <= 4:
        # Tier menengah: Cipher dan deret angka mulai seimbang
        weights = [0.25, 0.25, 0.20, 0.20, 0.10]
    else:
        # Tier tinggi: Fokus ke Lore, Cipher sulit, dan Deret kompleks
        weights = [0.15, 0.15, 0.15, 0.30, 0.25]
        
    # 3. ELEMENTAL AFFINITY (BIAS ELEMEN)
    # Membuat pemain merasakan tema yang berbeda saat melawan elemen tertentu
    if monster_element == "Api":
        weights[0] += 0.30  # 🔥 Api -> Matematika (Agresif, hitungan cepat/tekanan)
    elif monster_element == "Tanah":
        weights[1] += 0.30  # 🪨 Tanah -> Deret angka (Pondasi kokoh, urutan logis)
    elif monster_element == "Air":
        weights[2] += 0.30  # 💧 Air -> Linguistik/Anagram (Ketenangan, merangkai kata)
    elif monster_element in ["Petir", "Angin"]:
        weights[3] += 0.30  # ⚡ Petir -> Cipher (Cepat, sandi tersembunyi, pusing)
    elif monster_element in ["Kegelapan", "Cahaya"]:
        weights[4] += 0.35  # 🌑 Gelap/Cahaya -> Lore (Misteri dunia, sejarah Archivus)

    # 4. PILIH GENRE DENGAN BOBOT YANG SUDAH DIKALIBRASI
    genres = ["math", "sequence", "linguistic", "cipher", "lore"]
    chosen_genre = random.choices(genres, weights=weights, k=1)[0]
    
    # 5. PANGGIL MODUL PUZZLE DENGAN TIER EFEKTIF (BUKAN TIER ASLI)
    if chosen_genre == "math":
        return generate_math_puzzle(effective_tier)
    elif chosen_genre == "sequence":
        return generate_sequence_puzzle(effective_tier)
    elif chosen_genre == "linguistic":
        return generate_linguistic_puzzle(effective_tier)
    elif chosen_genre == "cipher":
        return generate_cipher_puzzle(effective_tier)
    else:
        return generate_lore_puzzle() # Lore biasanya statis/acak dari database
