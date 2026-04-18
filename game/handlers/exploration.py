# game/handlers/exploration.py

import asyncio
import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

# === IMPORTS UTAMA ===
from database import get_player, update_player, tick_buffs
from game.logic.states import GameState
from game.logic.stats import calculate_total_stats
from game.systems.exploration import process_move
from game.logic.combat import generate_battle_data, render_live_battle

# Import keyboard dari menu_handler (Termasuk get_rest_area_keyboard yang baru)
from game.logic.menu_handler import get_main_reply_keyboard, get_stance_keyboard, get_rest_area_keyboard

# Import Sistem Quest dari tempat aslinya
from game.systems.achievements import update_quest_progress

# Inisialisasi Router
router = Router()

# ==============================================================================
# 1. MOVEMENT & EXPLORATION (JALAN KAKI)
# ==============================================================================
@router.message(F.text.in_(["⬆️ Utara", "⬅️ Barat", "Timur ➡️", "⬇️ Selatan"]))
async def move_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    current_state = await state.get_state()
    
    # 1. CEK STATE: Mencegah jalan saat bertarung/event/istirahat
    if current_state in [GameState.in_combat, GameState.in_event, GameState.in_rest_area]:
        try: await message.delete() 
        except: pass
        warning_msg = await message.answer("⚠️ Selesaikan dulu urusanmu di depan sebelum bergerak maju!")
        await asyncio.sleep(2)
        try: await message.bot.delete_message(chat_id=message.chat.id, message_id=warning_msg.message_id)
        except: pass
        return
        
    try: await message.delete()
    except: pass
    
    # 2. CLEANUP: Hapus pesan eksplorasi sebelumnya
    state_data = await state.get_data()
    last_expl_msg = state_data.get("last_expl_msg_id")
    if last_expl_msg:
        try: await message.bot.delete_message(chat_id=message.chat.id, message_id=last_expl_msg)
        except: pass

    # 3. PREPARASI DATA & STATS
    await state.set_state(GameState.exploring)
    tick_buffs(user_id) 
    p = get_player(user_id)
    
    p['stats'] = calculate_total_stats(p) 
    luck_bonus = p['stats'].get('luck', 0)
    intel_bonus = p.get('intelligence', 10)
    
    # 4. ENERGI CHECK (Safety Net)
    current_energy = p.get('energy', 100)
    if current_energy <= 0:
        text_tired = (
            "😫 **KELELAHAN EKSTREM**\n\n"
            "Tubuhmu menolak untuk melangkah lebih jauh. Energimu habis (**0**).\n\n"
            "💡 *Solusi:* Gunakan **Makanan** dari Tas atau gunakan fitur **🧘 Meditasi** "
            "untuk memulihkan tenaga dengan bayaran sisa HP-mu."
        )
        return await message.answer(text_tired, reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")

    # 5. UPDATE PROGRES & ENERGI
    new_energy = current_energy - 1
    quest_notif = update_quest_progress(p, "move_steps", 1)
    
    update_player(user_id, {
        "energy": new_energy,
        "daily_quests": p.get('daily_quests', [])
    })
    
    # 6. LOGIKA PERGERAKAN
    event_type, event_data, narration = process_move(user_id, luck=luck_bonus, intel=intel_bonus)
    final_narration = f"{narration}\n{quest_notif}" if quest_notif else narration

    # 7. PENANGANAN HASIL EVENT
    if event_type in ["boss", "monster", "miniboss"]:
        is_boss = (event_type == "boss")
        is_miniboss = (event_type == "miniboss")
        tier_level = 5 if is_boss else min(5, max(1, (p.get('kills', 0) // 5) + 1))
        
        enemy_data = generate_battle_data(p, tier_level, is_boss=is_boss, is_miniboss=is_miniboss)
        await state.set_state(GameState.in_combat)
        
        safe_narration = final_narration.replace("**", "")
        combat_ui = render_live_battle(p, enemy_data, f"⚠️ <b>{safe_narration}</b>")
        sent_msg = await message.answer(combat_ui, parse_mode="HTML", reply_markup=get_stance_keyboard(is_boss))
        
        await state.update_data(
            battle_msg_id=sent_msg.message_id,
            enemy_data=enemy_data, 
            current_combo=0,
            last_expl_msg_id=None
        )

    elif event_type in ["npc", "hazard", "landmark"]:
        from game.logic.event_handler import get_event_interaction_kb
        kb = get_event_interaction_kb(event_type, event_data)
        sent_msg = await message.answer(f"{final_narration}", reply_markup=kb, parse_mode="Markdown")
        await state.update_data(last_expl_msg_id=sent_msg.message_id)

    elif event_type == "rest_area":
        await state.set_state(GameState.in_rest_area)
        kb = get_rest_area_keyboard()
        sent_msg = await message.answer(f"🏕️ **REST AREA**\n{final_narration}", reply_markup=kb, parse_mode="Markdown")
        await state.update_data(last_expl_msg_id=sent_msg.message_id)

    elif event_type == "event": 
        await state.set_state(GameState.in_event)
        await state.update_data(event_data=event_data)
        sent_msg = await message.answer(f"❓ **MYSTERY EVENT**\n{final_narration}\n\n*Ketik jawabanmu langsung di sini...*", parse_mode="Markdown")
        await state.update_data(last_expl_msg_id=sent_msg.message_id)

    else:
        status_line = f"\n\n⚡ Energi: {new_energy}/100"
        sent_msg = await message.answer(f"{final_narration}{status_line}", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
        await state.update_data(last_expl_msg_id=sent_msg.message_id)


# ==============================================================================
# 2. FITUR EMERGENCY: MEDITASI
# ==============================================================================
@router.message(GameState.exploring, F.text == "🧘 Meditasi")
async def meditation_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    p = get_player(user_id)
    
    if p.get('energy', 0) > 0:
        return await message.answer("⏳ **FOKUS TERJAGA**\n\nMeditasi hanya bisa dilakukan saat Energimu benar-benar habis (**0**).")

    if p['hp'] <= 10:
        return await message.answer("⚠️ **KONDISI KRITIS**\n\nTubuhmu terlalu lemah. Meditasi sekarang akan membunuhmu!")

    gain_energy = random.randint(8, 12)
    loss_hp = 10
    
    new_energy = min(100, p['energy'] + gain_energy)
    new_hp = max(1, p['hp'] - loss_hp)
    
    update_player(user_id, {"energy": new_energy, "hp": new_hp})

    await message.answer(
        f"🧘 **DEEP MEDITATION**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ Energi: +{gain_energy}\n"
        f"💔 HP: -{loss_hp}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔋 Status: ⚡ {new_energy} | ❤️ {new_hp}",
        parse_mode="Markdown"
    )

# ==============================================================================
# 3. HANDLER REST AREA (API UNGGUN / TENDA)
# ==============================================================================
@router.callback_query(GameState.in_rest_area)
async def rest_area_callback_handler(callback: CallbackQuery, state: FSMContext):
    """Menangkap interaksi tombol saat pemain berada di dalam Rest Area."""
    user_id = callback.from_user.id
    data = callback.data
    p = get_player(user_id)
    
    # --- OPSI 1: PASANG TENDA (BUTUH ITEM) ---
    if data == "rest_tent":
        inventory = p.get('inventory', [])
        
        # Cek apakah pemain punya tenda
        if "tenda" not in inventory:
            return await callback.answer("❌ Kamu tidak memiliki item 'Tenda' di dalam tas!", show_alert=True)
            
        try: await callback.message.delete()
        except: pass
        
        # Hapus 1 tenda dari tas
        inventory.remove("tenda")
        
        # Heal Maksimal (+100)
        new_hp = min(p.get('max_hp', 100), p.get('hp', 0) + 100)
        new_mp = min(p.get('max_mp', 50), p.get('mp', 0) + 100)
        new_energy = min(100, p.get('energy', 0) + 100)
        
        update_player(user_id, {"hp": new_hp, "mp": new_mp, "energy": new_energy, "inventory": inventory})
        await state.set_state(GameState.exploring)
        
        await callback.message.answer(
            f"⛺ **KEMAH YANG NYAMAN**\n\n"
            f"Kau mendirikan tenda dan tidur dengan nyenyak. Tubuhmu sepenuhnya bugar kembali!\n\n"
            f"*(💖 +100 HP | 💧 +100 MP | ⚡ +100 Energi)*\n"
            f"_[-1 Tenda digunakan]_", 
            reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown"
        )
        await callback.answer("Tidur nyenyak!")

    # --- OPSI 2: MENYALAKAN API (GRATIS) ---
    elif data == "rest_fire":
        try: await callback.message.delete()
        except: pass
        
        # Heal Sebagian (+50 HP/MP, +25 Energi)
        new_hp = min(p.get('max_hp', 100), p.get('hp', 0) + 50)
        new_mp = min(p.get('max_mp', 50), p.get('mp', 0) + 50)
        new_energy = min(100, p.get('energy', 0) + 25)
        
        update_player(user_id, {"hp": new_hp, "mp": new_mp, "energy": new_energy})
        await state.set_state(GameState.exploring)
        
        await callback.message.answer(
            f"🔥 **API UNGGUN MENYALA**\n\n"
            f"Kau duduk di dekat api yang berderak. Cukup untuk mengusir hawa dingin malam ini.\n\n"
            f"*(💖 +50 HP | 💧 +50 MP | ⚡ +25 Energi)*", 
            reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown"
        )
        await callback.answer("Istirahat sejenak...")

    # --- OPSI 3: LANJUT BERJALAN ---
    elif data == "rest_leave": 
        try: await callback.message.delete()
        except: pass
        
        await state.set_state(GameState.exploring)
        await callback.message.answer(
            "🚶‍♂️ Kamu mengabaikan tempat berlindung itu dan terus berjalan menembus kegelapan...", 
            reply_markup=get_main_reply_keyboard(p)
        )
        await callback.answer("Melanjutkan perjalanan...")
