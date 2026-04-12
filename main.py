import random
import time

# --- DATABASE MONSTER BERDASARKAN TIER (ENDLESS) ---
MONSTER_NAMES = {
    1: ["Shadow Crawler", "Dust Mite", "Hollow Whisper", "Lost Fragment", "Gloom Fiend"],
    2: ["Archivus Guard", "Void Stalker", "Ink Slime", "Memory Parasite", "Shattered Knight"],
    3: ["Soul Eater", "Memory Butcher", "The Forgotten Weaver", "Crimson Wraith", "Abyssal Hound"],
    4: ["Abyssal Knight", "Glitch Specter", "Time Devourer", "Chaos Oracle", "Void Behemoth"],
    5: ["Ancient Behemoth", "Reality Weaver", "Void Leviathan", "The First Scribe", "Astral Dragon"]
}

# --- DATABASE BANK KATA (LINGUISTIK) ---
WORDS_T1 = ["TINTA", "PENA", "BUKU", "KATA", "DEBU", "JALAN", "KABUT", "LUKA", "ASAP"]
WORDS_T2 = ["PEDANG", "LENTERA", "MEMORI", "KERTAS", "BAYANG", "JALUR", "HANCUR", "GELAP", "JIWA"]
WORDS_T3 = ["ARCHIVUS", "KEGELAPAN", "DISTORSI", "FRAGMEN", "WEAVER", "RAHASIA", "KUTUKAN", "KEABADIAN"]

# --- DATABASE LOGIKA & SEJARAH (LORE ARCHIVUS & EASTER EGGS) ---
LORE_PUZZLES = [
    {"q": "Aku punya lubang banyak, tapi bisa menampung air. Siapa aku?", "a": "spons"},
    {"q": "Semakin besar aku, semakin sedikit yang bisa kau lihat.", "a": "gelap"},
    {"q": "Apa nama entitas pencatat memori di dimensi Archivus ini?", "a": "ARCHIVUS"},
    {"q": "Tragedi kereta apa yang berujung pada hancurnya pegunungan Arklay? (Dua kata)", "a": "ECLIPTIC EXPRESS"},
    {"q": "Siapa pendiri yang dikhianati dan bangkit kembali dari lintah?", "a": "JAMES MARCUS"},
    {"q": "Senjata ikonik dari sang hantu Tsushima adalah? (Satu kata)", "a": "KATANA"},
    {"q": "Siapa dewa perang yang menghancurkan Olympus? (Dua kata)", "a": "KRATOS"},
    {"q": "Pangeran Lucis yang melakukan perjalanan bersama tiga sahabatnya adalah? (Satu kata)", "a": "NOCTIS"},
    {"q": "Jika kau mengucapkanku, kau akan merusakku. Siapa aku?", "a": "diam"}
]

def generate_math_puzzle(tier):
    """
    Menghasilkan ribuan kombinasi puzzle matematika dinamis berdasarkan tier.
    Kombinasi (A + B), (A x B), ((A x B) + C), hingga Aljabar (A x Y = B).
    """
    if tier == 1:
        # Penjumlahan / Pengurangan dasar
        a = random.randint(10, 50)
        b = random.randint(1, 30)
        op = random.choice(['+', '-'])
        # Pastikan hasil selalu positif jika pengurangan
        answer = str(a + b) if op == '+' else str(max(a, b) - min(a, b)) 
        real_q = f"{max(a, b)} - {min(a, b)}" if op == '-' else f"{a} + {b}"
        return f"Pecahkan distorsi numerik ini: {real_q} = ?", answer
        
    elif tier == 2:
        # Perkalian dasar
        a = random.randint(4, 12)
        b = random.randint(3, 9)
        return f"Sandi perkalian Archivus: {a} x {b} = ?", str(a * b)
        
    elif tier == 3:
        # Operasi campuran: (A x B) + C
        a = random.randint(3, 8)
        b = random.randint(3, 8)
        c = random.randint(10, 50)
        return f"Uraikan kode matriks ini: ({a} x {b}) + {c} = ?", str((a * b) + c)
        
    else:
        # Aljabar sederhana: A x Y = B
        a = random.randint(5, 12)
        x = random.randint(4, 12) # Nilai Y yang dicari
        b = a * x
        return f"Pecahkan anomali persamaan ini: {a} x Y = {b}. Berapa nilai Y?", str(x)

def generate_sequence_puzzle(tier):
    """
    Menghasilkan ribuan kombinasi deret angka logika.
    """
    start = random.randint(1, 10)
    
    if tier <= 2:
        # Deret Tambah (Contoh: 2, 4, 6, 8, ?)
        step = random.randint(2, 6)
        seq = [start + (i * step) for i in range(4)]
        answer = str(start + (4 * step))
        return f"Lengkapi deret memori ini: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ... ?", answer
        
    elif tier <= 4:
        # Deret Kali / Geometri (Contoh: 2, 4, 8, 16, ?)
        step = random.randint(2, 4)
        seq = [start * (step ** i) for i in range(4)]
        answer = str(start * (step ** 4))
        return f"Pecahkan pola eksponensial ini: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ... ?", answer
        
    else:
        # Deret Fibonacci Custom (Suku saat ini = Suku n-1 + Suku n-2)
        seq = [start, start + random.randint(1, 5)]
        for i in range(2, 5):
            seq.append(seq[-1] + seq[-2])
        answer = str(seq[-1] + seq[-2])
        return f"Sandi Kuno Archivus (Deret): {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, {seq[4]}, ... ?", answer

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
    """Mengambil pertanyaan logika atau sejarah dunia Archivus."""
    puzzle = random.choice(LORE_PUZZLES)
    return puzzle["q"], puzzle["a"]

def generate_battle_puzzle(tier_level=1, is_boss=False):
    """
    Sistem Multi-Genre Engine (Menghasilkan 1000+ Variasi).
    """
    # 1. Tentukan Identitas Monster
    if is_boss:
        m_name = random.choice(["THE KEEPER", "JAMES MARCUS ECHO", "VOID OVERLORD", "THE FINAL ARCHIVIST"])
        tier_label = "BOSS"
        # Boss damage skala besar
        damage = random.randint(25, 40) + (tier_level * 5)
    else:
        # Pastikan tier tidak melebihi 5 untuk index dictionary (Endless scale)
        safe_tier = min(tier_level, 5)
        m_name = random.choice(MONSTER_NAMES[safe_tier])
        tier_label = tier_level
        # Scaling damage yang progresif berdasarkan tier
        damage = random.randint(8, 15) + (tier_level * random.randint(3, 6))

    # 2. Tentukan Genre Puzzle (Genre SEQUENCE ditambahkan ke dalam pertempuran)
    genres = ["linguistik", "math", "sequence"]
    
    # Semakin tinggi tier, semakin bervariasi genre yang muncul (Lore mulai muncul)
    if tier_level >= 3 or is_boss:
        genres.append("lore")

    chosen_genre = random.choice(genres)

    if is_boss and random.random() > 0.6:
        # Pengecualian sinematik untuk Boss (Linguistik Berat)
        target_word = random.choice(["PENJAGA GERBANG", "DUNIA HAMPA", "MEMORI HILANG", "ECLIPTIC EXPRESS"])
        scrambled = list(target_word)
        random.shuffle(scrambled)
        question = f"SANG PENJAGA MENGHADANGMU! Susun segel kutukan ini: **{''.join(scrambled).upper()}**"
        answer = target_word
    else:
        # Eksekusi berdasarkan genre yang diundi
        if chosen_genre == "math":
            question, answer = generate_math_puzzle(tier_level)
        elif chosen_genre == "sequence":
            question, answer = generate_sequence_puzzle(tier_level)
        elif chosen_genre == "lore":
            question, answer = generate_lore_puzzle()
        else:
            question, answer = generate_linguistic_puzzle(tier_level)

    # 3. Dynamic Timer (Semakin tinggi tier, semakin cepat waktunya habis)
    timer_limit = max(20, 60 - (tier_level * 5)) if not is_boss else 45

    return {
        "monster_name": m_name,
        "tier": tier_label,
        "damage": damage,
        "question": question,
        "answer": answer,
        "timer": timer_limit,
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
