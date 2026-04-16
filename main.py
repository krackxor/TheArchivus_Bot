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
    render_live_battle, process_loot
)
from game.logic.stats import calculate_total_stats
from game.logic.inventory_manager import equip_item, unequip_item
from game.logic.menu_handler import get_inventory_menu, get_profile_menu

# === OLD ARCHITECTURE IMPORTS (YANG MASIH DIPAKAI) ===
from game.systems.exploration import process_move  
from game.systems.shop import get_shop_keyboard, process_purchase, get_rest_area_keyboard
from game.systems.events import roll_loot_drop, process_event_outcome, check_easter_egg
from game.entities.npcs import resolve_npc_action
from game.systems.achievements import (
    get_all_unlockable_achievements, award_achievement, generate_daily_quests,
    check_daily_quest_progress, calculate_level_from_exp, calculate_exp_needed
)
from game.items import get_item # Untuk akses data item

from utils.helper_ui import (
    create_hp_bar, create_mp_bar, create_energy_bar, create_status_card, create_combat_header,
    create_achievement_notification, create_loot_drop, create_level_up_animation,
    create_combo_indicator, create_daily_quest_card, create_boss_warning,
    create_death_screen, create_location_transition, create_inventory_display
)

dp = Dispatcher()
ADMIN_ID = 123456789  # GANTI DENGAN ID TELEGRAM-MU

# === HELPER DURABILITY (ADAPTED FOR 8-SLOT SYSTEM) ===
def reduce_equipment_durability(user_id, target_slot='weapon'):
    p = get_player(user_id)
    equipped = p.get('equipped', {})
    broken_items = []
    updates = {}
    
    item_id = equipped.get(target_slot)
    if item_id:
        # Pura-puranya item punya state durabilitas di inventory player
        # Dalam implementasi nyata, kamu butuh array object di DB, bukan cuma string ID
        pass # Disiapkan untuk logika durabilitas di database player
        
    return broken_items

# === ENHANCED KEYBOARDS ===
def get_main_reply_keyboard(player=None):
    keyboard = [
        [KeyboardButton(text="⬆️ Utara")],
        [KeyboardButton(text="⬅️ Barat"), KeyboardButton(text="Timur ➡️")],
        [KeyboardButton(text="⬇️ Selatan")],
        [KeyboardButton(text="📊 Profil & Tas")] # Diubah untuk integrasi full tombol
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, input_field_placeholder="⚔️ Pilih aksimu, Weaver...")

def get_stance_keyboard(is_boss=False):
    row1 = [
        InlineKeyboardButton(text="⚔️ Serang", callback_data="stance_attack"),
        InlineKeyboardButton(text="🔮 Skill", callback_data="menu_skill")
    ]
    row2 = [
        InlineKeyboardButton(text="🛡️ Bertahan", callback_data="stance_block"),
        InlineKeyboardButton(text="💨 Menghindar", callback_data="stance_dodge")
    ]
    row3 = [InlineKeyboardButton(text="🎒 Item", callback_data="menu_item")]
    if not is_boss: row3.append(InlineKeyboardButton(text="🏃 Kabur", callback_data="stance_run"))
    return InlineKeyboardMarkup(inline_keyboard=[row1, row2, row3])

# ... (Fungsi keyboard get_combat_skill_keyboard, get_combat_item_keyboard, get_chest_keyboard, get_grave_keyboard, get_idol_keyboard tetap sama seperti kodemu sebelumnya) ...

# === BACKGROUND TIMERS ===
async def combat_timeout_task(message: Message, state: FSMContext, puzzle: dict, user_id: int):
    timer = puzzle['timer']
    if str(timer) == "--": return # Time Warp diaktifkan

    for warning in [30, 15, 5]:
        if timer > warning:
            await asyncio.sleep(timer - warning)
            timer = warning
            
    await asyncio.sleep(timer)
    
    current_state = await state.get_state()
    data = await state.get_data()
    active_puzzle = data.get("puzzle", {})
    battle_msg_id = data.get("battle_msg_id")
    
    if current_state == GameState.in_combat and active_puzzle.get("generated_time") == puzzle["generated_time"]:
        p = get_player(user_id)
        p['stats'] = calculate_total_stats(p)
        
        # Monster Menyerang karena Timeout (Menggunakan Logic Combat Baru)
        raw_dmg, atk_log = calculate_damage(puzzle, p, is_attacker_player=False)
        
        new_hp = p['hp'] - raw_dmg
        update_player(user_id, {"hp": new_hp, "current_combo": 0})
        p['hp'] = new_hp 
        
        if new_hp <= 0:
            await state.set_state(GameState.exploring)
            stats = {'cycle': p.get('cycle', 1), 'kills': p['kills'], 'gold_lost': p['gold']}
            death_msg = create_death_screen("Waktu habis di pertarungan", stats)
            msg_text = reset_player_death(user_id, "death_combat")
            try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text="💀 **KAU TELAH GUGUR...**", parse_mode="Markdown")
            except: pass
            await message.answer(death_msg + "\n\n" + msg_text, reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
        else:
            new_puzzle = generate_battle_puzzle(p, puzzle.get('tier', 1), puzzle.get('is_boss', False), existing_monster=puzzle)
            new_puzzle['generated_time'] = None 
            await state.update_data(puzzle=new_puzzle, action_type=None)
            
            safe_puzzle = new_puzzle.copy()
            safe_puzzle['question'] = "Pilih aksi untuk mengungkap segel teka-teki!"
            safe_puzzle['timer'] = "--"
            
            log_msg = f"⏰ WAKTU HABIS! Kamu terlalu lambat!\n{atk_log} (-{raw_dmg} HP)"
            next_msg = render_live_battle(p, safe_puzzle, log_msg)
            
            try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text=next_msg, parse_mode="Markdown", reply_markup=get_stance_keyboard(puzzle.get('is_boss', False)))
            except TelegramBadRequest: pass

# === COMMAND HANDLERS ===
@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.first_name
    player = get_player(user_id, username)
    player['stats'] = calculate_total_stats(player) # Hitung stat saat login
    
    await state.set_state(GameState.exploring)
    welcome_msg = (
        f"━━━━━━━━━━━━━━━━━━━━\n📜 *THE ARCHIVUS* 📜\n━━━━━━━━━━━━━━━━━━━━\n"
        f"Selamat datang, {username}\n \nKau telah memasuki dimensi\ntanpa ujung ini sebagai\n"
        f"*{player.get('current_job', 'Novice Weaver')}*.\n━━━━━━━━━━━━━━━━━━━━\n"
        f"Cycle: {player.get('cycle', 1)} | Level: {player.get('level', 1)}\n"
        f"{create_hp_bar(player.get('hp',100), player.get('max_hp',100))}\n"
        f"{create_mp_bar(player.get('mp', 0), player.get('max_mp', 50))}\n"
        f"🔮 Ketik /help untuk panduan"
    )
    await message.answer(welcome_msg, reply_markup=get_main_reply_keyboard(player), parse_mode="Markdown")

# INTEGRASI MENU HANDLER (FULL TOMBOL UNTUK INVENTORY/PROFILE)
@dp.message(GameState.exploring, F.text == "📊 Profil & Tas")
async def profile_bag_handler(message: Message):
    p = get_player(message.from_user.id)
    p['stats'] = calculate_total_stats(p)
    stats = p['stats']
    
    text = (
        f"👤 **{p.get('name', 'Weaver')}** [{p.get('current_job', 'Novice Weaver')}]\n"
        f"❤️ HP: {p['hp']}/{p['max_hp']} | 🔵 MP: {p.get('mp',0)}/{p.get('max_mp',50)}\n"
        f"⚔️ ATK: {stats['p_atk']} | 🔮 MATK: {stats['m_atk']}\n"
        f"🛡️ DEF: {stats['p_def']} | 💨 SPD: {stats['speed']}\n"
        f"⚖️ Berat: {stats['total_weight']}\n\n"
        f"👇 Pilih menu di bawah ini:"
    )
    
    # Memanggil menu utama dari menu_handler.py
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎒 Buka Tas (Equip Item)", callback_data="menu_inventory")],
        [InlineKeyboardButton(text="👕 Lihat Baju Terpakai (Unequip)", callback_data="menu_profile")]
    ])
    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")


# === ROUTER TOMBOL INVENTORY (DARI MENU HANDLER) ===
@dp.callback_query(F.data.startswith("menu_") | F.data.startswith("equip_") | F.data.startswith("unequip_"))
async def inventory_button_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    data = callback.data
    p = get_player(user_id)
    p['stats'] = calculate_total_stats(p)

    # Cek state, jangan biarkan ganti baju pas berantem
    # (Opsional: tambahkan cek state di sini)

    if data == "menu_inventory":
        kb = get_inventory_menu(p)
        await callback.message.edit_text("🎒 **Isi Tas (Klik untuk Pasang):**", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb), parse_mode="Markdown")
        
    elif data == "menu_profile":
        kb = get_profile_menu(p)
        await callback.message.edit_text("👕 **Equipment Terpakai (Klik untuk Lepas):**", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb), parse_mode="Markdown")
        
    elif data.startswith("equip_"):
        item_id = data.replace("equip_", "")
        success, msg = equip_item(p, item_id) # Panggil logic cerdas
        update_player(user_id, {'inventory': p['inventory'], 'equipped': p['equipped'], 'current_job': p['current_job']})
        
        kb = get_inventory_menu(p)
        await callback.message.edit_text(f"{msg}\n\n🎒 **Sisa Tas:**", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb), parse_mode="Markdown")
        
    elif data.startswith("unequip_"):
        slot = data.replace("unequip_", "")
        success, msg = unequip_item(p, slot)
        update_player(user_id, {'inventory': p['inventory'], 'equipped': p['equipped'], 'current_job': p['current_job']})
        
        kb = get_profile_menu(p)
        await callback.message.edit_text(f"{msg}\n\n👕 **Equipment Tersisa:**", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb), parse_mode="Markdown")


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
    p['stats'] = calculate_total_stats(p) # Refresh stats
    
    # 1. CEK ENERGI & LOGIKA PUSING/RACUN (Tetap sama seperti kodemu)
    new_energy = p.get('energy', 100) - 1
    update_player(user_id, {"energy": new_energy})
    
    event_type, event_data, narration = process_move(user_id)
    
    # EVENT KOMBAT (MONSTER / BOSS)
    if event_type in ["boss", "monster", "miniboss"]:
        is_boss = (event_type == "boss")
        is_miniboss = (event_type == "miniboss")
        tier_level = 5 if is_boss else min(5, max(1, (p['kills'] // 5) + 1))
        
        # Panggil generator baru dari logic.combat
        puzzle = generate_battle_puzzle(p, tier_level, is_boss=is_boss, is_miniboss=is_miniboss)
        await state.set_state(GameState.in_combat)
        puzzle['generated_time'] = None 
        
        safe_puzzle = puzzle.copy()
        safe_puzzle['question'] = "Pilih aksi untuk mengungkap segel teka-teki!"
        safe_puzzle['timer'] = "--"
        
        combat_ui = render_live_battle(p, safe_puzzle, f"⚠️ {narration}")
        sent_msg = await message.answer(combat_ui, parse_mode="Markdown", reply_markup=get_stance_keyboard(is_boss))
        
        await state.update_data(
            battle_msg_id=sent_msg.message_id,
            puzzle=puzzle, 
            combat_start_hp=p['hp'], 
            current_combo=p.get('current_combo', 0),
            action_type=None
        )
        
    # EVENT LAINNYA (REST AREA, CHEST, DLL) -> Tidak berubah, sesuaikan dengan kodemu sebelumnya
    else:
        await message.answer(f"{narration}\n⚡ Energi: {new_energy}/100", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")


# === PUSAT LOGIKA JAWABAN PUZZLE (ATTACK / SKILL / RUN) ===
@dp.message(GameState.in_combat)
async def combat_answer_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    try: await message.delete()
    except TelegramBadRequest: pass 

    data = await state.get_data()
    puzzle = data.get("puzzle")
    action = data.get("action_type", "attack")
    battle_msg_id = data.get("battle_msg_id")
    
    if not puzzle: return
    
    effective_timer = 9999 if str(puzzle.get('timer')) == "--" else puzzle['timer']
    is_correct, is_timeout, time_taken = validate_answer(message.text, puzzle['answer'], puzzle['generated_time'], effective_timer)
    
    p = get_player(user_id)
    p['stats'] = calculate_total_stats(p)
    is_boss = puzzle.get('is_boss', False)
    
    result_msg = ""
    current_combo = data.get("current_combo", 0)

    if is_correct:
        if action == "attack":
            current_combo += 1
            # === MENGGUNAKAN MESIN DAMAGE BARU ===
            p_dmg, atk_log = calculate_damage(p, puzzle, is_attacker_player=True)
            
            puzzle['monster_hp'] -= p_dmg  
            result_msg = f"⚔️ {atk_log} Musuh -{p_dmg} HP."
            
        elif action == "skill":
            current_combo += 1
            # Skill memberikan modifier damage tambahan di mesin baru
            # Asumsi: skill memberikan buff stats sementara lalu serang
            temp_p = p.copy()
            temp_p['stats']['m_atk'] = int(temp_p['stats']['m_atk'] * 1.8)
            p_dmg, atk_log = calculate_damage(temp_p, puzzle, is_attacker_player=True)
            
            puzzle['monster_hp'] -= p_dmg
            result_msg = f"🔥 *SKILL ACTIVATED!* {atk_log} Musuh -{p_dmg} HP."
            
        elif action == "run":
            # Dodge chance sekarang ditarik dari stats yang sudah memperhitungkan berat equipment
            chance = p['stats']['dodge'] + 0.30 
            if random.random() < chance:
                await state.set_state(GameState.exploring)
                update_player(user_id, {'current_combo': 0})
                if battle_msg_id:
                    try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text="🏃💨 *KABUR!*", parse_mode="Markdown")
                    except: pass
                return await message.answer("🏃💨 *BERHASIL KABUR!*", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
            else:
                result_msg = "🧱 Jalan diblokir! Gagal kabur!"

        update_player(user_id, {'current_combo': current_combo})
        
        # CEK KEMATIAN MUSUH
        if puzzle['monster_hp'] <= 0:
            tier = puzzle.get('tier', 1)
            base_reward = 500 if is_boss else (int(tier) * 25)
            total_gold = base_reward + int(base_reward * (current_combo * 0.1))
            
            # === MENGGUNAKAN MESIN LOOT BARU ===
            drops = process_loot(puzzle.get('drops', []))
            inv = p.get('inventory', [])
            inv.extend(drops)
            
            update_player(user_id, {'kills': p['kills']+1, 'gold': p['gold']+total_gold, 'current_combo': current_combo, 'inventory': inv})
            
            await state.set_state(GameState.exploring)
            if battle_msg_id:
                try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text=f"🎉 **PERTARUNGAN SELESAI** 🎉\nMusuh telah hancur lebur.", parse_mode="Markdown")
                except: pass
                
            await message.answer(f"🎉 *KEMENANGAN!*\n{result_msg}\n\n💰 Bonus Gold: +{total_gold}\n🎁 Drops: {', '.join(drops) if drops else 'Tidak ada'}", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
        
        else:
            # MUSUH MASIH HIDUP, LANJUT RONDE
            new_puzzle = generate_battle_puzzle(p, puzzle.get('tier', 1), is_boss, existing_monster=puzzle)
            new_puzzle['generated_time'] = None 
            await state.update_data(puzzle=new_puzzle, current_combo=current_combo, action_type=None)
            
            safe_puzzle = new_puzzle.copy()
            safe_puzzle['question'] = "Pilih aksi untuk mengungkap segel teka-teki!"
            safe_puzzle['timer'] = "--"
            
            next_msg = render_live_battle(p, safe_puzzle, f"✅ {result_msg}")
            
            if battle_msg_id:
                try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text=next_msg, parse_mode="Markdown", reply_markup=get_stance_keyboard(is_boss))
                except TelegramBadRequest: pass

    # JIKA JAWABAN SALAH / TIMEOUT
    else:
        # === MONSTER MENYERANG BALIK (MESIN BARU) ===
        m_dmg, m_log = calculate_damage(puzzle, p, is_attacker_player=False)
        dmg_msg = f"❌ Salah/Terlambat!\n{m_log} (-{m_dmg} HP)"
            
        new_hp = p['hp'] - m_dmg
        update_player(user_id, {'current_combo': 0, 'hp': new_hp})
        
        if new_hp <= 0:
            msg_text = reset_player_death(user_id, "death_combat")
            await state.set_state(GameState.exploring)
            if battle_msg_id:
                try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text=f"💀 **KAU TELAH GUGUR...**", parse_mode="Markdown")
                except: pass
            await message.answer(f"💀 Dikalahkan oleh {puzzle['monster_name']}\n\n{msg_text}", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
        else:
            new_puzzle = generate_battle_puzzle(p, puzzle.get('tier', 1), is_boss, existing_monster=puzzle)
            new_puzzle['generated_time'] = None
            await state.update_data(puzzle=new_puzzle, action_type=None)
            
            safe_puzzle = new_puzzle.copy()
            safe_puzzle['question'] = "Pilih aksi untuk mengungkap segel teka-teki!"
            safe_puzzle['timer'] = "--"
            
            next_msg = render_live_battle(p, safe_puzzle, f"⚠️ *PERINGATAN!*\n{dmg_msg}")
            
            if battle_msg_id:
                try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text=next_msg, parse_mode="Markdown", reply_markup=get_stance_keyboard(is_boss))
                except TelegramBadRequest: pass

async def main():
    auto_seed_content()
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
