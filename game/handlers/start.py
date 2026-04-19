# game/handlers/start.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

# === LOGIC & DATABASE ===
from database import get_player, update_player
from game.logic.states import GameState
from game.logic.stats import calculate_total_stats
from game.logic.menu_handler import get_main_reply_keyboard

# Bungkus dalam try-except jika file quests.py belum lengkap
try:
    from game.data.quests import get_random_daily_quests
except ImportError:
    def get_random_daily_quests(count): return []

# === UI & CONSTANTS ===
# Lang sudah dihapus, kita menggunakan get_text untuk Multi-Bahasa
from game.ui_constants import Icon, Text, get_text
from utils.helper_ui import create_hp_bar, create_mp_bar

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.first_name
    
    # Ambil data pemain (jika baru, akan otomatis terbuat di MongoDB)
    player = get_player(user_id, username)
    lang = player.get('lang', 'id') # Ambil preferensi bahasa
    
    updates = {}
    
    # Inisialisasi data penting jika belum ada (Backward Compatibility)
    if 'skill_usages' not in player: 
        updates['skill_usages'] = {}
    if 'skill_cooldowns' not in player: 
        updates['skill_cooldowns'] = {}
    
    # Inisialisasi quest harian
    if not player.get('active_quests'):
        new_quests = get_random_daily_quests(count=3)
        if new_quests:
            updates['active_quests'] = new_quests
            player['active_quests'] = new_quests

    # Belas kasihan: beri energi awal jika pemain stuck
    if player.get('energy', 0) <= 0:
        updates['energy'] = 20
        player['energy'] = 20
        
    if updates:
        update_player(user_id, updates)
        
    # Kalkulasi stat terbaru sebelum masuk eksplorasi
    player['stats'] = calculate_total_stats(player)
    
    # Set status State Machine ke "Sedang Menjelajah"
    await state.set_state(GameState.exploring)
    
    # UI BARU: Lebih ringkas dan memanggil fungsi Multi-Bahasa
    welcome_msg = (
        f"{Text.LINE}\n"
        f"📜 **THE ARCHIVUS**\n"
        f"{Text.LINE}\n"
        f"Selamat datang, **{username}**\n\n"
        f"{Icon.LEVEL} {get_text(lang, 'LEVEL')} {player.get('level', 1)} "
        f"• Cycle {player.get('cycle', 1)}\n"
        f"{Icon.NPC} {player.get('current_job', 'Novice')}\n\n"
        f"{create_hp_bar(player.get('hp', 100), player.get('max_hp', 100))}\n"
        f"{create_mp_bar(player.get('mp', 0), player.get('max_mp', 50))}\n\n"
        f"{Icon.ENERGY} Energi: `{player.get('energy', 100)}/100`\n"
        f"{Icon.GOLD} Gold: `{player.get('gold', 0):,}G`\n"
        f"{Text.LINE}\n"
        f"{Icon.QUEST} {len(player.get('active_quests', []))} misi aktif\n\n"
        f"💬 _Ketik /help untuk panduan_"
    )
    
    # Mengirim pesan tanpa parameter parse_mode (sudah di-handle main.py)
    await message.answer(
        welcome_msg, 
        reply_markup=get_main_reply_keyboard(player)
    )

@router.message(F.text == "/help")
async def help_handler(message: Message):
    # UI BARU: Terstruktur dan menggunakan Icon terpusat dari ui_constants
    help_text = (
        f"{Icon.INFO} **PANDUAN ARCHIVUS**\n"
        f"{Text.LINE}\n\n"
        
        f"**🧭 EKSPLORASI**\n"
        f"• Gunakan tombol arah di bawah layar untuk berjalan.\n"
        f"• 1 langkah = -1 {Icon.ENERGY} Energi.\n"
        f"• Cari {Icon.LOC_CAFE} Kedai atau {Icon.LOC_INN} Penginapan jika energi kritis.\n\n"
        
        f"**{Icon.ATTACK} PERTEMPURAN**\n"
        f"• {Icon.ATTACK} Serang: Serangan standar.\n"
        f"• {Icon.SKILL} Skill: Serangan khusus (Membutuhkan {Icon.MP} MP).\n"
        f"• {Icon.DEFENSE} Bertahan: Mengurangi *damage* musuh.\n"
        f"• {Icon.DODGE} Menghindar: Peluang menghindari serangan total.\n\n"
        
        f"**{Icon.QUEST} MISI HARIAN**\n"
        f"• 3 misi baru diberikan setiap hari.\n"
        f"• Progress dihitung otomatis saat kamu bermain.\n\n"
        
        f"**{Icon.GEAR} PERALATAN**\n"
        f"• Perhatikan *durability* (daya tahan) senjatamu.\n"
        f"• Perbaiki perlengkapan yang rusak di menu 📊 Profil.\n\n"
        
        f"{Text.LINE}\n"
        f"💡 _Semakin dalam kamu turun, semakin gelap tempat ini._"
    )
    
    await message.answer(help_text)
