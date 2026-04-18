# game/data/quests.py

"""
MASTER DATA QUEST - The Archivus (Expanded Edition)
Daftar misi harian yang mencakup berbagai aspek gameplay: Combat, Lore, Ekonomi, dan Survival.
"""

DAILY_QUESTS_POOL = {
    # --- KATEGORI: COMBAT (Monster) ---
    "q_slayer_1": {
        "id": "q_slayer_1",
        "name": "Pembersihan Dimensi",
        "desc": "Kalahkan 5 monster penghuni Archivus.",
        "goal_type": "kill_monsters",
        "goal_value": 5,
        "reward_gold": 150,
        "reward_exp": 100,
        "icon": "⚔️"
    },
    "q_slayer_2": {
        "id": "q_slayer_2",
        "name": "Pemburu Elit",
        "desc": "Kalahkan 12 monster apa saja.",
        "goal_type": "kill_monsters",
        "goal_value": 12,
        "reward_gold": 400,
        "reward_exp": 300,
        "icon": "💀"
    },
    "q_slayer_boss": {
        "id": "q_slayer_boss",
        "name": "Penantang Takdir",
        "desc": "Kalahkan 1 Boss atau Mini-Boss.",
        "goal_type": "kill_boss",
        "goal_value": 1,
        "reward_gold": 1000,
        "reward_exp": 800,
        "icon": "👺"
    },

    # --- KATEGORI: SCHOLAR (Quiz & Pengetahuan) ---
    "q_scholar_1": {
        "id": "q_scholar_1",
        "name": "Haus Pengetahuan",
        "desc": "Jawab 3 Quiz dari buku kuno dengan benar.",
        "goal_type": "answer_quiz",
        "goal_value": 3,
        "reward_gold": 250,
        "reward_exp": 200,
        "icon": "📖"
    },
    "q_scholar_2": {
        "id": "q_scholar_2",
        "name": "Sang Archivist",
        "desc": "Jawab 7 Quiz dengan benar tanpa salah lebih dari 3 kali.",
        "goal_type": "answer_quiz",
        "goal_value": 7,
        "reward_gold": 600,
        "reward_exp": 500,
        "icon": "🧠"
    },

    # --- KATEGORI: ECONOMY (Belanja & Toko) ---
    "q_spender_1": {
        "id": "q_spender_1",
        "name": "Pelanggan Setia",
        "desc": "Beli 3 item di Rest Area (Toko).",
        "goal_type": "buy_items",
        "goal_value": 3,
        "reward_gold": 100,
        "reward_exp": 50,
        "icon": "💰"
    },
    "q_gold_digger": {
        "id": "q_gold_digger",
        "name": "Kolektor Emas",
        "desc": "Kumpulkan 1.000 Gold dari hasil pertarungan.",
        "goal_type": "earn_gold",
        "goal_value": 1000,
        "reward_gold": 300,
        "reward_exp": 200,
        "icon": "🪙"
    },

    # --- KATEGORI: SKILL MASTERY (Teknik Tempur) ---
    "q_warrior_1": {
        "id": "q_warrior_1",
        "name": "Ahli Teknik",
        "desc": "Gunakan Skill sebanyak 10 kali saat bertarung.",
        "goal_type": "use_skills",
        "goal_value": 10,
        "reward_gold": 250,
        "reward_exp": 200,
        "icon": "🔮"
    },
    "q_combo_king": {
        "id": "q_combo_king",
        "name": "Rantai Kematian",
        "desc": "Lakukan serangan Combo sebanyak 15 kali.",
        "goal_type": "perform_combo",
        "goal_value": 15,
        "reward_gold": 400,
        "reward_exp": 300,
        "icon": "🔗"
    },

    # --- KATEGORI: SURVIVAL (Eksplorasi & Perbaikan) ---
    "q_survivor_1": {
        "id": "q_survivor_1",
        "name": "Penjelajah Gigih",
        "desc": "Melangkah sebanyak 50 kali di dimensi ini.",
        "goal_type": "move_steps",
        "goal_value": 50,
        "reward_gold": 150,
        "reward_exp": 100,
        "icon": "👣"
    },
    "q_blacksmith_friend": {
        "id": "q_blacksmith_friend",
        "name": "Perawatan Gear",
        "desc": "Perbaiki peralatanmu di Bengkel Aethelred sebanyak 2 kali.",
        "goal_type": "repair_gear",
        "goal_value": 2,
        "reward_gold": 100,
        "reward_exp": 50,
        "icon": "⚒️"
    },
    "q_rest_day": {
        "id": "q_rest_day",
        "name": "Tidur Nyenyak",
        "desc": "Gunakan fitur Istirahat di Rest Area sebanyak 3 kali.",
        "goal_type": "rest_action",
        "goal_value": 3,
        "reward_gold": 150,
        "reward_exp": 100,
        "icon": "💤"
    },

    # --- KATEGORI: COLLECTION (Looting) ---
    "q_looter": {
        "id": "q_looter",
        "name": "Tukang Pungut",
        "desc": "Dapatkan 10 item dari hasil drop monster.",
        "goal_type": "collect_drops",
        "goal_value": 10,
        "reward_gold": 200,
        "reward_exp": 150,
        "icon": "🎁"
    },
    "q_potion_addict": {
        "id": "q_potion_addict",
        "name": "Pecandu Ramuan",
        "desc": "Gunakan 5 ramuan (HP/MP) apa saja.",
        "goal_type": "use_items",
        "goal_value": 5,
        "reward_gold": 150,
        "reward_exp": 100,
        "icon": "🧪"
    }
}

def get_random_daily_quests(count=3):
    """
    Mengambil quest harian secara acak. 
    Default ditingkatkan menjadi 3 quest per hari agar pemain lebih sibuk.
    """
    import random
    
    keys = list(DAILY_QUESTS_POOL.keys())
    # Pastikan tidak mengambil lebih banyak dari yang tersedia
    actual_count = min(count, len(keys))
    selected_keys = random.sample(keys, actual_count)
    
    assigned_quests = []
    for k in selected_keys:
        quest_data = DAILY_QUESTS_POOL[k].copy()
        # Data dinamis untuk player state
        quest_data["current"] = 0
        quest_data["status"] = "active" 
        assigned_quests.append(quest_data)
        
    return assigned_quests

def get_quest_info(quest_id):
    """Mengambil data mentah satu quest berdasarkan ID."""
    return DAILY_QUESTS_POOL.get(quest_id)
