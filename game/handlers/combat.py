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
from game.systems.achievements import update_quest_progress, calculate_level_from_exp

# === IMPORT SISTEM COMBAT & LOGIC ===
from game.logic.combat import generate_battle_data, render_live_battle, process_loot, apply_turn_status_effects
from game.logic.skills import get_available_skills, execute_skill, reduce_all_cooldowns, get_effective_skill, get_cooldown_remaining, get_monster_skill
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
        # Cegah pemain membaca buku (trigger_quiz) di tengah pertarungan
        if it and it.get('type') == 'consumable' and it.get('effect_type') != "trigger_quiz":
            counts[i] = counts.get(i, 0) + 1

    if not counts:
        return [[InlineKeyboardButton(text="📭 Tas Kosong", callback_data="close_popup")]]
    
    row = []
    for i_id, count in counts.items():
        it = get_item(i_id)
        # Gunakan 'combat_useitem_' agar tidak ditolak oleh menu.py
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
# 2. POP-UP HANDLER (SKILL & ITEM COMBAT)
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
    """Menangani saat pemain menggunakan Potion di tengah pertarungan."""
    user_id = callback.from_user.id
    item_id = callback.data.replace("combat_useitem_", "")
    p = get_player(user_id)
    
    # Hapus menu popup item
    try: await callback.message.delete()
    except: pass
    
    success, msg, p_new = use_consumable_item(p, item_id)
    if not success:
        return await callback.answer(msg, show_alert=True)

    quest_notif = update_quest_progress(p_new, "use_items", 1)
    data_st = await state.get_data()
    enemy_data = data_st.get("enemy_data")
    
    # Monster menyerang balik saat kita minum potion
    m_dmg, m_log = apply_monster_turn(enemy_data, p_new)
    
    # Tick Efek Status (Racun, Burn, dll)
    m_hpc, m_logs = apply_turn_status_effects(enemy_data, is_player=False)
    p_hpc, p_logs = apply_turn_status_effects(p_new, is_player=True)
    
    enemy_data['monster_hp'] = max(0, enemy_data['monster_hp'] + m_hpc)
    p_new['hp'] = max(0, p_new['hp'] + p_hpc)
    reduce_all_cooldowns(p_new)
    
    current_combo = data_st.get("current_combo", 0) + 1 # Minum item mempertahankan combo
    
    update_player(user_id, {
        "hp": p_new['hp'], "mp": p_new['mp'], 
        "inventory": p_new['inventory'], 
        "active_effects": p_new.get('active_effects', []),
        "daily_quests": p_new.get('daily_quests', []),
        "skill_cooldowns": p_new.get('skill_cooldowns', {})
    })
    
    full_log = f"🎒 {msg}\n{quest_notif}\n👾 {m_log}\n" + " ".join(m_logs + p_logs)
    await execute_end_of_turn(callback.message, state, user_id, p_new, enemy_data, full_log, current_combo, data_st.get("battle_msg_id"))


# ==============================================================================
# 3. MAIN COMBAT HANDLER (ATTACK, BLOCK, DODGE, SKILL)
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
    
    # --- A. TAMPILKAN SUB-MENU ---
    if action == "item":
        kb = get_combat_consumable_menu(p)
        return await callback.message.answer("🎒 **PILIH RAMUAN:**", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))

    if action == "skill":
        kb = get_skill_menu_keyboard(p, p['stats'])
        return await callback.message.answer("🔮 **DAFTAR MAGIC & SKILL:**", reply_markup=kb)

    # --- B. PREPARASI DATA COMBAT ---
    state_data = await state.get_data()
    enemy_data = state_data.get("enemy_data")
    battle_msg_id = state_data.get("battle_msg_id")
    
    if not enemy_data:
        return await callback.answer("❌ Data musuh hilang.", show_alert=True)
        
    m_name = enemy_data.get('monster_name', 'Musuh')
    result_msg = ""
    current_combo = state_data.get("current_combo", 0)

    # --- C. EKSEKUSI AKSI PEMAIN ---
    if action == "attack": 
        current_combo += 1
        res_type, p_val, status, p_log = execute_skill(p['stats'], enemy_data, "basic_attack", p)
        enemy_data['monster_hp'] -= p_val
        reduce_equipment_durability(user_id, target_slots=['weapon'], damage=1)
        
        m_dmg, m_log = apply_monster_turn(enemy_data, p)
        result_msg = f"⚔️ <b>SERANG:</b> {p_log}\n👾 <b>BALASAN:</b> {m_log}"
        
    elif action == "cast_skill" and skill_to_cast:
        eff_skill = get_effective_skill(p, skill_to_cast)
        if not eff_skill: return await callback.answer("❌ Skill tidak valid.", show_alert=True)
            
        mp_cost = eff_skill.get('mp_cost', 0)
        if p.get('mp', 0) < mp_cost:
            return await callback.answer(f"🔮 MP Tidak cukup! Butuh {mp_cost} MP.", show_alert=True)
            
        current_combo += 1
        p['mp'] -= mp_cost
        res_type, p_val, status, p_log = execute_skill(p['stats'], enemy_data, skill_to_cast, p)
        reduce_equipment_durability(user_id, target_slots=['weapon'], damage=2)
        
        if res_type == "damage":
            enemy_data['monster_hp'] -= p_val
            if status and status not in [e['type'] for e in enemy_data.get('monster_effects', [])]:
                enemy_data.setdefault('monster_effects', []).append({'type': status, 'value': int(p_val * 0.2) or 5})
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
            refund = int(m_dmg * 0.8) # 80% Damage ditangkis
            p['hp'] += refund
            reduce_equipment_durability(user_id, target_slots=['armor', 'head'], damage=1)
            result_msg = f"🛡️ <b>BERTAHAN:</b> (+{heal_amount} HP).\n👾 <b>TERTANGKIS:</b> {m_log} (-{max(0, m_dmg - refund)} HP)."
        else:
            result_msg = f"🛡️ <b>BERTAHAN:</b> (+{heal_amount} HP).\n👾 <b>MUSUH:</b> {m_log}"

    elif action == "dodge":
        base_dodge = 0.40
        player_dodge = p['stats'].get('dodge', 0.1) 
        weight_penalty = p['stats'].get('total_weight', 0) * 0.005 
        final_dodge = min(0.90, max(0.10, base_dodge + player_dodge - weight_penalty))

        if random.random() < final_dodge:
            current_combo += 1
            restore_mp = int(p.get('max_mp', 50) * 0.15)
            p['mp'] = min(p.get('max_mp', 50), p.get('mp', 0) + restore_mp)
            result_msg = f"💨 <b>PERFECT DODGE:</b> (+{restore_mp} MP).\n🎯 {m_name} menyerang angin!"
        else:
            current_combo = 0
            m_dmg, m_log = apply_monster_turn(enemy_data, p)
            if m_dmg > 0:
                refund = int(m_dmg * 0.2) 
                p['hp'] += refund
                reduce_equipment_durability(user_id, target_slots=['armor', 'head'], damage=1)
                result_msg = f"🧱 <b>GAGAL DODGE!</b> {m_log} (-{m_dmg - refund} HP)."
            else:
                result_msg = f"🧱 <b>GAGAL DODGE!</b>\n👾 <b>MUSUH:</b> {m_log}"

    elif action == "run":
        chance = p['stats'].get('dodge', 0.1) + 0.30 
        if random.random() < chance:
            await state.set_state(GameState.exploring)
            update_player(user_id, {'current_combo': 0, 'skill_cooldowns': {}})
            try: await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=battle_msg_id)
            except: pass
            return await callback.message.answer("🏃💨 Kamu berhasil melarikan diri ke dalam kabut.", reply_markup=get_main_reply_keyboard(p))
        else:
            current_combo = 0
            m_dmg, m_log = apply_monster_turn(enemy_data, p)
            result_msg = f"🧱 <b>GAGAL KABUR!</b>\n👾 <b>BALASAN:</b> {m_log}"

    # --- D. STATUS EFFECTS & TICK ---
    m_hp_change, m_status_logs = apply_turn_status_effects(enemy_data, is_player=False)
    p_hp_change, p_status_logs = apply_turn_status_effects(p, is_player=True)
    
    enemy_data['monster_hp'] = max(0, enemy_data['monster_hp'] + m_hp_change)
    p['hp'] = max(0, p['hp'] + p_hp_change)
    
    reduce_all_cooldowns(p)
    
    update_player(user_id, {
        "hp": p['hp'], "mp": p['mp'], 
        "active_effects": p.get('active_effects', []),
        "skill_usages": p.get('skill_usages', {}),
        "skill_cooldowns": p.get('skill_cooldowns', {}),
        "current_combo": current_combo
    })
    
    status_log_final = " ".join(m_status_logs + p_status_logs)
    full_log = f"{result_msg}\n{status_log_final}"

    # --- E. FINALIZE TURN ---
    await execute_end_of_turn(callback.message, state, user_id, p, enemy_data, full_log, current_combo, battle_msg_id)


# ==============================================================================
# 4. END OF TURN (MENANG, MATI, ATAU LANJUT)
# ==============================================================================

async def execute_end_of_turn(message: Message, state: FSMContext, user_id: int, p: dict, enemy_data: dict, full_log: str, current_combo: int, battle_msg_id: int):
    m_name = enemy_data.get('monster_name', 'Musuh')
    
    # --- SKENARIO 1: PEMAIN MENANG ---
    if enemy_data['monster_hp'] <= 0:
        tier = enemy_data.get('tier', 1)
        is_boss = enemy_data.get('is_boss', False)
        
        # Kalkulasi Reward & Combo Bonus
        combo_bonus = 1 + (current_combo * 0.1)
        total_gold = int((500 if is_boss else (tier * 25)) * combo_bonus)
        total_exp = int(enemy_data.get('exp_reward', 15 * tier) * combo_bonus)
        
        # Quest Updates
        quest_notif = update_quest_progress(p, "kill_monsters", 1)
        if is_boss or enemy_data.get('is_miniboss'):
            quest_notif += update_quest_progress(p, "kill_boss", 1)
        quest_notif += update_quest_progress(p, "earn_gold", total_gold)
        quest_notif += update_quest_progress(p, "perform_combo", current_combo)

        # Proses Level Up
        new_exp = p.get('exp', 0) + total_exp
        old_level = p.get('level', 1)
        new_level = calculate_level_from_exp(new_exp)
        
        level_up_msg = ""
        if new_level > old_level:
            hp_gain = 15 + (new_level * 2)
            mp_gain = 5 + (new_level)
            new_max_hp = p.get('max_hp', 100) + hp_gain
            new_max_mp = p.get('max_mp', 50) + mp_gain
            p.update({'max_hp': new_max_hp, 'max_mp': new_max_mp, 'hp': new_max_hp, 'mp': new_max_mp, 'level': new_level})
            level_up_msg = f"\n\n🆙 <b>LEVEL UP!</b> ({old_level} ➜ {new_level})\n💖 Max HP +{hp_gain} | 💧 Max MP +{mp_gain}"

        # Proses Loot
        drops = process_loot(enemy_data.get('drops', []))
        inv = p.get('inventory', [])
        inv.extend(drops)
        
        update_player(user_id, {
            'kills': p.get('kills', 0) + 1, 
            'gold': p['gold'] + total_gold, 
            'exp': p['exp'] + total_exp, 
            'level': p['level'],
            'hp': p['hp'], 'max_hp': p.get('max_hp'), 'max_mp': p.get('max_mp'),
            'inventory': inv,
            'daily_quests': p.get('daily_quests'), 
            'current_combo': 0, 'skill_cooldowns': {}
        })
        
        add_history(user_id, f"Menang melawan {m_name} (Combo x{current_combo})")
        if battle_msg_id:
            try: await message.bot.delete_message(chat_id=message.chat.id, message_id=battle_msg_id)
            except: pass
        
        await state.set_state(GameState.exploring)
        safe_drops = ", ".join(drops).replace("_", " ").title() if drops else "Hanya debu..."
        victory_text = (
            f"🎉 <b>KEMENANGAN!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👾 <b>{m_name}</b> telah tumbang!\n"
            f"⚔️ Combo Tertinggi: x{current_combo}\n\n"
            f"✨ EXP: +{total_exp}\n"
            f"💰 Gold: +{total_gold}\n"
            f"🎁 Drops: <i>{safe_drops}</i>"
            f"{quest_notif}{level_up_msg}"
        )
        await message.answer(victory_text, reply_markup=get_main_reply_keyboard(p), parse_mode="HTML")
        return

    # --- SKENARIO 2: PEMAIN MATI ---
    elif p['hp'] <= 0:
        death_text = reset_player_death(user_id, f"Dikalahkan oleh {m_name}")
        await state.set_state(GameState.exploring)
        if battle_msg_id:
            try: await message.bot.delete_message(chat_id=message.chat.id, message_id=battle_msg_id)
            except: pass
        await message.answer(f"💀 <b>ANDA MATI</b>\n\n{death_text}", reply_markup=get_main_reply_keyboard(p), parse_mode="HTML")
        return
        
    # --- SKENARIO 3: PERTARUNGAN LANJUT ---
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
