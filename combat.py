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
ANAGRAM_WORDS = ["archivus", "weaver", "memory", "shadow", "glitch", "silence", "hollow", "void"]

# --- GUDANG KATA BOSS (THE KEEPER) ---
BOSS_WORDS = ["ARCHIVUS ETERNAL", "WEAVER OF DESTINY", "HOLLOW MEMORIES", "BEYOND THE VOID"]

def generate_battle_puzzle(player_kills):
    """
    Menghasilkan teka-teki. 
    Setiap kelipatan 10 kills, akan memunculkan THE KEEPER (Boss).
    """
    # Cek apakah pemicu Boss aktif (Kelipatan 10)
    is_boss = (player_kills > 0 and player_kills % 10 == 0)
    
    if is_boss:
        # --- LOGIKA BOSS ---
        target_word = random.choice(BOSS_WORDS)
        scrambled = list(target_word)
        random.shuffle(scrambled)
        scrambled_word = "".join(scrambled)
        
        tier_name = "⚠️ THE KEEPER (BOSS)"
        answer = target_word
        question = f"SANG PENJAGA MENGHADANGMU! Susun segel ini: **{scrambled_word.upper()}**"
        timer = 12  # Waktu sangat sempit untuk kata panjang
        
    else:
        # --- LOGIKA MONSTER BIASA ---
        is_anagram = random.random() > 0.5
        if is_anagram:
            target_word = random.choice(ANAGRAM_WORDS)
            scrambled = list(target_word)
            random.shuffle(scrambled)
            scrambled_word = "".join(scrambled)
            while scrambled_word == target_word:
                random.shuffle(scrambled)
                scrambled_word = "".join(scrambled)
                
            tier_name = "The Glitch"
            answer = target_word
            question = f"Susun kembali kata yang terdistorsi ini: **{scrambled_word.upper()}**"
        else:
            puzzle = random.choice(LOGIC_PUZZLES)
            tier_name = "Shadow Lurker"
            answer = puzzle["a"]
            question = puzzle["q"]

        # --- SCALING DIFFICULTY (Timer & Distorsi Teks) ---
        if player_kills <= 10:
            timer = 20
            final_question = question
        elif player_kills <= 30:
            timer = 15
            if not is_anagram:
                final_question = question.replace('a', '*').replace('e', '*').replace('i', '*')
            else:
                final_question = f"{question} (Data Corrupted...)"
        else:
            timer = 10
            noise = random.choice([" [VOID]", " [ERROR]", " [NULL]"])
            final_question = f"{question.upper()} {noise}"
            
        question = final_question

    return {
        "monster_name": tier_name,
        "question": question,
        "answer": answer,
        "timer": timer,
        "is_boss": is_boss,
        "generated_time": time.time()
    }

def validate_answer(user_answer, correct_answer, generated_time, time_limit):
    time_taken = time.time() - generated_time
    if time_taken > time_limit:
        return (False, True)
    
    if user_answer.strip().lower() == correct_answer.lower():
        return (True, False)
        
    return (False, False)
