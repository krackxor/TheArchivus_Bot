# main.py

import asyncio
import random
import os
import time
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

# === ROOT IMPORTS ===
from database import client, get_player, update_player, auto_seed_content, reset_player_death, add_history, tick_buffs
from states import GameState
from config import BOT_TOKEN

# === NEW ARCHITECTURE IMPORTS (LOGIC FOLDER) ===
from game.logic.combat import (
    generate_battle_puzzle, validate_answer, calculate_damage, 
    render_live_battle, process_loot, apply_turn_status_effects
)
from game.logic.stats import calculate_total_stats
from game.logic.inventory_manager import (
    equip_item, unequip_item, process_repair_all, use_consumable_item
)
from game.logic.menu_handler import (
    get_inventory_menu, get_profile_menu, get_profile_main_menu, 
    generate_profile_text, get_consumable_menu
)

# === PUZZLE MANAGER ===
from game.puzzles.manager import get_random_puzzle

# === OLD ARCHITECTURE IMPORTS ===
from game.systems.exploration import process_move  
from game.systems.shop import get_shop_keyboard, process_purchase, get_rest_area_keyboard
from game.systems.events import roll_loot_drop, process_event_outcome, check_easter_egg
from game.entities.npcs import resolve_npc_action
from game.systems.achievements import (
    get_all_unlockable_achievements, award_achievement, generate_daily_quests,
    check_daily_quest_progress, calculate_level_from_exp, calculate_exp_needed
)
from game.items import get_item 

from utils.helper_ui import (
    create_hp_bar, create_mp_bar, create_energy_bar, create_status_card, create_combat_header,
    create_achievement_notification, create_loot_drop, create_level_up_animation,
    create_combo_indicator, create_daily_quest_card, create_boss_warning,
    create_death_screen, create_location_transition, create_inventory_display
)

dp = Dispatcher()
ADMIN_ID = 123456789 

# === DICTIONARY TRACKING TASK TIMEOUT ===
active_timers = {}

def cancel_active_timer(user_id):
    """Membatalkan timer asinkron jika ada."""
    task = active_timers.pop(user_id, None)
    if task and not task.done():
        task.cancel()

# === HELPER DURABILITY ===
def reduce_equipment_durability(user_id, target_slots=['weapon'], damage=1):
    p = get_player(user_id)
    equipped = p.get('equipped', {})
    inventory = p.get('inventory', [])
    durability_data = p.get('equipment_durability', {})
    broken_items = []
    updates_needed = False

    if isinstance(target_slots, str): target_slots = [target_slots]

    for slot in target_slots:
        item_id = equipped.get(slot)
        if not item_id: continue 
        if slot not in durability_data: durability_data[slot] = 50 
        durability_data[slot] -= damage
        updates_needed = True

        if durability_data[slot] <= 0:
            broken_items.append(item_id)
            del equipped[slot]
            del durability_data[slot]
            if item_id in inventory: inventory.remove(item_id)

    if updates_needed:
        update_data = {"equipment_durability": durability_data}
        if broken_items:
            update_data["equipped"] = equipped
            update_data["inventory"] = inventory
        update_player(user_id, update_data)
    return broken_items

# === KEYBOARDS ===
def get_main_reply_keyboard(player=None):
    keyboard = [
        [KeyboardButton(text="⬆️ Utara")],
        [KeyboardButton(text="⬅️ Barat"), KeyboardButton(text="Timur ➡️")],
        [KeyboardButton(text="⬇️ Selatan")],
        [KeyboardButton(text="📊 Profil & Tas")] 
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, input_field_placeholder="⚔️ Pilih aksimu, Weaver...")

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


# === BACKGROUND TIMERS ===
async def combat_timeout_task(message: Message, state: FSMContext, puzzle: dict, user_id: int):
    try:
        timer = puzzle['timer']
        if str(timer) == "--": return 
        await asyncio.sleep(timer)
        
        current_state = await state.get_state()
        data = await state.get_data()
        active_puzzle = data.get("puzzle", {})
        battle_msg_id = data.get("battle_msg_id")
        
        if current_state == GameState.in_combat and active_puzzle.get("generated_time") == puzzle["generated_time"]:
            p = get_player(user_id)
            p['stats'] = calculate_total_stats(p)
            raw_dmg, atk_log = calculate_damage(puzzle, p, is_attacker_player=False)
            reduce_equipment_durability(user_id, target_slots=['armor', 'head'], damage=2)
                
            new_hp = max(0, p['hp'] - raw_dmg)
            update_player(user_id, {"hp": new_hp, "current_combo": 0})
            p['hp'] = new_hp 
            
            if new_hp <= 0:
                await state.set_state(GameState.exploring)
                msg_text = reset_player_death(user_id, "death_combat")
                try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text="💀 **KAU TELAH GUGUR...**", parse_mode="Markdown")
                except: pass
                await message.answer(msg_text, reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
            else:
                new_q = get_random_puzzle(puzzle.get('tier', 1))
                puzzle['question'] = new_q['question']
                puzzle['answer'] = str(new_q['answer']).strip().lower()
                puzzle['generated_time'] = None 
                await state.update_data(puzzle=puzzle, action_type=None)
                
                log_msg = f"⏰ WAKTU HABIS!\n{atk_log} (-{raw_dmg} HP)"
                next_msg = render_live_battle(p, puzzle, log_msg)
                
                try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text=next_msg, parse_mode="Markdown", reply_markup=get_stance_keyboard(puzzle.get('is_boss', False)))
                except: pass
                active_timers[user_id] = asyncio.create_task(combat_timeout_task(message, state, puzzle, user_id))
    except asyncio.CancelledError: return
    finally:
        if user_id in active_timers and active_timers[user_id] == asyncio.current_task():
            active_timers.pop(user_id, None)

# === COMMAND HANDLERS ===
@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    player = get_player(user_id, message.from_user.first_name)
    player['stats'] = calculate_total_stats(player)
    await state.set_state(GameState.exploring)
    await message.answer("📜 *THE ARCHIVUS* 📜\nSelamat datang, Weaver.", reply_markup=get_main_reply_keyboard(player), parse_mode="Markdown")

@dp.message(GameState.exploring, F.text == "📊 Profil & Tas")
async def profile_bag_handler(message: Message):
    p = get_player(message.from_user.id)
    p['stats'] = calculate_total_stats(p)
    text = generate_profile_text(p, p['stats'])
    kb = get_profile_main_menu(p)
    await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=kb), parse_mode="Markdown")

# === BLACKSMITH (REPAIR) ===
@dp.callback_query(F.data == "menu_repair")
async def blacksmith_callback_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    p = get_player(user_id)
    new_durability, cost, count = process_repair_all(p)
    
    if count == 0:
        return await callback.answer("Aethelred: 'Gear-mu masih tajam. Pergi sana!'", show_alert=True)
    if p.get('gold', 0) < cost:
        return await callback.answer(f"Aethelred: 'Emasmu kurang! Butuh {cost}G.'", show_alert=True)
        
    update_player(user_id, {"gold": p['gold'] - cost, "equipment_durability": new_durability})
    
    repair_msg = (
        f"⚒️ **BENGKEL AETHELRED** ⚒️\n━━━━━━━━━━━━━━━━━━━━\n"
        f"💬 *'Nah, sekarang benda ini bisa membelah kulit iblis lagi.'*\n\n"
        f"🛠️ **Item Diperbaiki:** {count}\n💰 **Biaya:** -{cost} Gold\n✨ **Kondisi:** 100% (50/50)"
    )
    await callback.message.edit_text(repair_msg, parse_mode="Markdown")
    await callback.answer("Berhasil diperbaiki!")

# === MENU & INVENTORY CALLBACKS ===
@dp.callback_query(F.data.startswith("menu_") | F.data.startswith("equip_") | F.data.startswith("unequip_") | F.data.startswith("useitem_"))
async def inventory_button_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = callback.data
    p = get_player(user_id)
    p['stats'] = calculate_total_stats(p)

    if data == "menu_inventory":
        kb = get_inventory_menu(p)
        await callback.message.edit_text("🎒 **Isi Tas (Equipment):**", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb), parse_mode="Markdown")
    
    elif data == "menu_consumables":
        kb = get_consumable_menu(p)
        await callback.message.edit_text("🧪 **Daftar Ramuan (Consumables):**", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb), parse_mode="Markdown")

    elif data == "menu_profile":
        kb = get_profile_menu(p)
        await callback.message.edit_text("👕 **Equipment Terpakai:**", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb), parse_mode="Markdown")

    elif data == "menu_main_profile":
        text = generate_profile_text(p, p['stats'])
        kb = get_profile_main_menu(p)
        await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=kb), parse_mode="Markdown")

    elif data.startswith("equip_"):
        item_id = data.replace("equip_", "")
        _, msg = equip_item(p, item_id)
        update_player(user_id, {'inventory': p['inventory'], 'equipped': p['equipped'], 'current_job': p['current_job']})
        await callback.answer(msg)
        await callback.message.edit_text("🎒 **Isi Tas:**", reply_markup=InlineKeyboardMarkup(inline_keyboard=get_inventory_menu(p)), parse_mode="Markdown")

    elif data.startswith("unequip_"):
        slot = data.replace("unequip_", "")
        _, msg = unequip_item(p, slot)
        update_player(user_id, {'inventory': p['inventory'], 'equipped': p['equipped'], 'current_job': p['current_job']})
        await callback.answer(msg)
        await callback.message.edit_text("👕 **Equipment Terpakai:**", reply_markup=InlineKeyboardMarkup(inline_keyboard=get_profile_menu(p)), parse_mode="Markdown")

    elif data.startswith("useitem_"):
        item_id = data.replace("useitem_", "")
        # Cek apakah sedang bertarung
        current_state = await state.get_state()
        if current_state == GameState.in_combat:
            # Mode Combat: Jawab teka-teki dulu
            await state.update_data(selected_item_id=item_id, action_type="item")
            data_st = await state.get_data()
            puzzle = data_st.get("puzzle")
            puzzle['generated_time'] = time.time()
            await state.update_data(puzzle=puzzle)
            await callback.message.edit_text(render_live_battle(p, puzzle, f"Persiapan menggunakan item..."), parse_mode="Markdown")
        else:
            # Mode Eksplorasi: Gunakan langsung
            success, msg, p_new = use_consumable_item(p, item_id)
            if success:
                update_player(user_id, {'hp': p_new['hp'], 'mp': p_new['mp'], 'inventory': p_new['inventory'], 'active_effects': p_new.get('active_effects', [])})
                await callback.answer(msg, show_alert=True)
                await callback.message.edit_text("🧪 **Daftar Ramuan:**", reply_markup=InlineKeyboardMarkup(inline_keyboard=get_consumable_menu(p_new)), parse_mode="Markdown")

# === MOVEMENT ===
@dp.message(F.text.in_(["⬆️ Utara", "⬅️ Barat", "Timur ➡️", "⬇️ Selatan"]))
async def move_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if await state.get_state() == GameState.in_combat:
        return await message.answer("Selesaikan pertempuranmu!")
        
    await state.set_state(GameState.exploring)
    tick_buffs(user_id) 
    p = get_player(user_id)
    p['stats'] = calculate_total_stats(p)
    event_type, _, narration = process_move(user_id)
    
    if event_type in ["boss", "monster", "miniboss"]:
        puzzle = generate_battle_puzzle(p, min(5, (p['kills']//5)+1), is_boss=(event_type=="boss"))
        await state.set_state(GameState.in_combat)
        puzzle['generated_time'] = None 
        sent_msg = await message.answer(render_live_battle(p, puzzle, narration), parse_mode="Markdown", reply_markup=get_stance_keyboard(event_type=="boss"))
        await state.update_data(battle_msg_id=sent_msg.message_id, puzzle=puzzle, action_type=None)
        cancel_active_timer(user_id) 
        active_timers[user_id] = asyncio.create_task(combat_timeout_task(message, state, puzzle, user_id))
    else:
        await message.answer(narration, reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")

# === COMBAT STANCE ROUTER ===
@dp.callback_query(F.data.startswith("stance_"))
async def combat_stance_handler(callback: CallbackQuery, state: FSMContext):
    if await state.get_state() != GameState.in_combat:
        return await callback.answer("Sesi kedaluwarsa.", show_alert=True)
    
    action = callback.data.replace("stance_", "") 
    p = get_player(callback.from_user.id)
    
    if action == "item":
        kb = get_consumable_menu(p)
        if len(kb) <= 1: # Hanya tombol kembali
            return await callback.answer("Tas ramuanmu kosong!", show_alert=True)
        return await callback.message.edit_text("🎒 **PILIH ITEM:**", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))

    await state.update_data(action_type=action)
    state_data = await state.get_data()
    puzzle = state_data.get("puzzle")
    puzzle['generated_time'] = time.time()
    await state.update_data(puzzle=puzzle) 
    await callback.message.edit_text(render_live_battle(p, puzzle, f"Aksi: {action.upper()}! Jawab teka-tekinya!"), parse_mode="Markdown")

# === COMBAT ANSWER HANDLER ===
@dp.message(GameState.in_combat)
async def combat_answer_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    puzzle = data.get("puzzle")
    action = data.get("action_type", "attack")
    battle_msg_id = data.get("battle_msg_id")
    
    if not puzzle or puzzle.get('generated_time') is None:
        try: await message.delete()
        except: pass
        return

    cancel_active_timer(user_id)
    try: await message.delete()
    except: pass 

    is_correct, is_timeout, _ = validate_answer(message.text, puzzle['answer'], puzzle['generated_time'], puzzle['timer'])
    p = get_player(user_id)
    p['stats'] = calculate_total_stats(p)
    action_log = ""
    
    if is_correct:
        if action == "attack":
            p_dmg, log = calculate_damage(p, puzzle, is_attacker_player=True)
            reduce_equipment_durability(user_id, target_slots=['weapon'], damage=1)
            puzzle['monster_hp'] -= p_dmg
            action_log = f"{log} Musuh -{p_dmg} HP."
        elif action == "item":
            item_id = data.get("selected_item_id")
            success, item_msg, p_new = use_consumable_item(p, item_id)
            if success:
                p = p_new
                action_log = item_msg
            else: action_log = "❌ Gagal menggunakan item!"
        elif action == "block":
            heal = int(p['max_hp'] * 0.15)
            p['hp'] = min(p['max_hp'], p['hp'] + heal)
            action_log = f"🛡️ Bertahan! +{heal} HP."
        elif action == "skill":
            p_dmg, log = calculate_damage(p, puzzle, is_attacker_player=True)
            puzzle['monster_hp'] -= int(p_dmg * 1.8)
            action_log = f"🔮 Skill! Musuh -{int(p_dmg*1.8)} HP."
    else:
        m_dmg, log = calculate_damage(puzzle, p, is_attacker_player=False)
        p['hp'] = max(0, p['hp'] - m_dmg)
        action_log = f"❌ Salah! {log} -{m_dmg} HP."

    # STATUS EFFECTS ROUND TICK
    m_hp_change, m_logs = apply_turn_status_effects(puzzle, is_player=False)
    p_hp_change, p_logs = apply_turn_status_effects(p, is_player=True)
    
    puzzle['monster_hp'] = max(0, puzzle['monster_hp'] + m_hp_change)
    p['hp'] = max(0, p['hp'] + p_hp_change)
    
    update_player(user_id, {"hp": p['hp'], "mp": p['mp'], "inventory": p['inventory'], "active_effects": p.get('active_effects', [])})
    full_log = f"{action_log}\n" + " ".join(m_logs + p_logs)

    if puzzle['monster_hp'] <= 0:
        drops = process_loot(puzzle.get('drops', []))
        inv = p['inventory']; inv.extend(drops)
        new_exp = p['exp'] + puzzle['exp_reward']
        update_player(user_id, {'kills': p['kills']+1, 'gold': p['gold']+puzzle['gold_reward'], 'exp': new_exp, 'level': calculate_level_from_exp(new_exp), 'inventory': inv})
        await state.set_state(GameState.exploring)
        await message.answer(f"🎉 MENANG! EXP +{puzzle['exp_reward']} | Gold +{puzzle['gold_reward']}\nDrops: {', '.join(drops)}", reply_markup=get_main_reply_keyboard(p))
    elif p['hp'] <= 0:
        await state.set_state(GameState.exploring)
        await message.answer(reset_player_death(user_id, "death_combat"), reply_markup=get_main_reply_keyboard(p))
    else:
        new_q = get_random_puzzle(puzzle.get('tier', 1))
        puzzle.update({'question': new_q['question'], 'answer': str(new_q['answer']).lower(), 'generated_time': None})
        await state.update_data(puzzle=puzzle, action_type=None)
        try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text=render_live_battle(p, puzzle, full_log), parse_mode="Markdown", reply_markup=get_stance_keyboard(puzzle.get('is_boss', False)))
        except: pass
        active_timers[user_id] = asyncio.create_task(combat_timeout_task(message, state, puzzle, user_id))

async def main():
    auto_seed_content()
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
