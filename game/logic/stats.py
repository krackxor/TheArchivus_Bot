# game/logic/stats.py

"""
STATS CALCULATOR - The Archivus
Kalkulasi cerdas untuk semua stat berdasarkan 8 slot equipment.
Memperhitungkan Grip 2H, Durability, Weight Penalty, Job Bonus, 
Active Effects, dan Permanent Bonus (Pact/Altar).
"""

from game.items import get_item
import random

# Peringatan: Pastikan file game/logic/job_manager.py sudah dibuat!
try:
    from game.logic.job_manager import get_job_bonus
except ImportError:
    # Fallback sementara jika job_manager belum diimplementasi
    def get_job_bonus(job_name):
        return {"p_atk_mult": 1.0, "m_atk_mult": 1.0, "p_def_mult": 1.0, "speed_bonus": 0, "dodge_bonus": 0.0}

def calculate_total_stats(player):
    # 1. Inisialisasi Stat Dasar (dari level/base player)
    stats = {
        "p_atk": player.get('base_p_atk', 10),
        "m_atk": player.get('base_m_atk', 10),
        "p_def": player.get('base_p_def', 5),
        "m_def": player.get('base_m_def', 5),
        "speed": player.get('base_speed', 10),
        "dodge": 0.50, # Base 50%
        "total_weight": 0,
        "crit_rate": 5,
        "crit_dmg": 150
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
    weapon = get_item(weapon_id) if weapon_id else None
    
    # Ambil data durabilitas dinamis pemain dari database
    durability_data = player.get('equipment_durability', {})

    # 2. Cek Aturan Grip Senjata
    is_two_handed = weapon.get('grip') == '2H' if weapon else False

    # 3. Iterasi Semua Slot untuk Menghitung Stat & Berat
    for slot, item_id in equipped.items():
        if not item_id: continue
        item = get_item(item_id)
        if not item: continue

        # LOGIKA KHUSUS ARTIFACT/OFFHAND: Diabaikan statnya jika senjata 2H
        if slot == 'artifact' and is_two_handed:
            continue 

        # PENALTI DURABILITY: Jika barang rusak (0), bonus stat hilang 80%
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
        
        # Tambahan: Jika item (misal jubah/artefak) memberi bonus khusus
        if 'dodge' in item:
            stats['dodge'] += (item['dodge'] * durability_mult)
        if 'crit_rate' in item:
            stats['crit_rate'] += (item['crit_rate'] * durability_mult)

    # 4. LOGIKA BALANCE: Weight vs Dodge/Speed
    weight_penalty = int(stats['total_weight']) // 5
    
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
    wep_id_str = str(weapon_id).lower() if weapon_id else ""
    off_id_str = str(offhand_id).lower() if offhand_id else ""
    
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
    
    stats['offhand_type'] = "none"
    if any(k in off_id_str for k in ["shield", "buckler", "aegis"]): 
        stats['offhand_type'] = "shield"

    return stats


def calculate_damage(attacker_stats: dict, defender_stats: dict, is_magic: bool = False, skill_multiplier: float = 1.0) -> tuple:
    """
    Fungsi utilitas untuk menghitung damage akhir dalam pertarungan.
    Mengembalikan: (final_damage: int, is_crit: bool, is_dodged: bool)
    """
    # 1. Cek Dodge (Menghindar)
    dodge_chance = defender_stats.get('dodge', 0.05)
    # Konversi float ke persen (misal 0.50 -> 50%)
    if isinstance(dodge_chance, float):
        dodge_chance = int(dodge_chance * 100)
        
    if random.randint(1, 100) <= dodge_chance:
        return 0, False, True # Damage 0, tidak crit, BERHASIL menghindar

    # 2. Tentukan Attack dan Defense
    if is_magic or attacker_stats.get('attack_type') == 'magic':
        atk = attacker_stats.get('m_atk', 10)
        defense = defender_stats.get('m_def', 5)
    else:
        atk = attacker_stats.get('p_atk', 10)
        defense = defender_stats.get('p_def', 5)
        
    # Variansi Damage (± 10%) agar damage dinamis
    variance = random.uniform(0.9, 1.1)
    
    # Hitung damage kotor
    raw_damage = (atk * skill_multiplier) - defense
    
    # 3. Cek Critical Hit
    crit_rate = attacker_stats.get('crit_rate', 5)
    is_crit = random.randint(1, 100) <= crit_rate
    
    if is_crit:
        crit_mult = attacker_stats.get('crit_dmg', 150) / 100.0
        raw_damage *= crit_mult
        
    # Final Kalkulasi (Minimal damage = 1 jika tidak dodge)
    final_damage = int(max(1, raw_damage * variance))
    
    return final_damage, is_crit, False
