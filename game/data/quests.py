# game/data/quests.py

"""
MASTER DATA QUEST - The Archivus (Expanded Edition)
Daftar misi harian yang mencakup berbagai aspek gameplay dengan sistem tracker otomatis.
"""

import random

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

    # --- KATEGORI: ECONOMY (Belanja & Toko) ---
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
    }
}

# --- FUNGSIONALITAS LOGIKA ---

def update_quest_progress(player_data, goal_type, amount=1):
    """
    Memperbarui progres quest pemain berdasarkan aksi yang dilakukan.
    Fungsi ini harus dipanggil di event_handler atau combat_handler.
    """
    quests = player_data.get("active_quests", [])
    messages = []
    
    for quest in quests:
        if quest["status"] == "active" and quest["goal_type"] == goal_type:
            quest["current"] += amount
            
            # Cek apakah target tercapai
            if quest["current"] >= quest["goal_value"]:
                quest["current"] = quest["goal_value"]
                quest["status"] = "completed"
                
                # Berikan hadiah langsung ke pemain
                player_data["gold"] += quest["reward_gold"]
                player_data["exp"] += quest["reward_exp"]
                
                messages.append(
                    f"✨ **Quest Selesai: {quest['name']}**\n"
                    f"💰 +{quest['reward_gold']} Gold | 🎖️ +{quest['reward_exp']} EXP"
                )
    
    return player_data, messages

def get_random_daily_quests(count=3):
    """Mengambil quest harian secara acak dengan inisialisasi state."""
    keys = list(DAILY_QUESTS_POOL.keys())
    actual_count = min(count, len(keys))
    selected_keys = random.sample(keys, actual_count)
    
    assigned_quests = []
    for k in selected_keys:
        quest_data = DAILY_QUESTS_POOL[k].copy()
        quest_data["current"] = 0
        quest_data["status"] = "active"
        assigned_quests.append(quest_data)
        
    return assigned_quests

def get_quest_info(quest_id):
    """Mengambil data mentah satu quest berdasarkan ID."""
    return DAILY_QUESTS_POOL.get(quest_id)

def check_all_quests_status(player_quests):
    """Mengembalikan ringkasan teks untuk daftar misi pemain."""
    if not player_quests:
        return "Tidak ada misi aktif saat ini."
    
    summary = "📜 **DAFTAR MISI HARIAN**\n━━━━━━━━━━━━━━━━━━━━\n"
    for q in player_quests:
        status_icon = "✅" if q["status"] == "completed" else "⏳"
        summary += f"{status_icon} **{q['name']}**\n"
        summary += f"└ 📊 Progres: `{q['current']}/{q['goal_value']}`\n"
        
    return summary
