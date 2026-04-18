# game/data/npcs/requesters.py

"""
NPC Requester Database - The Archivus
Berisi NPC yang meminta item dari pemain. 
Mekanik: Kejutan (Hadiah tersembunyi) vs Jebakan (Penalti HP/Gold).
"""

REQUESTER_NPCS = {
    # --- NPC JUJUR (REWARD) ---
    "npc_beggar_honest": {
        "name": "Pengemis Tua",
        "role": "requester",
        "desc": "Seorang pria tua dengan pakaian compang-camping. Matanya terlihat tulus namun sangat lelah.",
        "dialog": "Tuan... tolong, hanya sepotong roti untuk bertahan hari ini. Aku tidak punya apa-apa lagi...",
        "request_item": "bread_01",
        "success_msg": "Pengemis itu menangis haru. 'Terima kasih, Weaver. Ambillah ini, aku menemukannya di reruntuhan.'",
        "reward": {
            "gold": 150,
            "item": "artifact_stone",
            "exp": 100
        }
    },

    "npc_lost_child": {
        "name": "Anak Hilang",
        "role": "requester",
        "desc": "Seorang anak kecil yang gemetar ketakutan di balik pilar batu.",
        "dialog": "Aku kedinginan... apa kau punya sesuatu yang hangat? Tolong aku...",
        "request_item": "item_mantel_bulu",
        "success_msg": "Anak itu tersenyum lebar. 'Hangat sekali! Ayahku bilang aku harus memberikan ini jika ada orang baik.'",
        "reward": {
            "gold": 500,
            "item": "rare_key_01",
            "exp": 300
        }
    },

    # --- NPC PENIPU (TRAP) ---
    "npc_beggar_evil": {
        "name": "Pria Bungkuk",
        "role": "requester",
        "desc": "Ia membungkuk aneh. Dari balik tudungnya, kau melihat seringai tipis yang tidak wajar.",
        "dialog": "Roti... berikan aku rotimu, petualang... Aku sangat, sangat lapar...",
        "request_item": "bread_01",
        "is_trap": True,
        "trap": {
            "hp_loss": 40,
            "gold_loss": 100,
            "msg": "Saat kau mendekat, ia menarik belati beracun dan menusuk lambungmu! 'Bodoh sekali!' teriaknya sambil lari ke kegelapan."
        }
    },

    "npc_mysterious_traveler": {
        "name": "Pengembara Misterius",
        "role": "requester",
        "desc": "Pria ini mengenakan topeng porselen. Tangannya terus bergerak gelisah di balik jubahnya.",
        "dialog": "Aku butuh ramuan biru itu... Berikan padaku, dan aku akan menunjukkan jalan keluar.",
        "request_item": "pot_blue_1",
        "is_trap": True,
        "trap": {
            "hp_loss": 20,
            "mp_loss": 30,
            "msg": "Ia melemparkan botol ramuan itu ke tanah hingga meledak menjadi gas tidur! Kamu terbangun dengan rasa sakit dan kehilangan energi."
        }
    }
}

# --- LOGIKA INTERAKSI REQUESTER ---

def process_npc_request(player, npc_id):
    """
    Memproses permintaan item oleh NPC.
    Mengembalikan: (success, message)
    """
    npc = REQUESTER_NPCS.get(npc_id)
    if not npc:
        return False, "❌ NPC tidak ditemukan."

    item_required = npc['request_item']
    
    # Cek apakah item ada di inventory pemain
    if item_required not in player.get('inventory', []):
        return False, f"❌ Kamu tidak memiliki {item_required.replace('_', ' ')}."

    # Proses pengambilan item dari inventory
    player['inventory'].remove(item_required)

    # --- LOGIKA TRAP (JEBAKAN) ---
    if npc.get('is_trap'):
        trap = npc['trap']
        player['hp'] -= trap['hp_loss']
        
        if 'gold_loss' in trap:
            player['gold'] = max(0, player['gold'] - trap['gold_loss'])
            
        if 'mp_loss' in trap:
            player['mp'] = max(0, player.get('mp', 0) - trap['mp_loss'])
            
        return True, f"⚠️ {trap['msg']} (HP -{trap['hp_loss']})"

    # --- LOGIKA REWARD (HADIAH) ---
    reward = npc['reward']
    player['gold'] += reward.get('gold', 0)
    player['exp'] += reward.get('exp', 0)
    
    if 'item' in reward:
        if 'inventory' not in player:
            player['inventory'] = []
        player['inventory'].append(reward['item'])
        
    return True, f"✅ {npc['success_msg']}"

def get_requester_data(npc_id):
    """Mengambil data NPC peminta berdasarkan ID."""
    return REQUESTER_NPCS.get(npc_id)

def get_all_requesters():
    """Mengambil seluruh database NPC requester."""
    return REQUESTER_NPCS
