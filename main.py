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
from game.logic.states import GameState
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
    create_combo_indicator, create_boss_warning,
    create_death_screen, create_location_transition, create_inventory_display
)

dp = Dispatcher()
ADMIN_ID = 123456789 

# === HELPER DURABILITY ===
def reduce_equipment_durability(user_id, target_slots=['weapon'], damage=1, chance=0.3):
    """Sistem Durabilitas: Peluang 30% durability berkurang saat beraksi."""
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
        current_state = await state.get_state()
        
        if current_state == GameState.in_combat:
            # PENGGUNAAN ITEM LANGSUNG DALAM COMBAT (TURN-BASED)
            success, msg, p_new = use_consumable_item(p, item_id)
            if not success:
                return await callback.answer(msg, show_alert=True)
            
            p = p_new
            data_st = await state.get_data()
            puzzle = data_st.get("puzzle")
            m_name = puzzle.get('monster_name', 'Musuh')
            
            # Monster Counter Attack
            m_dmg, m_log = calculate_damage(puzzle, p, is_attacker_player=False)
            p['hp'] -= m_dmg
            result_msg = f"🎒 **PAKAI RAMUAN:** {msg}\n👾 **BALASAN:** {m_name} menyerang! (-{m_dmg} HP)"
            
            # Tick Status Effects
            m_hpc, m_logs = apply_turn_status_effects(puzzle, is_player=False)
            p_hpc, p_logs = apply_turn_status_effects(p, is_player=True)
            puzzle['monster_hp'] = max(0, puzzle['monster_hp'] + m_hpc)
            p['hp'] = max(0, p['hp'] + p_hpc)
            
            current_combo = data_st.get("current_combo", 0) + 1
            update_player(user_id, {"hp": p['hp'], "mp": p['mp'], "inventory": p['inventory'], "active_effects": p.get('active_effects', [])})
            
            full_log = f"{result_msg}\n" + " ".join(m_logs + p_logs)
            await execute_end_of_turn(callback.message, state, user_id, p, puzzle, full_log, current_combo, data_st.get("battle_msg_id"))
            
        else:
            # PENGGUNAAN ITEM DI LUAR COMBAT
            success, msg, p_new = use_consumable_item(p, item_id)
            if success:
                update_player(user_id, {'hp': p_new['hp'], 'mp': p_new['mp'], 'inventory': p_new['inventory'], 'active_effects': p_new.get('active_effects', [])})
                await callback.answer(msg, show_alert=True)
                await callback.message.edit_text("🧪 **Daftar Ramuan:**", reply_markup=InlineKeyboardMarkup(inline_keyboard=get_consumable_menu(p_new)), parse_mode="Markdown")

# === MOVEMENT & EXPLORATION ===
@dp.message(F.text.in_(["⬆️ Utara", "⬅️ Barat", "Timur ➡️", "⬇️ Selatan"]))
async def move_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    current_state = await state.get_state()
    if current_state in [GameState.in_combat, GameState.in_event, GameState.in_rest_area]:
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
        
        # Init combat data (Hanya data statistik, tanpa perlu teka-teki)
        puzzle = generate_battle_puzzle(p, tier_level, is_boss=is_boss, is_miniboss=is_miniboss)
        puzzle['question'] = "Pilih aksimu dari menu di bawah!"
        puzzle['timer'] = "--" 
        
        await state.set_state(GameState.in_combat)
        combat_ui = render_live_battle(p, puzzle, f"⚠️ {narration}")
        sent_msg = await message.answer(combat_ui, parse_mode="Markdown", reply_markup=get_stance_keyboard(is_boss))
        
        await state.update_data(
            battle_msg_id=sent_msg.message_id,
            puzzle=puzzle, 
            current_combo=0
        )
    # EVENT NPC / CHEST YANG MEMBUTUHKAN PUZZLE BISA DIHANDLE DI SINI NANTINYA
    # elif event_type == "chest":
    #    await state.set_state(GameState.in_event)
    else:
        await message.answer(f"{narration}\n⚡ Energi: {new_energy}/100", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")


# === PUSAT LOGIKA COMBAT TURN-BASED (100% PURE BUTTON CLICK) ===
@dp.callback_query(F.data.startswith("stance_"))
async def combat_stance_handler(callback: CallbackQuery, state: FSMContext):
    if await state.get_state() != GameState.in_combat:
        return await callback.answer("⚠️ Sesi pertarungan ini sudah kedaluwarsa.", show_alert=True)
        
    action = callback.data.replace("stance_", "") 
    user_id = callback.from_user.id
    p = get_player(user_id)
    
    # 1. BUKA MENU ITEM SAAT COMBAT
    if action == "item":
        kb = get_consumable_menu(p)
        if not kb or len(kb) <= 1: return await callback.answer("Tas ramuanmu kosong!", show_alert=True)
        return await callback.message.edit_text("🎒 **PILIH RAMUAN:**", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))

    # Ambil Data Combat
    state_data = await state.get_data()
    puzzle = state_data.get("puzzle") # Saat ini berperan murni sebagai 'Enemy Data'
    battle_msg_id = state_data.get("battle_msg_id")
    
    if not puzzle:
        return await callback.answer("Data musuh tidak ditemukan.", show_alert=True)
        
    p['stats'] = calculate_total_stats(p)
    m_name = puzzle.get('monster_name', 'Musuh')
    result_msg = ""
    current_combo = state_data.get("current_combo", 0) + 1

    # --- 2. EKSEKUSI AKSI PEMAIN (TANPA TEKA-TEKI) ---
    if action == "attack": # (1:1 Turn)
        p_dmg, p_log = calculate_damage(p, puzzle, is_attacker_player=True)
        puzzle['monster_hp'] -= p_dmg
        broken_weapons = reduce_equipment_durability(user_id, target_slots=['weapon'], damage=1)
        wpn_msg = f" ⚠️ *Senjata retak!*" if broken_weapons else ""
        
        m_dmg, m_log = calculate_damage(puzzle, p, is_attacker_player=False)
        p['hp'] -= m_dmg
        result_msg = (
            f"⚔️ **SERANG:** {p_log} (-{p_dmg} HP){wpn_msg}\n"
            f"👾 **BALASAN:** {m_log} Kamu -{m_dmg} HP."
        )
        
    elif action == "skill": # (1:2 Turn - Recovery Penalty)
        temp_p = p.copy()
        temp_p['stats']['m_atk'] = int(temp_p['stats']['m_atk'] * 1.8)
        p_dmg, p_log = calculate_damage(temp_p, puzzle, is_attacker_player=True)
        puzzle['monster_hp'] -= p_dmg
        broken_weapons = reduce_equipment_durability(user_id, target_slots=['weapon'], damage=2)
        wpn_msg = f" ⚠️ *Senjata retak!*" if broken_weapons else ""
        
        m_dmg1, m_log1 = calculate_damage(puzzle, p, is_attacker_player=False)
        m_dmg2, m_log2 = calculate_damage(puzzle, p, is_attacker_player=False)
        total_m_dmg = m_dmg1 + m_dmg2
        p['hp'] -= total_m_dmg
        result_msg = (
            f"🔮 **SKILL:** {p_log} (-{p_dmg} HP){wpn_msg}\n"
            f"⚠️ **RECOVERY:** {m_name} menyerang 2x! (-{total_m_dmg} HP)"
        )

    elif action == "block": # (Damage Reduction)
        heal_amount = int(p.get('max_hp', 100) * 0.15)
        p['hp'] = min(p.get('max_hp', 100), p['hp'] + heal_amount)
        
        m_dmg, m_log = calculate_damage(puzzle, p, is_attacker_player=False)
        reduced_dmg = max(1, int(m_dmg * 0.2)) 
        p['hp'] -= reduced_dmg
        broken_armors = reduce_equipment_durability(user_id, target_slots=['armor', 'head'], damage=1)
        dur_msg = f" ⚠️ *Pelindung retak!*" if broken_armors else ""
        
        result_msg = (
            f"🛡️ **BERTAHAN:** Fokus memulihkan diri (+{heal_amount} HP).\n"
            f"👾 **TERTANGKIS:** Serangan {m_name} mereda (-{reduced_dmg} HP).{dur_msg}"
        )

    elif action == "dodge": # (Skip Monster Turn jika berhasil)
        base_dodge_chance = 0.50
        player_dodge_stat = p['stats'].get('dodge', 0.1) 
        weight_penalty = p['stats'].get('total_weight', 0) * 0.01
        final_dodge_chance = base_dodge_chance + player_dodge_stat - weight_penalty

        if random.random() < final_dodge_chance:
            restore_mp = int(p.get('max_mp', 50) * 0.20)
            p['mp'] = min(p.get('max_mp', 50), p.get('mp', 0) + restore_mp)
            result_msg = (
                f"💨 **PERFECT DODGE:** Menghindar kilat (+{restore_mp} MP).\n"
                f"🎯 {m_name} menyerang angin dan **kehilangan gilirannya**!"
            )
        else:
            m_dmg, m_log = calculate_damage(puzzle, p, is_attacker_player=False)
            reduced_dmg = max(1, int(m_dmg * 0.7)) 
            p['hp'] -= reduced_dmg
            broken_armors = reduce_equipment_durability(user_id, target_slots=['armor', 'head'], damage=1)
            dur_msg = f" ⚠️ *Pelindung retak!*" if broken_armors else ""
            result_msg = f"🧱 **GAGAL MENGHINDAR:** Terlalu lambat! (-{reduced_dmg} HP).{dur_msg}"

    elif action == "run":
        chance = p['stats']['dodge'] + 0.30 
        if random.random() < chance:
            await state.set_state(GameState.exploring)
            update_player(user_id, {'current_combo': 0})
            try: await callback.message.edit_text("🏃💨 *KABUR!*", parse_mode="Markdown")
            except: pass
            return await callback.message.answer("🏃💨 Kamu berhasil melarikan diri ke dalam kegelapan.", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
        else:
            m_dmg, m_log = calculate_damage(puzzle, p, is_attacker_player=False)
            p['hp'] -= m_dmg
            result_msg = f"🧱 **GAGAL KABUR:** Jalan diblokir!\n👾 **BALASAN:** {m_name} menebas punggungmu (-{m_dmg} HP)"

    # --- 3. TICK STATUS EFFECTS (BUFF/DEBUFF) ---
    m_hp_change, m_status_logs = apply_turn_status_effects(puzzle, is_player=False)
    p_hp_change, p_status_logs = apply_turn_status_effects(p, is_player=True)
    
    puzzle['monster_hp'] = max(0, puzzle['monster_hp'] + m_hp_change)
    p['hp'] = max(0, p['hp'] + p_hp_change)
    
    update_player(user_id, {"hp": p['hp'], "mp": p['mp'], "inventory": p['inventory'], "active_effects": p.get('active_effects', [])})
    
    status_log_final = " ".join(m_status_logs + p_status_logs)
    full_log = f"{result_msg}\n{status_log_final}"

    # Eksekusi fase Check Death & Rendering UI
    await execute_end_of_turn(callback.message, state, user_id, p, puzzle, full_log, current_combo, battle_msg_id)


# === HELPER: FASE END OF TURN & CHECK DEATH ===
async def execute_end_of_turn(message: Message, state: FSMContext, user_id: int, p: dict, puzzle: dict, full_log: str, current_combo: int, battle_msg_id: int):
    """Menangani logika kematian musuh, kematian pemain, atau ronde berlanjut."""
    m_name = puzzle.get('monster_name', 'Musuh')
    
    # KEMATIAN MUSUH
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
            'exp': new_exp, 'level': new_level, 'current_combo': 0, 'inventory': inv
        })
        
        await state.set_state(GameState.exploring)
        if battle_msg_id:
            try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text=f"🎉 **PERTARUNGAN SELESAI** 🎉\n{m_name} telah hancur lebur.", parse_mode="Markdown")
            except: pass
            
        await message.answer(f"🎉 *KEMENANGAN!*\n{full_log}\n\n✨ EXP: +{total_exp}\n💰 Gold: +{total_gold}\n🎁 Drops: {', '.join(drops) if drops else 'Tidak ada'}{level_up_msg}", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
    
    # KEMATIAN PEMAIN
    elif p['hp'] <= 0:
        msg_text = reset_player_death(user_id, "death_combat")
        await state.set_state(GameState.exploring)
        if battle_msg_id:
            try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text=f"💀 **KAU TELAH GUGUR...**", parse_mode="Markdown")
            except: pass
        await message.answer(f"💀 Dikalahkan oleh {m_name}\n\n{msg_text}", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
        
    # MUSUH MASIH HIDUP, LANJUT RONDE
    else:
        puzzle['question'] = "Pilih aksimu dari menu di bawah!"
        puzzle['timer'] = "--" 
        await state.update_data(puzzle=puzzle, current_combo=current_combo, action_type=None)
        
        next_msg = render_live_battle(p, puzzle, f"✅ {full_log}")
        
        if battle_msg_id:
            try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text=next_msg, parse_mode="Markdown", reply_markup=get_stance_keyboard(puzzle.get('is_boss', False)))
            except TelegramBadRequest: pass


# === EVENT PUZZLE (NON-COMBAT / EKSPLORASI) ===
@dp.message(GameState.in_event)
async def event_puzzle_handler(message: Message, state: FSMContext):
    """
    Handler ini HANYA digunakan ketika pemain menemukan puzzle saat eksplorasi 
    (misal: membuka peti harta karun atau NPC event).
    Saat ini sebagai placeholder untuk fitur event masa depan.
    """
    # ... Logika teka-teki untuk membuka chest / trap akan diimplementasikan di sini
    pass


async def main():
    auto_seed_content()
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
