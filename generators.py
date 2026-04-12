import random

# --- KONFIGURASI ITEM ---
# Item-item yang bisa diminta atau diberikan oleh NPC
ITEM_POOL = [
    {"id": "item_pedang", "name": "Pedang Karat"},
    {"id": "item_batu", "name": "Batu Jiwa"},
    {"id": "item_emas", "name": "Batangan Emas"},
    {"id": "item_buku", "name": "Lembaran Kosong"}
]

NPC_NAMES = ["The Wanderer", "Hollow Sentinel", "Echo of Silence", "Pale Weaver", "Blind Scholar"]
NPC_TRAITS = ["Gemetar", "Tenang", "Sinis", "Melankolis", "Marah"]

def generate_npc(is_liar=False):
    name = random.choice(NPC_NAMES)
    trait = random.choice(NPC_TRAITS)
    
    # --- LOGIKA PERMINTAAN (REQUIREMENT) ---
    # NPC bisa minta Gold atau Item secara acak
    if random.random() > 0.5:
        # Minta Gold (10 - 50 secara acak)
        req = {
            "type": "gold", 
            "amount": random.randint(10, 50), 
            "name": "Gold"
        }
    else:
        # Minta Item dari pool
        selected_item = random.choice(ITEM_POOL)
        req = {
            "type": "item", 
            "amount": 1, 
            "id": selected_item['id'], 
            "name": selected_item['name']
        }

    # --- LOGIKA DIALOG MANIPULATIF ---
    if is_liar:
        # NPC JAHAT: Bicara manis untuk menjebak
        dialogs = [
            "Anak muda, tolonglah orang tua ini. Aku punya rahasia besar untukmu...",
            "Aku menemukan barang berharga ini, tapi aku butuh sedikit bantuanmu.",
            "Wajahmu tampak lelah, berikan apa yang kuminta dan aku akan menyembuhkanmu.",
            "Tenanglah, aku bukan monster. Aku hanya ingin bertukar sedikit keberuntungan."
        ]
    else:
        # NPC BAIK: Bisa saja bicara kasar/marah padahal niatnya menolong
        dialogs = [
            "Berikan barang itu padaku atau kau akan menyesal di lorong berikutnya!",
            "Cepat serahkan! Archivus tidak punya waktu untuk Weaver yang lamban sepertimu!",
            "Kau tampak bodoh membawa barang itu. Biar aku yang mengurusnya untukmu.",
            "Jangan banyak tanya! Berikan saja jika kau masih ingin melihat matahari besok!"
        ]
    
    selected_dialog = random.choice(dialogs)
    
    return {
        "identity": f"{name} yang {trait}",
        "is_liar": is_liar,
        "dialog": selected_dialog,
        "requirement": req
    }

def get_death_message(cause):
    # Fallback jika database belum siap dengan naskah death_note
    death_notes = [
        "Tinta habis. Ceritamu terhenti di tengah kalimat.",
        "Namamu perlahan memudar dari halaman Archivus.",
        "Kegelapan menelan Weaver terakhir. Cahaya itu kini padam."
    ]
    return random.choice(death_notes)
