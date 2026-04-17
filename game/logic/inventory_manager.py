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
        if item.get('grip') == '2H':
            if equipped.get('artifact'):
                unequip_item(player, 'artifact')
                warning_msg = f"⚠️ **{item['name']}** butuh dua tangan. Artifact otomatis dilepas.\n"
    
    elif slot == 'artifact':
        weapon_id = equipped.get('weapon')
        if weapon_id:
            weapon = get_item(weapon_id)
            if weapon and weapon.get('grip') == '2H':
                return False, f"❌ Tanganmu penuh! Lepas **{weapon['name']}** terlebih dahulu."

    # --- LOGIKA CERDAS 2: PROSES EQUIP ---
    old_item_id = equipped.get(slot)
    if old_item_id:
        player['inventory'].append(old_item_id)

    equipped[slot] = item_id
    player['inventory'].remove(item_id)
    player['equipped'] = equipped

    # --- LOGIKA CERDAS 3: SINERGI & JOB CHECK ---
    detect_player_job(player)
    player['stats'] = calculate_total_stats(player)

    status_msg = f"✅ **{item['name']}** berhasil dipasang!"
    if warning_msg: status_msg = warning_msg + status_msg
    
    return True, status_msg

def unequip_item(player, slot):
    """Melepas item dari slot tertentu secara aman."""
    equipped = player.get('equipped', {})
    item_id = equipped.get(slot)

    if not item_id:
        return False, f"❌ Slot {slot} memang sudah kosong."

    item = get_item(item_id)
    item_name = item['name'] if item else slot

    player['inventory'].append(item_id)
    del equipped[slot]
    player['equipped'] = equipped

    detect_player_job(player)
    player['stats'] = calculate_total_stats(player)

    return True, f"📦 **{item_name}** telah dilepas."

# === SISTEM PANDAI BESI (REPAIR) ===

def process_repair_all(player):
    """
    Memperbaiki semua item yang terpasang ke 100%.
    Biaya: 10 Gold per 1 poin durabilitas yang hilang.
    """
    equipped = player.get('equipped', {})
    durability_data = player.get('equipment_durability', {})
    total_cost = 0
    items_repaired = 0
    
    for slot, item_id in equipped.items():
        current_dur = durability_data.get(slot, 50)
        if current_dur < 50:
            missing_dur = 50 - current_dur
            total_cost += missing_dur * 10 
            durability_data[slot] = 50
            items_repaired += 1
            
    return durability_data, total_cost, items_repaired

# === SISTEM CONSUMABLES (PENGGUNAAN ITEM) ===

def use_consumable_item(player, item_id):
    """
    Logika penggunaan item habis pakai (Potion, Antidote, dll).
    Mengembalikan: (success, message, updated_player)
    """
    item = get_item(item_id)
    if not item or item.get('type') != 'consumable':
        return False, "❌ Ini bukan item yang bisa dikonsumsi.", player

    inventory = player.get('inventory', [])
    if item_id not in inventory:
        return False, "❌ Item tidak ada di tas.", player

    msg = ""
    eff_type = item.get('effect_type')
    val = item.get('value', 0)

    # 1. Efek Pemulihan HP
    if eff_type == 'heal_hp':
        old_hp = player['hp']
        player['hp'] = min(player.get('max_hp', 100), player['hp'] + val)
        msg = f"💖 Meminum {item['name']}! (+{player['hp'] - old_hp} HP)"
    
    # 2. Efek Pemulihan MP
    elif eff_type == 'restore_mp':
        old_mp = player.get('mp', 0)
        player['mp'] = min(player.get('max_mp', 50), player.get('mp', 0) + val)
        msg = f"🔵 Meminum {item['name']}! (+{player['mp'] - old_mp} MP)"

    # 3. Efek Menetralkan Racun (Poison)
    elif eff_type == 'clear_poison':
        # Filter active_effects untuk membuang status poison
        active_effects = player.get('active_effects', [])
        player['active_effects'] = [e for e in active_effects if e['type'] != 'poison']
        msg = f"🧪 {item['name']} telah menetralkan racun dalam darahmu!"

    # Kurangi 1 jumlah item dari tas
    inventory.remove(item_id)
    player['inventory'] = inventory
    
    return True, msg, player
