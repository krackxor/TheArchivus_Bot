from database import get_player, update_player

def use_skill_reveal(user_id, puzzle_data):
    """
    Logika Skill Revelatio: Membuka satu huruf yang tersembunyi.
    Biaya: 10 MP per penggunaan.
    """
    player = get_player(user_id)
    cost = 10
    
    # 1. Validasi MP
    if player['mp'] < cost:
        return False, "🔮 MP kamu tidak cukup untuk merapal mantra!", puzzle_data.get('current_hint')

    # 2. Ambil data jawaban dan hint saat ini
    answer = puzzle_data['answer']
    # Jika hint belum ada (pertama kali pakai), buat string "_" sesuai panjang jawaban
    # Tetap pertahankan spasi jika jawaban memiliki spasi
    if 'current_hint' not in puzzle_data or not puzzle_data['current_hint']:
        current_hint = "".join([" " if char == " " else "_" for char in answer])
    else:
        current_hint = puzzle_data['current_hint']
    
    # 3. Cari indeks huruf yang masih tertutup (berupa "_")
    hidden_indices = [i for i, char in enumerate(current_hint) if char == "_"]
    
    # 4. Jika sudah terbuka semua
    if not hidden_indices:
        return False, "✨ Kebenaran sudah terungkap sepenuhnya!", current_hint

    # 5. Buka satu huruf (kita ambil indeks pertama yang ditemukan agar teratur dari kiri ke kanan)
    idx_to_reveal = hidden_indices[0]
    new_hint_list = list(current_hint)
    new_hint_list[idx_to_reveal] = answer[idx_to_reveal]
    new_hint = "".join(new_hint_list)

    # 6. Kurangi MP di database
    update_player(user_id, {"mp": player['mp'] - cost})
    
    return True, f"✨ Revelatio! Satu huruf terungkap. (-10 MP)", new_hint
