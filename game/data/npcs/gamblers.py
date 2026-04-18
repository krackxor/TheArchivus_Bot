# game/data/npcs/gamblers.py

"""
NPC Gambler Database - The Archivus
Berisi NPC perjudian (Mini-games).
Mekanik: High Risk High Reward menggunakan sistem taruhan Gold/Memory.
"""

import random

GAMBLER_NPCS = {
    "npc_void_gambler": {
        "name": "The Void Gambler",
        "role": "gambler",
        "desc": "Sosok tanpa wajah yang duduk di depan meja melayang. Ia memegang tiga koin yang terus berubah bentuk.",
        "dialog_greetings": [
            "Emas hanyalah logam... Memori hanyalah beban. Mari kita buat mereka lebih menarik.",
            "Keberuntungan adalah satu-satunya hukum yang tersisa di Archivus.",
            "Berani mempertaruhkan segalanya demi kejayaan sesaat?"
        ],
        "game_type": "coin_toss", # Tebak koin
        "bet_options": [100, 500, 1000],
        "multiplier": 2.0,
        "win_chance": 0.45, # 45% peluang menang (House always wins slightly)
        "win_msg": "Koin berhenti di sisi yang kau pilih! 'Keberuntungan tersenyum padamu... untuk sekarang.'",
        "lose_msg": "Koin itu menghilang ke dalam kehampaan. 'Kehampaan meminta tumbal, dan kau memberikannya.'"
    },

    "npc_dice_master": {
        "name": "The Bone Roller",
        "role": "gambler",
        "desc": "Ia mengocok dadu yang terbuat dari tulang monster purba. Suara gemeretaknya terdengar seperti tawa kering.",
        "dialog_greetings": [
            "Angka tinggi membawa berkat, angka rendah membawa maut.",
            "Dadu tidak pernah berbohong, hanya harapanmu yang menipumu."
        ],
        "game_type": "dice_roll", # Tebak angka (Besar/Kecil)
        "bet_options": [200, 1000, 5000],
        "multiplier": 1.8,
        "win_chance": 0.50,
        "win_msg": "Dadu menunjukkan angka tinggi! Kau mendapatkan emas tambahan.",
        "lose_msg": "Dadu berguling ke angka rendah. Emasmu kini menjadi milik Sang Penjaga."
    }
}

# --- LOGIKA EKSEKUSI PERJUDIAN ---

def process_gambling_action(player, npc_id, bet_amount, user_input):
    """
    Logika utama untuk memproses taruhan pemain.
    Mengembalikan: (is_win, message, final_reward)
    """
    npc = GAMBLER_NPCS.get(npc_id)
    if not npc:
        return False, "❌ NPC tidak ditemukan.", 0

    if player['gold'] < bet_amount:
        return False, "❌ Emasmu tidak cukup untuk taruhan ini.", 0

    # Tentukan Kemenangan berdasarkan Win Chance di Database
    # random.random() menghasilkan angka 0.0 - 1.0
    is_win = random.random() < npc.get('win_chance', 0.5)
    
    # Faktor Kecurangan Tambahan (5% chance otomatis kalah)
    if random.random() < 0.05:
        is_win = False

    if is_win:
        reward = int(bet_amount * npc['multiplier'])
        player['gold'] += (reward - bet_amount) # Tambahkan selisih kemenangan
        return True, f"🎉 {npc['win_msg']}", reward
    else:
        player['gold'] -= bet_amount
        return False, f"💀 {npc['lose_msg']}", 0

def get_gambler_data(npc_id):
    """Mengambil data NPC penjudi berdasarkan ID."""
    return GAMBLER_NPCS.get(npc_id)

# --- LOGIKA MINI-GAMES (Fungsi Pembantu) ---

def play_coin_toss(user_choice):
    """Logika visual untuk Tebak Koin."""
    result = random.choice(['Heads', 'Tails'])
    return result

def play_dice_roll():
    """Logika visual untuk Dadu."""
    return random.randint(1, 6)
