# game/puzzles/math.py

"""
Logika Teka-teki Matematika dan Deret Angka - The Archivus
Modul untuk menghasilkan gangguan numerik dan sandi pola angka.
"""

import random

def generate_math_puzzle(tier):
    """Menghasilkan kombinasi puzzle matematika dinamis berdasarkan tier."""
    if tier <= 1:
        # Penjumlahan / Pengurangan sederhana
        a = random.randint(10, 50)
        b = random.randint(1, 30)
        op = random.choice(['+', '-'])
        if op == '-':
            num1, num2 = max(a, b), min(a, b)
            return f"Pecahkan distorsi numerik ini: {num1} - {num2} = ?", str(num1 - num2)
        else:
            return f"Pecahkan distorsi numerik ini: {a} + {b} = ?", str(a + b)
        
    elif tier == 2:
        # Perkalian dasar
        a = random.randint(4, 12)
        b = random.randint(3, 9)
        return f"Sandi perkalian Archivus: {a} x {b} = ?", str(a * b)
        
    elif tier == 3:
        # Campuran (Perkalian dan Penjumlahan)
        a = random.randint(3, 8)
        b = random.randint(3, 8)
        c = random.randint(10, 50)
        return f"Uraikan kode matriks ini: ({a} x {b}) + {c} = ?", str((a * b) + c)
        
    else:
        # Tier 4 dan 5 (Aljabar sederhana mencari nilai Y)
        a = random.randint(5, 12)
        x = random.randint(4, 12) 
        b = a * x
        return f"Pecahkan anomali persamaan ini: {a} x Y = {b}. Berapa nilai Y?", str(x)

def generate_sequence_puzzle(tier):
    """Menghasilkan kombinasi deret angka (sequence)."""
    start = random.randint(1, 10)
    if tier <= 2:
        # Deret aritmatika
        step = random.randint(2, 6)
        seq = [start + (i * step) for i in range(4)]
        answer = str(start + (4 * step))
        return f"Lengkapi deret memori ini: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ... ?", answer
        
    elif tier <= 4:
        # Deret geometri
        step = random.randint(2, 3) # Dikurangi agar angka tidak terlalu raksasa
        seq = [start * (step ** i) for i in range(4)]
        answer = str(start * (step ** 4))
        return f"Pecahkan pola eksponensial ini: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ... ?", answer
        
    else:
        # Fibonacci-style
        seq = [start, start + random.randint(1, 5)]
        for i in range(2, 5):
            seq.append(seq[-1] + seq[-2])
        answer = str(seq[-1] + seq[-2])
        return f"Sandi Kuno Archivus (Deret): {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, {seq[4]}, ... ?", answer

def get_puzzle(tier=None):
    """
    Fungsi utama untuk dipanggil oleh manager.py.
    Memilih secara acak antara hitungan matematika atau deret angka.
    """
    if tier is None:
        tier = random.randint(1, 5)
        
    # Kocok antara tipe Math atau Sequence
    if random.choice(["math", "seq"]) == "math":
        q, a = generate_math_puzzle(tier)
    else:
        q, a = generate_sequence_puzzle(tier)
        
    return {
        "question": f"🔢 **NUMERICAL ANOMALY**\n_{q}_",
        "answer": a.strip().lower()
    }
