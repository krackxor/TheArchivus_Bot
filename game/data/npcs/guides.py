# game/data/npcs/guides.py

"""
NPC Guide Database - The Archivus
Berisi NPC penunjuk jalan. 
Mekanik: Penunjuk Jalan Jujur vs Penyesat (Evil Guide).
"""

GUIDE_NPCS = {
    # --- NPC JUJUR (TRUSTWORTHY) ---
    "npc_old_soldier": {
        "name": "Veteran Perang Arklay",
        "role": "guide",
        "desc": "Seorang pria tua dengan seragam usang yang robek. Ia duduk bersandar pada tumpukan batu.",
        "dialog": "Dengarkan aku, Weaver. Jika kau ingin tetap hidup, pergilah ke **Timur**. Aku melihat secercah cahaya di sana, jauh dari jangkauan mereka.",
        "is_evil": False,
        "correct_direction": "Timur",
        "clue": "Napasnya berat namun matanya menatapmu dengan rasa iba yang tulus."
    },

    "npc_lost_scholar": {
        "name": "Sarjana Tersesat",
        "role": "guide",
        "desc": "Seorang wanita yang terus mencatat sesuatu di buku kecilnya dengan gemetar.",
        "dialog": "Berdasarkan rasi bintang yang mulai pudar ini... jalan menuju area pemulihan ada di **Utara**. Jangan ke Selatan, ada sesuatu yang besar di sana.",
        "is_evil": False,
        "correct_direction": "Utara",
        "clue": "Ia terlihat sangat terobsesi dengan akurasi catatannya."
    },

    # --- NPC JAHAT / PENYESAT (DECEPTIVE) ---
    "npc_shadow_wanderer": {
        "name": "Shadow Wanderer",
        "role": "guide",
        "desc": "Sosok berjubah kelam yang wajahnya tidak terlihat jelas. Bayangannya tampak bergerak tidak sinkron dengan tubuhnya.",
        "dialog": "Mencari harta karun? Aku melihat peti emas yang melimpah di arah **Selatan**. Pergilah sekarang sebelum Weaver lain mengambilnya.",
        "is_evil": True,
        "fake_direction": "Selatan", # Ini arah yang akan membawamu ke TRAP atau BOSS
        "clue": "Suaranya terdengar seperti dua orang yang berbicara bersamaan dalam satu tenggorokan."
    },

    "npc_corrupted_spirit": {
        "name": "Roh Terkontaminasi",
        "role": "guide",
        "desc": "Sosok transparan yang separuh tubuhnya telah menghitam tertelan Miasma.",
        "dialog": "Ke **Barat**... jalannya aman... kabut di sana sudah menghilang... pergilah ke Barat...",
        "is_evil": True,
        "fake_direction": "Barat",
        "clue": "Ia terus menyeringai setiap kali kau menyebut kata 'aman'."
    }
}

# --- LOGIKA INTERAKSI GUIDE ---

def process_guide_interaction(player, npc_id):
    """
    Memproses konsekuensi dari mengikuti petunjuk arah NPC.
    Mengembalikan: (result_type, message)
    """
    npc = GUIDE_NPCS.get(npc_id)
    if not npc:
        return "error", "❌ NPC Guide tidak ditemukan."

    if npc['is_evil']:
        # Jika guide jahat, arahkan ke event buruk (Trap/Ambush)
        direction = npc['fake_direction']
        message = f"⚠️ Kamu mengikuti arah {direction}... {npc['clue']} Ternyata itu jebakan!"
        return "trap", message
    else:
        # Jika guide jujur, perjalanan terasa lebih aman
        direction = npc['correct_direction']
        message = f"✅ Kamu mengikuti arah {direction}. {npc['clue']} Perjalanan terasa lebih tenang."
        return "safe", message

def get_guide_data(npc_id):
    """Mengambil data NPC penunjuk jalan berdasarkan ID."""
    return GUIDE_NPCS.get(npc_id)

def get_all_guides():
    """Mengambil seluruh database NPC guide."""
    return GUIDE_NPCS
