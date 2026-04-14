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

# === NEW ARCHITECTURE IMPORTS ===
from game.systems.exploration import process_move  
from game.systems.shop import get_shop_keyboard, process_purchase
from game.systems.combat import generate_battle_puzzle, validate_answer, calculate_equipment_stats, calculate_dodge_chance, get_element_multiplier, process_staff_magic
from game.systems.events import roll_loot_drop, trigger_random_event, process_event_outcome, check_easter_egg
from game.systems.achievements import (
    get_all_unlockable_achievements, award_achievement, generate_daily_quests,
    check_daily_quest_progress, calculate_level_from_exp, calculate_exp_needed
)

# Memanggil dari folder utils/
from utils.helper_ui import (
    create_hp_bar, create_mp_bar, create_status_card, create_combat_header,
    create_achievement_notification, create_loot_drop, create_level_up_animation,
    create_combo_indicator, create_daily_quest_card, create_boss_warning,
    create_death_screen, create_location_transition, create_monster_card
)

dp = Dispatcher()
ADMIN_ID = 123456789  # GANTI DENGAN ID TELEGRAM-MU UNTUK AKSES CHEAT!

# === HELPER DURABILITY ===
def reduce_equipment_durability(user_id, damage_type):
    """Mengurangi durability barang. damage_type: 'weapon' atau 'armor'"""
    p = get_player(user_id)
    inventory = p.get('inventory', [])
    broken_items = []
    
    for item in inventory:
        if item.get('type') in ['weapon', 'shield', 'chest', 'head', 'gloves', 'boots']:
            if item.get('durability', 0) > 0:
                if damage_type == 'weapon' and item['type'] == 'weapon':
                    item['durability'] -= 1
                    if item['durability'] == 0:
                        broken_items.append(item['name'])
                elif damage_type == 'armor' and item['type'] in ['shield', 'chest', 'head', 'gloves', 'boots']:
                    item['durability'] -= 1
                    if item['durability'] == 0:
                        broken_items.append(item['name'])
                        
    update_player(user_id, {'inventory': inventory})
    return broken_items

# === ENHANCED KEYBOARDS ===
def get_main_reply_keyboard(player=None):
    keyboard = [
        [KeyboardButton(text="⬆️ Utara")],
        [KeyboardButton(text="⬅️ Barat"), KeyboardButton(text="Timur ➡️")],
        [KeyboardButton(text="⬇️ Selatan")],
        [KeyboardButton(text="📊 Status"), KeyboardButton(text="🎒 Inventory")],
        [KeyboardButton(text="🛒 Toko"), KeyboardButton(text="🏆 Quest")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, input_field_placeholder="⚔️ Pilih aksimu, Weaver...")

def get_stance_keyboard(is_boss=False):
    """Menu Utama Pertarungan (Main Menu)"""
    # Catatan: Jika library-mu mendukung parameter style, kamu bisa tambahkan style="success", dll.
    row1 = [
        InlineKeyboardButton(text="⚔️ Serang", callback_data="stance_attack"),
        InlineKeyboardButton(text="🔮 Skill", callback_data="menu_skill")
    ]
    row2 = [
        InlineKeyboardButton(text="🛡️ Bertahan", callback_data="stance_block"),
        InlineKeyboardButton(text="💨 Menghindar", callback_data="stance_dodge")
    ]
    row3 = [InlineKeyboardButton(text="🎒 Item", callback_data="menu_item")]
    if not is_boss:
        row3.append(InlineKeyboardButton(text="🏃 Kabur", callback_data="stance_run"))

    return InlineKeyboardMarkup(inline_keyboard=[row1, row2, row3])

def get_combat_skill_keyboard(player, player_stats):
    """Sub-Menu Daftar Skill"""
    buttons = []
    player_mp = player.get('mp', 0)
    inventory = player.get('inventory', [])
    
    # 1. Skill Senjata
    weapon = next((i for i in inventory if i.get('type') == 'weapon' and i.get('durability', 0) > 0), None)
    if weapon and weapon.get('skill'):
        sk = weapon['skill']
        buttons.append([InlineKeyboardButton(text=f"⚔️ {sk['name']} ({sk['cost']} MP)", callback_data=f"combat_do_skill_{sk['id']}")])

    # 2. Skill Tameng
    if player_stats.get("has_shield", False):
        shield = next((i for i in inventory if i.get('type') == 'shield' and i.get('durability', 0) > 0), None)
        if shield and shield.get('skill'):
            sk = shield['skill']
            buttons.append([InlineKeyboardButton(text=f"🛡️ {sk['name']} ({sk['cost']} MP)", callback_data=f"combat_do_skill_{sk['id']}")])

    # 3. Skill Bawaan/Utilitas
    buttons.append([InlineKeyboardButton(text="👁️ Revelatio (10 MP)", callback_data="combat_do_skill_reveal")])
    if player_mp >= 20: 
        buttons.append([InlineKeyboardButton(text="⏳ Time Warp (20 MP)", callback_data="combat_do_skill_timewarp")])
        
    buttons.append([InlineKeyboardButton(text="🔙 Kembali", callback_data="menu_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_combat_item_keyboard(player):
    """Sub-Menu Daftar Item Darurat"""
    inventory = player.get('inventory', [])
    # Filter hanya item yang bisa dipakai di combat
    usable_items = [i for i in inventory if i.get('effect', '').startswith(('heal_', 'mp_', 'resin_', 'repair_'))]
    
    buttons = []
    # Kelompokkan item agar tidak duplicate (misal Potion x3)
    item_counts = {}
    for item in usable_items:
        if item['id'] not in item_counts:
            item_counts[item['id']] = {'name': item['name'], 'count': 0}
        item_counts[item['id']]['count'] += 1

    for item_id, data in item_counts.items():
        buttons.append([InlineKeyboardButton(text=f"🎒 {data['name']} (x{data['count']})", callback_data=f"combat_do_item_{item_id}")])
    
    if not buttons:
        buttons.append([InlineKeyboardButton(text="❌ Tas Kosong", callback_data="menu_back")])
        
    buttons.append([InlineKeyboardButton(text="🔙 Kembali", callback_data="menu_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_event_keyboard(event):
    buttons = []
    if event['type'] == 'choice':
        for i, choice in enumerate(event['choices']):
            cost_text = f" (-{choice.get('cost', 0)} Gold)" if choice.get('cost', 0) > 0 else ""
            buttons.append([InlineKeyboardButton(text=choice['text'] + cost_text, callback_data=f"event_choice_{i}")])
    elif event['type'] == 'treasure':
        buttons.extend([[InlineKeyboardButton(text="🔓 Buka Peti", callback_data="event_open")], [InlineKeyboardButton(text="🚪 Tinggalkan", callback_data="event_ignore")]])
    elif event['type'] == 'shrine':
        buttons.extend([[InlineKeyboardButton(text="🙏 Berdoa", callback_data="event_pray")], [InlineKeyboardButton(text="🚶 Pergi", callback_data="event_ignore")]])
    elif event['type'] == 'gamble':
        buttons.extend([[InlineKeyboardButton(text=f"🎲 Bertaruh {event['bet_amount']} Gold", callback_data="event_gamble")], [InlineKeyboardButton(text="❌ Tolak", callback_data="event_ignore")]])
    elif event['type'] == 'shop':
        for i, item in enumerate(event['items']):
            cost = item['cost']
            cost_text = f"{cost} Gold" if cost > 0 else f"(Dapat {abs(cost)} Gold)"
            buttons.append([InlineKeyboardButton(text=f"{item['name']} - {cost_text}", callback_data=f"event_buy_{i}")])
        buttons.append([InlineKeyboardButton(text="🚪 Pergi", callback_data="event_ignore")])
    else:
        buttons.extend([[InlineKeyboardButton(text="✅ Terima", callback_data="event_accept")], [InlineKeyboardButton(text="❌ Tolak", callback_data="event_ignore")]])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# === BACKGROUND TIMERS ===
async def combat_timeout_task(message: Message, state: FSMContext, puzzle: dict, user_id: int):
    timer = puzzle['timer']
    for warning in [30, 15, 5]:
        if timer > warning:
            await asyncio.sleep(timer - warning)
            timer = warning
            
    await asyncio.sleep(timer)
    
    current_state = await state.get_state()
    data = await state.get_data()
    active_puzzle = data.get("puzzle", {})
    
    if current_state == GameState.in_combat and active_puzzle.get("generated_time") == puzzle["generated_time"]:
        p = get_player(user_id)
        action = data.get("action_type", "attack")
        
        raw_dmg = puzzle.get('damage', 10)
        final_dmg = raw_dmg
        dmg_msg = f"\n❌ Kamu terlalu lambat! (-{final_dmg} HP)"
        
        if action == "run": dmg_msg = f"\n❌ Gagal kabur karena telat! (-{final_dmg} HP)"
        elif action == "item": dmg_msg = f"\n❌ Ramuanmu jatuh karena telat! (-{final_dmg} HP)"
        elif action == "block":
            final_dmg = int(raw_dmg * 0.2)
            dmg_msg = f"\n🛡️ Kamu menahan dengan Tameng, namun telat! (Menerima {final_dmg} DMG)"
            
        new_hp = p['hp'] - final_dmg
        
        if new_hp <= 0:
            await state.set_state(GameState.exploring)
            stats = {'cycle': p.get('cycle', 1), 'kills': p['kills'], 'gold_lost': p['gold']}
            death_msg = create_death_screen("Waktu habis di pertarungan", stats)
            msg_text = reset_player_death(user_id, "death_combat")
            await message.answer(death_msg + "\n\n" + msg_text, reply_markup=get_main_reply_keyboard(), parse_mode="Markdown")
        else:
            # FIX BUG: TETAP DI COMBAT, GENERATE PUZZLE BARU
            update_player(user_id, {"hp": new_hp, "current_combo": 0})
            p_stats = calculate_equipment_stats(p)
            broken = reduce_equipment_durability(user_id, 'armor')
            broken_txt = f"\n🛡️ *CRACK!* Armormu hancur: {', '.join(broken)}!" if broken else ""
            
            new_puzzle = generate_battle_puzzle(p, puzzle.get('tier', 1), puzzle.get('is_boss', False))
            new_puzzle['generated_time'] = None # Hentikan timer sampai player pilih stance
            await state.update_data(puzzle=new_puzzle, action_type=None)
            
            monster_ui = create_monster_card(new_puzzle['monster_name'], new_puzzle['monster_element'], new_puzzle['monster_hp'], new_puzzle['monster_max_hp'])
            next_msg = f"⏰ *WAKTU HABIS!*\n*{puzzle['monster_name']}* menyerangmu!{dmg_msg}{broken_txt}\n\n*Musuh masih mengejarmu!*\n{monster_ui}\n\n_Pilih aksimu..._"
            
            await message.answer(next_msg, parse_mode="Markdown", reply_markup=get_stance_keyboard(puzzle.get('is_boss', False)))


# === CHEAT COMMANDS (DEV ONLY) ===
@dp.message(F.text == "/resetdb")
async def nuke_database_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id != ADMIN_ID: return await message.answer("❌ Akses ditolak!")
    DB_NAME = os.getenv("DB_NAME", "the_archivus_db")
    client.drop_database(DB_NAME)
    await state.clear()
    auto_seed_content()
    await message.answer(f"🔥 **BOOM! DATABASE '{DB_NAME}' RATA DENGAN TANAH!** 🔥\nKetik /start untuk melahirkan kembali dunia ini.", parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())

@dp.message(F.text == "/sultan")
async def sultan_handler(message: Message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID: return
    p = get_player(user_id)
    update_player(user_id, {"gold": p.get('gold', 0) + 50000})
    await message.answer("💸 **CHEAT ACTIVATED!**\nKamu mendapatkan +50.000 Gold.", parse_mode="Markdown")

@dp.message(F.text == "/godmode")
async def godmode_handler(message: Message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID: return
    p = get_player(user_id)
    inventory = p.get('inventory', [])
    for equip in inventory:
        if equip.get('type') in ['weapon', 'shield', 'chest', 'head', 'gloves', 'boots']: equip['durability'] = 500
    updates = {"hp": 9999, "max_hp": 9999, "mp": 9999, "max_mp": 9999, "inventory": inventory}
    update_player(user_id, updates)
    await message.answer("🛡️ **GOD MODE ON!**\nHP/MP jadi 9999. Equip kebal hancur!", parse_mode="Markdown")

@dp.message(F.text == "/forceboss")
async def forceboss_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id != ADMIN_ID: return
    p = get_player(user_id)
    p_stats = calculate_equipment_stats(p)
    puzzle = generate_battle_puzzle(p, 5, is_boss=True)
    puzzle['generated_time'] = None # Hentikan timer sampai player pilih stance
    
    await state.set_state(GameState.in_combat)
    await state.update_data(puzzle=puzzle, current_stage=1, target_stages=5, combat_start_hp=p['hp'], current_combo=0, action_type=None)
    
    monster_ui = create_monster_card(puzzle['monster_name'], puzzle['monster_element'], puzzle['monster_hp'], puzzle['monster_max_hp'])
    combat_msg = f"⚠️ *DEVELOPER OVERRIDE: MEMANGGIL BOSS!* ⚠️\n\n{monster_ui}\n\n_Pilih aksimu..._"
    
    await message.answer(combat_msg, parse_mode="Markdown", reply_markup=get_stance_keyboard(is_boss=True))


# === COMMAND HANDLERS ===
@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.first_name
    player = get_player(user_id, username)
    await state.set_state(GameState.exploring)
    welcome_msg = f"━━━━━━━━━━━━━━━━━━━━\n📜 *THE ARCHIVUS* 📜\n━━━━━━━━━━━━━━━━━━━━\nSelamat datang, {username}\n \nKau telah memasuki dimensi\ntanpa ujung ini sebagai\n*Weaver* - penenun takdir.\n━━━━━━━━━━━━━━━━━━━━\nCycle: {player.get('cycle', 1)} | Level: {player.get('level', 1)}\n{create_hp_bar(player['hp'], player['max_hp'])}\n{create_mp_bar(player['mp'], player['max_mp'])}\n🔮 Ketik /help untuk panduan"
    await message.answer(welcome_msg, reply_markup=get_main_reply_keyboard(player), parse_mode="Markdown")

@dp.message(F.text == "/help")
async def help_handler(message: Message):
    help_text = "📖 *PANDUAN THE ARCHIVUS*\n\n🎮 *Cara Bermain:*\n• Gunakan tombol arah untuk menjelajah\n• Pilih aksi di pertempuran (Serang, Bertahan, dll)\n• Jawab teka-teki kilat sesudahnya untuk mengeksekusi aksimu!\n• Gunakan Shield/Dodge dengan bijak."
    await message.answer(help_text, parse_mode="Markdown")

# === STATUS & MENU HANDLERS ===
@dp.message(GameState.exploring, F.text == "📊 Status")
async def status_handler(message: Message):
    p = get_player(message.from_user.id)
    status_card = create_status_card(p)
    status_card += f"\n🏆 Achievements: {len(p.get('achievements_unlocked', []))}/12"
    await message.answer(status_card, reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")

@dp.message(GameState.exploring, F.text == "🎒 Inventory")
async def inventory_handler(message: Message):
    p = get_player(message.from_user.id)
    from utils.helper_ui import create_inventory_display
    inv_display = create_inventory_display(p.get('inventory', []))
    
    keyboard = []
    usable_items = [i for i in p.get('inventory', []) if i.get('type') in ['potion', 'consumable']]
    for i, item in enumerate(usable_items[:5]): 
        keyboard.append([InlineKeyboardButton(text=f"Use: {item['name']}", callback_data=f"use_item_{item['id']}")])
    keyboard.append([InlineKeyboardButton(text="🔙 Close", callback_data="close_inventory")])
    
    await message.answer(inv_display, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard), parse_mode="Markdown")

# === MOVEMENT & EXPLORATION ===
@dp.message(F.text.in_(["⬆️ Utara", "⬅️ Barat", "Timur ➡️", "⬇️ Selatan"]))
async def move_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    current_state = await state.get_state()
    
    if current_state in [GameState.in_combat, GameState.in_event]:
        return await message.answer("Selesaikan dulu urusanmu di depan sebelum bergerak!")
        
    await state.set_state(GameState.exploring)
    
    tick_buffs(user_id) 
    
    player = get_player(user_id)
    event_type, event_data, narration = process_move(user_id)
    
    if event_type in ["boss", "monster", "miniboss"]:
        p = get_player(user_id)
        p_stats = calculate_equipment_stats(p)
        
        is_boss = (event_type == "boss")
        is_miniboss = (event_type == "miniboss")
        tier_level = 5 if is_boss else min(5, max(1, (p['kills'] // 5) + 1))
        
        puzzle = generate_battle_puzzle(p, tier_level, is_boss=is_boss, is_miniboss=is_miniboss)
        
        await state.set_state(GameState.in_combat)
        
        puzzle['generated_time'] = None 
        
        await state.update_data(
            puzzle=puzzle, 
            current_stage=1, 
            target_stages=5 if is_boss else (3 if is_miniboss else 1),
            combat_start_hp=p['hp'], 
            current_combo=player.get('current_combo', 0),
            action_type=None
        )
        
        monster_ui = create_monster_card(puzzle['monster_name'], puzzle['monster_element'], puzzle['monster_hp'], puzzle['monster_max_hp'])
        
        combo_text = create_combo_indicator(player.get('current_combo', 0))
        combat_msg = f"{narration}\n\n{combo_text}\n{monster_ui}\n\n_Pilih aksimu..._"
        
        await message.answer(combat_msg, parse_mode="Markdown", reply_markup=get_stance_keyboard(is_boss))
    else:
        await message.answer(narration, reply_markup=get_main_reply_keyboard(player), parse_mode="Markdown")

# === RANDOM EVENT HANDLERS ===
@dp.callback_query(GameState.in_event, F.data.startswith("event_"))
async def random_event_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    action = callback.data.replace("event_", "") 
    
    await state.set_state(GameState.exploring)
    await callback.message.delete()
    p = get_player(user_id)
    
    if action == "ignore":
        await callback.message.answer("🚶 Kamu mengabaikan hal itu dan melangkah pergi.", reply_markup=get_main_reply_keyboard(p))
    else:
        await callback.message.answer("✨ Kamu bereaksi terhadap kejadian tersebut dan melanjutkan perjalanan.", reply_markup=get_main_reply_keyboard(p))
        
    await callback.answer()

# === HANDLER NAVIGASI MENU COMBAT ===
@dp.callback_query(GameState.in_combat, F.data.startswith("menu_"))
async def combat_menu_nav_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    action = callback.data.replace("menu_", "")
    p = get_player(user_id)
    p_stats = calculate_equipment_stats(p)
    
    data = await state.get_data()
    puzzle = data.get("puzzle", {})
    is_boss = puzzle.get('is_boss', False)

    if action == "skill":
        await callback.message.edit_reply_markup(reply_markup=get_combat_skill_keyboard(p, p_stats))
    elif action == "item":
        await callback.message.edit_reply_markup(reply_markup=get_combat_item_keyboard(p))
    elif action == "back":
        await callback.message.edit_reply_markup(reply_markup=get_stance_keyboard(is_boss))
        
    await callback.answer()


# === HANDLER AKSI UTAMA (MEMUNCULKAN PUZZLE & TIMER) ===
@dp.callback_query(GameState.in_combat, F.data.startswith("stance_") | F.data.startswith("combat_do_"))
async def combat_action_trigger(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    puzzle = data.get("puzzle")
    p = get_player(user_id)
    
    if not puzzle: return await callback.answer("Error: Data pertempuran tidak ditemukan.", show_alert=True)
    
    raw_data = callback.data
    action = ""
    active_skill_id = None
    pending_item_id = None
    act_text = ""

    if raw_data.startswith("stance_"):
        action = raw_data.replace("stance_", "")
        if action == "attack": act_text = "⚔️ *Menerjang maju!*"
        elif action == "block": act_text = "🛡️ *Menahan posisi!*"
        elif action == "dodge": act_text = "💨 *Membaca arah serangan!*"
        elif action == "run": act_text = "🏃 *Mencari celah kabur!*"
        
    elif raw_data.startswith("combat_do_skill_"):
        action = "skill"
        active_skill_id = raw_data.replace("combat_do_skill_", "")
        act_text = "🔮 *Mempersiapkan sihir/skill khusus!*"
        
    elif raw_data.startswith("combat_do_item_"):
        action = "item"
        pending_item_id = raw_data.replace("combat_do_item_", "")
        act_text = "🎒 *Membongkar tas mencari item...*"

    if action == "block" or action == "dodge":
        if p['mp'] < 15: return await callback.answer("🔮 MP tidak cukup! (Butuh 15)", show_alert=True)
        update_player(user_id, {"mp": p['mp'] - 15})
        
    elif action == "skill":
        skill_cost = 0
        if active_skill_id == "reveal": skill_cost = 10
        elif active_skill_id == "timewarp": skill_cost = 20
        else:
            for item in p.get('inventory', []):
                if item.get('skill', {}).get('id') == active_skill_id:
                    skill_cost = item['skill']['cost']
                    break
                    
        if p['mp'] < skill_cost: return await callback.answer(f"🔮 MP tidak cukup! (Butuh {skill_cost})", show_alert=True)
        update_player(user_id, {"mp": p['mp'] - skill_cost})

    await state.update_data(action_type=action, active_skill_id=active_skill_id, pending_item=pending_item_id)

    puzzle['generated_time'] = time.time()
    await state.update_data(puzzle=puzzle)

    monster_ui = create_monster_card(puzzle['monster_name'], puzzle['monster_element'], puzzle['monster_hp'], puzzle['monster_max_hp'])
    time_emoji = "🟢" if puzzle['timer'] > 40 else "🟡" if puzzle['timer'] > 25 else "🔴"
    
    puzzle_ui = f"{monster_ui}\n\n{act_text}\n\n🧩 *PUZZLE:*\n`{puzzle['question']}`\n\n{time_emoji} *Waktu Eksekusi: {puzzle['timer']} Detik!*"
    
    await callback.message.edit_text(puzzle_ui, parse_mode="Markdown", reply_markup=None)
    asyncio.create_task(combat_timeout_task(callback.message, state, puzzle, user_id))


# === COMBAT LOGIC ===
@dp.message(GameState.in_combat)
async def combat_answer_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    puzzle = data.get("puzzle")
    action = data.get("action_type", "attack")
    if not puzzle: return
    
    is_correct, is_timeout, time_taken = validate_answer(message.text, puzzle['answer'], puzzle['generated_time'], puzzle['timer'])
    p = get_player(user_id)
    p_stats = calculate_equipment_stats(p)
    is_boss = puzzle.get('is_boss', False)
    
    result_msg = ""
    dmg_msg = ""
    broken_txt = ""
    current_combo = data.get("current_combo", 0)
    
    if is_correct:
        is_critical = time_taken < 10.0
        crit_msg = "\n💥 *CRITICAL HIT!*" if is_critical else ""
        
        if action == "attack":
            current_combo += 1
            broken = reduce_equipment_durability(user_id, 'weapon')
            broken_txt = f"\n⚠️ *PERINGATAN!* Senjatamu hancur: {', '.join(broken)}!" if broken else ""
            result_msg = f"⚔️ Serangan telak!{crit_msg}{broken_txt}"
            
        elif action == "item":
            item_id = data.get("pending_item")
            inventory = p.get('inventory', [])
            item_idx = next((i for i, item in enumerate(inventory) if item.get('id') == item_id), -1)
            
            if item_idx != -1:
                used_item = inventory.pop(item_idx)
                effect = used_item.get('effect', '')
                updates = {'inventory': inventory}
                
                if effect.startswith("heal_"):
                    amount = int(effect.split("_")[1])
                    updates['hp'] = min(p['max_hp'], p['hp'] + amount)
                    result_msg = f"🧪 Kamu menenggak Potion dengan aman! (+{amount} HP)"
                elif effect.startswith("mp_"):
                    amount = int(effect.split("_")[1])
                    updates['mp'] = min(p['max_mp'], p['mp'] + amount)
                    result_msg = f"🔮 MP Pulih dengan aman! (+{amount} MP)"
                elif effect.startswith("resin_"):
                    elemen = effect.split("_")[1]
                    updates['active_resin'] = elemen
                    updates['resin_duration'] = 3
                    result_msg = f"📜 Senjatamu memancarkan sihir {elemen} selama 3 turn."
                elif effect == "repair_all":
                    for equip in updates['inventory']:
                        if equip.get('type') in ['weapon', 'shield', 'chest', 'head', 'gloves', 'boots']:
                            equip['durability'] = equip.get('max_durability', 50)
                    result_msg = "⚒️ Semua equip-mu kembali mulus 100%!"
                    
                update_player(user_id, updates)
                p = get_player(user_id)
            else:
                result_msg = "❌ Gagal menggunakan item (Tidak ditemukan)."

        elif action == "dodge":
            current_combo += 1
            result_msg = f"💨 *PERFECT DODGE!* Kamu menghindar dan membalas serangan! (+1 Combo)"
            
        elif action == "block":
            result_msg = f"🛡️ Kamu menangkis, lalu mendorong musuh mundur!"
            
        elif action == "run":
            chance = calculate_dodge_chance(p_stats) + 0.30 
            if random.random() < chance:
                await state.set_state(GameState.exploring)
                update_player(user_id, {'current_combo': 0})
                return await message.answer("🏃💨 *BERHASIL KABUR!*\nKamu lolos dari maut dan kembali menjelajah.", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
            else:
                result_msg = "🧱 Jalanmu diblokir oleh musuh! Gagal kabur!"
                action = "failed_run"
                
        elif action == "skill":
            skill_id = data.get("active_skill_id")
            result_msg = f"🔥 *SKILL ACTIVATED!* Serangan sukses!"
            broken = reduce_equipment_durability(user_id, 'weapon')
            if broken: result_msg += f"\n⚠️ Senjatamu hancur: {', '.join(broken)}!"

        update_player(user_id, {'current_combo': current_combo, 'max_combo_reached': max(p.get('max_combo_reached', 0), current_combo)})
        
        if action in ["attack", "skill", "dodge"]:
            current_stage = data.get("current_stage", 1)
            target_stages = data.get("target_stages", 1)
            
            if current_stage < target_stages:
                tier_level = min(5, max(1, (p['kills'] // 5) + 1))
                new_puzzle = generate_battle_puzzle(p, tier_level, is_boss, existing_monster=None)
                new_puzzle['generated_time'] = None 
                await state.update_data(puzzle=new_puzzle, current_stage=current_stage + 1, current_combo=current_combo, action_type=None)
                
                combo_ind = create_combo_indicator(current_combo)
                monster_ui = create_monster_card(new_puzzle['monster_name'], new_puzzle['monster_element'], new_puzzle['monster_hp'], new_puzzle['monster_max_hp'])
                next_msg = f"✅ *BENAR!*\n{result_msg}\n{combo_ind}\n\n{monster_ui}\n\n_Pilih aksimu..._"
                
                await message.answer(next_msg, parse_mode="Markdown", reply_markup=get_stance_keyboard(is_boss))
            else:
                tier = puzzle.get('tier', 1)
                base_reward = 500 if is_boss else (tier * 25)
                total_gold = base_reward + int(base_reward * (current_combo * 0.1))
                new_cycle = p['cycle'] + 1 if is_boss else p['cycle']
                update_player(user_id, {'kills': p['kills']+1, 'gold': p['gold']+total_gold, 'current_combo': current_combo, 'cycle': new_cycle})
                
                await state.set_state(GameState.exploring)
                await message.answer(f"🎉 *KEMENANGAN!*\n{result_msg}\n\n💰 Gold: +{total_gold}", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
        else:
            new_puzzle = generate_battle_puzzle(p, puzzle.get('tier', 1), is_boss, existing_monster=puzzle)
            new_puzzle['generated_time'] = None
            await state.update_data(puzzle=new_puzzle, action_type=None)
            
            monster_ui = create_monster_card(new_puzzle['monster_name'], new_puzzle['monster_element'], new_puzzle['monster_hp'], new_puzzle['monster_max_hp'])
            next_msg = f"✅ *AMAN!*\n{result_msg}\n\nNamun *{puzzle['monster_name']}* masih menyerang!\n{monster_ui}\n\n_Pilih aksimu..._"
            await message.answer(next_msg, parse_mode="Markdown", reply_markup=get_stance_keyboard(is_boss))

    else:
        raw_damage = puzzle.get('damage', 10)
        final_damage = raw_damage
        
        if action == "block":
            final_damage = int(raw_damage * 0.2)
            dmg_msg = f"🛡️ Kamu menahan serangan dengan Tameng! (Menerima {final_damage} DMG)"
        elif action == "dodge":
            chance = calculate_dodge_chance(p_stats)
            if random.random() < chance:
                final_damage = 0
                dmg_msg = "💨 Kamu panik tapi berhasil menghindar! (Menerima 0 DMG)"
            else:
                dmg_msg = f"❌ Dodge Gagal! (Menerima {final_damage} DMG)"
        elif action == "item":
            item_id = data.get("pending_item")
            inventory = p.get('inventory', [])
            inventory = [i for i in inventory if i.get('id') != item_id]
            update_player(user_id, {'inventory': inventory})
            dmg_msg = f"❌ Gagal! Itemmu jatuh! (Menerima {final_damage} DMG)"
        elif action == "run":
            dmg_msg = f"❌ Gagal kabur! Diserang dari belakang! (Menerima {final_damage} DMG)"
        else:
            dmg_msg = f"❌ Kamu terlambat menangkis! (Menerima {final_damage} DMG)"
            
        new_hp = p['hp'] - final_damage
        update_player(user_id, {'current_combo': 0, 'hp': new_hp})
        
        if final_damage > 0:
            broken = reduce_equipment_durability(user_id, 'armor')
            if broken: dmg_msg += f"\n🛡️ *CRACK!* Armormu hancur: {', '.join(broken)}!"
        
        if new_hp <= 0:
            msg_text = reset_player_death(user_id, "death_combat")
            await state.set_state(GameState.exploring)
            await message.answer(f"💀 Dikalahkan oleh {puzzle['monster_name']}\n\n{msg_text}", reply_markup=get_main_reply_keyboard(), parse_mode="Markdown")
        else:
            new_puzzle = generate_battle_puzzle(p, puzzle.get('tier', 1), is_boss, existing_monster=puzzle)
            new_puzzle['generated_time'] = None
            await state.update_data(puzzle=new_puzzle, action_type=None)
            
            monster_ui = create_monster_card(new_puzzle['monster_name'], new_puzzle['monster_element'], new_puzzle['monster_hp'], new_puzzle['monster_max_hp'])
            next_msg = f"❌ *SALAH!*\n{dmg_msg}\n\n*Musuh tidak melepaskanmu!*\n{monster_ui}\n\n_Pilih aksimu..._"
            await message.answer(next_msg, parse_mode="Markdown", reply_markup=get_stance_keyboard(is_boss))


# === INVENTORY OUT OF COMBAT ===
@dp.callback_query(F.data.startswith("use_item_"))
async def use_item_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    item_id = callback.data.replace("use_item_", "")
    p = get_player(user_id)
    inventory = p.get('inventory', [])
    item_index = next((i for i, item in enumerate(inventory) if item.get('id') == item_id), -1)
    
    if item_index == -1: return await callback.answer("❌ Item habis!", show_alert=True)
    used_item = inventory.pop(item_index)
    effect = used_item.get('effect', '')
    updates = {'inventory': inventory}
    alert_msg = f"Memakai {used_item['name']}!\n"
    
    if effect.startswith("heal_"):
        amount = int(effect.split("_")[1])
        updates['hp'] = min(p['max_hp'], p['hp'] + amount)
        alert_msg += f"❤️ +{amount} HP"
    elif effect.startswith("mp_"):
        amount = int(effect.split("_")[1])
        updates['mp'] = min(p['max_mp'], p['mp'] + amount)
        alert_msg += f"🔮 +{amount} MP"
    elif effect.startswith("resin_"):
        elemen = effect.split("_")[1]
        updates['active_resin'] = elemen
        updates['resin_duration'] = 3
        alert_msg += f"📜 Senjatamu dialiri sihir {elemen} selama 3 pertarungan!"
    elif effect == "repair_all":
        for equip in updates['inventory']:
            if equip.get('type') in ['weapon', 'shield', 'chest', 'head', 'gloves', 'boots']:
                equip['durability'] = equip.get('max_durability', 50)
        alert_msg += "⚒️ Semua senjatamu tajam dan armormu utuh!"
    
    update_player(user_id, updates)
    await callback.message.delete()
    await callback.answer(alert_msg, show_alert=True)
    await callback.message.answer(f"✨ Kamu menggunakan *{used_item['name']}*.\n{alert_msg}", parse_mode="Markdown")

@dp.callback_query(F.data.in_(["close_inventory", "close_quests", "close_shop"]))
async def close_menu_handler(callback: CallbackQuery):
    await callback.message.delete()

@dp.callback_query(F.data.startswith("buy_"))
async def shop_purchase_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    success, message = process_purchase(user_id, callback.data)
    await callback.answer(message, show_alert=True)
        
# === BOILERPLATE ===
async def main():
    auto_seed_content()
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
