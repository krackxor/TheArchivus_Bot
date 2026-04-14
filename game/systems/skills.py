import random
from database import get_player, update_player

def use_skill_reveal(user_id, puzzle_data):
    """
    Logika Skill Revelatio: Membuka satu huruf yang tersembunyi secara acak.
    Biaya: 10 MP (Atau 5 MP jika memiliki Wisdom Tome).
    """
    player = get_player(user_id)
    
    # --- INTEGRASI ARTIFACT ---
    # Cek apakah pemain memiliki 'Wisdom Tome' (Kitab Kebijaksanaan)
    artifacts = player.get('artifacts', [])
    has_wisdom_tome = any(art.get('id') == 'wisdom_tome' for art in artifacts)
    
    # Biaya dasar 10 MP, diskon jadi 5 MP jika punya artifact
    cost = 5 if has_wisdom_tome else 10
    
    # 1. Validasi MP
    if player.get('mp', 0) < cost:
        return False, f"🔮 Fokusmu memudar... (Butuh {cost} MP untuk merapal ini)", puzzle_data.get('current_hint', '')

    # 2. Ambil data jawaban
    answer = puzzle_data['answer']
    
    # Inisialisasi hint jika belum ada
    if 'current_hint' not in puzzle_data or not puzzle_data['current_hint']:
        # Pertahankan spasi dan tanda baca (hanya ubah huruf/angka menjadi "_")
        current_hint = "".join([char if not char.isalnum() else "_" for char in answer])
    else:
        current_hint = puzzle_data['current_hint']
    
    # 3. Cari indeks huruf yang masih tertutup (berupa "_")
    hidden_indices = [i for i, char in enumerate(current_hint) if char == "_"]
    
    # 4. Jika sudah terbuka semua
    if not hidden_indices:
        return False, "✨ Kebenaran telah terungkap sepenuhnya!", current_hint

    # 5. Buka satu huruf secara ACAK (Memberikan efek ajaib yang lebih natural)
    idx_to_reveal = random.choice(hidden_indices)
    new_hint_list = list(current_hint)
    # Gunakan huruf asli dari jawaban (termasuk huruf besar/kecil yang sesuai)
    new_hint_list[idx_to_reveal] = answer[idx_to_reveal]
    new_hint = "".join(new_hint_list)

    # 6. Kurangi MP di database
    update_player(user_id, {"mp": player['mp'] - cost})
    
    # 7. Teks Notifikasi Dinamis
    if has_wisdom_tome:
        msg = f"📖 Kitab Kebijaksanaan beresonansi! Satu huruf terungkap. (-{cost} MP)"
    else:
        msg = f"✨ Revelatio! Sihirmu menyingkap satu kebenaran. (-{cost} MP)"
        
    return True, msg, new_hint
