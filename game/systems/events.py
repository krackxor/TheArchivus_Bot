"""
Random Events & Loot System
Membuat gameplay lebih unpredictable dan exciting
"""

import random

# === RANDOM EVENTS ===
RANDOM_EVENTS = {
    "treasure_chest": {
        "id": "treasure_chest",
        "name": "Peti Harta Karun",
        "description": "Sebuah peti berkarat tergeletak di sudut lorong...",
        "type": "treasure",
        "outcomes": [
            {"prob": 0.50, "result": "gold", "value": (50, 150), "text": "💰 Kau menemukan {value} Gold!"},
            {"prob": 0.25, "result": "item", "value": "random_potion", "text": "🧪 Kau menemukan ramuan misterius!"},
            {"prob": 0.15, "result": "trap", "value": 30, "text": "💥 JEBAKAN! Peti meledak! (-{value} HP)"},
            {"prob": 0.10, "result": "rare_item", "value": "artifact", "text": "✨ Artifact langka muncul dari cahaya emas!"}
        ]
    },
    
    "mysterious_shrine": {
        "id": "mysterious_shrine",
        "name": "Kuil Misterius",
        "description": "Cahaya lembut bersinar dari altar kuno...",
        "type": "shrine",
        "outcomes": [
            {"prob": 0.40, "result": "heal", "value": 50, "text": "✨ Cahaya hangat memulihkan lukamu (+{value} HP)"},
            {"prob": 0.30, "result": "mp_restore", "value": 30, "text": "🔮 Pikiranmu menjadi jernih (+{value} MP)"},
            {"prob": 0.20, "result": "curse", "value": 20, "text": "🌑 Kutukan menyelimuti! (-{value} Max HP sementara)"},
            {"prob": 0.10, "result": "blessing", "value": "stat_boost", "text": "👼 Berkah permanen! (+10 Max HP & +5 Max MP)"}
        ]
    },
    
    "gambling_demon": {
        "id": "gambling_demon",
        "name": "Iblis Perjudian",
        "description": "Sosok berkepala kambing menawarkanmu sebuah dadu...",
        "type": "gamble",
        "bet_amount": 100,
        "outcomes": [
            {"dice": [1, 2], "result": "lose_all", "text": "💀 BANGKRUT! Semua goldmu lenyap dalam asap hitam!"},
            {"dice": [3, 4], "result": "lose_bet", "text": "😈 Kau kalah! Iblis itu tertawa mengejek."},
            {"dice": [5], "result": "double", "text": "🎲 Kau menang! Gold x2!"},
            {"dice": [6], "result": "jackpot", "text": "🎰 JACKPOT! Gold x5 + Bonus Item!"}
        ]
    },
    
    "memory_well": {
        "id": "memory_well",
        "name": "Sumur Kenangan",
        "description": "Sumur gelap tanpa dasar. Bisikan samar terdengar dari dalam...",
        "type": "choice",
        "choices": [
            {
                "text": "💧 Minum airnya",
                "outcomes": [
                    {"prob": 0.50, "result": "vision", "text": "👁️ Visi masa depan! +50 EXP"},
                    {"prob": 0.30, "result": "poison", "text": "🤢 Air beracun! -20 HP"},
                    {"prob": 0.20, "result": "madness", "text": "🌀 Kegilaan! -30 MP tapi +200 Gold"}
                ]
            },
            {
                "text": "🪙 Lempar koin sebagai persembahan",
                "cost": 50,
                "outcomes": [
                    {"prob": 0.70, "result": "blessing", "text": "✨ Berkah diterima! HP & MP full!"},
                    {"prob": 0.30, "result": "nothing", "text": "... Tidak terjadi apa-apa."}
                ]
            },
            {
                "text": "🏃 Tinggalkan saja",
                "outcomes": [
                    {"prob": 1.0, "result": "safe", "text": "Kau melangkah pergi dengan hati-hati."}
                ]
            }
        ]
    },
    
    "shadow_merchant": {
        "id": "shadow_merchant",
        "name": "Pedagang Bayangan",
        "description": "Sosok tanpa wajah membuka lapak dagangan yang tidak wajar...",
        "type": "shop",
        "items": [
            {"name": "Elixir Kehidupan", "cost": 200, "effect": "full_heal"},
            {"name": "Pecahan Waktu", "cost": 150, "effect": "extra_time_buff"},
            {"name": "Kontrak Darah", "cost": -50, "effect": "hp_for_gold"},  # Negative cost = dapat gold
            {"name": "Lensa Kebenaran", "cost": 300, "effect": "reveal_npc_identity"}
        ]
    },
    
    "time_distortion": {
        "id": "time_distortion",
        "name": "Distorsi Waktu",
        "description": "Realitas bergetar. Waktu berjalan mundur dan maju secara bersamaan...",
        "type": "buff_debuff",
        "duration": 5,  # 5 encounters
        "outcomes": [
            {"prob": 0.40, "result": "time_slow", "text": "⏰ Waktu melambat! +15 detik untuk 5 combat berikutnya"},
            {"prob": 0.40, "result": "time_fast", "text": "⚡ Waktu mempercepat! -10 detik untuk 5 combat berikutnya"},
            {"prob": 0.20, "result": "time_stop", "text": "🕐 Waktu berhenti! Puzzle berikutnya tanpa timer!"}
        ]
    },
    
    "ghost_companion": {
        "id": "ghost_companion",
        "name": "Roh Pendamping",
        "description": "Roh Weaver terdahulu menawarkan bantuannya...",
        "type": "companion",
        "duration": 10,  # 10 encounters
        "effects": {
            "damage_boost": 0.25,  # +25% gold dari combat
            "hint_chance": 0.30,   # 30% chance dapat hint gratis
            "text": "👻 Roh pendamping akan membantumu untuk 10 pertarungan!"
        }
    }
}

# === LOOT TABLES ===
LOOT_TABLE_COMMON = [
    {"id": "minor_potion", "name": "Ramuan Kecil", "type": "potion", "effect": "heal_25", "rarity": "common"},
    {"id": "mana_vial", "name": "Botol Mana", "type": "potion", "effect": "mp_20", "rarity": "common"},
    {"id": "rusty_coin", "name": "Koin Berkarat", "type": "material", "value": 10, "rarity": "common"}
]

LOOT_TABLE_UNCOMMON = [
    {"id": "healing_potion", "name": "Ramuan Penyembuh", "type": "potion", "effect": "heal_50", "rarity": "uncommon"},
    {"id": "clarity_elixir", "name": "Elixir Kejernihan", "type": "potion", "effect": "mp_40", "rarity": "uncommon"},
    {"id": "silver_fragment", "name": "Pecahan Perak", "type": "material", "value": 25, "rarity": "uncommon"},
    {"id": "hint_scroll", "name": "Gulungan Petunjuk", "type": "consumable", "effect": "free_hint", "rarity": "uncommon"}
]

LOOT_TABLE_RARE = [
    {"id": "greater_potion", "name": "Ramuan Agung", "type": "potion", "effect": "heal_100", "rarity": "rare"},
    {"id": "arcane_essence", "name": "Esensi Arkana", "type": "potion", "effect": "mp_full", "rarity": "rare"},
    {"id": "time_shard", "name": "Pecahan Waktu", "type": "consumable", "effect": "extra_time", "rarity": "rare"},
    {"id": "gold_ingot", "name": "Batangan Emas", "type": "material", "value": 100, "rarity": "rare"}
]

LOOT_TABLE_EPIC = [
    {"id": "phoenix_tear", "name": "Air Mata Phoenix", "type": "potion", "effect": "revive_once", "rarity": "epic"},
    {"id": "wisdom_tome", "name": "Kitab Kebijaksanaan", "type": "artifact", "effect": "puzzle_easier", "rarity": "epic"},
    {"id": "lucky_charm", "name": "Jimat Keberuntungan", "type": "artifact", "effect": "better_loot", "rarity": "epic"},
    {"id": "combat_manual", "name": "Manual Pertempuran", "type": "artifact", "effect": "damage_boost", "rarity": "epic"}
]

LOOT_TABLE_LEGENDARY = [
    {"id": "keeper_heart", "name": "Jantung Penjaga", "type": "artifact", "effect": "max_hp_50", "rarity": "legendary"},
    {"id": "void_crystal", "name": "Kristal Kehampaan", "type": "artifact", "effect": "max_mp_50", "rarity": "legendary"},
    {"id": "omniscient_eye", "name": "Mata Mahatahu", "type": "artifact", "effect": "see_answers", "rarity": "legendary"},
    {"id": "archivus_key", "name": "Kunci Archivus", "type": "key_item", "effect": "unlock_secret", "rarity": "legendary"}
]

def roll_loot_drop(tier_level, is_boss=False):
    """Generate random loot based on tier"""
    drops = []
    
    if is_boss:
        # Boss selalu drop rare+
        drops.append(random.choice(LOOT_TABLE_RARE))
        
        # 50% chance epic
        if random.random() < 0.50:
            drops.append(random.choice(LOOT_TABLE_EPIC))
        
        # 10% chance legendary
        if random.random() < 0.10:
            drops.append(random.choice(LOOT_TABLE_LEGENDARY))
            
        # Bonus gold besar
        drops.append({"type": "gold", "value": random.randint(300, 500)})
        
    else:
        # Regular monster loot based on tier
        drop_chance = 0.30 + (tier_level * 0.10)  # 40% tier 1, 80% tier 5
        
        if random.random() < drop_chance:
            # Determine rarity based on tier
            rarity_roll = random.random()
            
            if tier_level >= 4 and rarity_roll < 0.05:
                # 5% legendary di tier 4+
                drops.append(random.choice(LOOT_TABLE_LEGENDARY))
            elif tier_level >= 3 and rarity_roll < 0.15:
                # 15% epic di tier 3+
                drops.append(random.choice(LOOT_TABLE_EPIC))
            elif tier_level >= 2 and rarity_roll < 0.35:
                # 35% rare di tier 2+
                drops.append(random.choice(LOOT_TABLE_RARE))
            elif rarity_roll < 0.60:
                # 60% uncommon
                drops.append(random.choice(LOOT_TABLE_UNCOMMON))
            else:
                # Common
                drops.append(random.choice(LOOT_TABLE_COMMON))
    
    return drops

def trigger_random_event(player_cycle, player_location):
    """Randomly trigger an event (10% chance per move)"""
    if random.random() > 0.10:
        return None
    
    # Weight events berdasarkan cycle
    if player_cycle == 1:
        # Early game: lebih banyak treasure dan heal
        pool = ["treasure_chest", "mysterious_shrine", "memory_well"]
    elif player_cycle <= 3:
        # Mid game: introduce gambling dan shops
        pool = ["treasure_chest", "mysterious_shrine", "gambling_demon", "shadow_merchant", "memory_well"]
    else:
        # Late game: semua events aktif
        pool = list(RANDOM_EVENTS.keys())
    
    event_id = random.choice(pool)
    return RANDOM_EVENTS[event_id]

def process_event_outcome(event, choice_index=0):
    """Process the outcome of an event"""
    if event['type'] == 'treasure':
        outcomes = event['outcomes']
        roll = random.random()
        cumulative = 0
        
        for outcome in outcomes:
            cumulative += outcome['prob']
            if roll <= cumulative:
                result = outcome.copy()
                
                # Handle range values (e.g., gold: (50, 150))
                if isinstance(result.get('value'), tuple):
                    result['value'] = random.randint(result['value'][0], result['value'][1])
                
                # Format text dengan value
                if '{value}' in result['text']:
                    result['text'] = result['text'].format(value=result['value'])
                
                return result
    
    elif event['type'] == 'shrine':
        outcomes = event['outcomes']
        roll = random.random()
        cumulative = 0
        
        for outcome in outcomes:
            cumulative += outcome['prob']
            if roll <= cumulative:
                return outcome
    
    elif event['type'] == 'choice':
        choice = event['choices'][choice_index]
        outcomes = choice['outcomes']
        roll = random.random()
        cumulative = 0
        
        for outcome in outcomes:
            cumulative += outcome['prob']
            if roll <= cumulative:
                return {**outcome, 'cost': choice.get('cost', 0)}
    
    elif event['type'] == 'gamble':
        dice_result = random.randint(1, 6)
        for outcome in event['outcomes']:
            if dice_result in outcome['dice']:
                return {**outcome, 'dice_rolled': dice_result}
    
    elif event['type'] == 'buff_debuff':
        outcomes = event['outcomes']
        roll = random.random()
        cumulative = 0
        
        for outcome in outcomes:
            cumulative += outcome['prob']
            if roll <= cumulative:
                return {**outcome, 'duration': event['duration']}
    
    return None

# === EASTER EGGS ===
EASTER_EGGS = {
    "konami_code": {
        "sequence": ["⬆️ Utara", "⬆️ Utara", "⬇️ Selatan", "⬇️ Selatan", 
                     "⬅️ Barat", "Timur ➡️", "⬅️ Barat", "Timur ➡️"],
        "reward": {"gold": 1000, "exp": 500, "item": "konami_badge"},
        "message": "🎮 **KONAMI CODE ACTIVATED!**\n30 Lives! ...wait, wrong game.\n\n+1000 Gold, +500 EXP, Special Badge!"
    },
    
    "666": {
        "trigger": "step_counter_666",
        "reward": {"item": "demon_contract", "effect": "double_gold_temp"},
        "message": "😈 You've reached step 666...\nThe demons offer you a contract.\nDouble gold for 10 battles, but at what cost?"
    },
    
    "secret_word_archivus": {
        "trigger": "type_exact_word",
        "word": "THETRUTHBEHINDARCHIVUS",
        "reward": {"achievement": "truth_seeker", "item": "hidden_page"},
        "message": "📜 **SECRET UNLOCKED**\n\nYou've spoken the forbidden phrase.\nA hidden page from the First Archive appears before you..."
    }
}

def check_easter_egg(player_data, action_type, action_value=None):
    """Check if player triggered an easter egg"""
    # Check konami code
    if action_type == "movement_sequence":
        recent_moves = player_data.get('recent_moves', [])
        if len(recent_moves) >= 8:
            if recent_moves[-8:] == EASTER_EGGS['konami_code']['sequence']:
                return EASTER_EGGS['konami_code']
    
    # Check 666 steps
    if action_type == "step_counter":
        if player_data.get('step_counter') == 666:
            return EASTER_EGGS['666']
    
    # Check secret word
    if action_type == "message_text":
        if action_value and action_value.upper().replace(" ", "") == EASTER_EGGS['secret_word_archivus']['word']:
            return EASTER_EGGS['secret_word_archivus']
    
    return None
