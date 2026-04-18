# game/data/environment/deadly.py

"""
Deadly Terrains Database - The Archivus
Berisi bahaya lingkungan maut yang membutuhkan Stat Check untuk dilewati.
Mekanik: Sukses (Selamat) vs Gagal (Damage Besar / Mati).
"""

import random

DEADLY_EVENTS = {
    "deadly_abyssal_chasm": {
        "name": "Jurang Kehampaan",
        "type": "deadly",
        "desc": "Jalan terputus oleh celah raksasa yang tak terlihat dasarnya. Angin dingin berhembus dari bawah.",
        "check_stat": "dodge", # Menggunakan stat Dodge untuk melompat
        "difficulty": 0.45,    # Butuh roll di atas 0.45 (setelah ditambah stat bonus)
        "success_msg": "🤸 **BERHASIL!** Dengan lompatan akrobatik, kau mendarat di sisi seberang dengan selamat.",
        "fail_msg": "💀 **JATUH!** Kau kehilangan pijakan dan terperosok ke dalam kegelapan. Tubuhmu menghantam batu tajam di bawah.",
        "fail_penalty": {
            "hp_percent": 0.8, # Kehilangan 80% HP saat ini
            "energy_loss": 50,
            "can_kill": True   # Jika HP rendah, pemain bisa langsung mati
        }
    },

    "deadly_spike_trap": {
        "name": "Lantai Berduri Kuno",
        "type": "deadly",
        "desc": "Ubin di depanmu tampak goyah. Kau melihat noda darah kering di sela-sela lubang kecil di lantai.",
        "check_stat": "speed",
        "difficulty": 0.55,
        "success_msg": "👟 **CEPAT!** Kau berlari melintasi ruangan sebelum mekanisme duri sempat menusukmu.",
        "fail_msg": "🩸 **TERTUSUK!** Duri besi berkarat muncul dari lantai dan merobek kakimu.",
        "fail_penalty": {
            "hp_loss": 40,
            "status": "bleed", # Memberikan status pendarahan
            "energy_loss": 20
        }
    },

    "deadly_falling_rubble": {
        "name": "Reruntuhan Langit-langit",
        "type": "deadly",
        "desc": "Struktur bangunan di sini sudah sangat rapuh. Getaran langkahmu membuat langit-langit mulai runtuh.",
        "check_stat": "luck",
        "difficulty": 0.60,
        "success_msg": "🍀 **BERUNTUNG.** Sebongkah batu besar jatuh tepat di sampingmu. Kau selamat tanpa goresan.",
        "fail_msg": "🧱 **TERTIMPA!** Reruntuhan batu menghantam pundakmu dengan telak.",
        "fail_penalty": {
            "hp_loss": 50,
            "energy_loss": 30
        }
    }
}

# --- LOGIKA INTERAKSI DEADLY EVENT ---

def process_deadly_interaction(player, event_id):
    """
    Memproses seluruh kejadian bahaya maut (Stat Check + Penalti).
    Mengembalikan: (is_success, message)
    """
    event = get_deadly_data(event_id)
    if not event:
        return False, "❌ Kejadian tidak ditemukan."
    
    # Ambil stat pemain yang dibutuhkan untuk pengecekan
    check_stat = event['check_stat']
    player_stat_val = player.get('stats', {}).get(check_stat, 0)
    
    # Lakukan pengecekan keberhasilan
    success = calculate_check_result(player_stat_val, event['difficulty'])
    
    if success:
        return True, event['success_msg']
    else:
        penalty = event['fail_penalty']
        
        # Terapkan penalti HP (Bisa berdasarkan persentase atau nilai tetap)
        if 'hp_percent' in penalty:
            loss = int(player.get('hp', 0) * penalty['hp_percent'])
            player['hp'] -= loss
        elif 'hp_loss' in penalty:
            player['hp'] -= penalty['hp_loss']
            
        # Terapkan penalti Energy
        if 'energy_loss' in penalty:
            player['energy'] = max(0, player.get('energy', 100) - penalty['energy_loss'])
            
        # Terapkan efek status jika gagal
        if 'status' in penalty:
            if 'status_effects' not in player:
                player['status_effects'] = []
            player['status_effects'].append(penalty['status'])
            
        # Pastikan HP tidak negatif kecuali jika bisa membunuh
        player['hp'] = max(0, player['hp'])
        
        # Cek kondisi kematian pemain
        if player['hp'] <= 0 and penalty.get('can_kill'):
            return False, f"{event['fail_msg']} (💀 Kamu tewas dalam kejadian ini!)"
            
        return False, f"{event['fail_msg']} (HP -{penalty.get('hp_loss', '??')})"

def get_deadly_data(event_id):
    """Mengambil data bahaya maut berdasarkan ID."""
    return DEADLY_EVENTS.get(event_id)

def get_all_deadly():
    """Mengambil semua daftar bahaya maut."""
    return DEADLY_EVENTS

def calculate_check_result(player_stat, difficulty):
    """
    Logika Stat Check: Roll acak (0-1) + bonus stat vs difficulty.
    """
    # Stat pemain memberikan bonus 50% dari nilainya ke roll acak
    roll = random.random() + (player_stat * 0.5)
    return roll >= difficulty
