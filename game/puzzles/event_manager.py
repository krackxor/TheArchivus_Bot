# game/puzzles/event_manager.py

import random
import logging

# Impor modul genre teka-teki yang sudah Anda buat
try:
    from game.puzzles import lore, math, words
except ImportError as e:
    logging.error(f"Gagal mengimpor modul teka-teki: {e}")

def get_random_event_puzzle():
    """
    Mengambil teka-teki secara acak dari salah satu genre: Lore, Math, atau Words.
    Fungsi ini memastikan narasi yang muncul bervariasi selama eksplorasi.
    
    Returns:
        dict: {
            "question": str,  # Narasi soal
            "answer": str,    # Jawaban (string/angka)
            "type": str       # Jenis genre (untuk keperluan log/UI)
        }
    """
    
    # List berisi modul yang tersedia
    # Jika Anda ingin salah satu genre lebih sering muncul, masukkan modul tersebut dua kali di list
    genres = [lore, math, words]
    
    # Pilih modul secara acak
    selected_module = random.choice(genres)
    
    try:
        # Panggil fungsi get_puzzle() yang ada di masing-masing file genre
        puzzle = selected_module.get_puzzle()
        
        # Tambahkan identitas tipe ke dalam dictionary output
        if selected_module == lore:
            puzzle["type"] = "Lore & History"
        elif selected_module == math:
            puzzle["type"] = "Numerical Cipher"
        else:
            puzzle["type"] = "Ancient Word"
            
        return puzzle
        
    except Exception as e:
        logging.error(f"Terjadi kesalahan saat mengambil puzzle dari {selected_module}: {e}")
        # Fallback jika terjadi error agar game tidak crash
        return {
            "question": "Sebuah segel sihir menghalangi jalanmu. Ketik 'OPEN' untuk mencoba membukanya.",
            "answer": "open",
            "type": "Fallback"
        }

def generate_anagram_puzzle(word_list):
    """
    Fungsi pembantu (Utility) jika Anda ingin membuat teka-teki kata acak 
    secara dinamis dari daftar kata di words.py.
    """
    original_word = random.choice(word_list).lower()
    scrambled = list(original_word)
    
    # Pastikan hasil acakan tidak sama dengan kata asli
    while len(original_word) > 1:
        random.shuffle(scrambled)
        if "".join(scrambled) != original_word:
            break
            
    scrambled_display = "-".join(scrambled).upper()
    
    return {
        "question": f"Prasasti kuno ini menampilkan huruf yang teracak sihir: **'{scrambled_display}'**. Apa kata aslinya?",
        "answer": original_word
    }
