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
from game.systems.shop import get_shop_keyboard, process_purchase, get_rest_area_keyboard
from game.systems.combat import (
    generate_battle_puzzle, validate_answer, calculate_equipment_stats, 
    calculate_dodge_chance, calculate_block_reduction, get_element_multiplier, 
    process_staff_magic, render_live_battle
)
from game.systems.events import roll_loot_drop, process_event_outcome, check_easter_egg
from game.entities.npcs import resolve_npc_action
from game.systems.achievements import (
    get_all_unlockable_achievements, award_achievement, generate_daily_quests,
    check_daily_quest_progress, calculate_level_from_exp, calculate_exp_needed
)

from utils.helper_ui import (
    create_hp_bar, create_mp_bar, create_energy_bar, create_status_card, create_combat_header,
    create_achievement_notification, create_loot_drop, create_level_up_animation,
    create_combo_indicator, create_daily_quest_card, create_boss_warning,
    create_death_screen, create_location_transition, create_inventory_display
)

dp = Dispatcher()
ADMIN_ID = 123456789  # GANTI DENGAN ID TELEGRAM-MU

# === HELPER DURABILITY ===
def reduce_equipment_durability(user_id, damage_type):
    p = get_player(user_id)
    inventory = p.get('inventory', [])
    broken_items = []
    
    for item in inventory:
        if item.get('type') in ['weapon', 'shield', 'chest', 'head', 'gloves', 'boots']:
            if item.get('durability', 0) > 0:
                if damage_type == 'weapon' and item['type'] == 'weapon':
                    item['durability'] -= 1
                    if item['durability'] == 0: broken_items.append(item['name'])
                elif damage_type == 'armor' and item['type'] in ['shield', 'chest', 'head', 'gloves', 'boots']:
                    item['durability'] -= 1
                    if item['durability'] == 0: broken_items.append(item['name'])
                        
    update_player(user_id, {'inventory': inventory})
    return broken_items

# === ENHANCED KEYBOARDS ===
def get_main_reply_keyboard(player=None):
    keyboard = [
        [KeyboardButton(text="⬆️ Utara")],
        [KeyboardButton(text="⬅️ Barat"), KeyboardButton(text="Timur ➡️")],
        [KeyboardButton(text="⬇️ Selatan")],
        [KeyboardButton(text="📊 Status"), KeyboardButton(text="🎒 Inventory")],
        [KeyboardButton(text="🏆 Quest")]
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

def get_combat_skill_keyboard(player, player_stats):
    buttons = []
    player_mp = player.get('mp', 0)
    inventory = player.get('inventory', [])
    
    weapon = next((i for i in inventory if i.get('type') == 'weapon' and i.get('durability', 0) > 0), None)
    if weapon and weapon.get('skill'):
        sk = weapon['skill']
        buttons.append([InlineKeyboardButton(text=f"⚔️ {sk['name']} ({sk['cost']} MP)", callback_data=f"combat_do_skill_{sk['id']}")])

    buttons.append([InlineKeyboardButton(text="👁️ Revelatio (10 MP)", callback_data="combat_do_skill_reveal")])
    if player_mp >= 20: 
        buttons.append([InlineKeyboardButton(text="⏳ Time Warp (20 MP)", callback_data="combat_do_skill_timewarp")])
        
    buttons.append([InlineKeyboardButton(text="🔙 Kembali", callback_data="menu_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_combat_item_keyboard(player):
    inventory = player.get('inventory', [])
    usable_items = [i for i in inventory if i.get('effect', '').startswith(('heal_', 'mp_', 'resin_', 'repair_', 'energy_', 'cure_'))]
    buttons = []
    item_counts = {}
    for item in usable_items:
        if item['id'] not in item_counts:
            item_counts[item['id']] = {'name': item['name'], 'count': 0}
        item_counts[item['id']]['count'] += 1

    for item_id, data in item_counts.items():
        buttons.append([InlineKeyboardButton(text=f"🎒 {data['name']} (x{data['count']})", callback_data=f"combat_do_item_{item_id}")])
    
    if not buttons: buttons.append([InlineKeyboardButton(text="❌ Tas Kosong", callback_data="menu_back")])
    buttons.append([InlineKeyboardButton(text="🔙 Kembali", callback_data="menu_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_chest_keyboard(chest_type):
    buttons = [
        [InlineKeyboardButton(text="🔓 Buka dengan Kunci", callback_data=f"chest_key_{chest_type}")],
        [InlineKeyboardButton(text="💥 Paksa Buka (Resiko!)", callback_data=f"chest_force_{chest_type}")],
        [InlineKeyboardButton(text="🚶 Tinggalkan", callback_data="chest_leave")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_grave_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🙏 Berdoa (+MP)", callback_data="grave_pray")],
        [InlineKeyboardButton(text="🚶 Lanjutkan Perjalanan", callback_data="grave_leave")]
    ])

def get_idol_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🩸 Beri Darah (-HP) -> Buff ATK", callback_data="idol_blood")],
        [InlineKeyboardButton(text="🔮 Beri Mana (-MP) -> Hapus Hazard", callback_data="idol_mana")],
        [InlineKeyboardButton(text="🚶 Berlalu", callback_data="idol_leave")]
    ])


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
        raw_dmg = puzzle.get('damage', 10)
        
        # INSTANT HP UPDATE LOGIC
        new_hp = p['hp'] - raw_dmg
        update_player(user_id, {"hp": new_hp, "current_combo": 0})
        p['hp'] = new_hp # Update lokal untuk UI
        
        if new_hp <= 0:
            await state.set_state(GameState.exploring)
            stats = {'cycle': p.get('cycle', 1), 'kills': p['kills'], 'gold_lost': p['gold']}
            death_msg = create_death_screen("Waktu habis di pertarungan", stats)
            msg_text = reset_player_death(user_id, "death_combat")
            try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text="💀 **KAU TELAH GUGUR...**", parse_mode="Markdown")
            except: pass
            await message.answer(death_msg + "\n\n" + msg_text, reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
        else:
            broken = reduce_equipment_durability(user_id, 'armor')
            broken_txt = f"\n🛡️ *CRACK!* Armormu hancur: {', '.join(broken)}!" if broken else ""
            
            new_puzzle = generate_battle_puzzle(p, puzzle.get('tier', 1), puzzle.get('is_boss', False), existing_monster=puzzle)
            new_puzzle['generated_time'] = None 
            await state.update_data(puzzle=new_puzzle, action_type=None)
            
            safe_puzzle = new_puzzle.copy()
            safe_puzzle['question'] = "Pilih aksi untuk mengungkap segel teka-teki!"
            safe_puzzle['timer'] = "--"
            
            log_msg = f"⏰ WAKTU HABIS! Kamu terlalu lambat! (-{raw_dmg} HP){broken_txt}"
            next_msg = render_live_battle(p, safe_puzzle, log_msg)
            
            try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text=next_msg, parse_mode="Markdown", reply_markup=get_stance_keyboard(puzzle.get('is_boss', False)))
            except TelegramBadRequest: pass

# === COMMAND HANDLERS ===
@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.first_name
    player = get_player(user_id, username)
    await state.set_state(GameState.exploring)
    welcome_msg = f"━━━━━━━━━━━━━━━━━━━━\n📜 *THE ARCHIVUS* 📜\n━━━━━━━━━━━━━━━━━━━━\nSelamat datang, {username}\n \nKau telah memasuki dimensi\ntanpa ujung ini sebagai\n*Weaver* - penenun takdir.\n━━━━━━━━━━━━━━━━━━━━\nCycle: {player.get('cycle', 1)} | Level: {player.get('level', 1)}\n{create_hp_bar(player.get('hp',100), player.get('max_hp',100))}\n{create_mp_bar(player.get('mp', 0), player.get('max_mp', 50))}\n{create_energy_bar(player.get('energy', 100), player.get('max_energy', 100))}\n🔮 Ketik /help untuk panduan"
    await message.answer(welcome_msg, reply_markup=get_main_reply_keyboard(player), parse_mode="Markdown")

@dp.message(GameState.exploring, F.text == "📊 Status")
async def status_handler(message: Message):
    p = get_player(message.from_user.id)
    status_card = create_status_card(p)
    status_card += f"\n🏆 Achievements: {len(p.get('achievements_unlocked', []))}/13"
    await message.answer(status_card, reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")

@dp.message(GameState.exploring, F.text == "🎒 Inventory")
async def inventory_handler(message: Message):
    p = get_player(message.from_user.id)
    inv_display = create_inventory_display(p)
    keyboard = []
    usable_items = [i for i in p.get('inventory', []) if i.get('type') in ['potion', 'consumable', 'food']]
    for i, item in enumerate(usable_items[:5]): 
        keyboard.append([InlineKeyboardButton(text=f"Use: {item['name']}", callback_data=f"use_item_{item['id']}")])
    keyboard.append([InlineKeyboardButton(text="🔙 Close", callback_data="close_inventory")])
    await message.answer(inv_display, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard), parse_mode="Markdown")


# === MOVEMENT & EXPLORATION (DENGAN ENERGI & DRIVER) ===
@dp.message(F.text.in_(["⬆️ Utara", "⬅️ Barat", "Timur ➡️", "⬇️ Selatan"]))
async def move_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    current_state = await state.get_state()
    if current_state in [GameState.in_combat, GameState.in_event, GameState.in_rest_area]:
        return await message.answer("Selesaikan dulu urusanmu di depan sebelum bergerak maju!")
        
    await state.set_state(GameState.exploring)
    tick_buffs(user_id) 
    
    p = get_player(user_id)
    
    # 1. CEK ENERGI
    if p.get('energy', 100) <= 0:
        return await message.answer("😫 **Kamu terlalu lelah!**\nEnergi habis. Kamu harus makan sesuatu sebelum bisa berjalan lagi.")

    # 2. LOGIKA PUSING (CONTROL NGACAR)
    actual_move = message.text
    dizzy_msg = ""
    if "dizzy" in p.get('debuffs', []):
        if random.random() < 0.5:
            actual_move = random.choice(["⬆️ Utara", "⬅️ Barat", "Timur ➡️", "⬇️ Selatan"])
            dizzy_msg = f"🌀 Kepalamu berputar... Alih-alih {message.text.lower()}, kamu malah berjalan ke {actual_move.lower()}!\n\n"

    # 3. LOGIKA RACUN (DARAH BERKURANG PER LANGKAH)
    poison_msg = ""
    if "poisoned" in p.get('debuffs', []):
        new_hp = p['hp'] - 5
        update_player(user_id, {"hp": new_hp})
        p['hp'] = new_hp
        poison_msg = f"\n🤢 *Racun menggerogoti nadimu...* (-5 HP)"
        
        if new_hp <= 0:
            stats = {'cycle': p.get('cycle', 1), 'kills': p['kills'], 'gold_lost': p['gold']}
            death_msg = create_death_screen("Tewas karena keracunan parah", stats)
            msg_text = reset_player_death(user_id, "death_poison")
            return await message.answer(death_msg + "\n\n" + msg_text, reply_markup=get_main_reply_keyboard(), parse_mode="Markdown")

    # 4. PROSES GERAK (DRIVER INTENSITAS)
    new_energy = p.get('energy', 100) - 1
    update_player(user_id, {"energy": new_energy})
    
    event_type, event_data, narration = process_move(user_id)
    
    # --- 5. HANDLING HASIL EXPLORATION ---
    
    # EVENT KOMBAT (MONSTER / BOSS)
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
        
        combat_ui = render_live_battle(p, safe_puzzle, f"⚠️ {dizzy_msg}{narration}{poison_msg}")
        sent_msg = await message.answer(combat_ui, parse_mode="Markdown", reply_markup=get_stance_keyboard(is_boss))
        
        await state.update_data(
            battle_msg_id=sent_msg.message_id,
            puzzle=puzzle, 
            combat_start_hp=p['hp'], 
            current_combo=p.get('current_combo', 0),
            action_type=None
        )
        
    # EVENT REST AREA (SHOP & HEAL)
    elif event_type == "rest_area":
        await state.set_state(GameState.in_rest_area)
        await message.answer(f"{dizzy_msg}{narration}{poison_msg}", reply_markup=get_rest_area_keyboard(), parse_mode="Markdown")

    # EVENT TREASURE CHEST
    elif event_type == "treasure_chest":
        await state.set_state(GameState.in_event)
        chest_type = event_data['type']
        await message.answer(f"{dizzy_msg}{narration}{poison_msg}", reply_markup=get_chest_keyboard(chest_type), parse_mode="Markdown")

    # EVENT GRAVE (KUBURAN)
    elif event_type == "grave":
        await state.set_state(GameState.in_event)
        await message.answer(f"{dizzy_msg}{narration}{poison_msg}", reply_markup=get_grave_keyboard(), parse_mode="Markdown")

    # EVENT IDOL (PATUNG SEMBAHAN)
    elif event_type == "idol":
        await state.set_state(GameState.in_event)
        await message.answer(f"{dizzy_msg}{narration}{poison_msg}", reply_markup=get_idol_keyboard(), parse_mode="Markdown")
        
    # EVENT NPC / LORE / TRAP / AMAN
    else:
        status_bar = f"\n⚡ Energi: {new_energy}/100 {poison_msg}"
        
        if event_type == "npc_lore" or event_type == "npc_mission":
            # Tampilkan UI khusus NPC Interaktif di sini (Bisa ditambahkan Inline Button 'Bicara')
            pass
            
        await message.answer(f"{dizzy_msg}{narration}{status_bar}", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")


# === HANDLER EVENT INTERAKSI (CHEST, GRAVE, IDOL, REST AREA) ===

@dp.callback_query(GameState.in_rest_area, F.data.startswith("rest_"))
async def rest_area_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    action = callback.data.replace("rest_", "")
    p = get_player(user_id)
    
    if action == "sleep":
        if p['gold'] < 20:
            return await callback.answer("❌ Uangmu tidak cukup untuk menginap! (Butuh 20G)", show_alert=True)
        update_player(user_id, {"gold": p['gold']-20, "hp": p['max_hp'], "mp": p['max_mp'], "energy": p['max_energy']})
        await callback.message.edit_text("🛏️ Kau tertidur pulas. HP, MP, dan Energi pulih sepenuhnya!", parse_mode="Markdown")
        await state.set_state(GameState.exploring)
        
    elif action == "shop":
        loc = p.get('location', "The Whispering Hall")
        await callback.message.edit_text("🛒 *Merchant Rest Area*\n'Silakan lihat-lihat, Weaver.'", reply_markup=get_shop_keyboard(loc), parse_mode="Markdown")
        
    elif action == "main_menu":
        await callback.message.edit_text("🏕️ **CAMPFIRE.** Hawa hangat menyambutmu.", reply_markup=get_rest_area_keyboard(), parse_mode="Markdown")
        
    elif action == "exit":
        await state.set_state(GameState.exploring)
        await callback.message.delete()
        await callback.message.answer("Beranjak dari api unggun, kau kembali melangkah ke dalam kegelapan...", reply_markup=get_main_reply_keyboard(p))


@dp.callback_query(GameState.in_event, F.data.startswith("chest_"))
async def chest_event_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    action, c_type = callback.data.split("_")[1], callback.data.split("_")[2] if len(callback.data.split("_"))>2 else ""
    p = get_player(user_id)
    
    if action == "leave":
        await state.set_state(GameState.exploring)
        await callback.message.edit_text("Kau mengabaikan peti itu dan berjalan pergi.")
        return
        
    elif action == "key":
        inv = p.get('inventory', [])
        required_key = "buy_key_magic" if c_type == "sealed" else "buy_key_iron"
        key_item = next((i for i in inv if i.get('id') == required_key), None)
        
        if not key_item:
            return await callback.answer(f"❌ Kau tidak punya Kunci yang tepat! ({required_key})", show_alert=True)
            
        inv.remove(key_item)
        drops = roll_loot_drop(tier_level=3) # Peti yang dibuka dengan kunci selalu wangi (Tier 3)
        update_player(user_id, {'inventory': inv})
        await state.set_state(GameState.exploring)
        await callback.message.edit_text(f"🔓 *KLIK!* Peti berhasil dibuka dengan aman!\n\n{create_loot_drop(drops)}", parse_mode="Markdown")
        
    elif action == "force":
        if random.random() < 0.4: # 40% gagal dan meledak
            dmg = random.randint(15, 30)
            update_player(user_id, {"hp": p['hp'] - dmg})
            await state.set_state(GameState.exploring)
            await callback.message.edit_text(f"💥 *BOOOM!* Peti itu berisi jebakan sihir! Kau terlempar dan kehilangan {dmg} HP!", parse_mode="Markdown")
        else:
            drops = roll_loot_drop(tier_level=1) # Paksa buka hadiahnya lebih ampas
            await state.set_state(GameState.exploring)
            await callback.message.edit_text(f"🔨 *KRAAAK!* Engselnya patah. Kau mendapat:\n\n{create_loot_drop(drops)}", parse_mode="Markdown")

@dp.callback_query(GameState.in_event, F.data.startswith("grave_"))
async def grave_event_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    action = callback.data.replace("grave_", "")
    
    if action == "leave":
        await callback.message.edit_text("Kau memberikan penghormatan dalam diam, lalu berlalu.")
    elif action == "pray":
        p = get_player(user_id)
        heal_mp = random.randint(15, 25)
        update_player(user_id, {"mp": min(p['max_mp'], p['mp'] + heal_mp)})
        await callback.message.edit_text(f"🙏 Jiwa Weaver terdahulu memberkatimu. Pikiranmu jernih (+{heal_mp} MP).", parse_mode="Markdown")
        
    await state.set_state(GameState.exploring)


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

    if action == "skill": await callback.message.edit_reply_markup(reply_markup=get_combat_skill_keyboard(p, p_stats))
    elif action == "item": await callback.message.edit_reply_markup(reply_markup=get_combat_item_keyboard(p))
    elif action == "back": await callback.message.edit_reply_markup(reply_markup=get_stance_keyboard(is_boss))
    await callback.answer()


# === HANDLER AKSI UTAMA (INSTAN DODGE/BLOCK ATAU MUNCULKAN PUZZLE) ===
@dp.callback_query(GameState.in_combat, F.data.startswith("stance_") | F.data.startswith("combat_do_"))
async def combat_action_trigger(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    puzzle = data.get("puzzle")
    p = get_player(user_id)
    p_stats = calculate_equipment_stats(p)
    
    if not puzzle: return await callback.answer("Error: Data pertempuran tidak ditemukan.", show_alert=True)
    
    raw_data = callback.data
    action = ""
    active_skill_id = None
    pending_item_id = None

    if raw_data.startswith("stance_"):
        action = raw_data.replace("stance_", "")
    elif raw_data.startswith("combat_do_skill_"):
        action = "skill"
        active_skill_id = raw_data.replace("combat_do_skill_", "")
    elif raw_data.startswith("combat_do_item_"):
        action = "item"
        pending_item_id = raw_data.replace("combat_do_item_", "")

    # 💥 LOGIKA INSTAN (TANPA PUZZLE) UNTUK DODGE & BLOCK 💥
    if action in ["dodge", "block"]:
        if p['mp'] < 5: 
            return await callback.answer("🔮 MP tidak cukup! (Butuh 5)", show_alert=True)
        
        raw_dmg = puzzle.get('damage', 10)
        final_dmg = raw_dmg
        log_msg = ""
        
        dodge_penalty = 0.20 if "dizzy" in p.get('debuffs', []) else 0.0

        if action == "dodge":
            chance = calculate_dodge_chance(p_stats) - dodge_penalty
            if random.random() < max(0.05, chance):
                log_msg = f"💨 *PERFECT DODGE!* Kamu menghindar dengan lincah (0 Damage)."
                final_dmg = 0
            else:
                dizzy_txt = " (Kepalamu pusing!)" if dodge_penalty > 0 else ""
                log_msg = f"❌ *DODGE GAGAL!*{dizzy_txt} Kamu gagal menghindar (-{raw_dmg} HP)."
                final_dmg = raw_dmg
                
        elif action == "block":
            reduction = calculate_block_reduction(p_stats)
            if "dizzy" in p.get('debuffs', []): reduction *= 0.8 
            
            final_dmg = max(1, int(raw_dmg * (1 - reduction)))
            log_msg = f"🛡️ *BLOCK!* Menahan serangan. Damage diredam: {int(reduction*100)}% (-{final_dmg} HP)."
            
        new_hp = p['hp'] - final_dmg
        update_player(user_id, {"hp": new_hp, "mp": p['mp'] - 5, "current_combo": 0})
        p['hp'] = new_hp
        p['mp'] = p['mp'] - 5
        
        if new_hp <= 0:
            await state.set_state(GameState.exploring)
            stats = {'cycle': p.get('cycle', 1), 'kills': p['kills'], 'gold_lost': p['gold']}
            death_msg = create_death_screen("Gugur saat bertahan/menghindar", stats)
            msg_text = reset_player_death(user_id, "death_combat")
            try: await callback.message.edit_text("💀 **KAU TELAH GUGUR...**", parse_mode="Markdown")
            except: pass
            await callback.message.answer(death_msg + "\n\n" + msg_text, reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
        else:
            new_puzzle = generate_battle_puzzle(p, puzzle.get('tier', 1), puzzle.get('is_boss', False), existing_monster=puzzle)
            new_puzzle['generated_time'] = None 
            await state.update_data(puzzle=new_puzzle, action_type=None)
            
            safe_puzzle = new_puzzle.copy()
            safe_puzzle['question'] = "Pilih aksi untuk mengungkap segel teka-teki!"
            safe_puzzle['timer'] = "--"
            
            next_ui = render_live_battle(p, safe_puzzle, log_msg)
            await callback.message.edit_text(next_ui, parse_mode="Markdown", reply_markup=get_stance_keyboard(puzzle.get('is_boss', False)))
        
        return 

    # 🧩 LOGIKA BERBASIS PUZZLE (ATTACK, SKILL, RUN, ITEM) 🧩
    act_text = ""
    if action == "attack": act_text = "⚔️ *Menerjang maju!*"
    elif action == "run": act_text = "🏃 *Mencari celah kabur!*"
    elif action == "skill": act_text = "🔮 *Mempersiapkan sihir khusus!*"
    elif action == "item": act_text = "🎒 *Membongkar tas mencari ramuan...*"
        
    if action == "skill":
        skill_cost = 10 if active_skill_id == "reveal" else 20 if active_skill_id == "timewarp" else 15
        if p['mp'] < skill_cost: return await callback.answer(f"🔮 MP tidak cukup! (Butuh {skill_cost})", show_alert=True)
        
        # LOGIKA TIME WARP (Membekukan waktu/timer puzzle)
        if active_skill_id == "timewarp":
            puzzle['timer'] = "--"
            act_text = "⏳ *TIME WARP AKTIF!* Waktu membeku! Kerjakan teka-teki tanpa batas waktu!"
            
        # LOGIKA REVELATIO (Membuka satu huruf acak di teka-teki)
        elif active_skill_id == "reveal":
            answer = puzzle['answer']
            if 'current_hint' not in puzzle:
                puzzle['current_hint'] = "".join(["_" if c.isalnum() else c for c in answer])
            
            hidden_indices = [i for i, char in enumerate(puzzle['current_hint']) if char == "_"]
            if hidden_indices:
                idx = random.choice(hidden_indices)
                hint_list = list(puzzle['current_hint'])
                hint_list[idx] = answer[idx]
                puzzle['current_hint'] = "".join(hint_list)
                puzzle['question'] += f"\n\n✨ Hint Revelatio: `{puzzle['current_hint']}`"
                act_text = "👁️ *REVELATIO!* Sebuah huruf terungkap di teka-teki!"

        update_player(user_id, {"mp": p['mp'] - skill_cost})
        p['mp'] -= skill_cost

    await state.update_data(action_type=action, active_skill_id=active_skill_id, pending_item=pending_item_id)

    puzzle['generated_time'] = time.time()
    await state.update_data(puzzle=puzzle)

    puzzle_ui = render_live_battle(p, puzzle, act_text)
    await callback.message.edit_text(puzzle_ui, parse_mode="Markdown", reply_markup=None)
    
    if puzzle['timer'] != "--":
        asyncio.create_task(combat_timeout_task(callback.message, state, puzzle, user_id))


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
    
    # Jika timer dibekukan (Time Warp), limit diatur ke sangat besar agar dianggap valid
    effective_timer = 9999 if str(puzzle.get('timer')) == "--" else puzzle['timer']
    is_correct, is_timeout, time_taken = validate_answer(message.text, puzzle['answer'], puzzle['generated_time'], effective_timer)
    
    p = get_player(user_id)
    p_stats = calculate_equipment_stats(p)
    is_boss = puzzle.get('is_boss', False)
    
    result_msg = ""
    current_combo = data.get("current_combo", 0)
    
    # EFEK PUSING 
    if "dizzy" in p.get('debuffs', []) and is_correct and action in ["attack", "skill"]:
        if random.random() < 0.3: 
            is_correct = False
            result_msg = "🌀 Kepalamu berputar! Seranganmu meleset sepenuhnya!"

    if is_correct:
        is_critical = time_taken < 10.0
        crit_msg = "\n💥 *CRITICAL HIT!*" if is_critical else ""
        
        if action == "attack":
            current_combo += 1
            p_dmg = max(1, p_stats['atk'] - puzzle.get('monster_def', 0))
            if is_critical: p_dmg = int(p_dmg * 1.5)
            
            puzzle['monster_hp'] -= p_dmg  
            broken = reduce_equipment_durability(user_id, 'weapon')
            broken_txt = f"\n⚠️ Senjatamu hancur: {', '.join(broken)}!" if broken else ""
            result_msg = f"⚔️ Serangan telak! Musuh -{p_dmg} HP.{crit_msg}{broken_txt}"
            
        elif action == "skill":
            current_combo += 1
            # Skill damage lebih besar
            p_dmg = max(1, int(p_stats['atk'] * 1.8) - puzzle.get('monster_def', 0))
            if is_critical: p_dmg = int(p_dmg * 1.5)
            
            puzzle['monster_hp'] -= p_dmg
            result_msg = f"🔥 *SKILL ACTIVATED!* Musuh -{p_dmg} HP.{crit_msg}"
            
        elif action == "item":
            item_id = data.get("pending_item")
            inventory = p.get('inventory', [])
            item_idx = next((i for i, item in enumerate(inventory) if item.get('id') == item_id), -1)
            
            if item_idx != -1:
                used_item = inventory.pop(item_idx)
                eff = used_item.get('effect', '')
                updates = {'inventory': inventory}
                
                if eff.startswith("heal_"):
                    amt = int(eff.split("_")[1]); updates['hp'] = min(p['max_hp'], p['hp'] + amt)
                    result_msg = f"🧪 Potion aman! (+{amt} HP)"
                elif eff.startswith("mp_"):
                    amt = int(eff.split("_")[1]); updates['mp'] = min(p.get('max_mp', 50), p.get('mp', 0) + amt)
                    result_msg = f"🔮 MP Pulih dengan aman! (+{amt} MP)"
                elif eff.startswith("energy_"):
                    amt = int(eff.split("_")[1]); updates['energy'] = min(p.get('max_energy', 100), p.get('energy', 0) + amt)
                    result_msg = f"⚡ Energi dipulihkan! (+{amt} EN)"
                elif eff.startswith("cure_"):
                    status_to_cure = eff.split("_")[1]
                    debuffs = p.get('debuffs', [])
                    if status_to_cure == "all": updates['debuffs'] = []
                    elif status_to_cure in debuffs:
                        debuffs.remove(status_to_cure)
                        updates['debuffs'] = debuffs
                    result_msg = f"✨ Tubuhmu terasa ringan, efek buruk hilang!"
                    
                update_player(user_id, updates)
                p = get_player(user_id)
            else:
                result_msg = "❌ Item tidak ditemukan."

        elif action == "run":
            chance = calculate_dodge_chance(p_stats) + 0.30 
            if "dizzy" in p.get('debuffs', []): chance -= 0.20 
            if random.random() < chance:
                await state.set_state(GameState.exploring)
                update_player(user_id, {'current_combo': 0})
                if battle_msg_id:
                    try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text="🏃💨 *KABUR!*", parse_mode="Markdown")
                    except: pass
                return await message.answer("🏃💨 *BERHASIL KABUR!*", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
            else:
                result_msg = "🧱 Jalan diblokir! Gagal kabur!"

        update_player(user_id, {'current_combo': current_combo, 'max_combo_reached': max(p.get('max_combo_reached', 0), current_combo)})
        
        # CEK KEMATIAN MUSUH
        if puzzle['monster_hp'] <= 0:
            tier = puzzle.get('tier', 1)
            base_reward = 500 if is_boss else (int(tier) * 25 if isinstance(tier, int) else 100)
            total_gold = base_reward + int(base_reward * (current_combo * 0.1))
            new_cycle = p['cycle'] + 1 if is_boss else p['cycle']
            
            drops = roll_loot_drop(tier_level=(5 if is_boss else int(tier)), is_boss=is_boss)
            inv = p.get('inventory', [])
            inv.extend([d for d in drops if d.get('type') != 'gold'])
            
            update_player(user_id, {'kills': p['kills']+1, 'gold': p['gold']+total_gold, 'current_combo': current_combo, 'cycle': new_cycle, 'inventory': inv})
            
            await state.set_state(GameState.exploring)
            if battle_msg_id:
                try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text=f"🎉 **PERTARUNGAN SELESAI** 🎉\nMusuh telah hancur lebur.", parse_mode="Markdown")
                except: pass
                
            loot_str = create_loot_drop(drops)
            await message.answer(f"🎉 *KEMENANGAN!*\n{result_msg}\n\n💰 Bonus Gold: +{total_gold}\n\n{loot_str}", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
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
                except:
                    sent = await message.answer(next_msg, parse_mode="Markdown", reply_markup=get_stance_keyboard(is_boss))
                    await state.update_data(battle_msg_id=sent.message_id)

    # JIKA JAWABAN SALAH / TIMEOUT
    else:
        if not result_msg: result_msg = "❌ Salah/Terlambat!"
        raw_damage = puzzle.get('damage', 10)
        final_damage = raw_damage
        dmg_msg = f"{result_msg} (-{final_damage} HP)"
            
        new_hp = p['hp'] - final_damage
        update_player(user_id, {'current_combo': 0, 'hp': new_hp})
        
        broken = reduce_equipment_durability(user_id, 'armor')
        if broken: dmg_msg += f"\n🛡️ *CRACK!* Armormu hancur!"
        
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
            
            next_msg = render_live_battle(p, safe_puzzle, f"❌ *GAGAL!*\n{dmg_msg}")
            
            if battle_msg_id:
                try: await message.bot.edit_message_text(chat_id=message.chat.id, message_id=battle_msg_id, text=next_msg, parse_mode="Markdown", reply_markup=get_stance_keyboard(is_boss))
                except:
                    sent = await message.answer(next_msg, parse_mode="Markdown", reply_markup=get_stance_keyboard(is_boss))
                    await state.update_data(battle_msg_id=sent.message_id)


# === PENGGUNAAN ITEM DI LUAR COMBAT ===
@dp.callback_query(F.data.startswith("use_item_"))
async def use_item_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    item_id = callback.data.replace("use_item_", "")
    p = get_player(user_id)
    inventory = p.get('inventory', [])
    item_index = next((i for i, item in enumerate(inventory) if item.get('id') == item_id), -1)
    
    if item_index == -1: return await callback.answer("❌ Item habis/tidak ditemukan!", show_alert=True)
    used_item = inventory.pop(item_index)
    effect = used_item.get('effect', '')
    updates = {'inventory': inventory}
    alert_msg = f"Memakai {used_item['name']}!\n"
    
    if effect.startswith("heal_"):
        amt = int(effect.split("_")[1]); updates['hp'] = min(p['max_hp'], p['hp'] + amt)
        alert_msg += f"❤️ +{amt} HP"
    elif effect.startswith("mp_"):
        amt = int(effect.split("_")[1]); updates['mp'] = min(p.get('max_mp', 50), p.get('mp', 0) + amt)
        alert_msg += f"🔮 +{amt} MP"
    elif effect.startswith("energy_"):
        amt = int(effect.split("_")[1]); updates['energy'] = min(p.get('max_energy', 100), p.get('energy', 100) + amt)
        alert_msg += f"⚡ +{amt} Energi"
    elif effect.startswith("cure_"):
        status_to_cure = effect.split("_")[1]
        debuffs = p.get('debuffs', [])
        if status_to_cure == "all": updates['debuffs'] = []
        elif status_to_cure in debuffs:
            debuffs.remove(status_to_cure)
            updates['debuffs'] = debuffs
        alert_msg += f"✨ Tubuhmu kembali segar!"
    elif effect.startswith("resin_"):
        elemen = effect.split("_")[1]; updates['active_resin'] = elemen; updates['resin_duration'] = 3
        alert_msg += f"📜 Senjatamu memancarkan sihir {elemen}!"
    elif effect == "repair_all":
        for equip in updates['inventory']:
            if equip.get('type') in ['weapon', 'shield', 'chest', 'head', 'gloves', 'boots']:
                equip['durability'] = equip.get('max_durability', 50)
        alert_msg += "⚒️ Equip-mu kembali utuh 100%!"
    
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

async def main():
    auto_seed_content()
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
