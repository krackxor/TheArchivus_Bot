import random
import time

# --- GUDANG TEKA-TEKI LOGIKA ---
LOGIC_PUZZLES = [
    {"q": "Aku punya banyak daun, tapi aku bukan pohon. Siapakah aku?", "a": "buku"},
    {"q": "Selalu jatuh tapi tidak pernah terluka. Apakah itu?", "a": "hujan"},
    {"q": "Semakin banyak kau ambil, semakin banyak yang tertinggal.", "a": "jejak"},
    {"q": "Aku tidak bisa bicara, tapi akan membalas jika kau bersuara.", "a": "gema"}
]

# --- GUDANG ANAGRAM (THE GLITCH) ---
# Kata-kata yang berhubungan dengan lore Archivus
ANAGRAM_WORDS = ["archivus", "weaver", "memory", "shadow", "glitch", "silence", "hollow", "void"]

def generate_battle_puzzle(player_kills):
    """
    Menghasilkan teka-teki acak antara Logika atau Anagram.
    Kesulitan meningkat berdasarkan jumlah kills pemain.
    """
    # Tentukan jenis monster (50% Logic, 50% Anagram)
    is_anagram = random.random() > 0.5
    
    if is_anagram:
        # LOGIKA ANAGRAM
        target_word = random.choice(ANAGRAM_WORDS)
        scrambled = list(target_word)
        random.shuffle(scrambled)
        scrambled_word = "".join(scrambled)
        
        # Pastikan kata yang diacak tidak sama dengan aslinya
        while scrambled_word == target_word:
            random.shuffle(scrambled)
            scrambled_word = "".join(scrambled)
            
        tier_name = "The Glitch"
        answer = target_word
        question = f"Susun kembali kata yang terdistorsi ini: **{scrambled_word.upper()}**"
    else:
        # LOGIKA TEKA-TEKI BIASA
        puzzle = random.choice(LOGIC_PUZZLES)
        tier_name = "Shadow Lurker"
        answer = puzzle["a"]
        question = puzzle["q"]

    # --- SCALING DIFFICULTY (Timer & Distorsi Teks) ---
    if player_kills <= 10:
        timer = 20
        # Teks normal
        final_question = question
    elif player_kills <= 30:
        timer = 15
        # Distorsi: Hilangkan vokal jika tipe teka-teki logika
        if not is_anagram:
            final_question = question.replace('a', '*').replace('e', '*').replace('i', '*')
        else:
            final_question = f"{question} (Data Corrupted...)"
    else:
        timer = 10
        # Distorsi Elit: Uppercase + Noise
        noise = random.choice([" [VOID]", " [ERROR]", " [NULL]"])
        final_question = f"{question.upper()} {noise}"

    return {
        "monster_name": tier_name,
        "question": final_question,
        "answer": answer,
        "timer": timer,
        "generated_time": time.time()
    }

def validate_answer(user_answer, correct_answer, generated_time, time_limit):
    """
    Validasi jawaban pemain.
    Return: (is_correct, is_timeout)
    """
    time_taken = time.time() - generated_time
    if time_taken > time_limit:
        return (False, True)
    
    if user_answer.strip().lower() == correct_answer.lower():
        return (True, False)
        
    return (False, False)
