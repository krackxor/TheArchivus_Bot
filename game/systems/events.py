# game/systems/events.py

"""
Sistem Random Events & Loot (The Archivus)
Terintegrasi dengan Shop, Equipment, dan Exploration Driver.
Membuat gameplay lebih dinamis, berisiko, dan penuh misteri.
"""

import random

# === RANDOM EVENTS POOL (SUB-EVENTS) ===
# Ini dipanggil ketika exploration.py memicu event "random_anomaly" atau interaksi khusus
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
    
    "gambling_demon": {
        "id": "gambling_demon",
        "name": "The Void Gambler",
        "description": "Sosok berjubah compang-camping memutar koin emas di jarinya. 'Berani bertaruh nasib, Weaver?'",
        "type": "gamble",
        "bet_amount": 100,
        "outcomes": [
            {"dice": [1, 2], "result": "lose_all", "text": "💀 BANGKRUT! Koinmu melebur menjadi debu hitam di tangannya!"},
            {"dice": [3, 4], "result": "lose_bet", "text": "😈 Kau kalah! Sosok itu tertawa parau dan menghilang."},
            {"dice": [5], "result": "double", "text": "🎲 Kau menang! Koinmu berlipat ganda! (Gold x2)"},
            {"dice": [6], "result": "jackpot", "text": "🎰 JACKPOT! 'Keberuntungan yang menakutkan...' bisiknya. (Gold x5 + Random Loot!)"}
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
                    {"prob": 0.20, "result": "madness", "text": "🌀 Kegilaan! Suara-suara merobek pikiranmu! (-30 MP, tapi +200 Gold di dasar sumur)"}
                ]
            },
            {
                "text": "🪙 Lempar koin persembahan (50G)",
                "cost": 50,
                "outcomes": [
                    {"prob": 0.70, "result": "blessing", "text": "✨ Sumur berpendar terang. Tubuhmu terasa ringan! (HP & MP Penuh)"},
                    {"prob": 0.30, "result": "nothing", "text": "*Plung...* Tidak terjadi apa-apa. Kau baru saja membuang uangmu."}
                ]
            },
            {
                "text": "🚶 Tinggalkan saja",
                "outcomes": [
                    {"prob": 1.0, "result": "safe", "text": "Kau menahan rasa penasaran dan melangkah pergi dengan aman."}
                ]
            }
        ]
    },
    
    "time_distortion": {
        "id": "time_distortion",
        "name": "Distorsi Realitas",
        "description": "Ruang dan waktu di sekitarmu bergetar. Jam di sakumu berputar tak terkendali...",
        "type": "buff_debuff",
        "duration": 5, # Efek untuk 5 langkah/pertarungan ke depan
        "outcomes": [
            {"prob": 0.40, "result": "time_slow", "text": "⏰ Waktu melambat! Musuh akan bergerak lebih lambat di 5 pertarungan berikutnya."},
            {"prob": 0.40, "result": "time_fast", "text": "⚡ Waktu mempercepat! Puzzle dan timer akan lebih cepat habis selama 5 langkah!"},
            {"prob": 0.20, "result": "time_stop", "text": "🕐 Waktu berhenti sementara! Hazard dan jebakan tidak akan melukaimu untuk 5 langkah."}
        ]
    }
}

# === LOOT TABLES (Terintegrasi format Inventory & UI kita) ===
# Consumables berbentuk Dictionary, Artefak/Equipment berbentuk String ID
LOOT_TABLE_COMMON = [
    {"id": "food_ration", "name": "🍞 Roti Kering", "type": "food", "effect": "energy_30", "rarity": "common"},
    {"id": "potion_heal", "name": "🧪 Minor HP Potion", "type": "potion", "effect": "heal_30", "rarity": "common"},
    {"type": "gold", "value": 25}
]

LOOT_TABLE_UNCOMMON = [
    {"id": "potion_heal_major", "name": "🧪 Major HP Potion", "type": "potion", "effect": "heal_80", "rarity": "uncommon"},
    {"id": "potion_mana", "name": "🔮 Tetesan Memori", "type": "potion", "effect": "mp_40", "rarity": "uncommon"},
    {"id": "buy_key_iron", "name": "🔑 Iron Key", "type": "utility", "effect": "key_iron", "rarity": "uncommon"},
    {"id": "cure_poison", "name": "🌿 Antidote", "type": "potion", "effect": "cure_poisoned", "rarity": "uncommon"}
]

LOOT_TABLE_RARE = [
    {"id": "buy_key_magic", "name": "🔮 Mana Crystal", "type": "utility", "effect": "key_magic", "rarity": "rare"},
    {"id": "repair_all_kit", "name": "⚒️ Repair Kit", "type": "utility", "effect": "repair_all", "rarity": "rare"},
    {"type": "gold", "value": 150}
]

# Artefak & Unique Equipment (Disimpan sebagai String ID untuk dicocokkan ke MASTER_ITEM_DB)
LOOT_TABLE_EPIC = [
    "phoenix_tear", 
    "weaver_diary", 
    "lucky_charm"
]

LOOT_TABLE_LEGENDARY = [
    "keeper_heart", 
    "void_orb"
]

def roll_loot_drop(tier_level=1, is_boss=False):
    """Fungsi untuk memanggil hasil jarahan (Loot) saat monster mati atau peti dibuka."""
    drops = []
    
    if is_boss:
        # Boss selalu drop Rare + Gold Besar
        drops.append(random.choice(LOOT_TABLE_RARE))
        drops.append({"type": "gold", "value": random.randint(300, 500)})
        
        # Peluang tambahan (Artefak)
        if random.random() < 0.50: drops.append(random.choice(LOOT_TABLE_EPIC))
        if random.random() < 0.10: drops.append(random.choice(LOOT_TABLE_LEGENDARY))
        
    else:
        # Drop monster biasa / Peti biasa
        drop_chance = 0.30 + (tier_level * 0.10) # Makin tinggi tier, makin sering drop item
        
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
    """Memproses hasil RNG (Random Number Generator) dari event spesifik."""
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

    elif event_type == 'gamble':
        dice_result = random.randint(1, 6)
        for outcome in event['outcomes']:
            if dice_result in outcome['dice']:
                return {**outcome, 'dice_rolled': dice_result}

    elif event_type == 'buff_debuff':
        roll = random.random()
        cumulative = 0
        for outcome in event['outcomes']:
            cumulative += outcome['prob']
            if roll <= cumulative:
                return {**outcome, 'duration': event['duration']}
                
    return None

# === EASTER EGGS (The Archivus Secrets) ===
EASTER_EGGS = {
    "konami_code": {
        "sequence": ["⬆️ Utara", "⬆️ Utara", "⬇️ Selatan", "⬇️ Selatan", "⬅️ Barat", "Timur ➡️", "⬅️ Barat", "Timur ➡️"],
        "reward": {"gold": 1000, "exp": 500, "item": "lucky_charm"},
        "message": "🎮 **KODE KUNO DIAKTIFKAN!**\nRuang dan waktu bergetar... Sebuah peti jatuh dari langit!\n\n+1000 Gold, +500 EXP, Jimat Keberuntungan didapatkan!"
    },
    
    "step_666": {
        "trigger": "step_counter_666",
        "reward": {"item": "buy_key_magic"},
        "message": "😈 **Langkah ke-666...**\nBayanganmu tersenyum padamu. Sebuah *Mana Crystal* tergeletak di kakimu. Jangan tanya dari mana asalnya."
    },
    
    "secret_word_archivus": {
        "trigger": "type_exact_word",
        "word": "THEARCHIVUSREMEMBERS",
        "reward": {"achievement": "truth_seeker", "gold": 500},
        "message": "📜 **RAHASIA TERBONGKAR**\n\nKau mengucapkan kalimat terlarang. Entitas di atas sana memberkatimu dengan pecahan emas masa lalu."
    }
}

def check_easter_egg(player_data, action_type, action_value=None):
    """Mengecek apakah pergerakan atau teks pemain memicu Easter Egg."""
    if action_type == "movement_sequence":
        recent_moves = player_data.get('recent_moves', [])
        if len(recent_moves) >= 8 and recent_moves[-8:] == EASTER_EGGS['konami_code']['sequence']:
            return EASTER_EGGS['konami_code']
            
    if action_type == "step_counter" and player_data.get('step_counter') == 666:
        return EASTER_EGGS['step_666']
        
    if action_type == "message_text":
        if action_value and action_value.upper().replace(" ", "") == EASTER_EGGS['secret_word_archivus']['word']:
            return EASTER_EGGS['secret_word_archivus']
            
    return None
