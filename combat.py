import random
import time

# --- 20 GUDANG TEKA-TEKI LOGIKA (MUDAH) ---
LOGIC_PUZZLES = [
    {"q": "Aku punya lubang banyak, tapi bisa menampung air. Siapa aku?", "a": "spons"},
    {"q": "Aku punya leher, tapi tidak punya kepala. Aku adalah...", "a": "botol"},
    {"q": "Aku punya gigi banyak, tapi tidak bisa menggigit.", "a": "sisir"},
    {"q": "Semakin besar aku, semakin sedikit yang bisa kau lihat.", "a": "gelap"},
    {"q": "Aku punya satu mata, tapi tidak bisa melihat apa-apa.", "a": "jarum"},
    {"q": "Aku selalu ada di depanmu, tapi kau tidak bisa melihatku.", "a": "masa depan"},
    {"q": "Jika kau mengucapkanku, kau akan merusakku. Siapa aku?", "a": "diam"},
    {"q": "Aku akan basah saat sedang mengeringkan.", "a": "handuk"},
    {"q": "Aku punya leher tapi tak punya kepala, punya lengan tapi tak punya tangan.", "a": "baju"},
    {"q": "Aku bisa pecah tanpa pernah disentuh atau dijatuhkan.", "a": "janji"},
    {"q": "Aku bisa bicara banyak bahasa tanpa punya mulut.", "a": "buku"},
    {"q": "Aku selalu lari, tapi tidak pernah lelah.", "a": "jam"},
    {"q": "Aku punya banyak kunci, tapi tidak bisa membuka satu pintu pun.", "a": "piano"},
    {"q": "Semakin banyak kau memberi padaku, semakin haus aku.", "a": "api"},
    {"q": "Aku bisa terbang tanpa sayap dan menangis tanpa mata.", "a": "awan"},
    {"q": "Aku hanya bisa hidup jika diberi makan, tapi mati jika diberi minum.", "a": "api"},
    {"q": "Milikmu, tapi lebih sering digunakan oleh orang lain.", "a": "nama"},
    {"q": "Aku selalu naik dan tidak pernah turun.", "a": "umur"},
    {"q": "Aku punya jari, tapi tidak punya kuku.", "a": "sarung tangan"},
    {"q": "Apa yang bisa kau tangkap, tapi tidak bisa kau lempar?", "a": "flu"}
]

# --- 20 GUDANG ANAGRAM (KATA ARCHIVUS & UMUM) ---
ANAGRAM_WORDS = [
    "tinta", "buku", "weaver", "shadow", "memory", "void", "hollow", "glitch",
    "kunci", "pintu", "gelap", "cahaya", "rutan", "pedang", "istana", "hantu",
    "darah", "nyawa", "emas", "mimpi"
]

# --- GUDANG KATA BOSS (THE KEEPER) ---
BOSS_WORDS = ["PENJAGA GERBANG", "MEMORI HILANG", "DUNIA HAMPA", "CAHAYA WEAVER"]

def generate_battle_puzzle(player_kills):
    """
    Menghasilkan teka-teki dengan rasio 50:50 antara Logika dan Anagram.
    """
    is_boss = (player_kills > 0 and player_kills % 10 == 0)
    
    if is_boss:
        target_word = random.choice(BOSS_WORDS)
        scrambled = list(target_word)
        random.shuffle(scrambled)
        scrambled_word = "".join(scrambled)
        
        tier_name = "⚠️ THE KEEPER (BOSS)"
        answer = target_word
        question = f"SANG PENJAGA MENGHADANGMU! Susun segel ini: **{scrambled_word.upper()}**"
        timer = 15 
        
    else:
        is_anagram = random.random() > 0.5
        if is_anagram:
            target_word = random.choice(ANAGRAM_WORDS)
            scrambled = list(target_word)
            random.shuffle(scrambled)
            scrambled_word = "".join(scrambled)
            # Pastikan tidak sama dengan aslinya
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

        # Scaling Kesulitan berdasarkan kills
        if player_kills <= 10:
            timer = 20
            final_question = question
        elif player_kills <= 30:
            timer = 15
            final_question = question.replace(' ', ' . ')
        else:
            timer = 10
            final_question = f"{question.upper()} [ERROR]"
            
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
