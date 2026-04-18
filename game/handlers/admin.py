# game/handlers/admin.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from database import get_player, update_player
from game.items import get_item # Ditambahkan untuk validasi item

router = Router()

# Ganti dengan ID Telegram kamu (gunakan bot @userinfobot untuk mengetahui ID-mu)
# Tips: Di masa depan, lebih aman memindahkan ADMIN_ID ini ke file config.py
ADMIN_ID = 123456789  

def is_admin(user_id: int) -> bool:
    """Mengecek apakah user memiliki otorisasi sebagai admin."""
    return user_id == ADMIN_ID

# ==============================================================================
# 0. COMMAND: /admin (Menu Bantuan Khusus Developer)
# ==============================================================================
@router.message(Command("admin"))
async def admin_menu_help(message: Message):
    user_id = message.from_user.id
    if not is_admin(user_id): return
    
    help_text = (
        "🛠️ **ARCHIVUS OVERSEER CONSOLE** 🛠️\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "Selamat datang, Creator. Berikut alat pengujian Anda:\n\n"
        "💰 `/givegold [jumlah]` - Menambahkan/Mengurangi Gold\n"
        "🎁 `/giveitem [item_id]` - Memasukkan item ke tas\n"
        "⭐ `/giveexp [jumlah]` - Memberikan EXP instan\n"
        "💖 `/heal` - Memulihkan 100% HP, MP, dan Energi\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )
    await message.answer(help_text, parse_mode="Markdown")

# ==============================================================================
# 1. COMMAND: /givegold (Memberi Gold)
# ==============================================================================
@router.message(Command("givegold"))
async def admin_give_gold(message: Message):
    user_id = message.from_user.id
    if not is_admin(user_id): return
    
    try:
        # Membaca format: /givegold 5000 (bisa juga pakai minus: /givegold -100)
        amount = int(message.text.split()[1])
        p = get_player(user_id)
        new_gold = max(0, p.get('gold', 0) + amount) # Cegah minus
        
        update_player(user_id, {"gold": new_gold})
        await message.answer(f"🛠️ [ADMIN] Saldo Gold disesuaikan. Total saat ini: **{new_gold:,} G**", parse_mode="Markdown")
    except (IndexError, ValueError):
        await message.answer("⚠️ Format salah. Gunakan: `/givegold [jumlah angka]`", parse_mode="Markdown")

# ==============================================================================
# 2. COMMAND: /giveitem (Memberi Item Spesifik)
# ==============================================================================
@router.message(Command("giveitem"))
async def admin_give_item(message: Message):
    user_id = message.from_user.id
    if not is_admin(user_id): return
    
    try:
        # Membaca format: /giveitem potion_heal
        item_id = message.text.split()[1].lower()
        
        # Validasi: Cek apakah item benar-benar ada di database (game.items)
        if not get_item(item_id):
            return await message.answer(f"⚠️ Item dengan ID `{item_id}` tidak ditemukan di database game.items!", parse_mode="Markdown")
            
        p = get_player(user_id)
        inventory = p.get('inventory', [])
        inventory.append(item_id)
        
        update_player(user_id, {"inventory": inventory})
        await message.answer(f"🛠️ [ADMIN] Berhasil menyisipkan item `{item_id}` ke dalam tas.", parse_mode="Markdown")
    except IndexError:
        await message.answer("⚠️ Format salah. Gunakan: `/giveitem [item_id]`", parse_mode="Markdown")

# ==============================================================================
# 3. COMMAND: /giveexp (Menambahkan EXP Cepat)
# ==============================================================================
@router.message(Command("giveexp"))
async def admin_give_exp(message: Message):
    user_id = message.from_user.id
    if not is_admin(user_id): return
    
    try:
        amount = int(message.text.split()[1])
        p = get_player(user_id)
        new_exp = p.get('exp', 0) + amount
        
        update_player(user_id, {"exp": new_exp})
        await message.answer(f"🛠️ [ADMIN] +{amount} EXP diberikan. *(Catatan: Level up akan terpicu otomatis pada aksi pertarungan selanjutnya)*", parse_mode="Markdown")
    except (IndexError, ValueError):
        await message.answer("⚠️ Format salah. Gunakan: `/giveexp [jumlah angka]`", parse_mode="Markdown")

# ==============================================================================
# 4. COMMAND: /heal (Memulihkan HP & MP & Energi 100%)
# ==============================================================================
@router.message(Command("heal"))
async def admin_heal_full(message: Message):
    user_id = message.from_user.id
    if not is_admin(user_id): return
    
    p = get_player(user_id)
    update_player(user_id, {
        "hp": p.get('max_hp', 100),
        "mp": p.get('max_mp', 50),
        "energy": 100
    })
    
    await message.answer("🛠️ [ADMIN] Intervensi sistem: Tubuh Weaver telah dipulihkan ke 100% (HP, MP, Energi).")
