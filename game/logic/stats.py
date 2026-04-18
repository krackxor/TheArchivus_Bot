# game/logic/stats.py

from game.items import get_item
from game.logic.job_manager import get_job_bonus

def calculate_total_stats(player):
    """
    Kalkulasi cerdas untuk semua stat berdasarkan 8 slot equipment.
    Memperhitungkan Grip 2H, Durability, Weight Penalty, Job Bonus, 
    Active Effects, dan Permanent Bonus (Pact/Altar).
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

    # --- TAMBAHAN: Bonus Permanen dari Kontrak Darah (Pacts/Altar) ---
    perm_bonus = player.get('permanent_bonus', {})
    for stat_key, stat_val in perm_bonus.items():
        if stat_key in stats:
            stats[stat_key] += stat_val
    # -----------------------------------------------------------------

    equipped = player.get('equipped', {})
    weapon_id = equipped.get('weapon')
    offhand_id = equipped.get('artifact') # Dulu namanya artifact, sekarang dipakai sbg offhand di beberapa kasus
    weapon = get_item(weapon_id)
    
    # Ambil data durabilitas dinamis pemain dari database
    durability_data = player.get('equipment_durability', {})

    # 2. Cek Aturan Grip Senjata
    is_two_handed = weapon.get('grip') == '2H' if weapon else False

    # 3. Iterasi Semua Slot untuk Menghitung Stat & Berat
    for slot, item_id in equipped.items():
        item = get_item(item_id)
        if not item:
            continue

        # LOGIKA KHUSUS ARTIFACT/OFFHAND: Diabaikan statnya jika senjata 2H
        if slot == 'artifact' and is_two_handed:
            continue 

        # PENALTI DURABILITY: Jika barang rusak (0), bonus stat hilang 80%
        # Mengambil durabilitas dari record pemain, bukan data statis item
        current_durability = durability_data.get(slot, 50)
        
        durability_mult = 1.0
        if current_durability <= 0:
            durability_mult = 0.2
            # Senjata rusak terasa lebih berat/beban karena tumpul/patah
            stats['total_weight'] += item.get('weight', 0) * 1.5 
        else:
            stats['total_weight'] += item.get('weight', 0)

        # Tambahkan Stat ke Total (Dikali durability multiplier)
        stats['p_atk'] += int(item.get('p_atk', 0) * durability_mult)
        stats['m_atk'] += int(item.get('m_atk', 0) * durability_mult)
        stats['p_def'] += int(item.get('p_def', 0) * durability_mult)
        stats['m_def'] += int(item.get('m_def', 0) * durability_mult)
        stats['speed'] += int(item.get('speed', 0) * durability_mult)
        
        # Tambahan: Jika item (misal jubah/artefak) memberi bonus dodge
        if 'dodge' in item:
            stats['dodge'] += (item['dodge'] * durability_mult)

    # 4. LOGIKA BALANCE: Weight vs Dodge/Speed
    weight_penalty = stats['total_weight'] // 5
    
    stats['dodge'] = max(0.05, stats['dodge'] - (weight_penalty * 0.02))
    stats['speed'] = max(1, stats['speed'] - weight_penalty)

    # 5. BONUS SET JOB (Menggunakan job_manager.py)
    job_name = player.get('current_job', 'Novice Weaver')
    job_bonuses = get_job_bonus(job_name)
    
    # Terapkan multiplier stat dari Job
    stats['p_atk'] = int(stats['p_atk'] * job_bonuses['p_atk_mult'])
    stats['m_atk'] = int(stats['m_atk'] * job_bonuses['m_atk_mult'])
    stats['p_def'] = int(stats['p_def'] * job_bonuses['p_def_mult'])
    
    # Tambahkan bonus flat untuk speed dan dodge
    stats['speed'] += job_bonuses['speed_bonus']
    stats['dodge'] += job_bonuses['dodge_bonus']

    # === 6. LOGIKA BUFF/DEBUFF STAT SEMENTARA ===
    # Memproses efek dari ramuan atau sihir yang tersimpan di player
    active_effects = player.get('active_effects', [])
    for effect in active_effects:
        eff_type = effect.get('type') # misal: 'atk_buff', 'def_debuff'
        value = effect.get('value', 0)
        
        if eff_type == 'atk_buff':
            stats['p_atk'] += value
            stats['m_atk'] += value
        elif eff_type == 'def_buff':
            stats['p_def'] += value
            stats['m_def'] += value
        elif eff_type == 'atk_debuff':
            stats['p_atk'] = max(1, stats['p_atk'] - value)
            stats['m_atk'] = max(1, stats['m_atk'] - value)
        elif eff_type == 'def_debuff':
            stats['p_def'] = max(1, stats['p_def'] - value)
            stats['m_def'] = max(1, stats['m_def'] - value)
        elif eff_type == 'speed_debuff':
            stats['speed'] = max(1, stats['speed'] - value)
        elif eff_type == 'dodge_buff':
            stats['dodge'] += value
    
    # Cap maksimal untuk dodge agar tidak bisa 100% menghindar (maksimal 90%)
    stats['dodge'] = min(0.90, stats['dodge'])

    # Elemen utama player dan tipe serangan diambil dari senjata
    if weapon:
        stats['element'] = weapon.get('element', 'none')
        stats['attack_type'] = 'magic' if weapon.get('m_atk', 0) > weapon.get('p_atk', 0) else 'physical'
    else:
        stats['element'] = 'none'
        stats['attack_type'] = 'physical'

    # === 7. DETEKSI TIPE SENJATA (UNTUK SISTEM SKILL) ===
    # Ubah ID ke string huruf kecil dan amankan jika None
    wep_id_str = str(weapon_id).lower() if weapon_id else ""
    off_id_str = str(offhand_id).lower() if offhand_id else ""
    
    # Deteksi Senjata Utama (Weapon)
    stats['weapon_type'] = "unarmed"
    if any(k in wep_id_str for k in ["dagger", "knife", "shiv"]): 
        stats['weapon_type'] = "dagger"
    elif any(k in wep_id_str for k in ["bow", "crossbow"]): 
        stats['weapon_type'] = "bow"
    elif any(k in wep_id_str for k in ["dual", "twin"]): 
        stats['weapon_type'] = "dual_swords"
    elif any(k in wep_id_str for k in ["staff", "wand", "scepter"]): 
        stats['weapon_type'] = "staff"
    elif any(k in wep_id_str for k in ["sword", "blade", "katana", "claymore"]): 
        stats['weapon_type'] = "sword"
    
    # Deteksi Senjata Kiri/Tameng (Offhand/Artifact)
    stats['offhand_type'] = "none"
    if any(k in off_id_str for k in ["shield", "buckler", "aegis"]): 
        stats['offhand_type'] = "shield"

    return stats
