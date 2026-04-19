# game/handlers/start.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from database import get_player, update_player
from game.logic.states import GameState
from game.logic.stats import calculate_total_stats
from game.logic.menu_handler import get_main_reply_keyboard
from game.data.quests import get_random_daily_quests

# Import UI Constants untuk konsistensi
from game.ui_constants import Icon, Text, Lang
from utils.helper_ui import create_hp_bar, create_mp_bar, create_status_card_compact

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.first_name
    
    player = get_player(user_id, username)
    
    # Inisialisasi data pemain
    updates = {}
    
    if 'skill_usages' not in player: 
        updates['skill_usages'] = {}
    if 'skill_cooldowns' not in player: 
        updates['skill_cooldowns'] = {}
    
    # Inisialisasi quest harian
    if not player.get('active_quests'):
        new_quests = get_random_daily_quests(count=3)
        updates['active_quests'] = new_quests
        player['active_quests'] = new_quests

    # Belas kasihan: beri energi awal
    if player.get('energy', 0) <= 0:
        updates['energy'] = 20
        player['energy'] = 20
        
    if updates:
        update_player(user_id, updates)
        
    player['stats'] = calculate_total_stats(player)
    await state.set_state(GameState.exploring)
    
    # UI BARU: Lebih ringkas dan mudah dibaca
    welcome_msg = (
        f"{Text.LINE}\n"
        f"📜 **THE ARCHIVUS**\n"
        f"{Text.LINE}\n"
        f"Selamat datang, **{username}**\n\n"
        f"{Icon.LEVEL} Level {player.get('level', 1)} "
        f"• Cycle {player.get('cycle', 1)}\n"
        f"🎭 {player.get('current_job', 'Novice Weaver')}\n\n"
        f"{create_hp_bar(player.get('hp', 100), player.get('max_hp', 100))}\n"
        f"{create_mp_bar(player.get('mp', 0), player.get('max_mp', 50))}\n\n"
        f"{Icon.ENERGY} Energi: `{player.get('energy', 100)}/100`\n"
        f"{Icon.GOLD} Gold: `{player.get('gold', 0):,}G`\n"
        f"{Text.LINE}\n"
        f"{Icon.QUEST} {len(player.get('active_quests', []))} misi aktif\n\n"
        f"💬 _Ketik /help untuk bantuan_"
    )
    
    await message.answer(
        welcome_msg, 
        reply_markup=get_main_reply_keyboard(player), 
        parse_mode="Markdown"
    )

@router.message(F.text == "/help")
async def help_handler(message: Message):
    # UI BARU: Lebih terstruktur dan ringkas
    help_text = (
        f"{Icon.INFO} **PANDUAN ARCHIVUS**\n"
        f"{Text.LINE}\n\n"
        
        f"**🧭 EKSPLORASI**\n"
        f"• Pakai tombol arah untuk jalan\n"
        f"• 1 langkah = 1 energi\n"
        f"• Cari Rest Area saat energi habis\n\n"
        
        f"**{Icon.ATTACK} PERTEMPURAN**\n"
        f"• Serang: Damage standar\n"
        f"• Skill: Serangan kuat (-MP)\n"
        f"• Bertahan: Kurangi damage\n"
        f"• Menghindar: Hindari total\n"
        f"• Combo: Serang beruntun = bonus\n\n"
        
        f"**{Icon.QUEST} MISI HARIAN**\n"
        f"• 3 misi baru setiap hari\n"
        f"• Selesaikan untuk reward besar\n"
        f"• Progress otomatis terhitung\n\n"
        
        f"**{Icon.GEAR} PERALATAN**\n"
        f"• Durability habis = gear rusak\n"
        f"• Perbaiki di Bengkel (menu Profil)\n"
        f"• Equipment rusak = lemah\n\n"
        
        f"{Text.LINE}\n"
        f"💡 _Gunakan tas dengan bijak_"
    )
    
    await message.answer(help_text, parse_mode="Markdown")
