# game/data/npcs/quizzes.py

"""
NPC Quiz Database - The Archivus
Berisi NPC cendekiawan yang memberikan tantangan pengetahuan.
Mekanik: Jawaban benar = Reward, Jawaban salah = Malu/Penalti kecil.
"""

import random

QUIZ_NPCS = {
    "npc_scholar_titus": {
        "name": "Scholar Titus",
        "role": "quiz_master",
        "desc": "Seorang pria paruh baya dengan kacamata retak yang terus memegang tumpukan perkamen berdebu.",
        "dialog_greetings": [
            "Hanya pikiran yang tajam yang bisa menembus kabut Archivus. Siap diuji?",
            "Pengetahuan adalah satu-satunya senjata yang tidak akan pernah tumpul.",
            "Berhenti sejenak, Weaver. Mari kita lihat seberapa banyak kau mengingat sejarah dunia ini."
        ],
        "quizzes": [
            {
                "question": "Apa nama virus yang menghancurkan Raccoon City dalam catatan kuno?",
                "answer": "t-virus",
                "reward": {"gold": 200, "exp": 150}
            },
            {
                "question": "Siapa Weaver pertama yang berhasil memetakan The Whispering Hall?",
                "answer": "aethelred",
                "reward": {"gold": 300, "exp": 200}
            },
            {
                "question": "Berapa jumlah sayap yang dimiliki oleh Sang Penjaga Siklus Keempat?",
                "answer": "6",
                "reward": {"gold": 500, "exp": 400, "item": "scroll_of_wisdom"}
            }
        ],
        "fail_msg": "Titus menghela napas kecewa. 'Mungkin kau harus lebih banyak membaca daripada sekadar mengayunkan pedang.'"
    },

    "npc_riddle_statue": {
        "name": "Prasasti Teka-teki",
        "role": "quiz_master",
        "desc": "Batu tegak yang bersinar biru redup dengan ukiran huruf yang bergerak-gerak.",
        "dialog_greetings": [
            "Bicaralah, atau kau takkan pernah lewat...",
            "Suara dari masa lalu menuntut jawabanmu."
        ],
        "quizzes": [
            {
                "question": "Aku tidak punya mulut tapi bisa menjawab jika kau panggil. Siapa aku?",
                "answer": "gema",
                "reward": {"exp": 500, "item": "ancient_coin"}
            },
            {
                "question": "Aku selalu ada di depanmu tapi kau tidak bisa melihatku. Apakah aku?",
                "answer": "masa depan",
                "reward": {"exp": 600}
            }
        ],
        "fail_msg": "Cahaya pada batu meredup. Seolah-olah kau baru saja kehilangan kesempatan berharga."
    }
}

def get_quiz_npc(npc_id):
    """Mengambil data NPC kuis berdasarkan ID."""
    return QUIZ_NPCS.get(npc_id)

def get_random_quiz(npc_id):
    """Mengambil satu pertanyaan kuis secara acak dari NPC tertentu."""
    npc = QUIZ_NPCS.get(npc_id)
    if npc and "quizzes" in npc:
        return random.choice(npc["quizzes"])
    return None

def check_quiz_answer(user_input, correct_answer):
    """Validasi jawaban user (case-insensitive)."""
    return str(user_input).strip().lower() == str(correct_answer).strip().lower()
