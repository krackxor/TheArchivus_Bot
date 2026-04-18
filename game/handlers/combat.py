# game/handlers/combat.py

import asyncio
import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramRetryAfter

# === IMPORTS UTAMA ===
from database import get_player, update_player, reset_player_death, add_history
from game.logic.states import GameState
from game.logic.stats import calculate_total_stats
from game.logic.menu_handler import get_main_reply_keyboard, get_stance_keyboard

# Sinkronisasi dengan sistem Quest & Progress Modular
from game.data.quests import update_quest_progress
from game.systems.progression import calculate_level_from_exp

# === IMPORT SISTEM COMBAT & LOGIC ===
from game.logic.combat import (
    generate_battle_data, 
    render_live_battle, 
    process_loot, 
    apply_turn_status_effects, 
    finalize_battle
)
from game.logic.skills import (
    get_available_skills, 
    execute_skill, 
    reduce_all_cooldowns, 
    get_effective_skill, 
    get_cooldown_remaining, 
    get_monster_skill
)
from game.logic.inventory_manager import use_consumable_item
from game.items import get_item

router = Router()

# ==============================================================================
# 1. HELPER KHUSUS COMBAT
# ==============================================================================

def reduce_equipment_durability(user_id, target_slots=['weapon'], damage=1, chance=0.3):
    """Mengurangi durabilitas gear (senjata/armor) saat bertarung."""
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
        
        # Inisialisasi durabilitas jika belum ada
        if slot not in durability_data: durability_data[slot] = 50 
            
        durability_data[slot] -= damage
        updates_needed = True

        if durability_data[slot] <= 0:
            broken_items.append(item_id)
            del equipped[slot]
            del durability_data[slot]
            if item_id in inventory: inventory.remove(item_id)

    if updates_needed:
        update_player(user_id, {
            "equipment_durability": durability_data,
            "equipped": equipped,
            "inventory": inventory
        })

    return broken_items

def get_skill_menu_keyboard(player, player_stats):
    """Membuat pop-up tombol untuk daftar Skill yang sedang tidak Cooldown."""
    available_skills = get_available_skills(player, player_stats)
    keyboard = []
    
    for skill_id in available_skills:
        skill = get_effective_skill(player, skill_id)
        if not skill: continue
            
        cooldown = get_cooldown_remaining(player, skill_id)
        btn_text = f"{skill['name']} - 💧 {skill.get('mp_cost', 0)}"
        
        if cooldown > 0:
            btn_text = f"⏳ {skill['name']} (CD: {cooldown})"
            cb_data = "ignore_cooldown"
        else:
            cb_data = f"useskill_{skill_id}"
            
        keyboard.append([InlineKeyboardButton(text=btn_text, callback_data=cb_data)])
        
    keyboard.append([InlineKeyboardButton(text="❌ Tutup", callback_data="close_popup")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_combat_consumable_menu(player):
    """Membuat pop-up khusus untuk Ramuan di tengah pertarungan."""
    buttons = []
    inventory = player.get('inventory', [])
    counts = {}
    for i in inventory:
        it = get_item(i)
        if it and it.get('type') == 'consumable' and it.get('effect_type') != "trigger_quiz":
            counts[i] = counts.get(i, 0) + 1

    if not counts:
        return [[InlineKeyboardButton(text="📭 Tas Kosong", callback_data="close_popup")]]
    
    row = []
    for i_id, count in counts.items():
        it = get_item(i_id)
        row.append(InlineKeyboardButton(text=f"🧪 {it['name']} ({count}x)", callback_data=f"combat_useitem_{i_id}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row: buttons.append(row)
    
    buttons.append([InlineKeyboardButton(text="❌ Tutup", callback_data="close_popup")])
    return buttons

def apply_monster_turn(enemy_data, player):
    """Mengeksekusi AI Monster (Giliran Musuh) dan menerapkan efek ke pemain."""
    m_skill_id = get_monster_skill(enemy_data)
    m_res_type, m_val, m_status, m_log = execute_skill(enemy_data, player['stats'], m_skill_id, None)
    
    actual_dmg = 0
    if m_res_type == "damage":
        actual_dmg = m_val
        player['hp'] -= m_val
    elif m_res_type == "heal":
        enemy_data['monster_hp'] = min(enemy_data.get('monster_max_hp', 999), enemy_data['monster_hp'] + m_val)
        
    if m_status and m_status not in [e.get('type') for e in player.get('active_effects', [])]:
        player.setdefault('active_effects', []).append({'type': m_status, 'value': 5, 'duration': 3})
        
    return actual_dmg, m_log

# ==============================================================================
# 2. CALLBACK HANDLERS (POP-UP)
# ==============================================================================

@router.callback_query(F.data.in_(["close_popup", "ignore_cooldown"]))
async def popup_handler(callback: CallbackQuery):
    if callback.data == "ignore_cooldown":
        return await callback.answer("⏳ Skill ini masih dalam Cooldown!", show_alert=True)
    try: 
        await callback.message.delete()
        await callback.answer()
    except: 
        pass

@router.callback_query(GameState.in_combat, F.data.startswith("combat_useitem_"))
async def combat_useitem_handler(callback: CallbackQuery, state: FSMContext):
    """Menangani penggunaan Potion di tengah pertarungan."""
    user_id = callback.from_user.id
    item_id = callback.data.replace("combat_useitem_", "")
    p = get_player(user_id)
    
    try: await callback.message.delete()
    except: pass
    
    success, msg, p_new = use_consumable_item(p, item_id)
    if not success:
        return await callback.answer(msg, show_alert=True)

    # Trigger Quest: Potion Addict
    p_new, quest_notif = update_quest_progress(p_new, "use_items", 1)
    
    data_st = await state.get_data()
    enemy_data = data_st.get("enemy_data")
    
    # Monster menyerang balik
    m_dmg, m_log = apply_monster_turn(enemy_data, p_new)
    
    # Tick Efek Status
    m_hpc, m_logs = apply_turn_status_effects(enemy_data, is_player=False)
    p_hpc, p_logs = apply_turn_status_effects(p_new, is_player=True)
    
    enemy_data['monster_hp'] = max(0, enemy_data['monster_hp'] + m_hpc)
    p_new['hp'] = max(0, p_new['hp'] + p_hpc)
    reduce_all_cooldowns(p_new)
    
    current_combo = data_st.get("current_combo", 0)
    update_player(user_id, p_new)
    
    full_log = f"🎒 {msg}\n" + ("\n".join(quest_notif) if quest_notif else "") + f"\n👾 {m_log}\n" + " ".join(m_logs + p_logs)
    await execute_end_of_turn(callback.message, state, user_id, p_new, enemy_data, full_log, current_combo, data_st.get("battle_msg_id"))

# ==============================================================================
# 3. MAIN COMBAT HANDLER (STANCE & SKILL)
# ==============================================================================

@router.callback_query(F.data.startswith("stance_") | F.data.startswith("useskill_"))
async def combat_stance_handler(callback: CallbackQuery, state: FSMContext):
    if await state.get_state() != GameState.in_combat:
        return await callback.answer("⚠️ Pertarungan ini sudah kedaluwarsa.", show_alert=True)
        
    user_id = callback.from_user.id
    p = get_player(user_id)
    p['stats'] = calculate_total_stats(p)
    
    action = ""
    skill_to_cast = None
    
    if callback.data.startswith("stance_"):
        action = callback.data.replace("stance_", "") 
    elif callback.data.startswith("useskill_"):
        action = "cast_skill"
        skill_to_cast = callback.data.replace("useskill_", "")
        try: await callback.message.delete()
        except: pass
    
    if action == "item":
        kb = get_combat_consumable_menu(p)
        return await callback.message.answer("🎒 **PILIH RAMUAN:**", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))

    if action == "skill":
        kb = get_skill_menu_keyboard(p, p['stats'])
        return await callback.message.answer("🔮 **DAFTAR MAGIC & SKILL:**", reply_markup=kb)

    state_data = await state.get_data()
    enemy_data = state_data.get("enemy_data")
    battle_msg_id = state_data.get("battle_msg_id")
    
    if not enemy_data:
        return await callback.answer("❌ Data musuh hilang.", show_alert=True)
        
    result_msg = ""
    current_combo = state_data.get("current_combo", 0)

    # --- LOGIKA AKSI ---
    if action == "attack": 
        current_combo += 1
        res_type, p_val, status, p_log = execute_skill(p['stats'], enemy_data, "basic_attack", p)
        enemy_data['monster_hp'] -= p_val
        reduce_equipment_durability(user_id, target_slots=['weapon'], damage=1)
        m_dmg, m_log = apply_monster_turn(enemy_data, p)
        result_msg = f"⚔️ <b>SERANG:</b> {p_log}\n👾 <b>BALASAN:</b> {m_log}"
        
    elif action == "cast_skill" and skill_to_cast:
        eff_skill = get_effective_skill(p, skill_to_cast)
        mp_cost = eff_skill.get('mp_cost', 0)
        if p.get('mp', 0) < mp_cost:
            return await callback.answer(f"🔮 MP Tidak cukup!", show_alert=True)
            
        current_combo += 1
        p['mp'] -= mp_cost
        
        # Trigger Quest: Ahli Teknik
        p, _ = update_quest_progress(p, "use_skills", 1)
        
        res_type, p_val, status, p_log = execute_skill(p['stats'], enemy_data, skill_to_cast, p)
        reduce_equipment_durability(user_id, target_slots=['weapon'], damage=2)
        
        if res_type == "damage":
            enemy_data['monster_hp'] -= p_val
        elif res_type == "heal":
            p['hp'] = min(p.get('max_hp', 100), p['hp'] + p_val)
        
        m_dmg, m_log = apply_monster_turn(enemy_data, p)
        result_msg = f"🌟 {p_log}\n👾 <b>BALASAN:</b> {m_log}"

    elif action == "block": 
        current_combo = 0 
        heal_amount = int(p.get('max_hp', 100) * 0.10) 
        p['hp'] = min(p.get('max_hp', 100), p['hp'] + heal_amount)
        m_dmg, m_log = apply_monster_turn(enemy_data, p)
        if m_dmg > 0:
            refund = int(m_dmg * 0.8)
            p['hp'] += refund
            reduce_equipment_durability(user_id, target_slots=['armor', 'head'], damage=1)
            result_msg = f"🛡️ <b>TANGKIS:</b> (+{heal_amount} HP).\n👾 <b>DAMPAK:</b> -{max(0, m_dmg - refund)} HP."
        else:
            result_msg = f"🛡️ <b>BERTAHAN:</b> (+{heal_amount} HP).\n👾 <b>MUSUH:</b> {m_log}"

    elif action == "dodge":
        base_dodge = 0.40
        player_dodge = p['stats'].get('dodge', 0.1) 
        final_dodge = min(0.90, max(0.10, base_dodge + player_dodge))

        if random.random() < final_dodge:
            current_combo += 1
            restore_mp = int(p.get('max_mp', 50) * 0.15)
            p['mp'] = min(p.get('max_mp', 50), p.get('mp', 0) + restore_mp)
            result_msg = f"💨 <b>ELAKAN SEMPURNA:</b> (+{restore_mp} MP).\n🎯 Musuh meleset!"
        else:
            current_combo = 0
            m_dmg, m_log = apply_monster_turn(enemy_data, p)
            result_msg = f"🧱 <b>GAGAL MENGELAK!</b> {m_log}"

    elif action == "run":
        if random.random() < (p['stats'].get('dodge', 0.1) + 0.30):
            await state.set_state(GameState.exploring)
            update_player(user_id, {'current_combo': 0, 'skill_cooldowns': {}})
            try: await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=battle_msg_id)
            except: pass
            return await callback.message.answer("🏃💨 Kamu kabur ke kegelapan.", reply_markup=get_main_reply_keyboard(p))
        else:
            current_combo = 0
            m_dmg, m_log = apply_monster_turn(enemy_data, p)
            result_msg = f"🧱 <b>GAGAL KABUR!</b>\n👾 <b>BALASAN:</b> {m_log}"

    # Update Per Round
    m_hpc, m_s_logs = apply_turn_status_effects(enemy_data, is_player=False)
    p_hpc, p_s_logs = apply_turn_status_effects(p, is_player=True)
    enemy_data['monster_hp'] = max(0, enemy_data['monster_hp'] + m_hpc)
    p['hp'] = max(0, p['hp'] + p_hpc)
    reduce_all_cooldowns(p)
    
    update_player(user_id, p)
    full_log = f"{result_msg}\n" + " ".join(m_s_logs + p_s_logs)
    await execute_end_of_turn(callback.message, state, user_id, p, enemy_data, full_log, current_combo, battle_msg_id)

# ==============================================================================
# 4. FINALIZE TURN (RESULTS)
# ==============================================================================

async def execute_end_of_turn(message: Message, state: FSMContext, user_id: int, p: dict, enemy_data: dict, full_log: str, current_combo: int, battle_msg_id: int):
    # --- PEMAIN MENANG ---
    if enemy_data['monster_hp'] <= 0:
        # Trigger Quest: Combo King
        p, combo_notif = update_quest_progress(p, "perform_combo", current_combo)
        
        # Proses Reward Modular & Quest Slayer
        p, loot, quest_notifs = finalize_battle(p, enemy_data)
        
        total_exp = enemy_data['exp_reward']
        old_level = p.get('level', 1)
        p['exp'] += total_exp
        new_level = calculate_level_from_exp(p['exp'])
        
        level_up_msg = ""
        if new_level > old_level:
            p['level'] = new_level
            level_up_msg = f"\n\n🆙 <b>LEVEL UP! ({new_level})</b>"
        
        update_player(user_id, p)
        add_history(user_id, f"Menang melawan {enemy_data['monster_name']} (Combo x{current_combo})")
        
        if battle_msg_id:
            try: await message.bot.delete_message(chat_id=message.chat.id, message_id=battle_msg_id)
            except: pass
        
        await state.set_state(GameState.exploring)
        safe_loot = ", ".join(loot).replace('_',' ').title() if loot else "None"
        victory_text = (
            f"🎉 <b>KEMENANGAN!</b>\n━━━━━━━━━━━━━━━━━━━━\n"
            f"👾 <b>{enemy_data['monster_name']}</b> telah tumbang!\n"
            f"✨ EXP: +{total_exp} | 💰 Gold: +{enemy_data['gold_reward']}\n"
            f"🎁 Loot: {safe_loot}\n"
            f"{''.join(quest_notifs)}{''.join(combo_notif)}{level_up_msg}"
        )
        await message.answer(victory_text, reply_markup=get_main_reply_keyboard(p), parse_mode="HTML")
        return

    # --- PEMAIN MATI ---
    elif p['hp'] <= 0:
        death_text = reset_player_death(user_id, f"Dibunuh oleh {enemy_data['monster_name']}")
        await state.set_state(GameState.exploring)
        if battle_msg_id:
            try: await message.bot.delete_message(chat_id=message.chat.id, message_id=battle_msg_id)
            except: pass
        await message.answer(f"💀 <b>TERKUNCI DALAM KEGELAPAN</b>\n\n{death_text}", reply_markup=get_main_reply_keyboard(p), parse_mode="HTML")
        return
        
    # --- PERTARUNGAN BERLANJUT ---
    else:
        await state.update_data(enemy_data=enemy_data, current_combo=current_combo)
        next_msg = render_live_battle(p, enemy_data, f"💬 {full_log}")
        if battle_msg_id:
            try:
                await message.bot.edit_message_text(
                    chat_id=message.chat.id, message_id=battle_msg_id, 
                    text=next_msg, parse_mode="HTML", 
                    reply_markup=get_stance_keyboard(enemy_data.get('is_boss', False))
                )
            except TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after)
            except Exception:
                new_battle_msg = await message.answer(next_msg, parse_mode="HTML", reply_markup=get_stance_keyboard(enemy_data.get('is_boss', False)))
                await state.update_data(battle_msg_id=new_battle_msg.message_id)
