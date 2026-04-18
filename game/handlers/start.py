# game/handlers/start.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

# Import logika game
from database import get_player, update_player
from game.logic.states import GameState
from game.logic.stats import calculate_total_stats
from game.logic.menu_handler import get_main_reply_keyboard
from utils.helper_ui import create_hp_bar, create_mp_bar

# Import Master Data untuk Inisialisasi
from game.data.quests import get_random_daily_quests

# Inisialisasi Router untuk file ini
router = Router()

@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.first_name
    
    # Ambil atau buat data pemain di database
    player = get_player(user_id, username)
    
    # --- INISIALISASI DATA PEMAIN BARU / LOGIN ---
    updates = {}
    
    # 1. Pastikan struktur data skill ada
    if 'skill_usages' not in player: updates['skill_usages'] = {}
    if 'skill_cooldowns' not in player: updates['skill_cooldowns'] = {}
    
    # 2. Inisialisasi Misi Harian jika belum ada
    if not player.get('active_quests'):
        new_quests = get_random_daily_quests(count=3)
        updates['active_quests'] = new_quests
        player['active_quests'] = new_quests

    # 3. Belas Kasihan Archivus: Beri energi awal jika 0
    if player.get('energy', 0) <= 0:
        updates['energy'] = 20
        player['energy'] = 20
        
    # Simpan semua inisialisasi ke database jika ada perubahan
    if updates:
        update_player(user_id, updates)
        
    # Hitung stat berdasarkan equipment yang sedang dipakai
    player['stats'] = calculate_total_stats(player) 
    
    # Kunci state pemain ke mode penjelajahan
    await state.set_state(GameState.exploring)
    
    # Render UI Pesan Sambutan
    welcome_msg = (
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📜 *THE ARCHIVUS* 📜\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Selamat datang kembali, {username}\n\n"
        f"Kau terjebak di dimensi tanpa ujung ini sebagai\n"
        f"*{player.get('current_job', 'Novice Weaver')}*.\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔄 Cycle: `{player.get('cycle', 1)}` | 📈 Level: `{player.get('level', 1)}`\n\n"
        f"{create_hp_bar(player.get('hp',100), player.get('max_hp',100))}\n"
        f"{create_mp_bar(player.get('mp', 0), player.get('max_mp', 50))}\n\n"
        f"⚡ Energi: `{player.get('energy', 100)}/100`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 *Misi Aktif: {len(player.get('active_quests', []))} Misi*\n"
        f"🔮 *Ketik /help untuk panduan kontrol.*"
    )
    
    # Tampilkan keyboard navigasi di bawah layar
    await message.answer(welcome_msg, reply_markup=get_main_reply_keyboard(player), parse_mode="Markdown")

@router.message(F.text == "/help")
async def help_handler(message: Message):
    help_text = (
        "📜 **ARCHIVUS PROTOCOL: GUIDANCE**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "Selamat datang di pusat bantuan, Weaver. Berikut instruksi dasar untuk bertahan hidup:\n\n"
        
        "🧭 **EKSPLORASI & ENERGI**\n"
        "• Gunakan tombol arah untuk menjelajah.\n"
        "• Tiap langkah mengonsumsi **1 Energi**.\n"
        "• Jika Energi 0, gunakan **Makanan** atau temukan **Rest Area**.\n\n"
        
        "⚔️ **SISTEM PERTEMPURAN**\n"
        "• **Skill:** Serangan kuat menggunakan MP.\n"
        "• **Block:** Mitigasi damage & pulihkan sedikit HP.\n"
        "• **Dodge:** Hindaran total & bonus MP jika sukses.\n"
        "• **Combo:** Serangan beruntun meningkatkan bonus Gold/EXP.\n\n"
        
        "🎯 **MISI HARIAN (QUESTS)**\n"
        "• Selesaikan misi aktif untuk **Reward Besar**.\n"
        "• Progres dihitung otomatis saat bertarung, belanja, atau melangkah.\n\n"
        
        "🛠️ **GEAR & DURABILITAS**\n"
        "• Senjata/Armor yang rusak (0 durabilitas) kehilangan daya tempur.\n"
        "• Perbaiki Gear di **Bengkel Aethelred** melalui menu Profil.\n\n"
        
        "🧠 **KECERDASAN (INTEL)**\n"
        "• Jawab Quiz dari NPC atau buku kuno untuk menaikkan Intel.\n"
        "• Intel tinggi membuka akses ke **Landmark** & Event langka.\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🔮 *Ingatan adalah senjata terbaikmu di sini.*"
    )
    await message.answer(help_text, parse_mode="Markdown")
