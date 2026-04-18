# game/logic/inventory_manager.py

from game.items import get_item as get_equip # Database Equipment
from game.consumables.items import get_item as get_consumable # Database Tenda & Potion
from game.logic.stats import calculate_total_stats
from game.logic.job_manager import detect_player_job

def get_any_item(item_id):
    """Mencari item di database equipment maupun consumable."""
    item = get_equip(item_id)
    if not item:
        item = get_consumable(item_id)
    return item

def equip_item(player, item_id):
    """
    Memasang item ke slot yang sesuai. 
    Menangani konflik 1H/2H, update Job, dan kalkulasi stat otomatis.
    """
    item = get_equip(item_id) # Equipment hanya ada di database equip
    if not item:
        return False, "❌ Item tidak ditemukan atau bukan peralatan tempur."

    if item_id not in player.get('inventory', []):
        return False, "❌ Kau tidak memiliki item ini di tasmu."

    slot = item.get('type') 
    
    if slot == 'artifact':
        slot = 'offhand'
        
    equipped = player.get('equipped', {})
    warning_msg = ""

    # --- LOGIKA 1: KONFLIK 2-HANDED (2H) vs OFFHAND ---
    if slot == 'weapon':
        if item.get('grip') == '2H':
            if equipped.get('offhand'):
                unequip_item(player, 'offhand')
                warning_msg = f"⚠️ **{item['name']}** butuh dua tangan. Tangan kirimu dikosongkan.\n"
    
    elif slot == 'offhand':
        weapon_id = equipped.get('weapon')
        if weapon_id:
            weapon = get_equip(weapon_id)
            if weapon and weapon.get('grip') == '2H':
                return False, f"❌ Tanganmu penuh! Lepas **{weapon['name']}** (2H) terlebih dahulu."

    # --- LOGIKA 2: PROSES PERGANTIAN ITEM ---
    old_item_id = equipped.get(slot)
    if old_item_id:
        player['inventory'].append(old_item_id)

    equipped[slot] = item_id
    player['inventory'].remove(item_id)
    player['equipped'] = equipped

    # --- LOGIKA 3: UPDATE JOB & STAT ---
    detect_player_job(player)
    player['stats'] = calculate_total_stats(player)

    status_msg = f"✅ **{item['name']}** berhasil dipasang!"
    if warning_msg: 
        status_msg = warning_msg + status_msg
    
    return True, status_msg

def unequip_item(player, slot):
    """Melepas item dari slot tertentu secara aman ke inventory."""
    equipped = player.get('equipped', {})
    item_id = equipped.get(slot)

    if not item_id:
        return False, f"❌ Slot {slot} memang sudah kosong."

    item = get_equip(item_id)
    item_name = item['name'] if item else slot

    player['inventory'].append(item_id)
    del equipped[slot]
    player['equipped'] = equipped

    detect_player_job(player)
    player['stats'] = calculate_total_stats(player)

    return True, f"📦 **{item_name}** telah dilepas ke tas."

# === SISTEM CONSUMABLES (PENGGUNAAN ITEM) ===

def use_consumable_item(player, item_id):
    """
    Logika penggunaan item habis pakai.
    """
    item = get_consumable(item_id)
    if not item:
        return False, "❌ Item tidak ditemukan di daftar barang habis pakai.", player

    inventory = player.get('inventory', [])
    if item_id not in inventory:
        return False, "❌ Item tidak ada di tas.", player

    # --- PROTEKSI TENDA ---
    if item.get('effect_type') == 'camp_gear':
        return False, "⛺ **Tenda** hanya bisa dipasang saat kamu menemukan **Rest Area** (Api Unggun)!", player

    msg = ""
    eff_type = item.get('effect_type')
    val = item.get('value', 0)

    # 1. Pemulihan HP
    if eff_type == 'heal_hp':
        if player['hp'] >= player.get('max_hp', 100):
            return False, "❌ Darahmu sudah penuh!", player
        old_hp = player['hp']
        player['hp'] = min(player.get('max_hp', 100), player['hp'] + val)
        msg = f"💖 Meminum {item['name']}! (+{player['hp'] - old_hp} HP)"
    
    # 2. Pemulihan MP
    elif eff_type == 'restore_mp':
        if player.get('mp', 0) >= player.get('max_mp', 50):
            return False, "❌ Mana milikmu sudah penuh!", player
        old_mp = player.get('mp', 0)
        player['mp'] = min(player.get('max_mp', 50), player.get('mp', 0) + val)
        msg = f"🔵 Meminum {item['name']}! (+{player['mp'] - old_mp} MP)"

    # 3. Pemulihan Energi
    elif eff_type == 'restore_energy':
        if player.get('energy', 100) >= player.get('max_energy', 100):
            return False, "❌ Kau masih sangat bertenaga!", player
        old_en = player.get('energy', 100)
        player['energy'] = min(player.get('max_energy', 100), player.get('energy', 100) + val)
        msg = f"🍴 Memakan {item['name']}! (+{player['energy'] - old_en} Energi)"

    # 4. Pemicu Quiz
    elif eff_type == 'trigger_quiz':
        msg = f"📖 Kau mulai membaca {item['name']}..."
    
    else:
        return False, "❌ Item ini belum memiliki fungsi dalam sistem.", player

    # Hapus item setelah digunakan (Kecuali Tenda, karena tenda dihapus di exploration.py)
    inventory.remove(item_id)
    player['inventory'] = inventory
    
    return True, msg, player

# === SISTEM REPAIR (DURABILITY) ===

def process_repair_all(player):
    """Memperbaiki seluruh equipment yang terpasang."""
    equipped = player.get('equipped', {})
    durability_data = player.get('equipment_durability', {})
    total_cost = 0
    items_repaired = 0
    
    for slot in equipped.keys():
        current_dur = durability_data.get(slot, 50)
        if current_dur < 50:
            missing_dur = 50 - current_dur
            total_cost += missing_dur * 5
            durability_data[slot] = 50
            items_repaired += 1
            
    return durability_data, total_cost, items_repaired
