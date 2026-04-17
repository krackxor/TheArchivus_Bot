# game/logic/inventory_manager.py

from game.items import get_item
from game.logic.stats import calculate_total_stats
from game.logic.job_manager import detect_player_job

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
    detect_player_job(player)
    
    # Recalculate stats agar perubahan langsung terasa
    player['stats'] = calculate_total_stats(player)

    status_msg = f"✅ **{item['name']}** berhasil dipasang!"
    
    if warning_msg:
        status_msg = warning_msg + status_msg
    
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

# === SISTEM PANDAI BESI (REPAIR) ===

def process_repair_all(player):
    """
    Menghitung biaya dan memperbaiki semua item yang terpasang ke 100%.
    Biaya: 10 Gold per 1 poin durabilitas yang hilang.
    Maksimal durabilitas: 50
    """
    equipped = player.get('equipped', {})
    durability_data = player.get('equipment_durability', {})
    total_cost = 0
    items_repaired = 0
    
    # Iterasi setiap item yang sedang dipakai
    for slot, item_id in equipped.items():
        # Dapatkan durabilitas saat ini (default 50 jika baru)
        current_dur = durability_data.get(slot, 50)
        
        if current_dur < 50:
            missing_dur = 50 - current_dur
            # Hitung biaya per poin perbaikan (10 Gold)
            total_cost += missing_dur * 10 
            
            # Pulihkan ke maksimal
            durability_data[slot] = 50
            items_repaired += 1
            
    return durability_data, total_cost, items_repaired
