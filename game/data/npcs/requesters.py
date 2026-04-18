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

def get_requester_data(npc_id):
    """Mengambil data NPC peminta berdasarkan ID."""
    return REQUESTER_NPCS.get(npc_id)

def get_all_requesters():
    """Mengambil seluruh database NPC requester."""
    return REQUESTER_NPCS
