# game/logic/job_manager.py

"""
JOB MANAGER - The Archivus
Menangani deteksi otomatis sinergi 8-Slot Equipment.
Jika kombinasi item sesuai, pemain akan mendapatkan Job/Class khusus.
"""

from database import update_player

# === MASTER JOB RECIPES (RESEP CLASS) ===
# Masukkan ID item yang akurat dari file weapons.py, armors.py, dll.
# Untuk class pengguna 2H (Two-Handed), slot 'artifact' / 'offhand' tidak perlu diisi.

JOB_DEFINITIONS = {
    "Blizzard Sovereign": {
        "weapon": "ice_staff",
        "armor": "blizzard_robe",
        "head": "circlet_of_north",
        "mask": "frozen_visage",
        "gloves": "weaver_mits",
        "boots": "permafrost_treads",
        "cloak": "frost_cloak",
        "artifact": "everfrost_shard"
    },
    "Dread Knight": {
        "weapon": "mountain_crusher",  # Senjata 2H
        "armor": "full_plate_mail",
        "head": "iron_helm",
        "mask": "ancient_mask",        # Contoh topeng pelengkap
        "gloves": "heavy_gauntlets",
        "boots": "steadfast_boots",
        "cloak": "frost_cloak"
        # Tanpa Artifact karena tangannya memegang 2H Greatsword
    },
    "Void Sage": {
        "weapon": "void_grimoire",     # Senjata 2H
        "armor": "blizzard_robe",
        "head": "weaver_hood",
        "mask": "ancient_mask",
        "gloves": "weaver_mits",
        "boots": "scout_boots",
        "cloak": "void_mantle"
    },
    "Holy Templar": {                  # --- BARU: KELAS UNTUK SKILL LIGHT / HEAL ---
        "weapon": "silver_longsword",  # Asumsi item 1H
        "armor": "templar_plate",
        "head": "iron_helm",
        "mask": "holy_visor",
        "gloves": "heavy_gauntlets",
        "boots": "steadfast_boots",
        "cloak": "radiant_cloak",
        "artifact": "sacred_tome"      # Atau bisa pakai 'shield' jika namanya beda
    },
    "Phantom Archer": {
        "weapon": "oak_shortbow",      # Senjata 2H
        "armor": "assassin_garb",
        "head": "leather_hood",
        "mask": "eagle_eye_monocle",
        "gloves": "archers_cold_grip",
        "boots": "scout_boots",
        "cloak": "mist_weaver_cloak"
    },
    "Blood Reaper": {
        "weapon": "crimson_hunger",    # Senjata 2H
        "armor": "assassin_garb",
        "head": "leather_hood",
        "mask": "plague_doctor_mask",
        "gloves": "heavy_gauntlets",
        "boots": "scout_boots",
        "cloak": "void_mantle"
    },
    "The Faceless": {
        "weapon": "hollow_husk",       # 1H Weapon
        "armor": "glacier_plate",
        "head": "iron_helm",
        "mask": "ancient_mask",
        "gloves": "heavy_gauntlets",
        "boots": "permafrost_treads",
        "cloak": "void_mantle",
        "artifact": "void_orb"
    }
    # Tambahkan sisa resep class lainnya di sini seiring bertambahnya item...
}

def detect_player_job(player):
    """
    Mengecek isi slot 'equipped' pemain.
    Mengembalikan: (job_name, achievement_message)
    """
    equipped = player.get('equipped', {})
    old_job = player.get('current_job', 'Novice Weaver')
    new_job = "Novice Weaver" # Default jika tidak ada yang cocok
    achievement_msg = None

    # Iterasi semua resep Job di database
    for job_name, requirements in JOB_DEFINITIONS.items():
        is_match = True
        
        # Cek setiap syarat slot dari resep Job tersebut
        for slot, required_item_id in requirements.items():
            # Jika item di slot tersebut tidak sama dengan syarat, berarti batal
            if equipped.get(slot) != required_item_id:
                is_match = False
                break
        
        # Jika semua syarat terpenuhi
        if is_match:
            new_job = job_name
            break

    # Jika terjadi perubahan Job (Naik pangkat atau turun pangkat)
    if new_job != old_job:
        player['current_job'] = new_job
        
        # Update database untuk menyimpan job baru
        update_player(player['user_id'], {'current_job': new_job})
        
        if new_job != "Novice Weaver":
            achievement_msg = (
                f"🌟 **SINERGI TERDETEKSI!** 🌟\n"
                f"Kombinasi perlengkapanmu memancarkan resonansi yang kuat.\n"
                f"Kau kini telah diakui sebagai seorang **{new_job}**!"
            )
        else:
            achievement_msg = (
                f"⚠️ **Sinergi Terputus.**\n"
                f"Kombinasi perlengkapanmu tidak lagi sempurna.\n"
                f"Kau kembali menjadi **Novice Weaver**."
            )

    return new_job, achievement_msg

def get_job_bonus(job_name):
    """
    Mengembalikan bonus stat spesifik berdasarkan Job yang aktif.
    Dipanggil di `game/logic/stats.py`.
    """
    bonuses = {
        "p_atk_mult": 1.0,
        "m_atk_mult": 1.0,
        "p_def_mult": 1.0,
        "speed_bonus": 0,
        "dodge_bonus": 0.0
    }

    if job_name == "Blizzard Sovereign":
        bonuses["m_atk_mult"] = 1.20  # +20% Magic Attack
    elif job_name == "Dread Knight":
        bonuses["p_def_mult"] = 1.25  # +25% Physical Defense
        bonuses["p_atk_mult"] = 1.10  # +10% Physical Attack
    elif job_name == "Holy Templar":  # --- BARU ---
        bonuses["p_def_mult"] = 1.20  # +20% Physical Defense
        bonuses["m_atk_mult"] = 1.15  # +15% Magic Attack (Untuk heal/skill light)
    elif job_name == "Phantom Archer":
        bonuses["speed_bonus"] = 5    # +5 Flat Speed
        bonuses["dodge_bonus"] = 0.10 # +10% Dodge
    elif job_name == "Void Sage":
        bonuses["m_atk_mult"] = 1.25
        bonuses["dodge_bonus"] = 0.05
    elif job_name == "Blood Reaper":
        bonuses["p_atk_mult"] = 1.15
        bonuses["speed_bonus"] = 2
    elif job_name == "The Faceless":
        bonuses["p_atk_mult"] = 1.10
        bonuses["m_atk_mult"] = 1.10
        bonuses["p_def_mult"] = 1.10

    return bonuses
