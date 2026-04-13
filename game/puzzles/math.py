"""
Logika Teka-teki Matematika dan Deret Angka - Versi Canggih
"""

import random

def generate_math_puzzle(tier: int):
    """Menghasilkan puzzle matematika dinamis berdasarkan tier (1-6)"""
    
    if tier == 1:  # Very Easy
        a = random.randint(15, 60)
        b = random.randint(5, 35)
        op = random.choice(['+', '-'])
        if op == '+':
            return f"Pecahkan distorsi numerik: {a} + {b} = ?", str(a + b)
        else:
            return f"Pecahkan distorsi numerik: {a + b} - {b} = ?", str(a)
    
    elif tier == 2:  # Easy
        a = random.randint(6, 15)
        b = random.randint(4, 12)
        return f"Sandi perkalian Archivus: {a} × {b} = ?", str(a * b)
    
    elif tier == 3:  # Medium
        a = random.randint(4, 9)
        b = random.randint(4, 9)
        c = random.randint(20, 80)
        return f"Uraikan kode matriks: ({a} × {b}) + {c} = ?", str((a * b) + c)
    
    elif tier == 4:  # Hard
        a = random.randint(5, 12)
        b = random.randint(3, 8)
        c = random.randint(10, 40)
        return f"Persamaan kuantum: {a} × Y + {c} = {a * b + c}. Berapa nilai Y?", str(b)
    
    elif tier == 5:  # Very Hard
        a = random.randint(3, 7)
        b = random.randint(2, 6)
        c = random.randint(5, 15)
        d = random.randint(10, 50)
        # (a × Y) + b = c × d  →  Y = ((c*d) - b) / a
        right = c * d
        answer = (right - b) // a   # pastikan hasil integer
        return f"Anomali dimensi: ({a} × Y) + {b} = {c} × {d}. Berapa Y?", str(answer)
    
    else:  # Tier 6 - Expert
        # Persamaan dua variabel sederhana (bentuk linier)
        x = random.randint(2, 6)
        y = random.randint(3, 8)
        a = random.randint(2, 5)
        b = random.randint(2, 5)
        total = a * x + b * y
        return (f"Persamaan dual Archivus:\n"
                f"{a}X + {b}Y = {total}\n"
                f"Diketahui X = {x}, berapa nilai Y?"), str(y)


def generate_sequence_puzzle(tier: int):
    """Menghasilkan puzzle deret angka dengan tingkat kesulitan berbeda"""
    
    if tier <= 2:  # Easy - Aritmatika
        start = random.randint(5, 20)
        step = random.randint(3, 7)
        seq = [start + (i * step) for i in range(5)]
        answer = start + (5 * step)
        return f"Lengkapi deret memori: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, {seq[4]}, ... ?", str(answer)
    
    elif tier <= 4:  # Medium-Hard - Geometri / Pangkat
        start = random.randint(2, 5)
        ratio = random.randint(2, 4)
        seq = [start * (ratio ** i) for i in range(5)]
        answer = start * (ratio ** 5)
        return f"Pola eksponensial kuno: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, {seq[4]}, ... ?", str(answer)
    
    else:  # Tier 5-6 - Fibonacci-like + variasi
        a = random.randint(3, 12)
        b = random.randint(5, 18)
        seq = [a, b]
        for _ in range(4):
            seq.append(seq[-1] + seq[-2])
        
        # Tambah sedikit twist (kadang dikali 2 atau dikurangi 1)
        twist = random.choice([0, 1, 2])
        if twist == 1:
            seq[-1] += 1
        elif twist == 2:
            seq[-1] *= 2
            
        answer = seq[-1] + seq[-2]
        return f"Sandi Kuno Archivus (Deret Quantum): {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, {seq[4]}, ... ?", str(answer)


# === Fungsi Helper untuk Generate Multiple Puzzle ===
def generate_puzzle_set(count: int = 5, min_tier: int = 1, max_tier: int = 6):
    """Generate beberapa puzzle sekaligus dengan tier acak"""
    puzzles = []
    for i in range(count):
        tier = random.randint(min_tier, max_tier)
        if random.random() < 0.5:
            q, ans = generate_math_puzzle(tier)
            tipe = "Matematika"
        else:
            q, ans = generate_sequence_puzzle(tier)
            tipe = "Deret Angka"
        
        puzzles.append({
            "no": i + 1,
            "tier": tier,
            "tipe": tipe,
            "pertanyaan": q,
            "jawaban": ans
        })
    return puzzles


# Contoh penggunaan
if __name__ == "__main__":
    print("=== TEKA-TEKI ARCHIVUS - Versi Canggih ===\n")
    
    # Generate 1 puzzle tier tinggi
    q, a = generate_math_puzzle(6)
    print("Puzzle Tier 6:")
    print(q)
    print(f"Jawaban: {a}\n")
    
    # Generate set puzzle
    print("=== Set Puzzle Random (Tier 3-6) ===")
    puzzle_set = generate_puzzle_set(count=6, min_tier=3, max_tier=6)
    
    for p in puzzle_set:
        print(f"{p['no']}. [{p['tipe']}] Tier {p['tier']}")
        print(p['pertanyaan'])
        print(f"Jawaban: {p['jawaban']}")
        print("-" * 60)
