"""
Logika Teka-teki Matematika dan Deret Angka
"""

import random

def generate_math_puzzle(tier):
    """Menghasilkan kombinasi puzzle matematika dinamis berdasarkan tier."""
    if tier == 1:
        # Penjumlahan / Pengurangan sederhana
        a = random.randint(10, 50)
        b = random.randint(1, 30)
        op = random.choice(['+', '-'])
        answer = str(a + b) if op == '+' else str(max(a, b) - min(a, b)) 
        real_q = f"{max(a, b)} - {min(a, b)}" if op == '-' else f"{a} + {b}"
        return f"Pecahkan distorsi numerik ini: {real_q} = ?", answer
        
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
        # Deret aritmatika (tambah-tambahan tetap)
        step = random.randint(2, 6)
        seq = [start + (i * step) for i in range(4)]
        answer = str(start + (4 * step))
        return f"Lengkapi deret memori ini: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ... ?", answer
        
    elif tier <= 4:
        # Deret geometri (perkalian tetap eksponensial)
        step = random.randint(2, 4)
        seq = [start * (step ** i) for i in range(4)]
        answer = str(start * (step ** 4))
        return f"Pecahkan pola eksponensial ini: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ... ?", answer
        
    else:
        # Deret ala Fibonacci (angka berikutnya adalah jumlah 2 angka sebelumnya)
        seq = [start, start + random.randint(1, 5)]
        for i in range(2, 5):
            seq.append(seq[-1] + seq[-2])
        answer = str(seq[-1] + seq[-2])
        return f"Sandi Kuno Archivus (Deret): {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, {seq[4]}, ... ?", answer
