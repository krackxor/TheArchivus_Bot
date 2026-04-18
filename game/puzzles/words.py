# game/puzzles/words.py

"""
Logika Teka-teki Bahasa, Anagram, dan Kriptografi (Cipher) - The Archivus
Modul untuk menguji ketelitian linguistik dan pemecahan sandi para Weaver.
"""

import random

# --- DATASET KATA ---
WORDS_T1 = [
    "TINTA", "PENA", "BUKU", "KATA", "DEBU", "JALAN", "KABUT", "LUKA", "ASAP", "GELAP",
    "MATI", "LARI", "JIWA", "PINTU", "MATA", "ATMA", "ROH", "ARUS", "ALUR", "DUNIA",
    "INTI", "RASA", "SUCI", "BUMI", "NADI", "FANA", "DOA", "BESI", "EMAS", "GHOIB",
    "JATI", "KALA", "MAYA", "OTAK", "TALI", "ADAB", "AKAL", "ALAM", "AMAL", "ARAK"
]

WORDS_T2 = [
    "PEDANG", "LENTERA", "MEMORI", "KERTAS", "BAYANG", "HANCUR", "TERIAK", "KUTUKAN", "PENJAGA",
    "RAHASIA", "SENJATA", "FRAGMEN", "CAHAYA", "DIMENSI", "GERBANG", "DESTINI", "MISTERI", "UTUSAN",
    "SIMBOL", "KODRAT", "NYAWA", "TAKDIR", "SPIRIT", "OBSESI", "DENDAM", "HIKMAH", "TUMBAL", "AKHIRAT"
]

WORDS_T3 = [
    "ARCHIVUS", "KEGELAPAN", "DISTORSI", "KEABADIAN", "PENGKHIANAT", "KEHAMPAAN", "NEMESIS", "LABIRIN", 
    "PERADABAN", "SINGGANA", "KEMURNIAN", "MANUSKRIP", "REINKARNASI", "EKSISTENSI", "HORIZON", 
    "PANDEMONIUM", "RESONANSI", "SPIRITUAL", "UNIVERSUM", "MANIFESTASI", "KONTEMPLASI"
]

def generate_linguistic_puzzle(tier):
    """Menghasilkan teka-teki Anagram (Kata Acak)."""
    if tier <= 1:
        word = random.choice(WORDS_T1)
    elif tier <= 3:
        word = random.choice(WORDS_T2)
    else:
        word = random.choice(WORDS_T3)
        
    scrambled = list(word)
    while True:
        random.shuffle(scrambled)
        if "".join(scrambled) != word:
            break
            
    return f"Susun kembali kata terdistorsi ini: **'{''.join(scrambled).upper()}'**", word.lower()

def generate_cipher_puzzle(tier):
    """Teka-teki sandi (Pembalikan, Indeks, atau Hitung Huruf)."""
    mode = random.randint(1, 3)
    
    if mode == 1 or tier <= 2:
        # Mode: Teks Terbalik
        word = random.choice(WORDS_T1 + WORDS_T2)
        reversed_word = word[::-1]
        return f"Mantra ini tertulis terbalik: **'{reversed_word}'**. Apa makna aslinya?", word.lower()
        
    elif mode == 2:
        # Mode: Pencarian Indeks Huruf
        word = random.choice(WORDS_T2 + WORDS_T3)
        n = random.randint(1, len(word))
        answer = word[n-1].lower()
        return f"Dalam kata agung **'{word}'**, huruf ke-{n} adalah kunci segelnya. Huruf apakah itu?", answer
        
    else:
        # Mode: Menghitung Huruf Tertentu (Fokus Mata)
        target_char = random.choice(['X', 'Z', 'V', 'Q', 'W'])
        count = random.randint(3, 6)
        noise_chars = "ABCDEFGHIJKLMNPRSTU"
        noise = [random.choice(noise_chars) for _ in range(12)]
        for _ in range(count):
            noise.insert(random.randint(0, len(noise)), target_char)
        noise_str = "".join(noise)
        
        return f"Jangan berkedip! Berapa banyak huruf **'{target_char}'** yang menyusup di sini: `{noise_str}`?", str(count)

def get_puzzle(tier=None):
    """
    Pintu utama untuk manager.py.
    Memilih antara Anagram atau Cipher secara acak.
    """
    if tier is None:
        tier = random.randint(1, 5)
        
    # Kocok antara tipe Linguistic (Anagram) atau Kriptografi (Cipher)
    if random.choice(["ling", "ciph"]) == "ling":
        q, a = generate_linguistic_puzzle(tier)
    else:
        q, a = generate_cipher_puzzle(tier)
        
    return {
        "question": f"📜 **LINGUISTIC ANOMALY**\n_{q}_",
        "answer": a.strip().lower()
    }
