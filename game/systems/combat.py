"""
Sistem Pertarungan, Engine Genre, dan Validasi Waktu
"""
import time
import random

# Memanggil Entitas
from game.entities.monsters import get_random_monster
from game.entities.bosses import get_random_boss

# Memanggil Puzzle Manager (Satu pintu untuk semua genre!)
from game.puzzles.manager import get_random_puzzle

def generate_battle_puzzle(tier_level=1, is_boss=False):
    """Sistem Multi-Genre Engine (Dikelola oleh Manager)."""
    
    if is_boss:
        m_name = get_random_boss()
        tier_label = "BOSS"
        damage = random.randint(25, 40) + (tier_level * 5)
    else:
        m_name = get_random_monster(tier_level)
        tier_label = tier_level
        damage = random.randint(8, 15) + (tier_level * random.randint(3, 6))

    # Boss memiliki probabilitas tinggi mengeluarkan puzzle naratif sinematik
    if is_boss and random.random() > 0.6:
        target_word = random.choice(["PENJAGA GERBANG", "DUNIA HAMPA", "MEMORI HILANG", "ECLIPTIC EXPRESS", "SANG PENGKHIANAT"])
        scrambled = list(target_word.replace(" ", "")) # Hilangkan spasi saat diacak
        random.shuffle(scrambled)
        question = f"SANG PENJAGA MENGHADANGMU! Susun segel kutukan ini (Tanpa spasi): *{''.join(scrambled).upper()}*"
        answer = target_word.replace(" ", "").lower()
    else:
        # Otak pemilih puzzle (Manager) akan mengurus sisanya!
        question, answer = get_random_puzzle(tier_level)

    # Dynamic Timer
    timer_limit = max(20, 60 - (tier_level * 5)) if not is_boss else 45

    return {
        "monster_name": m_name,
        "tier": tier_label,
        "damage": damage,
        "question": question,
        "answer": str(answer).lower(), # Pastikan jawaban diseragamkan huruf kecil
        "timer": timer_limit,
        "is_boss": is_boss,
        "generated_time": time.time()
    }

def validate_answer(user_answer, correct_answer, generated_time, time_limit):
    """Validasi jawaban pemain melawan waktu dan string."""
    time_taken = time.time() - generated_time
    if time_taken > time_limit:
        return (False, True) 
    
    clean_user = str(user_answer).strip().lower()
    clean_correct = str(correct_answer).strip().lower()
    
    if clean_user == clean_correct:
        return (True, False)
        
    return (False, False)
