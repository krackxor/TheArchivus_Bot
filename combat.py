import random
import time

BASE_PUZZLES = [
    {"q": "Aku punya banyak daun, tapi aku bukan pohon. Siapakah aku?", "a": "buku"},
    {"q": "Selalu jatuh tapi tidak pernah terluka. Apakah itu?", "a": "hujan"},
    {"q": "Semakin banyak kau ambil, semakin banyak yang tertinggal.", "a": "jejak"},
    {"q": "Aku tidak bisa bicara, tapi akan membalas jika kau bersuara.", "a": "gema"}
]

def generate_battle_puzzle(player_kills):
    puzzle = random.choice(BASE_PUZZLES)
    question = puzzle["q"]
    answer = puzzle["a"]
    
    if player_kills <= 10:
        tier_name, timer, final_question = "Shadow Grunt", 20, question
    elif player_kills <= 30:
        tier_name, timer = "Echo Phantom", 15
        final_question = question.replace('a', '*').replace('e', '*')
    else:
        tier_name, timer = "Void Sentinel", 10
        noise = random.choice([" [KOSONG]", " [JANGAN PERCAYA MATAMU]", " [HAMPA]"])
        final_question = f"{question.upper()}{noise}"

    return {
        "monster_name": tier_name,
        "question": final_question,
        "answer": answer,
        "timer": timer,
        "generated_time": time.time()
    }

def validate_answer(user_answer, correct_answer, generated_time, time_limit):
    time_taken = time.time() - generated_time
    if time_taken > time_limit:
        return (False, True) # (Benar/Salah, Timeout)
    if user_answer.strip().lower() == correct_answer.lower():
        return (True, False)
    return (False, False)
