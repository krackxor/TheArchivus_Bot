def calculate_total_stats(player):
    """
    Kalkulasi cerdas untuk semua stat berdasarkan 8 slot equipment.
    Memperhitungkan Grip 2H, Durability, dan Weight Penalty.
    """
    # 1. Inisialisasi Stat Dasar (dari level/base player)
    stats = {
        "p_atk": player.get('base_p_atk', 10),
        "m_atk": player.get('base_m_atk', 10),
        "p_def": player.get('base_p_def', 5),
        "m_def": player.get('base_m_def', 5),
        "speed": player.get('base_speed', 10),
        "dodge": 0.50, # Base 50%
        "total_weight": 0
    }

    equipped = player.get('equipped', {})
    weapon = get_item(equipped.get('weapon'))
    artifact = get_item(equipped.get('artifact'))

    # 2. Cek Aturan Grip Senjata
    is_two_handed = weapon.get('grip') == '2H' if weapon else False

    # 3. Iterasi Semua Slot untuk Menghitung Stat & Berat
    for slot, item_id in equipped.items():
        item = get_item(item_id)
        if not item:
            continue

        # LOGIKA KHUSUS ARTIFACT: Diabaikan statnya jika senjata 2H
        # Kecuali item tersebut adalah "Cursed" atau "Passive Bone" yang tidak butuh tangan
        if slot == 'artifact' and is_two_handed:
            continue 

        # PENALTI DURABILITY: Jika barang rusak (0), bonus stat hilang 80%
        durability_mult = 1.0
        if item.get('durability', 1) <= 0:
            durability_mult = 0.2
            # Senjata rusak sangat berat karena tumpul/patah
            stats['total_weight'] += item.get('weight', 0) * 1.5 
        else:
            stats['total_weight'] += item.get('weight', 0)

        # Tambahkan Stat ke Total (Dikali durability multiplier)
        stats['p_atk'] += item.get('p_atk', 0) * durability_mult
        stats['m_atk'] += item.get('m_atk', 0) * durability_mult
        stats['p_def'] += item.get('p_def', 0) * durability_mult
        stats['m_def'] += item.get('m_def', 0) * durability_mult
        stats['speed'] += item.get('speed', 0) * durability_mult

    # 4. LOGIKA BALANCE: Weight vs Dodge/Speed
    # Rumus: Setiap 5 unit berat mengurangi 2% Dodge dan 1 poin Speed
    weight_penalty = stats['total_weight'] // 5
    
    stats['dodge'] = max(0.05, stats['dodge'] - (weight_penalty * 0.02))
    stats['speed'] = max(1, stats['speed'] - weight_penalty)

    # 5. BONUS SET JOB (Jika 8 slot terpenuhi & Akurat)
    # Ini fungsi yang kita buat sebelumnya untuk mendeteksi Job
    from game.items.manager import detect_player_job
    job_name, _ = detect_player_job(player)
    
    if job_name != "Novice Weaver":
        # Memberikan bonus 10% pada stat utama Job
        if "Archer" in job_name or "Assassin" in job_name:
            stats['speed'] += 5
            stats['dodge'] += 0.05
        elif "Knight" in job_name or "Warden" in job_name:
            stats['p_def'] = int(stats['p_def'] * 1.15)
        elif "Sage" in job_name or "Sovereign" in job_name:
            stats['m_atk'] = int(stats['m_atk'] * 1.15)

    return stats
