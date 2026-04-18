# game/handlers/event.py

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

# === IMPORTS UTAMA ===
from database import get_player, update_player
from game.logic.states import GameState
from game.logic.stats import calculate_total_stats

# Import fungsi UI & Sistem
from game.logic.menu_handler import get_main_reply_keyboard
from game.systems.achievements import update_quest_progress

# Import sistem event spesifik
from game.systems.events import process_event_outcome
from game.logic.event_handler import handle_event_interaction

# Inisialisasi Router
router = Router()

# ==============================================================================
# 1. INTERAKSI TOMBOL (NPC, HAZARD, LANDMARK)
# ==============================================================================
@router.callback_query(F.data.startswith("evt_"))
async def process_events_callback(callback: CallbackQuery, state: FSMContext):
    """
    Menangani klik tombol dari interaksi dunia eksplorasi.
    Contoh: Menjawab tantangan NPC, membuka peti, atau memeriksa lokasi.
    """
    user_id = callback.from_user.id
    p = get_player(user_id)
    
    # Pastikan stats terbaru ikut terbawa untuk perhitungan di event_handler
    # (Misal: Sebuah event butuh mengecek stat Intelligence atau Luck)
    p['stats'] = calculate_total_stats(p)
    
    # Serahkan eksekusi logika mendetail ke handler event pusat
    await handle_event_interaction(callback, state, p)


# ==============================================================================
# 2. JAWABAN TEKA-TEKI / PUZZLE / KUIS (TEXT INPUT)
# ==============================================================================
@router.message(GameState.in_event)
async def event_puzzle_handler(message: Message, state: FSMContext):
    """
    Menangkap teks bebas (jawaban) dari pemain saat mereka berada 
    di dalam state Mystery Event / Kuis Lore.
    """
    user_id = message.from_user.id
    p = get_player(user_id)
    
    # Ambil data event/puzzle yang sedang aktif dari sesi FSM
    state_data = await state.get_data()
    event_data = state_data.get("event_data")
    
    # Keamanan: Jika entah bagaimana pemain ada di state ini tapi datanya kosong
    if not event_data:
        await state.set_state(GameState.exploring)
        return await message.answer(
            "Teka-teki telah memudar menjadi debu...", 
            reply_markup=get_main_reply_keyboard(p)
        )
    
    # Ambil jawaban pemain, hilangkan spasi berlebih, dan ubah ke huruf kecil
    player_answer = message.text.strip().lower()
    
    # Proses hasil jawaban pemain
    success, reward_msg, loot = process_event_outcome(p, event_data, player_answer)
    
    if success:
        # [QUEST UPDATE] Tambah progres misi harian menjawab Kuis
        quest_notif = update_quest_progress(p, "answer_quiz", 1)
        
        # Tambahkan hadiah loot ke tas pemain (jika ada)
        if loot:
            p['inventory'].extend(loot)
        
        # Kalkulasi reward bonus stat & gold berdasarkan tier puzzle
        tier = event_data.get('tier', 1)
        intel_gain = tier * 2
        gold_gain = event_data.get("gold_reward", 50)
        
        new_intel = p.get("intelligence", 10) + intel_gain
        new_gold = p.get("gold", 0) + gold_gain
        
        # Simpan perubahan besar-besaran ke Database
        update_player(user_id, {
            "inventory": p['inventory'],
            "intelligence": new_intel,
            "scholar_level": p.get("scholar_level", 0) + 1,
            "gold": new_gold,
            "daily_quests": p.get('daily_quests', [])
        })
        
        success_final = (
            f"✅ **BERHASIL!**\n{reward_msg}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🧠 Intelligence +{intel_gain}\n"
            f"💰 Gold +{gold_gain}\n"
            f"{quest_notif}"
        )
        await message.answer(success_final, reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
        
    else:
        # Jika salah jawab, berikan pesan gagal tanpa reward tambahan
        await message.answer(
            f"❌ **GAGAL!**\n{reward_msg}", 
            reply_markup=get_main_reply_keyboard(p), 
            parse_mode="Markdown"
        )
    
    # Setelah menjawab (baik benar maupun salah), bebaskan pemain ke mode eksplorasi
    await state.set_state(GameState.exploring)
    # Bersihkan sisa data event yang sudah selesai
    await state.update_data(event_data=None)
