# game/puzzles/manager.py

"""
Manager Puzzle (Refactored for Genre-Based Architecture)
Bertugas mendistribusikan permintaan teka-teki ke modul yang tepat (math, words, lore).
Mendukung label genre untuk tampilan UI yang lebih informatif.
"""

import random
import logging

# Impor modul genre teka-teki
from game.puzzles import lore, math, words

def get_random_puzzle(tier_level=1, monster_element="none", win_streak=0):
    """
    Mengambil teka-teki secara acak dari genre yang tersedia.
    """
    
    # List modul genre yang tersedia
    genres = [lore, math, words]
    
    # Jika tier tinggi, kita bisa mengatur probabilitas atau jenis kuis di sini
    selected_module = random.choice(genres)
    
    try:
        # Panggil fungsi get_puzzle() dari modul yang terpilih
        # lore.py sekarang mengembalikan format: {"question": "...", "answer": "..."}
        puzzle = selected_module.get_puzzle()
        
        # Tambahkan label genre untuk mempercantik UI
        if selected_module == lore:
            puzzle["genre"] = "Lore & Strategy"
        elif selected_module == math:
            puzzle["genre"] = "Logic & Math"
        else:
            puzzle["genre"] = "Words & Riddles"
            
        return puzzle
        
    except Exception as e:
        logging.error(f"Gagal mengambil puzzle dari {selected_module}: {e}")
        # Fallback jika ada file yang error
        return {
            "question": "Sebutkan kata kunci kuno: 'ARCHIVUS'",
            "answer": "archivus",
            "genre": "System"
        }

def validate_puzzle_answer(user_answer, correct_answer):
    """
    Utility untuk memvalidasi jawaban secara case-insensitive.
    """
    return str(user_answer).strip().lower() == str(correct_answer).strip().lower()

# ==============================================================================
# FUNGSI ADAPTOR (JEMBATAN UNTUK MAIN ARCHITECTURE)
# ==============================================================================
def generate_puzzle(tier=1):
    """
    Fungsi jembatan yang dibutuhkan oleh handlers/event.py dan event_handler.py.
    Memformat data agar sesuai dengan format Event Sistem Utama.
    """
    # Ambil puzzle mentah
    raw_puzzle = get_random_puzzle(tier_level=tier)
    
    # Ambil jawaban dan pastikan formatnya string lower-case
    correct_answer = str(raw_puzzle.get("answer", "")).lower()
    
    # Bungkus menjadi format event_data yang dipahami oleh FSM (State Machine)
    # Sangat Penting: 'answers' harus berupa LIST [] agar tidak error saat loop check
    event_data = {
        "type": "quiz",
        "tier": tier,
        "genre": raw_puzzle.get("genre", "Mystery"),
        # Format tampilan kuis di chat
        "question": raw_puzzle.get('question', ''),
        "answers": [correct_answer],  # List agar kompatibel dengan sistem validasi multi-answer
        "gold_reward": tier * 50,     # Reward Gold: Tier 1 = 50, Tier 2 = 100, dst
        "exp_reward": tier * 30       # Reward EXP
    }
    
    return event_data
