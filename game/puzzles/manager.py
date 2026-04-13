"""
Manager Puzzle
Bertugas mengatur probabilitas dan mendistribusikan permintaan puzzle 
ke modul yang tepat (math, words, lore).
"""

import random

# Import semua fungsi pembuat puzzle dari file-file kategori
from .math import generate_math_puzzle, generate_sequence_puzzle
from .words import generate_linguistic_puzzle, generate_cipher_puzzle
from .lore import generate_lore_puzzle

def get_random_puzzle(tier):
    """
    Mengambil satu puzzle acak berdasarkan tier kesulitan.
    Mengembalikan tuple: (Pertanyaan_String, Jawaban_String)
    """
    
    # 1. Tentukan bobot/probabilitas genre berdasarkan tier
    if tier <= 2:
        # Tier rendah: Fokus ke matematika dasar dan anagram
        genres = ["math", "sequence", "linguistic", "cipher", "lore"]
        weights = [0.35, 0.15, 0.30, 0.10, 0.10] 
    elif tier <= 4:
        # Tier menengah: Cipher dan deret angka mulai sering muncul
        genres = ["math", "sequence", "linguistic", "cipher", "lore"]
        weights = [0.25, 0.25, 0.20, 0.20, 0.10]
    else:
        # Tier tinggi/Boss: Fokus ke lore, cipher sulit, dan aljabar
        genres = ["math", "sequence", "linguistic", "cipher", "lore"]
        weights = [0.15, 0.15, 0.15, 0.30, 0.25]
        
    # 2. Pilih genre secara acak berdasarkan bobot
    chosen_genre = random.choices(genres, weights=weights, k=1)[0]
    
    # 3. Panggil fungsi yang sesuai dengan genre yang terpilih
    if chosen_genre == "math":
        return generate_math_puzzle(tier)
    elif chosen_genre == "sequence":
        return generate_sequence_puzzle(tier)
    elif chosen_genre == "linguistic":
        return generate_linguistic_puzzle(tier)
    elif chosen_genre == "cipher":
        return generate_cipher_puzzle(tier)
    else:
        return generate_lore_puzzle()
