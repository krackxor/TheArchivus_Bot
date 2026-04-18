# game/puzzles/lore.py

"""
Lore, Logic, & Trivia - The Archivus (Revised Edition)
Modul untuk teka-teki naratif, sejarah dunia, dan referensi budaya pop.
"""

import random

# --- DATABASE TEKA-TEKI ---
# Format: {"q": "Pertanyaan", "a": "jawaban_singkat"}
LORE_DATA = [
    # === KATEGORI: THE ARCHIVUS LORE ===
    {"q": "Siapa entitas yang menenun takdir di dimensi ini?", "a": "weaver"},
    {"q": "Mata uang kuno berupa pecahan memori di Archivus disebut?", "a": "memori"},
    {"q": "Gelar bagi penjaga raksasa yang muncul di akhir setiap Cycle?", "a": "penjaga"},
    {"q": "Energi spiritual yang terkuras saat menggunakan Revelatio adalah?", "a": "mp"},
    {"q": "Tempat peristirahatan abadi para Weaver yang telah gugur?", "a": "grave"},
    {"q": "Apa nama artefak keberuntungan milik sang Iblis Perjudian?", "a": "lucky charm"},

    # === KATEGORI: CLASSIC RIDDLES (LOGIKA) ===
    {"q": "Aku punya lubang banyak, tapi bisa menampung air. Siapa aku?", "a": "spons"},
    {"q": "Semakin besar aku, semakin sedikit yang bisa kau lihat.", "a": "gelap"},
    {"q": "Jika kau mengucapkanku, kau akan merusakku. Siapa aku?", "a": "rahasia"},
    {"q": "Aku selalu datang tapi tak pernah tiba. Siapa aku?", "a": "besok"},
    {"q": "Aku milikmu, tapi orang lain lebih sering menggunakannya. Apakah itu?", "a": "nama"},
    {"q": "Aku ringan seperti bulu, tapi manusia terkuat pun tak bisa menahanku lama.", "a": "napas"},
    {"q": "Aku punya kota tapi tak punya rumah, punya gunung tapi tak punya pohon.", "a": "peta"},
    {"q": "Matahari membesarkanku, namun malam membunuhku. Siapa aku?", "a": "bayangan"},

    # === KATEGORI: SOULS-LIKE & RPG TRIVIA ===
    {"q": "Titik api tempat para Chosen Undead beristirahat disebut?", "a": "bonfire"},
    {"q": "Gelar bagi pemain yang mencari Erdtree di Elden Ring?", "a": "tarnished"},
    {"q": "Pedang raksasa milik Cloud Strife di Final Fantasy VII?", "a": "buster sword"},
    {"q": "Burung ikonik berwarna kuning yang menjadi maskot RPG klasik?", "a": "chocobo"},
    {"q": "Fasilitas rahasia tempat penelitian virus Umbrella sering disebut Lab...?", "a": "nest"},
    {"q": "Senjata rantai ikonik milik Kratos di God of War?", "a": "blades of chaos"},
    {"q": "Siapa kapten S.T.A.R.S yang mengkhianati Jill dan Chris?", "a": "wesker"},

    # === KATEGORI: ANIME & MYTHOLOGY ===
    {"q": "Energi kehidupan yang dialirkan para ninja melalui segel tangan?", "a": "chakra"},
    {"q": "Prinsip alkimia di FMA: Pertukaran harus dilakukan secara...?", "a": "setara"},
    {"q": "Bentuk pelepasan terakhir pedang seorang Shinigami disebut?", "a": "bankai"},
    {"q": "Siapa pahlawan yang bisa mengalahkan musuh hanya dengan satu pukulan?", "a": "saitama"},
    {"q": "Buah terlarang yang memberikan kekuatan namun mengutuk pemakannya?", "a": "buah iblis"}
]

def get_puzzle():
    """
    Mengambil satu teka-teki lore secara acak.
    Sinkron dengan manager.py.
    """
    selected = random.choice(LORE_DATA)
    return {
        "question": f"📜 **LORE & RIDDLE**\n_{selected['q']}_",
        "answer": selected['a'].lower()
    }

def generate_lore_puzzle():
    """
    Fungsi legacy/tambahan untuk kompatibilitas jika dibutuhkan 
    oleh modul combat versi lama.
    """
    puzzle = random.choice(LORE_DATA)
    return puzzle["q"], puzzle["a"]
