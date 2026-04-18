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

# ==============================================================================
# FUNGSI ADAPTOR (JEMBATAN UNTUK MAIN ARCHITECTURE)
# ==============================================================================
def generate_puzzle(tier=1):
    """
    Fungsi jembatan yang dibutuhkan oleh handlers/menu.py dan event_handler.py.
    Mengambil data dari get_random_puzzle lalu memformatnya agar sesuai 
    dengan format Event Sistem Utama.
    """
    # Ambil puzzle mentah dari sistem genre-mu
    raw_puzzle = get_random_puzzle(tier_level=tier)
    
    # Ambil jawaban (string) dan ubah ke huruf kecil untuk validasi
    correct_answer = raw_puzzle.get("answer", "").lower()
    
    # Bungkus menjadi format event_data yang dipahami oleh FSM (State Machine)
    # process_event_outcome mengecek kunci 'answers' sebagai sebuah List
    event_data = {
        "type": "quiz",
        "tier": tier,
        "genre": raw_puzzle.get("genre", "Mystery"),
        "question": f"[{raw_puzzle.get('genre', 'Mystery')}] {raw_puzzle.get('question', '')}",
        "answers": [correct_answer], # Diubah menjadi list agar tidak error saat divalidasi
        "gold_reward": tier * 50,    # Reward dinamis berdasarkan tier
        "exp_reward": tier * 50
    }
    
    return event_data
