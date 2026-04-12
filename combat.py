import random
import time

# --- DATABASE MONSTER BERDASARKAN TIER (ENDLESS) ---
MONSTER_NAMES = {
    1: ["Shadow Crawler", "Dust Mite", "Hollow Whisper"],
    2: ["Archivus Guard", "Void Stalker", "Ink Slime"],
    3: ["Soul Eater", "Memory Butcher", "The Forgotten Weaver"],
    4: ["Abyssal Knight", "Glitch Specter", "Time Devourer"],
    5: ["Ancient Behemoth", "Reality Weaver", "Void Leviathan"]
}

# --- DATABASE BANK KATA (LINGUISTIK) ---
WORDS_T1 = ["TINTA", "PENA", "BUKU", "KATA", "DEBU"]
WORDS_T2 = ["PEDANG", "LENTERA", "MEMORI", "KERTAS", "BAYANG", "JALUR"]
WORDS_T3 = ["ARCHIVUS", "KEGELAPAN", "DISTORSI", "FRAGMEN", "WEAVER", "RAHASIA"]

# --- DATABASE LOGIKA & SEJARAH (LORE ARCHIVUS & EASTER EGGS) ---
LORE_PUZZLES = [
    {"q": "Aku punya lubang banyak, tapi bisa menampung air. Siapa aku?", "a": "spons"},
    {"q": "Semakin besar aku, semakin sedikit yang bisa kau lihat.", "a": "gelap"},
    {"q": "Apa nama entitas pencatat memori di dimensi Archivus ini?", "a": "ARCHIVUS"},
    {"q": "Tragedi kereta apa yang berujung pada hancurnya pegunungan Arklay? (Dua kata)", "a": "ECLIPTIC EXPRESS"},
    {"q": "Siapa pendiri yang dikhianati dan bangkit kembali dari lintah?", "a": "JAMES MARCUS"},
    {"q": "Jika kau mengucapkanku, kau akan merusakku. Siapa aku?", "a": "diam"}
]

def generate_math_puzzle(tier):
    """Menghasilkan puzzle matematika berdasarkan tier kesulitan."""
    if tier <= 2:
        a = random.randint(10, 50)
        b = random.randint(1, 20)
        op = random.choice(['+', '-'])
        answer = str(a + b) if op == '+' else str(a - b)
        return f"Pecahkan distorsi numerik ini: {a} {op} {b} = ?", answer
    else:
        # Tier 3 ke atas pakai perkalian
        a = random.randint(5, 15)
        b = random.randint(3, 9)
        answer = str(a * b)
        return f"Pecahkan kode perkalian ini: {a} x {b} = ?", answer

def generate_linguistic_puzzle(tier):
    """Menghasilkan anagram/word scramble."""
    if tier == 1:
        word = random.choice(WORDS_T1)
    elif tier in [2, 3]:
        word = random.choice(WORDS_T2)
    else:
        word = random.choice(WORDS_T3)
        
    scrambled = list(word)
    random.shuffle(scrambled)
    # Pastikan kata yang diacak tidak kebetulan sama persis
    while "".join(scrambled) == word:
        random.shuffle(scrambled)
        
    return f"Susun kembali kata terdistorsi: **{''.join(scrambled).upper()}**", word

def generate_lore_puzzle():
    """Mengambil pertanyaan logika atau sejarah."""
    puzzle = random.choice(LORE_PUZZLES)
    return puzzle["q"], puzzle["a"]

def generate_battle_puzzle(tier_level=1, is_boss=False):
    """
    Menghasilkan puzzle pertarungan dengan sistem Multi-Genre.
    """
    # 1. Tentukan Identitas Monster
    if is_boss:
        m_name = random.choice(["THE KEEPER", "JAMES MARCUS ECHO", "VOID OVERLORD", "THE FINAL ARCHIVIST"])
        tier_label = "BOSS"
        damage = random.randint(25, 40)
    else:
        # Pastikan tier tidak melebihi 5 untuk index dictionary (Endless scale)
        safe_tier = min(tier_level, 5)
        m_name = random.choice(MONSTER_NAMES[safe_tier])
        tier_label = tier_level
        # Scaling damage yang adil: Tier 1 (3-6), Tier 5 (15-30)
        damage = tier_level * random.randint(3, 6)

    # 2. Tentukan Genre Puzzle
    genres = ["linguistik", "math"]
    # Semakin tinggi tier, semakin bervariasi genre yang muncul
    if tier_level >= 3 or is_boss:
        genres.append("lore")

    chosen_genre = random.choice(genres)

    if is_boss and random.random() > 0.5:
        # Pengecualian sinematik untuk Boss
        target_word = random.choice(["PENJAGA GERBANG", "DUNIA HAMPA", "MEMORI HILANG"])
        scrambled = list(target_word)
        random.shuffle(scrambled)
        question = f"SANG PENJAGA MENGHADANGMU! Susun segel ini: **{''.join(scrambled).upper()}**"
        answer = target_word
    else:
        # Eksekusi berdasarkan genre
        if chosen_genre == "math":
            question, answer = generate_math_puzzle(tier_level)
        elif chosen_genre == "lore":
            question, answer = generate_lore_puzzle()
        else:
            question, answer = generate_linguistic_puzzle(tier_level)

    return {
        "monster_name": m_name,
        "tier": tier_label,
        "damage": damage,
        "question": question,
        "answer": answer,
        "timer": 60, # Waktu standar 1 menit
        "is_boss": is_boss,
        "generated_time": time.time()
    }

def validate_answer(user_answer, correct_answer, generated_time, time_limit):
    """Validasi jawaban pemain melawan waktu dan string."""
    time_taken = time.time() - generated_time
    if time_taken > time_limit:
        return (False, True) # (Benar/Salah, Timeout/Tidak)
    
    # Hapus spasi berlebih dan abaikan huruf besar/kecil
    clean_user = user_answer.strip().lower()
    clean_correct = correct_answer.strip().lower()
    
    if clean_user == clean_correct:
        return (True, False)
        
    return (False, False)
