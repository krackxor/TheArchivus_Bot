# game/puzzles/manager.py

"""
Manager Puzzle (Refactored for Genre-Based Architecture)
Bertugas mendistribusikan permintaan teka-teki ke modul yang tepat (math, words, lore).
Mendukung label genre untuk tampilan UI yang lebih informatif.
"""

import random
import logging

# Impor modul genre teka-teki
# Pastikan file lore.py, math.py, dan words.py memiliki fungsi get_puzzle()
from game.puzzles import lore, math, words

def get_random_puzzle(tier_level=1, monster_element="none", win_streak=0):
    """
    Mengambil teka-teki secara acak dari genre yang tersedia.
    Sinkron dengan combat.py dan event eksplorasi.
    
    Returns:
        dict: {"question": str, "answer": str, "genre": str}
    """
    
    # List modul genre yang tersedia
    genres = [lore, math, words]
    
    # Pilih modul secara acak
    selected_module = random.choice(genres)
    
    try:
        # Panggil fungsi get_puzzle() dari modul yang terpilih
        # Fungsi ini harus mengembalikan dict: {"question": "...", "answer": "..."}
        puzzle = selected_module.get_puzzle()
        
        # Tambahkan label genre untuk mempercantik UI di combat/event
        if selected_module == lore:
            puzzle["genre"] = "Lore"
        elif selected_module == math:
            puzzle["genre"] = "Math"
        else:
            puzzle["genre"] = "Words"
            
        return puzzle
        
    except Exception as e:
        logging.error(f"Terjadi kesalahan saat mengambil puzzle dari {selected_module}: {e}")
        # Fallback Puzzle jika file genre error atau belum lengkap
        return {
            "question": "Sebutkan kata kunci kuno untuk lewat: 'ARCHIVUS'",
            "answer": "archivus",
            "genre": "System"
        }

def validate_puzzle_answer(user_answer, correct_answer):
    """
    Utility sederhana untuk memvalidasi jawaban.
    """
    return str(user_answer).strip().lower() == str(correct_answer).strip().lower()
