import random
import time

# --- DATABASE MONSTER BERDASARKAN TIER ---
MONSTER_TIERS = {
    1: [
        {"name": "Shadow Crawler", "damage": random.randint(3, 5)},
        {"name": "Hollow Soul", "damage": random.randint(3, 5)},
        {"name": "Dust Mite", "damage": random.randint(3, 5)}
    ],
    2: [
        {"name": "Archivus Guard", "damage": random.randint(6, 8)},
        {"name": "Void Stalker", "damage": random.randint(6, 8)},
        {"name": "Glitch Specter", "damage": random.randint(6, 8)}
    ],
    3: [
        {"name": "Soul Eater", "damage": random.randint(9, 12)},
        {"name": "Memory Butcher", "damage": random.randint(9, 12)},
        {"name": "The Forgotten Weaver", "damage": random.randint(9, 12)}
    ],
    "BOSS": [
        {"name": "THE KEEPER", "damage": 15},
        {"name": "JAMES MARCUS ECHO", "damage": 14},
        {"name": "VOID OVERLORD", "damage": 15}
    ]
}

# --- DATABASE TEKA-TEKI ---
LOGIC_PUZZLES = [
    {"q": "Aku punya lubang banyak, tapi bisa menampung air. Siapa aku?", "a": "spons"},
    {"q": "Aku punya leher, tapi tidak punya kepala. Aku adalah...", "a": "botol"},
    {"q": "Aku punya gigi banyak, tapi tidak bisa menggigit.", "a": "sisir"},
    {"q": "Semakin besar aku, semakin sedikit yang bisa kau lihat.", "a": "gelap"},
    {"q": "Jika kau mengucapkanku, kau akan merusakku. Siapa aku?", "a": "diam"}
]

ANAGRAM_WORDS = ["tinta", "weaver", "shadow", "memory", "kunci", "cahaya", "pedang"]

def generate_battle_puzzle(player_kills):
    """
    Menghasilkan teka-teki dengan Tiering Monster dan Damage Dinamis.
    """
    # 1. Tentukan Tier berdasarkan jumlah kill atau acak untuk variasi
    if player_kills > 0 and player_kills % 10 == 0:
        tier = "BOSS"
    elif player_kills > 20:
        tier = 3
    elif player_kills > 10:
        tier = 2
    else:
        tier = 1

    # 2. Pilih Monster dari Tier tersebut
    monster_info = random.choice(MONSTER_TIERS[tier])
    
    # 3. Tentukan Jenis Puzzle (Anagram vs Logika)
    is_boss = (tier == "BOSS")
    if is_boss:
        target_word = random.choice(["PENJAGA GERBANG", "DUNIA HAMPA", "MEMORI HILANG"])
        scrambled = list(target_word)
        random.shuffle(scrambled)
        question = f"SANG PENJAGA MENGHADANGMU! Susun segel ini: **{''.join(scrambled).upper()}**"
        answer = target_word
    else:
        if random.random() > 0.5: # Anagram
            target_word = random.choice(ANAGRAM_WORDS)
            scrambled = list(target_word)
            random.shuffle(scrambled)
            question = f"Susun kembali kata terdistorsi: **{''.join(scrambled).upper()}**"
            answer = target_word
        else: # Logika
            puzzle = random.choice(LOGIC_PUZZLES)
            question = puzzle["q"]
            answer = puzzle["a"]

    return {
        "monster_name": monster_info["name"],
        "tier": tier,
        "damage": monster_info["damage"],
        "question": question,
        "answer": answer,
        "timer": 60,  # Waktu diperbarui menjadi 1 menit
        "is_boss": is_boss,
        "generated_time": time.time()
    }

def validate_answer(user_answer, correct_answer, generated_time, time_limit):
    time_taken = time.time() - generated_time
    if time_taken > time_limit:
        return (False, True) # Terlalu lama
    
    if user_answer.strip().lower() == correct_answer.lower():
        return (True, False) # Benar
        
    return (False, False) # Salah
