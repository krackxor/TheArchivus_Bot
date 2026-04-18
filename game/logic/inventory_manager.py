# game/logic/inventory_manager.py

from game.items import get_item
from game.logic.stats import calculate_total_stats
from game.logic.job_manager import detect_player_job

def equip_item(player, item_id):
    """
    Memasang item ke slot yang sesuai. 
    Menangani konflik 1H/2H, update Job, dan kalkulasi stat otomatis.
    """
    item = get_item(item_id)
    if not item:
        return False, "❌ Item tidak ditemukan di database."

    if item_id not in player.get('inventory', []):
        return False, "❌ Kau tidak memiliki item ini di tasmu."

    # 'weapon', 'armor', 'head', 'mask', 'cloak', 'offhand', 'artifact', dll.
    slot = item.get('type') 
    
    # Adaptasi: Jika tipe item adalah shield, masukkan ke slot offhand
    if slot == 'shield':
        slot = 'offhand'
        
    equipped = player.get('equipped', {})
    
    warning_msg = ""

    # --- LOGIKA 1: KONFLIK 2-HANDED (2H) vs OFFHAND ---
    if slot == 'weapon':
        if item.get('grip') == '2H':
            if equipped.get('offhand'):
                # Lepas offhand otomatis jika pakai senjata 2H
                unequip_item(player, 'offhand')
                warning_msg = f"⚠️ **{item['name']}** butuh dua tangan. Tangan kirimu dikosongkan.\n"
    
    elif slot == 'offhand':
        weapon_id = equipped.get('weapon')
        if weapon_id:
            weapon = get_item(weapon_id)
            if weapon and weapon.get('grip') == '2H':
                return False, f"❌ Tanganmu penuh! Lepas **{weapon['name']}** (2H) terlebih dahulu."

    # --- LOGIKA 2: PROSES PERGANTIAN ITEM ---
    # Jika di slot yang sama sudah ada barang, kembalikan barang lama ke tas
    old_item_id = equipped.get(slot)
    if old_item_id:
        player['inventory'].append(old_item_id)

    # Pasang barang baru dan hapus dari tas
    equipped[slot] = item_id
    player['inventory'].remove(item_id)
    player['equipped'] = equipped

    # --- LOGIKA 3: UPDATE JOB & CACHING STAT ---
    detect_player_job(player)
    # Penting: Re-kalkulasi stat hanya dilakukan saat ganti equipment
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

    item = get_item(item_id)
    item_name = item['name'] if item else slot

    player['inventory'].append(item_id)
    del equipped[slot]
    player['equipped'] = equipped

    # Re-kalkulasi setelah lepas item
    detect_player_job(player)
    player['stats'] = calculate_total_stats(player)

    return True, f"📦 **{item_name}** telah dilepas ke tas."

# === SISTEM PANDAI BESI (REPAIR) ===

def process_repair_all(player):
    """
    Memperbaiki semua item yang terpasang ke kondisi maksimal (50/50).
    Biaya: 5 Gold per poin durabilitas (Disesuaikan agar lebih balance).
    """
    equipped = player.get('equipped', {})
    durability_data = player.get('equipment_durability', {})
    total_cost = 0
    items_repaired = 0
    
    for slot in equipped.keys():
        current_dur = durability_data.get(slot, 50)
        if current_dur < 50:
            missing_dur = 50 - current_dur
            total_cost += missing_dur * 5 # Biaya perbaikan per poin
            durability_data[slot] = 50
            items_repaired += 1
            
    return durability_data, total_cost, items_repaired

# === SISTEM CONSUMABLES (PENGGUNAAN ITEM) ===

def use_consumable_item(player, item_id):
    """
    Logika penggunaan item habis pakai (Potion, Antidote, dll).
    Mendukung pemulihan HP, MP, dan pembersihan status efek negatif.
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

    # 1. Efek Pemulihan HP (Potion)
    if eff_type == 'heal_hp':
        if player['hp'] >= player.get('max_hp', 100):
            return False, "❌ Darahmu sudah penuh!", player
        old_hp = player['hp']
        player['hp'] = min(player.get('max_hp', 100), player['hp'] + val)
        msg = f"💖 Meminum {item['name']}! (+{player['hp'] - old_hp} HP)"
    
    # 2. Efek Pemulihan MP (Mana Potion)
    elif eff_type == 'restore_mp':
        if player.get('mp', 0) >= player.get('max_mp', 50):
            return False, "❌ Mana milikmu sudah penuh!", player
        old_mp = player.get('mp', 0)
        player['mp'] = min(player.get('max_mp', 50), player.get('mp', 0) + val)
        msg = f"🔵 Meminum {item['name']}! (+{player['mp'] - old_mp} MP)"

    # 3. Efek Penawar Racun (Antidote)
    elif eff_type == 'clear_poison':
        active_effects = player.get('active_effects', [])
        # Cek apakah memang sedang terkena racun
        if not any(e['type'] == 'poison' for e in active_effects):
            return False, "❌ Kau tidak sedang terkena racun.", player
            
        player['active_effects'] = [e for e in active_effects if e['type'] != 'poison']
        msg = f"🧪 {item['name']} menetralkan racun di tubuhmu!"

    # Kurangi item setelah berhasil digunakan
    inventory.remove(item_id)
    player['inventory'] = inventory
    
    return True, msg, player
