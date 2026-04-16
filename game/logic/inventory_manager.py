# game/logic/inventory_manager.py

from game.items import get_item
from game.logic.stats import calculate_total_stats
from game.logic.job_manager import detect_player_job # Diperbarui ke jalur yang benar

def equip_item(player, item_id):
    """
    Sistem cerdas untuk memasang item. 
    Menangani konflik 1H/2H, update Job, dan kalkulasi stat otomatis.
    """
    item = get_item(item_id)
    if not item:
        return False, "❌ Item tidak ditemukan di database."

    if item_id not in player.get('inventory', []):
        return False, "❌ Kau tidak memiliki item ini di tasmu."

    slot = item.get('type') # 'weapon', 'armor', 'artifact', dll.
    equipped = player.get('equipped', {})
    
    warning_msg = ""

    # --- LOGIKA CERDAS 1: KONFLIK 2-HANDED (2H) ---
    if slot == 'weapon':
        # Jika memasang senjata 2H, otomatis lepas Artifact
        if item.get('grip') == '2H':
            if equipped.get('artifact'):
                unequip_item(player, 'artifact')
                warning_msg = f"⚠️ **{item['name']}** terlalu berat dan butuh dua tangan. Artifact milikmu otomatis dilepas.\n"
    
    elif slot == 'artifact':
        # Jika mencoba pasang Artifact tapi senjata saat ini adalah 2H
        weapon_id = equipped.get('weapon')
        if weapon_id:
            weapon = get_item(weapon_id)
            if weapon and weapon.get('grip') == '2H':
                return False, f"❌ Tanganmu penuh! Lepas **{weapon['name']}** terlebih dahulu jika ingin memakai Artifact."

    # --- LOGIKA CERDAS 2: PROSES EQUIP ---
    # Jika slot sudah terisi, pindahkan item lama kembali ke inventory
    old_item_id = equipped.get(slot)
    if old_item_id:
        player['inventory'].append(old_item_id)

    # Pasang item baru
    equipped[slot] = item_id
    player['inventory'].remove(item_id)
    player['equipped'] = equipped

    # --- LOGIKA CERDAS 3: SINERGI & JOB CHECK ---
    # Setiap kali ganti equipment, cek apakah Job berubah
    job_name, achievement_msg = detect_player_job(player)
    
    # Recalculate stats agar perubahan langsung terasa
    player['stats'] = calculate_total_stats(player)

    status_msg = f"✅ **{item['name']}** berhasil dipasang!"
    
    # Gabungkan semua pesan notifikasi (Warning -> Status -> Achievement)
    if warning_msg:
        status_msg = warning_msg + status_msg
        
    if achievement_msg:
        status_msg += f"\n\n{achievement_msg}"
    
    return True, status_msg

def unequip_item(player, slot):
    """Melepas item dari slot tertentu secara aman."""
    equipped = player.get('equipped', {})
    item_id = equipped.get(slot)

    if not item_id:
        return False, f"❌ Slot {slot} memang sudah kosong."

    item = get_item(item_id)
    item_name = item['name'] if item else slot

    # Pindahkan ke inventory
    player['inventory'].append(item_id)
    del equipped[slot]
    player['equipped'] = equipped

    # Reset Job & Stats
    detect_player_job(player)
    player['stats'] = calculate_total_stats(player)

    return True, f"📦 **{item_name}** telah dilepas dan dimasukkan ke dalam tas."
