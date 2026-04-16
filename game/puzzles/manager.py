# game/puzzles/manager.py

"""
Manager Puzzle (Smart Puzzle Engine)
Bertugas mengatur probabilitas dan mendistribusikan permintaan puzzle 
ke modul yang tepat (math, words, lore).
Dilengkapi dengan DDA (Dynamic Difficulty) dan Elemental Bias.
"""

import random

# Import semua fungsi pembuat puzzle dari file-file kategori 
# (Asumsi fungsi-fungsi ini mengembalikan Tuple: (pertanyaan, jawaban))
from .math import generate_math_puzzle, generate_sequence_puzzle
from .words import generate_linguistic_puzzle, generate_cipher_puzzle
from .lore import generate_lore_puzzle

def get_random_puzzle(tier, monster_element="none", win_streak=0):
    """
    Mengambil satu puzzle secara cerdas (Smart Selection).
    Mengembalikan format dictionary yang sinkron dengan combat.py: 
    {"question": "...", "answer": "..."}
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
    # Menyesuaikan dengan format elemen di database The Archivus
    elem = monster_element.lower()
    
    if elem in ["fire", "blood"]:
        weights[0] += 0.30  # Math (Agresif, butuh hitungan cepat/di bawah tekanan)
    elif elem in ["earth", "ice"]:
        weights[1] += 0.30  # Sequence (Pondasi kokoh, urutan logis, sistematis)
    elif elem in ["water", "poison", "wind"]:
        weights[2] += 0.30  # Linguistic/Anagram (Fleksibel, meracik atau membalik kata)
    elif elem in ["lightning"]:
        weights[3] += 0.30  # Cipher (Cepat, sandi tersembunyi, sangat menguras fokus)
    elif elem in ["dark", "light", "void"]:
        weights[4] += 0.35  # Lore (Misteri kosmis, sejarah dunia The Archivus)

    # 4. PILIH GENRE DENGAN BOBOT YANG SUDAH DIKALIBRASI
    genres = ["math", "sequence", "linguistic", "cipher", "lore"]
    chosen_genre = random.choices(genres, weights=weights, k=1)[0]
    
    # 5. PANGGIL MODUL PUZZLE DENGAN TIER EFEKTIF
    # Tangkap balikan Tuple (q, a) dari masing-masing generator
    if chosen_genre == "math":
        q, a = generate_math_puzzle(effective_tier)
    elif chosen_genre == "sequence":
        q, a = generate_sequence_puzzle(effective_tier)
    elif chosen_genre == "linguistic":
        q, a = generate_linguistic_puzzle(effective_tier)
    elif chosen_genre == "cipher":
        q, a = generate_cipher_puzzle(effective_tier)
    else:
        q, a = generate_lore_puzzle()
        
    # 6. KEMBALIKAN DALAM FORMAT DICTIONARY UNTUK COMBAT.PY
    return {
        "question": str(q),
        "answer": str(a).strip().lower()
    }
