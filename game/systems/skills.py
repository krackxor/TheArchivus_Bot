# game/systems/skills.py

"""
Sistem Skill (Combat Skills)
Logika untuk kemampuan khusus pemain saat fase pertarungan.
Terintegrasi dengan MP, Artifacts, dan State Puzzle.
"""

import random
from database import get_player, update_player

def use_skill_reveal(user_id, puzzle_data):
    """
    Logika Skill Revelatio: Membuka satu huruf yang tersembunyi secara acak.
    Biaya: 10 MP (Atau 5 MP jika memiliki Wisdom Tome).
    """
    player = get_player(user_id)
    
    # --- INTEGRASI ARTIFACT & EQUIPMENT ---
    # Memeriksa apakah pemain memiliki 'Wisdom Tome' baik di tas maupun yang dipakai
    # Dalam arsitektur kita, Artefak permanen ada di list 'artifacts'
    artifacts = player.get('artifacts', [])
    has_wisdom_tome = any(art == 'wisdom_tome' or (isinstance(art, dict) and art.get('id') == 'wisdom_tome') for art in artifacts)
    
    # Biaya dasar 10 MP, diskon jadi 5 MP jika punya artifact
    cost = 5 if has_wisdom_tome else 10
    
    # 1. Validasi MP
    current_mp = player.get('mp', 0)
    if current_mp < cost:
        return False, f"🔮 Fokusmu memudar... (Butuh {cost} MP, MP saat ini: {current_mp})", puzzle_data.get('current_hint', '')

    # 2. Ambil data jawaban dan hint saat ini
    answer = puzzle_data['answer']
    current_hint = puzzle_data.get('current_hint', "")

    # Inisialisasi hint jika masih kosong (awal turn)
    if not current_hint:
        # Gunakan karakter asli untuk simbol/spasi, dan "_" untuk huruf/angka
        current_hint = "".join([char if not char.isalnum() else "_" for char in answer])
    
    # 3. Cari indeks huruf yang masih tertutup (berupa "_")
    hidden_indices = [i for i, char in enumerate(current_hint) if char == "_"]
    
    # 4. Jika sudah terbuka semua (safety check)
    if not hidden_indices:
        return False, "✨ Kebenaran telah terungkap sepenuhnya!", current_hint

    # 5. Buka satu huruf secara ACAK (Logic: RNG)
    idx_to_reveal = random.choice(hidden_indices)
    new_hint_list = list(current_hint)
    
    # Pastikan mengambil karakter asli dari jawaban (case sensitive)
    new_hint_list[idx_to_reveal] = answer[idx_to_reveal]
    new_hint = "".join(new_hint_list)

    # 6. Update Database
    update_player(user_id, {"mp": current_mp - cost})
    
    # 7. Pesan Notifikasi yang Imersif
    if has_wisdom_tome:
        msg = f"📖 **Wisdom Tome** beresonansi! Satu rahasia tersingkap. (-{cost} MP)"
    else:
        msg = f"✨ **Revelatio!** Sihirmu menyingkap satu huruf kebenaran. (-{cost} MP)"
        
    return True, msg, new_hint
