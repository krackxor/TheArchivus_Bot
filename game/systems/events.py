# game/systems/events.py

"""
Sistem Random Events & Loot (The Archivus)
Terintegrasi dengan Shop, Equipment, dan Exploration Driver.
Mendukung interaksi dinamis di bawah State GameState.in_event.
"""

import random

# === RANDOM EVENTS POOL ===
# Ini dipanggil ketika exploration.py memicu event non-combat atau interaksi khusus
RANDOM_EVENTS = {
    "mysterious_shrine": {
        "id": "mysterious_shrine",
        "name": "Altar Sang Pendahulu",
        "description": "Cahaya biru lembut bersinar dari altar kuno yang retak...",
        "type": "shrine",
        "outcomes": [
            {"prob": 0.40, "result": "heal", "value": 50, "text": "✨ Cahaya hangat memulihkan lukamu (+{value} HP)"},
            {"prob": 0.30, "result": "mp_restore", "value": 40, "text": "🔮 Pikiranmu menjadi sangat jernih (+{value} MP)"},
            {"prob": 0.20, "result": "curse", "value": 20, "text": "🌑 Kutukan menyelimuti! Altar ini menolakmu (-{value} Max HP sementara)"},
            {"prob": 0.10, "result": "blessing", "value": "stat_boost", "text": "👼 Berkah Permanen! (+10 Max HP & +5 Max MP)"}
        ]
    },
    
    "memory_well": {
        "id": "memory_well",
        "name": "Sumur Kenangan (Memory Well)",
        "description": "Sumur gelap tanpa dasar. Genangan di bawahnya memantulkan wajah yang bukan milikmu...",
        "type": "choice",
        "choices": [
            {
                "text": "💧 Minum airnya",
                "outcomes": [
                    {"prob": 0.50, "result": "vision", "text": "👁️ Visi masa lalu mengalir ke otakmu! (+50 EXP)"},
                    {"prob": 0.30, "result": "poison", "text": "🤢 Air itu adalah tinta beracun! (-20 HP & Status: Poisoned)"},
                    {"prob": 0.20, "result": "madness", "text": "🌀 Kegilaan! Suara-suara merobek pikiranmu! (-30 MP, tapi +200 Gold)"}
                ]
            },
            {
                "text": "🪙 Lempar koin (50G)",
                "cost": 50,
                "outcomes": [
                    {"prob": 0.70, "result": "blessing", "text": "✨ Sumur berpendar terang. Tubuhmu terasa ringan! (HP & MP Penuh)"},
                    {"prob": 0.30, "result": "nothing", "text": "*Plung...* Tidak terjadi apa-apa. Kau baru saja membuang uangmu."}
                ]
            },
            {
                "text": "🚶 Tinggalkan",
                "outcomes": [
                    {"prob": 1.0, "result": "safe", "text": "Kau melangkah pergi dengan aman."}
                ]
            }
        ]
    },
    
    "time_distortion": {
        "id": "time_distortion",
        "name": "Distorsi Realitas",
        "description": "Ruang dan waktu di sekitarmu bergetar. Jam di sakumu berputar tak terkendali...",
        "type": "buff_debuff",
        "duration": 5,
        "outcomes": [
            {"prob": 0.40, "result": "time_slow", "text": "⏰ Waktu melambat! Musuh bergerak lebih lambat di 5 ronde berikutnya."},
            {"prob": 0.40, "result": "time_fast", "text": "⚡ Waktu mempercepat! Timer puzzle akan lebih cepat habis!"},
            {"prob": 0.20, "result": "time_stop", "text": "🕐 Waktu berhenti! Hazard tidak akan melukaimu untuk 5 langkah."}
        ]
    }
}

# === LOOT TABLES ===
# Format disesuaikan: Hanya string ID item agar tidak crash saat masuk ke inventory pemain
LOOT_TABLE_COMMON = ["food_ration", "potion_heal"]
LOOT_TABLE_UNCOMMON = ["potion_heal_major", "potion_mana", "buy_key_iron", "cure_poison"]
LOOT_TABLE_RARE = ["repair_all_kit", "buy_key_magic"]
LOOT_TABLE_EPIC = ["phoenix_tear", "weaver_diary", "lucky_charm"]
LOOT_TABLE_LEGENDARY = ["keeper_heart", "void_orb"]

def roll_loot_drop(tier_level=1, is_boss=False):
    """Fungsi untuk memanggil hasil jarahan (Loot) Item."""
    drops = []
    
    if is_boss:
        drops.append(random.choice(LOOT_TABLE_RARE))
        if random.random() < 0.50: drops.append(random.choice(LOOT_TABLE_EPIC))
        if random.random() < 0.10: drops.append(random.choice(LOOT_TABLE_LEGENDARY))
    else:
        drop_chance = 0.30 + (tier_level * 0.10)
        if random.random() < drop_chance:
            rarity_roll = random.random()
            if tier_level >= 4 and rarity_roll < 0.05:
                drops.append(random.choice(LOOT_TABLE_LEGENDARY))
            elif tier_level >= 3 and rarity_roll < 0.15:
                drops.append(random.choice(LOOT_TABLE_EPIC))
            elif tier_level >= 2 and rarity_roll < 0.35:
                drops.append(random.choice(LOOT_TABLE_RARE))
            elif rarity_roll < 0.60:
                drops.append(random.choice(LOOT_TABLE_UNCOMMON))
            else:
                drops.append(random.choice(LOOT_TABLE_COMMON))
                
    return drops

def process_event_outcome(event, choice_index=0):
    """Memproses hasil RNG dari event spesifik."""
    event_type = event.get('type')
    
    if event_type in ['shrine', 'treasure']:
        roll = random.random()
        cumulative = 0
        for outcome in event['outcomes']:
            cumulative += outcome['prob']
            if roll <= cumulative:
                result = outcome.copy()
                if isinstance(result.get('value'), tuple):
                    result['value'] = random.randint(result['value'][0], result['value'][1])
                if '{value}' in result.get('text', ''):
                    result['text'] = result['text'].format(value=result['value'])
                return result

    elif event_type == 'choice':
        choice = event['choices'][choice_index]
        roll = random.random()
        cumulative = 0
        for outcome in choice['outcomes']:
            cumulative += outcome['prob']
            if roll <= cumulative:
                return {**outcome, 'cost': choice.get('cost', 0)}

    elif event_type == 'buff_debuff':
        roll = random.random()
        cumulative = 0
        for outcome in event['outcomes']:
            cumulative += outcome['prob']
            if roll <= cumulative:
                return {**outcome, 'duration': event.get('duration', 3)}
                
    return None

# === EASTER EGGS ===
EASTER_EGGS = {
    "konami_code": {
        "sequence": ["⬆️ Utara", "⬆️ Utara", "⬇️ Selatan", "⬇️ Selatan", "⬅️ Barat", "Timur ➡️", "⬅️ Barat", "Timur ➡️"],
        "reward": {"gold": 1000, "exp": 500, "item": "lucky_charm"},
        "message": "🎮 **KODE KUNO DIAKTIFKAN!**\n+1000 Gold, +500 EXP, Jimat Keberuntungan!"
    },
    "step_666": {
        "trigger": "step_counter_666",
        "reward": {"item": "buy_key_magic"},
        "message": "😈 **Langkah ke-666...**\nBayanganmu tersenyum. Sebuah *Mana Crystal* muncul di kakimu."
    }
}

def check_easter_egg(player_data, action_type, action_value=None):
    """Mengecek pemicu Easter Egg."""
    if action_type == "movement_sequence":
        recent_moves = player_data.get('recent_moves', [])
        if len(recent_moves) >= 8 and recent_moves[-8:] == EASTER_EGGS['konami_code']['sequence']:
            return EASTER_EGGS['konami_code']
            
    if action_type == "step_counter" and player_data.get('step_counter') == 666:
        return EASTER_EGGS['step_666']
            
    return None
