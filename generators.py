import random

def generate_npc(player_gold=0, is_liar=None):
    if is_liar is None:
        is_liar = random.choice([True, False])
    
    # Pilih nama tanpa embel-embel trait
    name = random.choice(NPC_NAMES)
    req = None
    
    # --- 1. FASE EARLY (Gold < 300) ---
    if player_gold < 300:
        if is_liar:
            dialogs = [
                "Ke Utara saja, Weaver. Aku melihat cahaya pintu keluar di sana.",
                "Barat adalah jalan paling cepat menuju Toko. Jangan lewatkan itu.",
                "Aku bersumpah Timur sedang kosong. Monster-monster sedang tidur."
            ]
        else:
            dialogs = [
                "Hati-hati, aku mendengar geraman di Selatan. Putar baliklah.",
                "Gunakan jalan Barat jika ingin menghindari jebakan di lorong ini.",
                "Tetaplah di jalur Utara, Archivus sedang stabil di arah itu."
            ]
            
    # --- 2. FASE MID (300 <= Gold < 800) ---
    elif 300 <= player_gold < 800:
        amt = int(player_gold * 0.15)
        req = {"type": "gold", "amount": amt, "name": "Gold"}
        
        if is_liar:
            dialogs = [
                f"Beri aku {amt} Gold, dan aku akan membisikkan rahasia besar padamu.",
                f"Aku butuh {amt} Gold. Sebagai gantinya, kau akan selamat dari maut."
            ]
        else:
            dialogs = [
                f"Aku butuh {amt} Gold untuk menyalakan lentera ini kembali. Bantu aku?",
                f"Sisihkan {amt} Gold untukku, aku akan menjamin langkahmu lebih kuat."
            ]

    # --- 3. FASE LATE (Gold >= 800) ---
    else:
        if random.random() > 0.5:
            amt = int(player_gold * 0.3)
            req = {"type": "gold", "amount": amt, "name": "Gold"}
            dialogs = [f"Harta itu terlalu berat untukmu. Setor {amt} Gold padaku sekarang!"]
        else:
            selected_item = random.choice(ITEM_POOL)
            req = {"type": "item", "amount": 1, "id": selected_item['id'], "name": selected_item['name']}
            dialogs = [f"Berikan {selected_item['name']}-mu. Orang mati tidak butuh barang mewah."]

    return {
        # Identity HANYA berisi Nama: misal "The Wanderer"
        "identity": name, 
        "is_liar": is_liar,
        "dialog": random.choice(dialogs),
        "requirement": req
    }
