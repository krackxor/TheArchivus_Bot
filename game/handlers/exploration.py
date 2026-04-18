# game/handlers/exploration.py

import asyncio
import random
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

# === IMPORTS ===
from database import get_player, update_player, tick_buffs
from game.logic.states import GameState
from game.logic.stats import calculate_total_stats
from game.systems.exploration import process_move
from game.logic.menu_handler import get_main_reply_keyboard
from game.logic.combat import generate_battle_data, render_live_battle
from game.systems.shop import get_rest_area_keyboard

# Inisialisasi Router
router = Router()

# ==============================================================================
# HELPER SEMENTARA (Pastikan ini nanti ada di game/systems/achievements.py)
# ==============================================================================
def update_quest_progress(player: dict, goal_type: str, amount: int = 1) -> str:
    player_quests = player.get('daily_quests', [])
    notif_msg = ""
    for q in player_quests:
        if q['status'] == "active" and q['goal_type'] == goal_type:
            q['current'] += amount
            if q['current'] >= q['goal_value']:
                q['current'] = q['goal_value']
                q['status'] = "completed"
                player['gold'] += q.get('reward_gold', 0)
                player['exp'] += q.get('reward_exp', 0)
                notif_msg += f"\n🎯 **QUEST SELESAI:** {q['icon']} {q['name']} (+{q['reward_gold']}G)"
    return notif_msg

# HELPER SEMENTARA (Pastikan ini nanti dipindah ke game/logic/menu_handler.py)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
def get_stance_keyboard(is_boss=False):
    row1 = [
        InlineKeyboardButton(text="⚔️ Serang", callback_data="stance_attack"),
        InlineKeyboardButton(text="🔮 Skill", callback_data="stance_skill")
    ]
    row2 = [
        InlineKeyboardButton(text="🛡️ Bertahan", callback_data="stance_block"),
        InlineKeyboardButton(text="💨 Menghindar", callback_data="stance_dodge")
    ]
    row3 = [InlineKeyboardButton(text="🎒 Item", callback_data="stance_item")]
    if not is_boss: row3.append(InlineKeyboardButton(text="🏃 Kabur", callback_data="stance_run"))
    return InlineKeyboardMarkup(inline_keyboard=[row1, row2, row3])
# ==============================================================================


# === MOVEMENT & EXPLORATION ===
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


# --- FITUR EMERGENCY: MEDITASI ---
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
