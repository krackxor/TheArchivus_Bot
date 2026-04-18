# game/systems/progression.py

"""
Sistem Kenaikan Level dan Atribut (Progression System)
Mengatur kurva EXP, pemulihan saat naik level, dan alokasi Stat Point (SP).
"""

from database import get_player, update_player, add_history

def calculate_max_exp(level):
    """
    Rumus kurva EXP. Semakin tinggi level, semakin eksponensial kebutuhannya.
    Lv 1 -> 100 EXP
    Lv 2 -> 282 EXP
    Lv 3 -> 519 EXP
    (Menggunakan basis 100 agar seimbang dengan reward monster)
    """
    return int(100 * (level ** 1.5))

def add_exp(user_id, amount):
    """
    Menambahkan EXP ke pemain dan mengecek apakah mereka naik level.
    Bisa memicu level up berkali-kali jika EXP yang didapat sangat besar (misal dari Bos).
    """
    p = get_player(user_id)
    current_exp = p.get('exp', 0) + amount
    current_level = p.get('level', 1)
    max_exp = calculate_max_exp(current_level)

    leveled_up = False
    stat_points_gained = 0
    level_up_messages = []

    # Pakai while-loop berjaga-jaga jika EXP melimpah dan naik >1 level sekaligus
    while current_exp >= max_exp:
        leveled_up = True
        current_exp -= max_exp
        current_level += 1
        
        # Bonus Atribut Otomatis per Level
        p['max_hp'] = p.get('max_hp', 100) + 15
        p['max_mp'] = p.get('max_mp', 50) + 5
        p['max_energy'] = p.get('max_energy', 100) + 5

        # Hadiah Level Up: HP, MP, dan Energi pulih 100%
        p['hp'] = p['max_hp']
        p['mp'] = p['max_mp']
        p['energy'] = p['max_energy']

        # Berikan 3 Stat Point setiap naik level
        stat_points_gained += 3
        
        level_up_messages.append(
            f"🔼 **LEVEL UP!** Kau mencapai Level {current_level}!\n"
            f"❤️ Max HP meningkat!\n"
            f"✨ Kau mendapatkan 3 Stat Point (SP) baru."
        )
        # Update max_exp untuk level berikutnya dalam loop
        max_exp = calculate_max_exp(current_level)

    # Menyiapkan data untuk disimpan
    updates = {
        'exp': current_exp,
        'level': current_level,
        'exp_needed': max_exp # Simpan cache agar main.py tidak perlu hitung ulang
    }

    if leveled_up:
        updates.update({
            'max_hp': p['max_hp'], 'hp': p['hp'],
            'max_mp': p['max_mp'], 'mp': p['mp'],
            'max_energy': p['max_energy'], 'energy': p['energy'],
            'stat_points': p.get('stat_points', 0) + stat_points_gained
        })
        add_history(user_id, f"Mencapai Level {current_level}. Sesuatu di dalam dirimu terasa semakin buas.")

    # Simpan ke database
    update_player(user_id, updates)

    return leveled_up, current_level, "\n\n".join(level_up_messages)

def allocate_stat_point(user_id, stat_type):
    """
    Menggunakan 1 Stat Point (SP) untuk menaikkan Base Stat permanen pemain.
    """
    p = get_player(user_id)
    sp = p.get('stat_points', 0)

    if sp <= 0:
        return False, "❌ Kau tidak memiliki Stat Point (SP) yang tersisa."

    # Mapping stat yang boleh dinaikkan dan jumlah pertumbuhannya per 1 SP
    valid_stats = {
        "p_atk": ("base_p_atk", "Physical Attack", 2),
        "m_atk": ("base_m_atk", "Magic Attack", 2),
        "p_def": ("base_p_def", "Physical Defense", 2),
        "m_def": ("base_m_def", "Magic Defense", 2),
        "speed": ("base_speed", "Speed", 1) # Speed sangat berharga, naiknya pelan
    }

    if stat_type not in valid_stats:
        return False, "❌ Atribut tidak dikenali oleh sistem."

    db_key, stat_name, increment = valid_stats[stat_type]

    # Ambil base stat saat ini (default 10) lalu tambahkan
    new_val = p.get(db_key, 10) + increment
    
    # Update ke database: Kurangi 1 SP, Naikkan stat
    update_player(user_id, {db_key: new_val, 'stat_points': sp - 1})

    return True, f"✨ Kau mengalirkan jiwamu ke dalam {stat_name}. Atribut ini meningkat menjadi **{new_val}**!"
