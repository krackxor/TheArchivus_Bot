"""
Sistem Pertarungan, Engine Genre, dan Validasi Waktu
Kini mendukung sistem Equipment (Defense dari Armor).
"""
import time
import random

# Memanggil Entitas
from game.entities.monsters import get_random_monster
from game.entities.bosses import get_random_boss

# Memanggil Puzzle Manager
from game.puzzles.manager import get_random_puzzle

def calculate_equipment_stats(player):
    """
    Menghitung total bonus dari equipment yang ada di inventory.
    """
    inventory = player.get('inventory', [])
    total_def = 0
    total_atk = 0 # Bisa digunakan jika ingin menambah sistem damage ke monster
    
    for item in inventory:
        total_def += item.get('bonus_def', 0)
        total_atk += item.get('bonus_atk', 0)
        
    return total_atk, total_def

def generate_battle_puzzle(player, tier_level=1, is_boss=False):
    """Sistem Multi-Genre Engine dengan kalkulasi stat pertahanan pemain."""
    
    # 1. Tentukan Nama & Damage Dasar Monster
    if is_boss:
        m_name = get_random_boss()
        tier_label = "BOSS"
        base_damage = random.randint(25, 40) + (tier_level * 5)
    else:
        m_name = get_random_monster(tier_level)
        tier_label = tier_level
        base_damage = random.randint(8, 15) + (tier_level * random.randint(3, 6))

    # 2. Kalkulasi Pertahanan (EQUIPMENT CHECK)
    _, bonus_def = calculate_equipment_stats(player)
    
    # Damage akhir = Damage monster - Defense pemain (Minimal 1 damage tetap masuk)
    final_damage = max(1, base_damage - bonus_def)

    # 3. Pilih Puzzle (Boss Sinematik vs Manager)
    if is_boss and random.random() > 0.6:
        target_word = random.choice(["PENJAGA GERBANG", "DUNIA HAMPA", "MEMORI HILANG", "ECLIPTIC EXPRESS", "SANG PENGKHIANAT"])
        scrambled = list(target_word.replace(" ", ""))
        random.shuffle(scrambled)
        question = f"SANG PENJAGA MENGHADANGMU! Susun segel kutukan ini (Tanpa spasi): *{''.join(scrambled).upper()}*"
        answer = target_word.replace(" ", "").lower()
    else:
        question, answer = get_random_puzzle(tier_level)

    # 4. Dynamic Timer
    timer_limit = max(20, 60 - (tier_level * 5)) if not is_boss else 45

    return {
        "monster_name": m_name,
        "tier": tier_label,
        "damage": final_damage, # Damage yang sudah dikurangi defense
        "base_damage": base_damage, # Simpan damage asli untuk info jika perlu
        "defense_applied": bonus_def,
        "question": question,
        "answer": str(answer).lower(),
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
