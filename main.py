# main.py

import asyncio
import random
import os
import time
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest, TelegramRetryAfter

# === ROOT IMPORTS ===
from database import client, get_player, update_player, auto_seed_content, reset_player_death, add_history, tick_buffs
from game.logic.states import GameState
from config import BOT_TOKEN

# === NEW ARCHITECTURE IMPORTS (LOGIC FOLDER) ===
from game.logic.combat import (
    generate_battle_data, calculate_damage, 
    render_live_battle, process_loot, apply_turn_status_effects
)
# IMPORT SISTEM SKILL BARU
from game.logic.skills import (
    get_available_skills, execute_skill, reduce_all_cooldowns, 
    get_effective_skill, get_cooldown_remaining, ACTIVE_SKILLS, get_monster_skill
)
from game.logic.stats import calculate_total_stats
from game.logic.inventory_manager import equip_item, unequip_item, process_repair_all, use_consumable_item
from game.logic.menu_handler import get_inventory_menu, get_profile_menu, get_consumable_menu, get_profile_main_menu, generate_profile_text

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
    create_combo_indicator, create_boss_warning,
    create_death_screen, create_location_transition, create_inventory_display,
    create_daily_quest_card
)

dp = Dispatcher()
ADMIN_ID = 123456789 

# === HELPER DURABILITY ===
def reduce_equipment_durability(user_id, target_slots=['weapon'], damage=1, chance=0.3):
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
        InlineKeyboardButton(text="🔮 Skill", callback_data="stance_skill") # Tombol untuk buka menu skill
    ]
    row2 = [
        InlineKeyboardButton(text="🛡️ Bertahan", callback_data="stance_block"),
        InlineKeyboardButton(text="💨 Menghindar", callback_data="stance_dodge")
    ]
    row3 = [InlineKeyboardButton(text="🎒 Item", callback_data="stance_item")]
    if not is_boss: row3.append(InlineKeyboardButton(text="🏃 Kabur", callback_data="stance_run"))
    return InlineKeyboardMarkup(inline_keyboard=[row1, row2, row3])

# Membuat Menu Pop-up untuk Skill
def get_skill_menu_keyboard(player, player_stats):
    available_skills = get_available_skills(player, player_stats)
    keyboard = []
    
    for skill_id in available_skills:
        skill = get_effective_skill(player, skill_id)
        if not skill: continue
            
        cooldown = get_cooldown_remaining(player, skill_id)
        btn_text = f"{skill['name']} - 💧 {skill['mp_cost']}"
        
        if cooldown > 0:
            btn_text = f"⏳ {skill['name']} (CD: {cooldown})"
            cb_data = "ignore_cooldown"
        else:
            cb_data = f"useskill_{skill_id}"
            
        keyboard.append([InlineKeyboardButton(text=btn_text, callback_data=cb_data)])
        
    keyboard.append([InlineKeyboardButton(text="🔙 Kembali", callback_data="close_popup")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# === COMMAND HANDLERS ===
@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.first_name
    player = get_player(user_id, username)
    
    # Inisialisasi dictionary skill jika player baru
    if 'skill_usages' not in player: player['skill_usages'] = {}
    if 'skill_cooldowns' not in player: player['skill_cooldowns'] = {}
    update_player(user_id, {"skill_usages": player['skill_usages'], "skill_cooldowns": player['skill_cooldowns']})
    
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

# Menutup pop-up menu (kembali ke battle UI utama)
@dp.callback_query(F.data == "close_popup" | F.data == "ignore_cooldown")
async def popup_handler(callback: CallbackQuery, state: FSMContext):
    if callback.data == "ignore_cooldown":
        return await callback.answer("⏳ Skill ini belum siap digunakan!", show_alert=True)
    try: await callback.message.delete()
    except: pass

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

# === HELPER: MONSTER AI TURN ===
def apply_monster_turn(enemy_data, player):
    """Mengeksekusi AI Monster dan menerapkan efek ke pemain."""
    m_skill_id = get_monster_skill(enemy_data)
    m_res_type, m_val, m_status, m_log = execute_skill(enemy_data, player['stats'], m_skill_id, None)
    
    actual_dmg = 0
    if m_res_type == "damage":
        actual_dmg = m_val
        player['hp'] -= m_val
    elif m_res_type == "heal":
        enemy_data['monster_hp'] = min(enemy_data.get('monster_max_hp', 999), enemy_data['monster_hp'] + m_val)
        
    # Terapkan Debuff jika ada
    if m_status and m_status not in [e.get('type') for e in player.get('active_effects', [])]:
        player.setdefault('active_effects', []).append({'type': m_status, 'value': 5, 'duration': 3})
        
    return actual_dmg, m_log

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
        current_state = await state.get_state()
        
        try: await callback.message.delete()
        except: pass
        
        if current_state == GameState.in_combat:
            success, msg, p_new = use_consumable_item(p, item_id)
            if not success:
                return await callback.answer(msg, show_alert=True)
            
            p = p_new
            data_st = await state.get_data()
            enemy_data = data_st.get("enemy_data")
            m_name = enemy_data.get('monster_name', 'Musuh')
            
            m_dmg, m_log = apply_monster_turn(enemy_data, p)
            result_msg = f"🎒 <b>PAKAI RAMUAN:</b> {msg}\n👾 <b>BALASAN:</b> {m_log}"
            
            m_hpc, m_logs = apply_turn_status_effects(enemy_data, is_player=False)
            p_hpc, p_logs = apply_turn_status_effects(p, is_player=True)
            enemy_data['monster_hp'] = max(0, enemy_data['monster_hp'] + m_hpc)
            p['hp'] = max(0, p['hp'] + p_hpc)
            
            reduce_all_cooldowns(p)
            current_combo = data_st.get("current_combo", 0) + 1
            update_player(user_id, {"hp": p['hp'], "mp": p['mp'], "inventory": p['inventory'], "active_effects": p.get('active_effects', []), "skill_cooldowns": p.get('skill_cooldowns', {})})
            
            full_log = f"{result_msg}\n" + " ".join(m_logs + p_logs)
            await execute_end_of_turn(callback.message, state, user_id, p, enemy_data, full_log, current_combo, data_st.get("battle_msg_id"))
        else:
            success, msg, p_new = use_consumable_item(p, item_id)
            if success:
                update_player(user_id, {'hp': p_new['hp'], 'mp': p_new['mp'], 'inventory': p_new['inventory'], 'active_effects': p_new.get('active_effects', [])})
                await callback.answer(msg, show_alert=True)

# === MOVEMENT & EXPLORATION ===
@dp.message(F.text.in_(["⬆️ Utara", "⬅️ Barat", "Timur ➡️", "⬇️ Selatan"]))
async def move_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    current_state = await state.get_state()
    
    if current_state in [GameState.in_combat, GameState.in_event, GameState.in_rest_area]:
        try: await message.delete() 
        except: pass
        warning_msg = await message.answer("⚠️ Selesaikan dulu urusanmu di depan sebelum bergerak maju!")
        await asyncio.sleep(3)
        try: await message.bot.delete_message(chat_id=message.chat.id, message_id=warning_msg.message_id)
        except: pass
        return
        
    try: await message.delete()
    except: pass
    
    state_data = await state.get_data()
    last_expl_msg = state_data.get("last_expl_msg_id")
    if last_expl_msg:
        try: await message.bot.delete_message(chat_id=message.chat.id, message_id=last_expl_msg)
        except: pass

    await state.set_state(GameState.exploring)
    tick_buffs(user_id) 
    p = get_player(user_id)
    p['stats'] = calculate_total_stats(p) 
    
    if 'skill_usages' not in p: p['skill_usages'] = {}
    if 'skill_cooldowns' not in p: p['skill_cooldowns'] = {}
    
    new_energy = p.get('energy', 100) - 1
    update_player(user_id, {"energy": new_energy})
    
    event_type, event_data, narration = process_move(user_id)
    
    if event_type in ["boss", "monster", "miniboss"]:
        is_boss = (event_type == "boss")
        is_miniboss = (event_type == "miniboss")
        tier_level = 5 if is_boss else min(5, max(1, (p['kills'] // 5) + 1))
        
        enemy_data = generate_battle_data(p, tier_level, is_boss=is_boss, is_miniboss=is_miniboss)
        
        await state.set_state(GameState.in_combat)
        safe_narration = narration.replace("**", "")
        combat_ui = render_live_battle(p, enemy_data, f"⚠️ <b>{safe_narration}</b>")
        
        sent_msg = await message.answer(combat_ui, parse_mode="HTML", reply_markup=get_stance_keyboard(is_boss))
        
        await state.update_data(
            battle_msg_id=sent_msg.message_id,
            enemy_data=enemy_data, 
            current_combo=0,
            last_expl_msg_id=None
        )
    else:
        sent_msg = await message.answer(f"{narration}\n⚡ Energi: {new_energy}/100", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
        await state.update_data(last_expl_msg_id=sent_msg.message_id)


# === PUSAT LOGIKA COMBAT TURN-BASED ===
@dp.callback_query(F.data.startswith("stance_") | F.data.startswith("useskill_"))
async def combat_stance_handler(callback: CallbackQuery, state: FSMContext):
    if await state.get_state() != GameState.in_combat:
        return await callback.answer("⚠️ Sesi pertarungan ini sudah kedaluwarsa.", show_alert=True)
        
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
        kb = get_consumable_menu(p)
        if not kb or len(kb) <= 1: return await callback.answer("Tas ramuanmu kosong!", show_alert=True)
        return await callback.message.answer("🎒 **PILIH RAMUAN:**", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))

    if action == "skill":
        kb = get_skill_menu_keyboard(p, p['stats'])
        return await callback.message.answer("🔮 **DAFTAR MAGIC & SKILL:**", reply_markup=kb)

    state_data = await state.get_data()
    enemy_data = state_data.get("enemy_data")
    battle_msg_id = state_data.get("battle_msg_id")
    
    if not enemy_data:
        return await callback.answer("Data musuh tidak ditemukan.", show_alert=True)
        
    m_name = enemy_data.get('monster_name', 'Musuh')
    result_msg = ""
    current_combo = state_data.get("current_combo", 0) + 1

    # --- 3. EKSEKUSI AKSI PEMAIN ---
    if action == "attack": 
        res_type, p_val, status, p_log = execute_skill(p['stats'], enemy_data, "basic_attack", p)
        enemy_data['monster_hp'] -= p_val
        broken_weapons = reduce_equipment_durability(user_id, target_slots=['weapon'], damage=1)
        wpn_msg = f" ⚠️ <i>Senjata retak!</i>" if broken_weapons else ""
        
        m_dmg, m_log = apply_monster_turn(enemy_data, p)
        result_msg = f"⚔️ <b>SERANG:</b> {p_log}{wpn_msg}\n👾 <b>BALASAN:</b> {m_log}"
        
    elif action == "cast_skill" and skill_to_cast:
        skill_info = ACTIVE_SKILLS.get(skill_to_cast)
        mp_cost = get_effective_skill(p, skill_to_cast).get('mp_cost', 0)
        if p.get('mp', 0) < mp_cost:
            return await callback.answer(f"🔮 MP Tidak cukup! Butuh {mp_cost} MP.", show_alert=True)
            
        p['mp'] -= mp_cost
        
        res_type, p_val, status, p_log = execute_skill(p['stats'], enemy_data, skill_to_cast, p)
        broken_weapons = reduce_equipment_durability(user_id, target_slots=['weapon'], damage=2)
        wpn_msg = f" ⚠️ <i>Senjata retak!</i>" if broken_weapons else ""
        
        if res_type == "damage":
            enemy_data['monster_hp'] -= p_val
            if status and status not in [e['type'] for e in enemy_data['monster_effects']]:
                enemy_data['monster_effects'].append({'type': status, 'value': int(p_val * 0.2) or 5})
        elif res_type == "heal":
            p['hp'] = min(p.get('max_hp', 100), p['hp'] + p_val)
        
        m_dmg, m_log = apply_monster_turn(enemy_data, p)
        result_msg = f"🌟 {p_log}{wpn_msg}\n👾 <b>BALASAN:</b> {m_log}"

    elif action == "block": 
        heal_amount = int(p.get('max_hp', 100) * 0.15)
        p['hp'] = min(p.get('max_hp', 100), p['hp'] + heal_amount)
        
        m_dmg, m_log = apply_monster_turn(enemy_data, p)
        if m_dmg > 0:
            refund = int(m_dmg * 0.8) # Kurangi damage 80%
            p['hp'] += refund
            reduced_dmg = m_dmg - refund
            broken_armors = reduce_equipment_durability(user_id, target_slots=['armor', 'head'], damage=1)
            dur_msg = f" ⚠️ <i>Pelindung retak!</i>" if broken_armors else ""
            result_msg = f"🛡️ <b>BERTAHAN:</b> (+{heal_amount} HP).\n👾 <b>TERTANGKIS:</b> {m_log} (-{reduced_dmg} HP).{dur_msg}"
        else:
            result_msg = f"🛡️ <b>BERTAHAN:</b> (+{heal_amount} HP).\n👾 <b>MUSUH:</b> {m_log}"

    elif action == "dodge":
        base_dodge_chance = 0.50
        player_dodge_stat = p['stats'].get('dodge', 0.1) 
        weight_penalty = p['stats'].get('total_weight', 0) * 0.01
        final_dodge_chance = base_dodge_chance + player_dodge_stat - weight_penalty

        if random.random() < final_dodge_chance:
            restore_mp = int(p.get('max_mp', 50) * 0.20)
            p['mp'] = min(p.get('max_mp', 50), p.get('mp', 0) + restore_mp)
            result_msg = f"💨 <b>PERFECT DODGE:</b> Menghindar kilat (+{restore_mp} MP).\n🎯 {m_name} menyerang angin dan kehilangan gilirannya!"
        else:
            m_dmg, m_log = apply_monster_turn(enemy_data, p)
            if m_dmg > 0:
                refund = int(m_dmg * 0.3) # Terkena damage 70% karena gagal menghindar
                p['hp'] += refund
                reduced_dmg = m_dmg - refund
                broken_armors = reduce_equipment_durability(user_id, target_slots=['armor', 'head'], damage=1)
                dur_msg = f" ⚠️ <i>Pelindung retak!</i>" if broken_armors else ""
                result_msg = f"🧱 <b>GAGAL MENGHINDAR:</b> Terlalu lambat! {m_log} (-{reduced_dmg} HP).{dur_msg}"
            else:
                result_msg = f"🧱 <b>GAGAL MENGHINDAR:</b> Terlalu lambat!\n👾 <b>MUSUH:</b> {m_log}"

    elif action == "run":
        chance = p['stats']['dodge'] + 0.30 
        if random.random() < chance:
            await state.set_state(GameState.exploring)
            update_player(user_id, {'current_combo': 0})
            try: await message.bot.delete_message(chat_id=message.chat.id, message_id=battle_msg_id)
            except: pass
            
            p['skill_cooldowns'] = {}
            update_player(user_id, {'skill_cooldowns': {}})
            
            return await callback.message.answer("🏃💨 Kamu berhasil melarikan diri ke dalam kegelapan.", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
        else:
            m_dmg, m_log = apply_monster_turn(enemy_data, p)
            result_msg = f"🧱 <b>GAGAL KABUR:</b> Jalan diblokir!\n👾 <b>BALASAN:</b> {m_log}"

    # --- 4. TICK STATUS EFFECTS & COOLDOWN ---
    m_hp_change, m_status_logs = apply_turn_status_effects(enemy_data, is_player=False)
    p_hp_change, p_status_logs = apply_turn_status_effects(p, is_player=True)
    
    enemy_data['monster_hp'] = max(0, enemy_data['monster_hp'] + m_hp_change)
    p['hp'] = max(0, p['hp'] + p_hp_change)
    
    reduce_all_cooldowns(p)
    
    update_player(user_id, {
        "hp": p['hp'], "mp": p['mp'], 
        "inventory": p['inventory'], 
        "active_effects": p.get('active_effects', []),
        "skill_usages": p.get('skill_usages', {}),
        "skill_cooldowns": p.get('skill_cooldowns', {}),
        "last_skill_used": p.get('last_skill_used', None)
    })
    
    status_log_final = " ".join(m_status_logs + p_status_logs)
    full_log = f"{result_msg}\n{status_log_final}"

    await execute_end_of_turn(callback.message, state, user_id, p, enemy_data, full_log, current_combo, battle_msg_id)


# === HELPER: FASE END OF TURN & CHECK DEATH ===
async def execute_end_of_turn(message: Message, state: FSMContext, user_id: int, p: dict, enemy_data: dict, full_log: str, current_combo: int, battle_msg_id: int):
    m_name = enemy_data.get('monster_name', 'Musuh')
    
    if enemy_data['monster_hp'] <= 0:
        tier = enemy_data.get('tier', 1)
        is_boss = enemy_data.get('is_boss', False)
        
        base_gold = 500 if is_boss else (int(tier) * 25)
        total_gold = base_gold + int(base_gold * (current_combo * 0.1))
        base_exp = enemy_data.get('exp_reward', 10 * tier)
        total_exp = base_exp + int(base_exp * (current_combo * 0.1))
        
        new_exp = p.get('exp', 0) + total_exp
        current_level = p.get('level', 1)
        new_level = calculate_level_from_exp(new_exp)
        
        level_up_msg = ""
        if new_level > current_level:
            new_max_hp = p.get('max_hp', 100) + 10
            new_max_mp = p.get('max_mp', 50) + 5
            update_player(user_id, {'max_hp': new_max_hp, 'max_mp': new_max_mp, 'hp': new_max_hp, 'mp': new_max_mp})
            level_up_msg = f"\n\n🆙 <b>LEVEL UP!</b> Kamu telah mencapai Level {new_level}! (+Max HP & MP)"

        drops = process_loot(enemy_data.get('drops', []))
        inv = p.get('inventory', [])
        inv.extend(drops)
        
        update_player(user_id, {
            'kills': p['kills']+1, 'gold': p['gold']+total_gold, 
            'exp': new_exp, 'level': new_level, 'current_combo': 0, 'inventory': inv,
            'skill_cooldowns': {}
        })
        
        await state.set_state(GameState.exploring)
        
        if battle_msg_id:
            try: await message.bot.delete_message(chat_id=message.chat.id, message_id=battle_msg_id)
            except: pass
        
        safe_drops = ", ".join(drops).replace("_", " ").title() if drops else "Tidak ada"
        
        victory_text = (
            f"🎉 <b>KEMENANGAN!</b>\n"
            f"{full_log}\n\n"
            f"✨ EXP: +{total_exp}\n"
            f"💰 Gold: +{total_gold}\n"
            f"🎁 Drops: {safe_drops}"
            f"{level_up_msg}"
        )
        
        sent_msg = await message.answer(victory_text, reply_markup=get_main_reply_keyboard(p), parse_mode="HTML")
        await state.update_data(last_expl_msg_id=sent_msg.message_id)
        return
    
    elif p['hp'] <= 0:
        msg_text = reset_player_death(user_id, "death_combat")
        await state.set_state(GameState.exploring)
        
        if battle_msg_id:
            try: await message.bot.delete_message(chat_id=message.chat.id, message_id=battle_msg_id)
            except: pass
            
        await message.answer(f"💀 Dikalahkan oleh {m_name}\n\n{msg_text}", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
        return
        
    else:
        await state.update_data(enemy_data=enemy_data, current_combo=current_combo, action_type=None)
        
        next_msg = render_live_battle(p, enemy_data, f"✅ {full_log}")
        
        if battle_msg_id:
            try:
                await message.bot.edit_message_text(
                    chat_id=message.chat.id, 
                    message_id=battle_msg_id, 
                    text=next_msg, 
                    parse_mode="HTML", 
                    reply_markup=get_stance_keyboard(enemy_data.get('is_boss', False))
                )
            except TelegramRetryAfter as e:
                print(f"Rate limited by Telegram. Sleep for {e.retry_after} seconds.")
            except TelegramBadRequest as e:
                if "can't parse entities" in str(e):
                    try:
                        await message.bot.edit_message_text(
                            chat_id=message.chat.id, 
                            message_id=battle_msg_id, 
                            text=next_msg, 
                            parse_mode=None, 
                            reply_markup=get_stance_keyboard(enemy_data.get('is_boss', False))
                        )
                    except: pass


# === EVENT PUZZLE (NON-COMBAT / EKSPLORASI) ===
@dp.message(GameState.in_event)
async def event_puzzle_handler(message: Message, state: FSMContext):
    """Placeholder untuk event puzzle di eksplorasi."""
    pass


async def main():
    auto_seed_content()
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
