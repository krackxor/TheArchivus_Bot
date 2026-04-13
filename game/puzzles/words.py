"""
Logika Teka-teki Bahasa, Anagram, dan Kriptografi (Cipher)
Berisi ratusan kosa kata untuk menguji ketelitian Weaver.
"""

import random

# --- TIER 1: KATA PENDEK (3-5 HURUF) ---
WORDS_T1 = [
    "TINTA", "PENA", "BUKU", "KATA", "DEBU", "JALAN", "KABUT", "LUKA", "ASAP", "GELAP",
    "MATI", "LARI", "JIWA", "PINTU", "MATA", "ATMA", "ROH", "ARUS", "ALUR", "DUNIA",
    "INTI", "RASA", "SUCI", "BUMI", "LANGI", "NADI", "FANA", "DOA", "BESI", "EMAS",
    "GHOIB", "JATI", "KALA", "MAYA", "OTAK", "TALI", "UMAT", "WANGI", "ZAKAT", "ADAB",
    "AKAL", "ALAM", "AMAL", "ARAK", "ASAL", "AYAT", "BAJA", "BARA", "BISA", "BUKA",
    "BUTI", "CITRA", "DANA", "DOSA", "DUKA", "ESOK", "FAJAR", "GUNA", "HATI", "ILMU",
    "JEDA", "KACA", "KAUM", "KIRA", "KUAT", "LAUT", "LUAS", "MANA", "MILIK", "NAMA",
    "PAGI", "RAJA", "SARI", "TEPI", "TUAN", "ULAR", "USIA", "WAKTU", "YAKIN", "ZONA"
    # Tambahkan kata 3-5 huruf lainnya di sini...
]

# --- TIER 2: KATA MENENGAH (6-8 HURUF) ---
WORDS_T2 = [
    "PEDANG", "LENTERA", "MEMORI", "KERTAS", "BAYANG", "JALUR", "HANCUR", "TERIAK", "KUTUKAN", "PENJAGA",
    "RAHASIA", "SENJATA", "FRAGMEN", "CAHAYA", "DIMENSI", "GERBANG", "DESTINI", "MISTERI", "UTUSAN", "PENULIS",
    "UTOPIS", "SIMBOL", "KODRAT", "NYAWA", "TAKDIR", "SPIRIT", "OBSESI", "DENDAM", "HIKMAH", "SASTRA",
    "TUMBAL", "UTUSAN", "WANGSIT", "ZIARAH", "AKHIRAT", "BANGKIT", "CERMIN", "DAHSYAT", "ENTITAS", "FILSAFAT",
    "GEJALA", "HAKIKAT", "ISYARAT", "JAGAT", "KRISTAL", "LEGENDA", "MANTRA", "NURANI", "OBJEK", "PARADE",
    "QANUN", "RIWAYAT", "SABDA", "TAHTA", "UKIRAN", "VAKUM", "WASIAT", "XENON", "YUDISIAL", "ZAMAN",
    "BINTANG", "PESONA", "SUNYI", "KEMBAR", "TELAGA", "KELANA", "BUDAYA", "BAHASA", "HURUF", "SULAM"
    # Tambahkan kata 6-8 huruf lainnya di sini...
]

# --- TIER 3: KATA SULIT & FRASA (9+ HURUF) ---
WORDS_T3 = [
    "ARCHIVUS", "KEGELAPAN", "DISTORSI", "KEABADIAN", "PENGKHIANAT", "KEHAMPAAN", "NEMESIS", "LABIRIN", "PERADABAN", "SINGGANA",
    "KEMURNIAN", "MANUSKRIP", "REINKARNASI", "EKSISTENSI", "HORIZON", "PANDEMONIUM", "RESONANSI", "SPIRITUAL", "TELEPATI", "UNIVERSUM",
    "VIBRASI", "WANGSIT", "XENOFOBIA", "YURISDIKSI", "ZODIAK", "KATULISTIWA", "METAMORFOSA", "NARASI", "OBSERVASI", "PARADIGMA",
    "REVOLUSI", "SINKRONISASI", "TRANSMISI", "URGENSI", "VISUALISASI", "WACANA", "YURISPRUDENSI", "ZIGGURAT", "KONTEMPLASI", "MANIFESTASI",
    "PENENUNTAKDIR", "SANGBENJAGA", "KERAJAANHAMPA", "MEMORIHILANG", "SEJARAHKUNO", "DUNIAMAYA", "PINTUKEBENARAN", "CAHAYALANGIT", "JIWATERBELENGGU"
    # Tambahkan kata panjang lainnya di sini...
]

def generate_linguistic_puzzle(tier):
    """Menghasilkan teka-teki acak kata (Anagram)."""
    if tier == 1:
        word = random.choice(WORDS_T1)
    elif tier in [2, 3]:
        word = random.choice(WORDS_T2)
    else:
        word = random.choice(WORDS_T3)
        
    scrambled = list(word)
    random.shuffle(scrambled)
    while "".join(scrambled) == word:
        random.shuffle(scrambled)
        
    return f"Susun kembali kata terdistorsi: *{''.join(scrambled).upper()}*", word

def generate_cipher_puzzle(tier):
    """Teka-teki sandi (Pembalikan, Indeks, atau Hitung Huruf)."""
    mode = random.randint(1, 3)
    
    if mode == 1 or tier <= 2:
        # Mode: Teks Terbalik
        word = random.choice(WORDS_T1 + WORDS_T2)
        reversed_word = word[::-1]
        return f"Mantra ini ditulis terbalik: *{reversed_word}*. Apa makna aslinya?", word
        
    elif mode == 2:
        # Mode: Pencarian Indeks Huruf
        word = random.choice(WORDS_T2 + WORDS_T3)
        n = random.randint(1, len(word))
        answer = word[n-1]
        return f"Dalam kata agung *{word}*, huruf ke-{n} adalah kunci segelnya. Huruf apakah itu?", answer
        
    else:
        # Mode: Menghitung Huruf Tertentu (Fokus Mata)
        target_char = random.choice(['X', 'Z', 'V', 'Q', 'W'])
        count = random.randint(3, 7)
        # Buat string acak (noise)
        noise_chars = "ABCDEFGHIJKLMNPRSTU"
        noise = [random.choice(noise_chars) for _ in range(15)]
        # Masukkan target_char sebanyak 'count' kali secara acak
        for _ in range(count):
            noise.insert(random.randint(0, len(noise)), target_char)
        noise_str = "".join(noise)
        
        return f"Jangan berkedip! Berapa banyak huruf *{target_char}* yang menyusup di sini: `{noise_str}`?", str(count)
