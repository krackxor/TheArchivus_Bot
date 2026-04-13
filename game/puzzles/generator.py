"""
Kumpulan Logika Puzzle & Trivia
File ini berisi semua fungsi untuk menghasilkan soal secara acak (procedural generation) 
berdasarkan tingkat kesulitan (tier).
"""

import random

# --- DATABASE BANK KATA (LINGUISTIK) ---
WORDS_T1 = ["TINTA", "PENA", "BUKU", "KATA", "DEBU", "JALAN", "KABUT", "LUKA", "ASAP", "GELAP", "MATI", "LARI", "JIWA", "PINTU"]
WORDS_T2 = ["PEDANG", "LENTERA", "MEMORI", "KERTAS", "BAYANG", "JALUR", "HANCUR", "TERIAK", "KUTUKAN", "PENJAGA", "RAHASIA"]
WORDS_T3 = ["ARCHIVUS", "KEGELAPAN", "DISTORSI", "FRAGMEN", "WEAVER", "KEABADIAN", "PENGKHIANAT", "KEHAMPAAN", "NEMESIS", "LABIRIN"]

# --- DATABASE LOGIKA & SEJARAH (LORE ARCHIVUS & EASTER EGGS) ---
LORE_PUZZLES = [
    {"q": "Aku punya lubang banyak, tapi bisa menampung air. Siapa aku?", "a": "spons"},
    {"q": "Semakin besar aku, semakin sedikit yang bisa kau lihat.", "a": "gelap"},
    {"q": "Apa nama entitas pencatat memori di dimensi Archivus ini?", "a": "ARCHIVUS"},
    {"q": "Tragedi kereta apa yang berujung pada hancurnya pegunungan Arklay? (Dua kata)", "a": "ECLIPTIC EXPRESS"},
    {"q": "Siapa pendiri yang dikhianati dan bangkit kembali dari lintah?", "a": "JAMES MARCUS"},
    {"q": "Organisasi payung yang menciptakan virus mematikan itu bernama?", "a": "UMBRELLA"},
    {"q": "Kota yang hancur lebur oleh penyebaran virus T adalah Raccoon...? (Satu kata)", "a": "CITY"},
    {"q": "Senjata ikonik dari sang hantu Tsushima adalah? (Satu kata)", "a": "KATANA"},
    {"q": "Siapa dewa perang yang menghancurkan Olympus? (Dua kata)", "a": "KRATOS"},
    {"q": "Senjata rantai ikonik milik sang Dewa Perang adalah Blade of...? (Satu kata)", "a": "CHAOS"},
    {"q": "Pangeran Lucis yang melakukan perjalanan bersama tiga sahabatnya adalah? (Satu kata)", "a": "NOCTIS"},
    {"q": "Nama pedang raksasa milik Cloud Strife adalah? (Dua kata)", "a": "BUSTER SWORD"},
    {"q": "Pusat dari energi Mako di dunia FF7 adalah kota?", "a": "MIDGAR"},
    {"q": "Jika kau mengucapkanku, kau akan merusakku. Siapa aku?", "a": "diam"},
    {"q": "Mata uang yang digunakan oleh para Weaver di Archivus disebut pecahan...", "a": "MEMORI"},
    {"q": "NPC pencuri yang menguji ingatanmu dengan kuis disebut The Memory...?", "a": "THIEF"}
]

def generate_math_puzzle(tier):
    """Menghasilkan kombinasi puzzle matematika dinamis berdasarkan tier."""
    if tier == 1:
        a = random.randint(10, 50)
        b = random.randint(1, 30)
        op = random.choice(['+', '-'])
        answer = str(a + b) if op == '+' else str(max(a, b) - min(a, b)) 
        real_q = f"{max(a, b)} - {min(a, b)}" if op == '-' else f"{a} + {b}"
        return f"Pecahkan distorsi numerik ini: {real_q} = ?", answer
        
    elif tier == 2:
        a = random.randint(4, 12)
        b = random.randint(3, 9)
        return f"Sandi perkalian Archivus: {a} x {b} = ?", str(a * b)
        
    elif tier == 3:
        a = random.randint(3, 8)
        b = random.randint(3, 8)
        c = random.randint(10, 50)
        return f"Uraikan kode matriks ini: ({a} x {b}) + {c} = ?", str((a * b) + c)
        
    else:
        # Tier 4 dan 5 (Aljabar sederhana)
        a = random.randint(5, 12)
        x = random.randint(4, 12) 
        b = a * x
        return f"Pecahkan anomali persamaan ini: {a} x Y = {b}. Berapa nilai Y?", str(x)

def generate_sequence_puzzle(tier):
    """Menghasilkan kombinasi deret angka logika."""
    start = random.randint(1, 10)
    if tier <= 2:
        step = random.randint(2, 6)
        seq = [start + (i * step) for i in range(4)]
        answer = str(start + (4 * step))
        return f"Lengkapi deret memori ini: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ... ?", answer
        
    elif tier <= 4:
        step = random.randint(2, 4)
        seq = [start * (step ** i) for i in range(4)]
        answer = str(start * (step ** 4))
        return f"Pecahkan pola eksponensial ini: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ... ?", answer
        
    else:
        # Fibonacci-like sequence untuk tier 5
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
    # Pastikan kata yang diacak tidak sama dengan kata aslinya
    while "".join(scrambled) == word:
        random.shuffle(scrambled)
        
    return f"Susun kembali kata terdistorsi: **{''.join(scrambled).upper()}**", word

def generate_cipher_puzzle(tier):
    """GENRE BARU: Kriptografi, Pembalikan Teks, dan Observasi Pola"""
    if tier <= 2:
        # Teks Terbalik (Reverse String)
        word = random.choice(WORDS_T1 + WORDS_T2)
        reversed_word = word[::-1]
        return f"Mantra ini ditulis terbalik oleh roh penasaran: **{reversed_word}**. Apa makna aslinya?", word
        
    elif tier == 3:
        # Pencarian Indeks Huruf
        word = random.choice(WORDS_T3)
        n = random.randint(1, len(word))
        answer = word[n-1]
        return f"Dalam kata agung **{word}**, huruf ke-{n} adalah kunci segelnya. Huruf apakah itu?", answer
        
    else:
        # Glitch / Noise Counting (Fokus Mata) untuk Tier 4 & 5
        target_char = random.choice(['X', 'Z', 'V', 'Q'])
        count = random.randint(3, 8)
        noise = [random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'H', 'J', 'W', 'Y']) for _ in range(15)]
        
        for _ in range(count):
            noise.insert(random.randint(0, len(noise)), target_char)
        noise_str = "".join(noise)
        
        return f"Jangan berkedip! Berapa banyak huruf **{target_char}** yang menyusup dalam distorsi ini: **{noise_str}**?", str(count)

def generate_lore_puzzle():
    """Mengambil pertanyaan logika atau sejarah dunia Archivus/Easter Eggs."""
    puzzle = random.choice(LORE_PUZZLES)
    return puzzle["q"], puzzle["a"]
