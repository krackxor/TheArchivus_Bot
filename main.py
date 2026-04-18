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
from game.logic.inventory_manager import equip_item, unequip_item, process_repair_all, use_consumable_item
from game.logic.menu_handler import get_inventory_menu, get_profile_menu, get_consumable_menu, get_profile_main_menu, generate_profile_text

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
def reduce_equipment_durability(user_id, target_slots=['weapon'], damage=1, chance=0.3):
    """
    Sistem Durabilitas Baru: Ada peluang 30% durability berkurang saat beraksi.
    """
    if random.random() > chance:
        return []

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
            m_name = puzzle.get('monster_name', 'Musuh')
            
            raw_dmg, atk_log = calculate_damage(puzzle, p, is_attacker_player=False)
            broken_armors = reduce_equipment_durability(user_id, target_slots=['armor', 'head'], damage=2, chance=1.0)
            dur_msg = f"\n⚠️ *Pelindung hancur:* {', '.join(broken_armors)}" if broken_armors else ""
                
            new_hp = p['hp'] - raw_dmg
            update_player(user_id, {"hp": new_hp, "current_combo": 0})
            p['hp'] = new_hp 
            
            if new_hp <= 0:
                await state.set_state(GameState.exploring)
                msg_text = reset_player_death(user_id, "death_combat")
                try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text="💀 **KAU TELAH GUGUR...**", parse_mode="Markdown")
                except: pass
                await message.answer(f"💀 Dikalahkan oleh {m_name}\n\n{msg_text}", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
            else:
                new_q = get_random_puzzle(puzzle.get('tier', 1))
                puzzle['question'] = new_q['question']
                puzzle['answer'] = str(new_q['answer']).strip().lower()
                puzzle['generated_time'] = None 
                await state.update_data(puzzle=puzzle, action_type=None)
                
                safe_puzzle = puzzle.copy()
                safe_puzzle['question'] = "Pilih aksi untuk mengungkap segel teka-teki!"
                safe_puzzle['timer'] = "--"
                
                log_msg = (
                    f"⏳ **WAKTU HABIS!** Segel tertutup!\n"
                    f"👾 **SERANGAN {m_name.upper()}:** {atk_log} (-{raw_dmg} HP){dur_msg}"
                )
                next_msg = render_live_battle(p, safe_puzzle, log_msg)
                
                try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text=next_msg, parse_mode="Markdown", reply_markup=get_stance_keyboard(puzzle.get('is_boss', False)))
                except TelegramBadRequest: pass
                
                active_timers[user_id] = asyncio.create_task(combat_timeout_task(message, state, puzzle, user_id))

    except asyncio.CancelledError: return
    finally:
        if user_id in active_timers and active_timers[user_id] == asyncio.current_task():
            active_timers.pop(user_id, None)


# === COMMAND HANDLERS ===
@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.first_name
    player = get_player(user_id, username)
    player['stats'] = calculate_total_stats(player) 
    
    await state.set_state(GameState.exploring)
    welcome_msg = (
        f"━━━━━━━━━━━━━━━━━━━━\n📜 *THE ARCHIVUS* 📜\n━━━━━━━━━━━━━━━━━━━━\n"
        f"Selamat datang, {username}\n\nKau telah memasuki dimensi\ntanpa ujung ini sebagai\n"
        f"*{player.get('current_job', 'Novice Weaver')}*.\n━━━━━━━━━━━━━━━━━━━━\n"
        f"Cycle: {player.get('cycle', 1)} | Level: {player.get('level', 1)}\n"
        f"{create_hp_bar(player.get('hp',100), player.get('max_hp',100))}\n"
        f"{create_mp_bar(player.get('mp', 0), player.get('max_mp', 50))}\n"
        f"🔮 Ketik /help untuk panduan"
    )
    await message.answer(welcome_msg, reply_markup=get_main_reply_keyboard(player), parse_mode="Markdown")

@dp.message(GameState.exploring, F.text == "📊 Profil & Tas")
async def profile_bag_handler(message: Message):
    p = get_player(message.from_user.id)
    p['stats'] = calculate_total_stats(p)
    text = generate_profile_text(p, p['stats'])
    kb = get_profile_main_menu(p)
    await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=kb), parse_mode="Markdown")


# === BLACKSMITH CALLBACK ===
@dp.callback_query(F.data == "menu_repair")
async def blacksmith_callback_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    p = get_player(user_id)
    new_durability, cost, count = process_repair_all(p)
    
    if count == 0: return await callback.answer("Aethelred: 'Gear-mu masih tajam. Pergi sana!'", show_alert=True)
    if p.get('gold', 0) < cost: return await callback.answer(f"Aethelred: 'Emasmu kurang! Butuh {cost}G.'", show_alert=True)
        
    update_player(user_id, {"gold": p['gold'] - cost, "equipment_durability": new_durability})
    repair_msg = (
        f"⚒️ **BENGKEL AETHELRED** ⚒️\n━━━━━━━━━━━━━━━━━━━━\n"
        f"💬 *'Nah, sekarang benda ini bisa membelah kulit iblis lagi.'*\n\n"
        f"🛠️ **Item Diperbaiki:** {count}\n💰 **Biaya:** -{cost} Gold\n✨ **Kondisi:** 100% (50/50)"
    )
    await callback.message.edit_text(repair_msg, parse_mode="Markdown")
    await callback.answer("Berhasil diperbaiki!")


# === INVENTORY CALLBACKS ===
@dp.callback_query(F.data.startswith("menu_") | F.data.startswith("equip_") | F.data.startswith("unequip_") | F.data.startswith("useitem_"))
async def inventory_button_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = callback.data
    p = get_player(user_id)
    p['stats'] = calculate_total_stats(p)

    if data == "menu_inventory":
        await callback.message.edit_text("🎒 **Isi Tas (Equipment):**", reply_markup=InlineKeyboardMarkup(inline_keyboard=get_inventory_menu(p)), parse_mode="Markdown")
    elif data == "menu_consumables":
        await callback.message.edit_text("🧪 **Daftar Ramuan:**", reply_markup=InlineKeyboardMarkup(inline_keyboard=get_consumable_menu(p)), parse_mode="Markdown")
    elif data == "menu_profile":
        await callback.message.edit_text("👕 **Equipment Terpakai:**", reply_markup=InlineKeyboardMarkup(inline_keyboard=get_profile_menu(p)), parse_mode="Markdown")
    elif data == "menu_main_profile":
        await callback.message.edit_text(generate_profile_text(p, p['stats']), reply_markup=InlineKeyboardMarkup(inline_keyboard=get_profile_main_menu(p)), parse_mode="Markdown")
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
        if await state.get_state() == GameState.in_combat:
            await state.update_data(selected_item_id=item_id, action_type="item")
            d_st = await state.get_data()
            puzzle = d_st.get("puzzle")
            puzzle['generated_time'] = time.time()
            await state.update_data(puzzle=puzzle)
            await callback.message.edit_text(render_live_battle(p, puzzle, f"Persiapan menenggak ramuan...\n👇 CEPAT JAWAB TEKA-TEKI! 👇"), parse_mode="Markdown")
        else:
            success, msg, p_new = use_consumable_item(p, item_id)
            if success:
                update_player(user_id, {'hp': p_new['hp'], 'mp': p_new['mp'], 'inventory': p_new['inventory'], 'active_effects': p_new.get('active_effects', [])})
                await callback.answer(msg, show_alert=True)
                await callback.message.edit_text("🧪 **Daftar Ramuan:**", reply_markup=InlineKeyboardMarkup(inline_keyboard=get_consumable_menu(p_new)), parse_mode="Markdown")


# === MOVEMENT & EXPLORATION ===
@dp.message(F.text.in_(["⬆️ Utara", "⬅️ Barat", "Timur ➡️", "⬇️ Selatan"]))
async def move_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if await state.get_state() in [GameState.in_combat, GameState.in_event, GameState.in_rest_area]:
        return await message.answer("Selesaikan dulu urusanmu di depan sebelum bergerak maju!")
        
    await state.set_state(GameState.exploring)
    tick_buffs(user_id) 
    p = get_player(user_id)
    p['stats'] = calculate_total_stats(p) 
    
    new_energy = p.get('energy', 100) - 1
    update_player(user_id, {"energy": new_energy})
    
    event_type, event_data, narration = process_move(user_id)
    
    if event_type in ["boss", "monster", "miniboss"]:
        is_boss = (event_type == "boss")
        is_miniboss = (event_type == "miniboss")
        tier_level = 5 if is_boss else min(5, max(1, (p['kills'] // 5) + 1))
        
        puzzle = generate_battle_puzzle(p, tier_level, is_boss=is_boss, is_miniboss=is_miniboss)
        await state.set_state(GameState.in_combat)
        puzzle['generated_time'] = None 
        
        safe_puzzle = puzzle.copy()
        safe_puzzle['question'] = "Pilih aksi untuk mengungkap segel teka-teki!"
        safe_puzzle['timer'] = "--"
        
        combat_ui = render_live_battle(p, safe_puzzle, f"⚠️ {narration}")
        sent_msg = await message.answer(combat_ui, parse_mode="Markdown", reply_markup=get_stance_keyboard(is_boss))
        
        await state.update_data(battle_msg_id=sent_msg.message_id, puzzle=puzzle, combat_start_hp=p['hp'], current_combo=0, action_type=None)
        cancel_active_timer(user_id) 
        active_timers[user_id] = asyncio.create_task(combat_timeout_task(message, state, puzzle, user_id))
    else:
        await message.answer(f"{narration}\n⚡ Energi: {new_energy}/100", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")


# === COMBAT STANCE ROUTER ===
@dp.callback_query(F.data.startswith("stance_"))
async def combat_stance_handler(callback: CallbackQuery, state: FSMContext):
    if await state.get_state() != GameState.in_combat:
        return await callback.answer("⚠️ Sesi pertarungan ini sudah kedaluwarsa.", show_alert=True)
        
    action = callback.data.replace("stance_", "") 
    p = get_player(callback.from_user.id)
    
    if action == "item":
        kb = get_consumable_menu(p)
        if not kb or len(kb) <= 1: return await callback.answer("Tas ramuanmu kosong!", show_alert=True)
        return await callback.message.edit_text("🎒 **PILIH RAMUAN:**", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))

    state_data = await state.get_data()
    puzzle = state_data.get("puzzle")
    if not puzzle: return await callback.answer("Data musuh tidak ditemukan.", show_alert=True)
        
    await state.update_data(action_type=action)
    p['stats'] = calculate_total_stats(p)
    
    puzzle['generated_time'] = time.time()
    await state.update_data(puzzle=puzzle) 
    
    action_names = {"attack": "⚔️ MENYERANG", "run": "🏃 KABUR", "block": "🛡️ BERTAHAN", "dodge": "💨 MENGHINDAR", "skill": "🔮 CAST SKILL"}
    selected_action = action_names.get(action, "AKSI")
    
    combat_ui = render_live_battle(p, puzzle, f"{selected_action} DIPILIH!\n\n👇 **SELANJUTNYA: KETIK JAWABAN TEKA-TEKI INI DI CHAT!** 👇")
    try:
        await callback.message.edit_text(combat_ui, parse_mode="Markdown", reply_markup=None)
        await callback.answer(f"Segel terbuka! Cepat jawab!")
    except TelegramBadRequest: pass


# === PUSAT LOGIKA COMBAT TURN-BASED (1:1, 1:2, SKIP TURN) ===
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
        warn_msg = await message.answer("⚠️ **Tunggu dulu!** Pilih tombol aksi dulu sebelum menjawab!", parse_mode="Markdown")
        await asyncio.sleep(3) 
        try: await warn_msg.delete()
        except: pass
        return

    cancel_active_timer(user_id)
    try: await message.delete()
    except: pass 

    effective_timer = 9999 if str(puzzle.get('timer')) == "--" else puzzle['timer']
    is_correct, is_timeout, time_taken = validate_answer(message.text, puzzle['answer'], puzzle['generated_time'], effective_timer)
    
    p = get_player(user_id)
    p['stats'] = calculate_total_stats(p)
    is_boss = puzzle.get('is_boss', False)
    m_name = puzzle.get('monster_name', 'Musuh')
    
    result_msg = ""
    current_combo = data.get("current_combo", 0)

    if is_correct:
        current_combo += 1
        
        # --- 1. AKSI ATTACK (1:1) ---
        if action == "attack":
            p_dmg, p_log = calculate_damage(p, puzzle, is_attacker_player=True)
            puzzle['monster_hp'] -= p_dmg
            
            broken_weapons = reduce_equipment_durability(user_id, target_slots=['weapon'], damage=1)
            wpn_msg = f" ⚠️ *Senjata retak!*" if broken_weapons else ""
            
            m_dmg, m_log = calculate_damage(puzzle, p, is_attacker_player=False)
            p['hp'] -= m_dmg
            
            result_msg = (
                f"⚔️ **SERANGANMU:** {p_log} {m_name} terkena tebasanmu! (-{p_dmg} HP){wpn_msg}\n"
                f"👾 **BALASAN {m_name.upper()}:** {m_log} Kamu -{m_dmg} HP."
            )
            
        # --- 2. AKSI SKILL (1:2 - Recovery Penalty) ---
        elif action == "skill":
            temp_p = p.copy()
            temp_p['stats']['m_atk'] = int(temp_p['stats']['m_atk'] * 1.8)
            p_dmg, p_log = calculate_damage(temp_p, puzzle, is_attacker_player=True)
            puzzle['monster_hp'] -= p_dmg
            
            broken_weapons = reduce_equipment_durability(user_id, target_slots=['weapon'], damage=2)
            wpn_msg = f" ⚠️ *Senjata retak parah!*" if broken_weapons else ""
            
            m_dmg1, m_log1 = calculate_damage(puzzle, p, is_attacker_player=False)
            m_dmg2, m_log2 = calculate_damage(puzzle, p, is_attacker_player=False)
            total_m_dmg = m_dmg1 + m_dmg2
            p['hp'] -= total_m_dmg
            
            result_msg = (
                f"🔮 **SKILL BURST:** {p_log} Sihirmu mengenai telak! (-{p_dmg} HP){wpn_msg}\n"
                f"⚠️ **RECOVERY PENALTY:** Kamu kelelahan! {m_name} menyerang 2x! (-{total_m_dmg} HP)"
            )

        # --- 3. AKSI BLOCK (Damage Reduction) ---
        elif action == "block":
            heal_amount = int(p.get('max_hp', 100) * 0.15)
            p['hp'] = min(p.get('max_hp', 100), p['hp'] + heal_amount)
            
            m_dmg, m_log = calculate_damage(puzzle, p, is_attacker_player=False)
            reduced_dmg = max(1, int(m_dmg * 0.2)) 
            p['hp'] -= reduced_dmg
            
            broken_armors = reduce_equipment_durability(user_id, target_slots=['armor', 'head'], damage=1)
            dur_msg = f" ⚠️ *Pelindungmu retak!*" if broken_armors else ""
            
            result_msg = (
                f"🛡️ **BERTAHAN:** Fokus menangkis (+{heal_amount} HP).\n"
                f"👾 **SERANGAN TERTANGKIS:** {m_name} hanya memberikan -{reduced_dmg} HP padamu.{dur_msg}"
            )

        # --- 4. AKSI DODGE (Skip Monster Turn) ---
        elif action == "dodge":
            base_dodge_chance = 0.50
            player_dodge_stat = p['stats'].get('dodge', 0.1) 
            weight_penalty = p['stats'].get('total_weight', 0) * 0.01
            final_dodge_chance = base_dodge_chance + player_dodge_stat - weight_penalty

            if random.random() < final_dodge_chance:
                restore_mp = int(p.get('max_mp', 50) * 0.20)
                p['mp'] = min(p.get('max_mp', 50), p.get('mp', 0) + restore_mp)
                result_msg = (
                    f"💨 **PERFECT DODGE:** Secepat kilat (+{restore_mp} MP).\n"
                    f"🎯 {m_name} menyerang angin dan **kehilangan gilirannya**!"
                )
            else:
                m_dmg, m_log = calculate_damage(puzzle, p, is_attacker_player=False)
                reduced_dmg = max(1, int(m_dmg * 0.7)) 
                p['hp'] -= reduced_dmg
                broken_armors = reduce_equipment_durability(user_id, target_slots=['armor', 'head'], damage=1)
                dur_msg = f" ⚠️ *Pelindung menahan benturan!*" if broken_armors else ""
                result_msg = (
                    f"🧱 **GAGAL MENGHINDAR:** Terlalu lambat!\n"
                    f"👾 **TERKENA HIT:** Serangan {m_name} bersarang di tubuhmu (-{reduced_dmg} HP).{dur_msg}"
                )

        # --- 5. AKSI ITEM (1:1) ---
        elif action == "item":
            item_id = data.get("selected_item_id")
            success, item_msg, p_new = use_consumable_item(p, item_id)
            if success:
                p = p_new
                m_dmg, m_log = calculate_damage(puzzle, p, is_attacker_player=False)
                p['hp'] -= m_dmg
                result_msg = (
                    f"🎒 **PAKAI RAMUAN:** {item_msg}\n"
                    f"👾 **CELAH TERBUKA:** {m_name} menerjang saat kau menenggak ramuan! (-{m_dmg} HP)"
                )
            else:
                result_msg = "❌ Gagal menggunakan item!"

        # --- 6. AKSI KABUR ---
        elif action == "run":
            chance = p['stats']['dodge'] + 0.30 
            if random.random() < chance:
                await state.set_state(GameState.exploring)
                update_player(user_id, {'current_combo': 0})
                if battle_msg_id:
                    try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text="🏃💨 *KABUR!*", parse_mode="Markdown")
                    except: pass
                return await message.answer("🏃💨 Kamu berhasil melarikan diri ke dalam kegelapan.", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
            else:
                m_dmg, m_log = calculate_damage(puzzle, p, is_attacker_player=False)
                p['hp'] -= m_dmg
                result_msg = (
                    f"🧱 **GAGAL KABUR:** {m_name} memblokir jalan keluar!\n"
                    f"👾 **SERANGAN BALIK:** Punggungmu ditebas saat mencoba lari! (-{m_dmg} HP)"
                )
                
        update_player(user_id, {'current_combo': current_combo})

    # --- JAWABAN SALAH / TIMEOUT ---
    else:
        current_combo = 0
        m_dmg, m_log = calculate_damage(puzzle, p, is_attacker_player=False)
        p['hp'] -= int(m_dmg * 1.5)
        
        broken_armors = reduce_equipment_durability(user_id, target_slots=['armor', 'head'], damage=2, chance=1.0)
        dur_msg = f" ⚠️ *Pelindungmu hancur!*" if broken_armors else ""
            
        update_player(user_id, {'current_combo': 0, 'hp': p['hp']})
        result_msg = (
            f"❌ **FOKUS HANCUR:** Segel teka-teki gagal dipecahkan!\n"
            f"💥 **CRITICAL STRIKE:** {m_name} melancarkan serangan brutal! (-{int(m_dmg * 1.5)} HP){dur_msg}"
        )

    # === TICK STATUS EFFECTS (BUFF/DEBUFF) ===
    m_hp_change, m_status_logs = apply_turn_status_effects(puzzle, is_player=False)
    p_hp_change, p_status_logs = apply_turn_status_effects(p, is_player=True)
    
    puzzle['monster_hp'] = max(0, puzzle['monster_hp'] + m_hp_change)
    p['hp'] = max(0, p['hp'] + p_hp_change)
    
    update_player(user_id, {"hp": p['hp'], "mp": p['mp'], "inventory": p['inventory'], "active_effects": p.get('active_effects', [])})
    
    status_log_final = " ".join(m_status_logs + p_status_logs)
    full_log = f"{result_msg}\n{status_log_final}"

    # --- CEK KEMATIAN MUSUH ---
    if puzzle['monster_hp'] <= 0:
        tier = puzzle.get('tier', 1)
        is_boss = puzzle.get('is_boss', False)
        
        base_gold = 500 if is_boss else (int(tier) * 25)
        total_gold = base_gold + int(base_gold * (current_combo * 0.1))
        base_exp = puzzle.get('exp_reward', 10 * tier)
        total_exp = base_exp + int(base_exp * (current_combo * 0.1))
        
        new_exp = p.get('exp', 0) + total_exp
        current_level = p.get('level', 1)
        new_level = calculate_level_from_exp(new_exp)
        
        level_up_msg = ""
        if new_level > current_level:
            new_max_hp = p.get('max_hp', 100) + 10
            new_max_mp = p.get('max_mp', 50) + 5
            update_player(user_id, {'max_hp': new_max_hp, 'max_mp': new_max_mp, 'hp': new_max_hp, 'mp': new_max_mp})
            level_up_msg = f"\n\n🆙 **LEVEL UP!** Kamu telah mencapai Level {new_level}! (+Max HP & MP)"

        drops = process_loot(puzzle.get('drops', []))
        inv = p.get('inventory', [])
        inv.extend(drops)
        
        update_player(user_id, {
            'kills': p['kills']+1, 'gold': p['gold']+total_gold, 
            'exp': new_exp, 'level': new_level, 'current_combo': current_combo, 'inventory': inv
        })
        
        await state.set_state(GameState.exploring)
        if battle_msg_id:
            try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text=f"🎉 **PERTARUNGAN SELESAI** 🎉\n{m_name} telah hancur lebur.", parse_mode="Markdown")
            except: pass
            
        await message.answer(f"🎉 *KEMENANGAN!*\n{full_log}\n\n✨ EXP: +{total_exp}\n💰 Gold: +{total_gold}\n🎁 Drops: {', '.join(drops) if drops else 'Tidak ada'}{level_up_msg}", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
    
    # --- CEK KEMATIAN PEMAIN ---
    elif p['hp'] <= 0:
        msg_text = reset_player_death(user_id, "death_combat")
        await state.set_state(GameState.exploring)
        if battle_msg_id:
            try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text=f"💀 **KAU TELAH GUGUR...**", parse_mode="Markdown")
            except: pass
        await message.answer(f"💀 Dikalahkan oleh {m_name}\n\n{msg_text}", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
        
    # --- MUSUH MASIH HIDUP, LANJUT RONDE ---
    else:
        new_q = get_random_puzzle(puzzle.get('tier', 1))
        puzzle['question'] = new_q['question']
        puzzle['answer'] = str(new_q['answer']).strip().lower()
        puzzle['generated_time'] = None 
        await state.update_data(puzzle=puzzle, current_combo=current_combo, action_type=None)
        
        safe_puzzle = puzzle.copy()
        safe_puzzle['question'] = "Pilih aksi untuk mengungkap segel teka-teki!"
        safe_puzzle['timer'] = "--"
        
        icon = "✅" if is_correct else "⚠️"
        next_msg = render_live_battle(p, safe_puzzle, f"{icon} {full_log}")
        
        if battle_msg_id:
            try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text=next_msg, parse_mode="Markdown", reply_markup=get_stance_keyboard(is_boss))
            except TelegramBadRequest: pass
            
        active_timers[user_id] = asyncio.create_task(combat_timeout_task(message, state, puzzle, user_id))

async def main():
    auto_seed_content()
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
