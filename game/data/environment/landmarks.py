# game/data/environment/landmarks.py

"""
Landmarks Database - The Archivus
Berisi lokasi interaktif permanen di peta yang memberikan buff, 
pembersihan kutukan, atau interaksi puzzle khusus.
"""

import random

LANDMARKS = {
    "landmark_altar_cleansing": {
        "name": "Altar Pembersihan",
        "type": "landmark",
        "desc": "Sebuah altar marmer putih yang memancarkan aura suci. Air jernih mengalir dari celah-celahnya.",
        "interaction": "pray",
        "effect": "clear_debuffs",
        "msg": "✨ Kau membasuh wajahmu di altar. Semua rasa sakit dan racun dalam tubuhmu seketika sirna!",
        "requirement": None
    },
    
    "landmark_graveyard_ancient": {
        "name": "Kuburan Kuno",
        "type": "landmark",
        "desc": "Ribuan nisan berlumut berdiri di sini. Tanah terasa dingin dan berdenyut perlahan.",
        "interaction": "dig",
        "effect": "random_loot",
        "msg": "🪦 Kau menggali tanah yang gembur dan menemukan sebuah fragmen masa lalu!",
        "danger_chance": 0.4, # Peluang muncul monster Undead saat digali
        "requirement": "item_sekop"
    },

    "landmark_church_abandoned": {
        "name": "Rumah Ibadah Terbengkalai",
        "type": "landmark",
        "desc": "Atapnya sudah runtuh, namun patung dewi di tengahnya masih utuh, menatap kosong ke langit.",
        "interaction": "rest",
        "effect": "restore_mp",
        "msg": "🧘 Kedamaian di tempat ini memulihkan fokus mentalmu. Mana milikmu terisi kembali.",
        "requirement": None
    },

    "landmark_statue_cipher": {
        "name": "Patung Bersandi",
        "type": "landmark",
        "desc": "Patung raksasa tanpa wajah yang memegang buku batu. Ada ukiran yang terus berubah di alasnya.",
        "interaction": "solve",
        "effect": "trigger_puzzle",
        "msg": "📜 Patung itu menuntut jawaban atas teka-tekinya sebelum kau diizinkan lewat.",
        "requirement": None
    },

    "landmark_mystic_lake": {
        "name": "Danau Mistik",
        "type": "landmark",
        "desc": "Air danau ini berwarna perak kebiruan. Kau bisa melihat pantulan dirimu di masa depan di permukaannya.",
        "interaction": "drink",
        "effect": "buff_luck",
        "msg": "💧 Air danau terasa manis. Kau merasa hari ini keberuntungan akan berpihak padamu! (Luck Buff)",
        "requirement": "item_botol_kosong"
    }
}

# --- LOGIKA INTERAKSI LANDMARK ---

def process_landmark_interaction(player, landmark_id):
    """
    Logika untuk mengeksekusi efek dari landmark terhadap pemain.
    Mengembalikan: (success_status, message)
    """
    landmark = LANDMARKS.get(landmark_id)
    if not landmark:
        return False, "❌ Landmark tidak ditemukan."

    # 1. Cek Syarat Item (Requirement)
    req_item = landmark.get('requirement')
    if req_item and req_item not in player.get('inventory', []):
        return False, f"❌ Kamu membutuhkan {req_item.replace('item_', '').replace('_', ' ')} untuk berinteraksi di sini."

    # 2. Eksekusi Efek Berdasarkan Jenisnya
    effect = landmark.get('effect')
    
    if effect == "clear_debuffs":
        # Menghapus semua status efek negatif
        player['status_effects'] = []
        
    elif effect == "restore_mp":
        # Memulihkan MP ke nilai maksimal
        player['mp'] = player.get('max_mp', 100)
        
    elif effect == "buff_luck":
        # Memberikan bonus keberuntungan permanen/sementara
        if 'stats' not in player:
            player['stats'] = {}
        player['stats']['luck'] = player['stats'].get('luck', 0) + 5
        
    elif effect == "random_loot":
        # Logika penggalian dengan risiko kemunculan musuh (Ambush)
        if random.random() < landmark.get('danger_chance', 0):
            return "ambush", "⚠️ Sesuatu yang busuk bangkit dari tanah! Persiapkan senjatamu!"
        
        # Berikan item acak ke dalam inventory
        if 'inventory' not in player:
            player['inventory'] = []
        player['inventory'].append("item_old_relic")
        
    elif effect == "trigger_puzzle":
        # Menandai bahwa pemain harus menghadapi kuis/puzzle khusus
        return "puzzle", landmark['msg']

    return True, landmark['msg']

def get_landmark_data(landmark_id):
    """Mengambil data landmark berdasarkan ID."""
    return LANDMARKS.get(landmark_id)

def get_all_landmarks():
    """Mengambil seluruh daftar landmark."""
    return LANDMARKS
