import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

# === ROOT IMPORTS ===
from database import get_player, update_player, auto_seed_content, reset_player_death, add_history
from states import GameState
from config import BOT_TOKEN

# === NEW ARCHITECTURE IMPORTS ===
# Memanggil dari folder game/systems/
from game.systems.exploration import process_move  
from game.systems.shop import get_shop_keyboard, process_purchase
from game.systems.combat import generate_battle_puzzle, validate_answer
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
    create_death_screen, create_location_transition
)

dp = Dispatcher()

# === ENHANCED KEYBOARDS ===

def get_main_reply_keyboard(player=None):
    """Enhanced main keyboard dengan quick info"""
    keyboard = [
        [KeyboardButton(text="⬆️ Utara")],
        [KeyboardButton(text="⬅️ Barat"), KeyboardButton(text="Timur ➡️")],
        [KeyboardButton(text="⬇️ Selatan")],
        [
            KeyboardButton(text="📊 Status"), 
            KeyboardButton(text="🎒 Inventory")
        ],
        [
            KeyboardButton(text="🛒 Toko"),
            KeyboardButton(text="🏆 Quest")
        ]
    ]
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="⚔️ Pilih aksimu, Weaver..."
    )

def get_enhanced_combat_keyboard(player_mp, has_companion=False):
    """Combat keyboard dengan skill options"""
    buttons = [[InlineKeyboardButton(text="🔮 Revelatio (10 MP)", callback_data="skill_reveal")]]
    
    # Additional skills unlocked di level tertentu
    if player_mp >= 20:
        buttons.append([InlineKeyboardButton(text="⚡ Time Warp (20 MP)", callback_data="skill_timewarp")])
    
    if player_mp >= 30:
        buttons.append([InlineKeyboardButton(text="🛡️ Shield (30 MP)", callback_data="skill_shield")])
    
    if has_companion:
        buttons.append([InlineKeyboardButton(text="👻 Bantuan Roh (Gratis)", callback_data="companion_help")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_event_keyboard(event):
    """Keyboard untuk random events"""
    buttons = []
    
    if event['type'] == 'choice':
        for i, choice in enumerate(event['choices']):
            cost_text = f" (-{choice.get('cost', 0)} Gold)" if choice.get('cost', 0) > 0 else ""
            buttons.append([InlineKeyboardButton(
                text=choice['text'] + cost_text,
                callback_data=f"event_choice_{i}"
            )])
    elif event['type'] == 'treasure':
        buttons.append([InlineKeyboardButton(text="🔓 Buka Peti", callback_data="event_open")])
        buttons.append([InlineKeyboardButton(text="🚪 Tinggalkan", callback_data="event_ignore")])
    elif event['type'] == 'shrine':
        buttons.append([InlineKeyboardButton(text="🙏 Berdoa", callback_data="event_pray")])
        buttons.append([InlineKeyboardButton(text="🚶 Pergi", callback_data="event_ignore")])
    elif event['type'] == 'gamble':
        buttons.append([InlineKeyboardButton(text=f"🎲 Bertaruh {event['bet_amount']} Gold", callback_data="event_gamble")])
        buttons.append([InlineKeyboardButton(text="❌ Tolak", callback_data="event_ignore")])
    elif event['type'] == 'shop':
        for i, item in enumerate(event['items']):
            cost = item['cost']
            cost_text = f"{cost} Gold" if cost > 0 else f"(Dapat {abs(cost)} Gold)"
            buttons.append([InlineKeyboardButton(
                text=f"{item['name']} - {cost_text}",
                callback_data=f"event_buy_{i}"
            )])
        buttons.append([InlineKeyboardButton(text="🚪 Pergi", callback_data="event_ignore")])
    else:
        buttons.append([InlineKeyboardButton(text="✅ Terima", callback_data="event_accept")])
        buttons.append([InlineKeyboardButton(text="❌ Tolak", callback_data="event_ignore")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# === BACKGROUND TIMERS (ENHANCED) ===

async def combat_timeout_task(message: Message, state: FSMContext, puzzle: dict, user_id: int):
    """Enhanced timeout dengan visual countdown"""
    timer = puzzle['timer']
    
    # Kirim countdown di intervals tertentu
    warning_times = [30, 15, 5]
    
    for warning in warning_times:
        if timer > warning:
            await asyncio.sleep(timer - warning)
            timer = warning
            
            # Update message dengan warning
            try:
                warning_text = f"⚠️ *WAKTU TERSISA: {warning} DETIK!*"
                # Bisa edit message kalau mau (optional)
            except:
                pass
    
    # Wait sisa waktu
    await asyncio.sleep(timer)
    
    current_state = await state.get_state()
    data = await state.get_data()
    active_puzzle = data.get("puzzle", {})
    
    if current_state == GameState.in_combat and active_puzzle.get("generated_time") == puzzle["generated_time"]:
        p = get_player(user_id)
        damage = puzzle.get('damage', 10)
        new_hp = p['hp'] - damage
        
        await state.set_state(GameState.exploring)
        
        if new_hp <= 0:
            stats = {'cycle': p.get('cycle', 1), 'kills': p['kills'], 'gold_lost': p['gold']}
            death_msg = create_death_screen("Waktu habis di pertarungan", stats)
            msg_text = reset_player_death(user_id, "death_combat")
            
            await message.answer(death_msg + "\n\n" + msg_text, reply_markup=get_main_reply_keyboard(), parse_mode="Markdown")
        else:
            update_player(user_id, {"hp": new_hp})
            # Reset combo
            update_player(user_id, {"current_combo": 0})
            
            await message.answer(
                f"⏰ *WAKTU HABIS!*\n\n*{puzzle['monster_name']}* menyerangmu!\n{create_hp_bar(new_hp, p['max_hp'])}", 
                reply_markup=get_main_reply_keyboard(),
                parse_mode="Markdown"
            )

# === COMMAND HANDLERS ===

@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.first_name
    
    player = get_player(user_id, username)
    await state.set_state(GameState.exploring)
    
    welcome_msg = f"""
━━━━━━━━━━━━━━━━━━━━
📜 *THE ARCHIVUS* 📜
━━━━━━━━━━━━━━━━━━━━
Selamat datang, {username}
 
Kau telah memasuki dimensi
tanpa ujung ini sebagai
*Weaver* - penenun takdir.
 
Bertahanlah, pecahkan
misteri, dan catatkan
namamu dalam sejarah...
━━━━━━━━━━━━━━━━━━━━

Cycle: {player.get('cycle', 1)} | Level: {player.get('level', 1)}
{create_hp_bar(player['hp'], player['max_hp'])}
{create_mp_bar(player['mp'], player['max_mp'])}

🔮 Ketik /help untuk panduan
"""
    
    await message.answer(welcome_msg, reply_markup=get_main_reply_keyboard(player), parse_mode="Markdown")
    
    # Check daily quests
    import datetime
    last_login = player.get('last_login')
    today = datetime.datetime.now().date()
    
    if not last_login or last_login != str(today):
        # Reset daily quests
        daily_quests = generate_daily_quests()
        update_player(user_id, {
            'last_login': str(today),
            'daily_quests': daily_quests,
            'daily_stats': {}
        })
        
        quest_card = create_daily_quest_card([
            {**q, 'progress': 0, 'completed': False} 
            for q in daily_quests
        ])
        
        await message.answer(f"🌅 *DAILY QUESTS UPDATED!*\n\n{quest_card}", parse_mode="Markdown")

@dp.message(F.text == "/help")
async def help_handler(message: Message):
    help_text = """
📖 *PANDUAN THE ARCHIVUS*

🎮 *Cara Bermain:*
• Gunakan tombol arah untuk menjelajah
• Pecahkan puzzle untuk mengalahkan monster
• Kumpulkan gold dan item
• Tingkatkan level dan unlock skill

⚔️ *Combat:*
• Jawab puzzle dengan benar dalam waktu yang ditentukan
• Gunakan skill dengan menekan tombol di combat
• Combo = bonus reward!

🏆 *Progression:*
• Selesaikan Daily Quests untuk bonus
• Unlock Achievements untuk reward permanen
• Level up = stat boost + skill baru

💡 *Tips:*
• Kelola MP dengan bijak untuk skill
• Simpan ramuan untuk boss fight
• NPC bisa baik atau jahat - hati-hati!
• Loot drops bervariasi berdasarkan tier monster

🎁 *Easter Eggs:*
• Explore dan eksperimen untuk menemukan rahasia!

_Selamat berpetualang, Weaver!_
"""
    await message.answer(help_text, parse_mode="Markdown")

# === STATUS & INVENTORY HANDLERS ===

@dp.message(GameState.exploring, F.text == "📊 Status")
async def status_handler(message: Message):
    p = get_player(message.from_user.id)
    
    status_card = create_status_card(p)
    
    # Add achievements progress
    unlocked_count = len(p.get('achievements_unlocked', []))
    total_achievements = 12  # Update based on actual count
    
    status_card += f"\n🏆 Achievements: {unlocked_count}/{total_achievements}"
    
    # Add active buffs
    active_buffs = p.get('active_buffs', [])
    if active_buffs:
        status_card += "\n\n✨ *ACTIVE BUFFS:*\n"
        for buff in active_buffs:
            status_card += f"• {buff['name']} ({buff.get('duration', 0)} left)\n"
    
    await message.answer(status_card, reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")

@dp.message(GameState.exploring, F.text == "🎒 Inventory")
async def inventory_handler(message: Message):
    p = get_player(message.from_user.id)
    from utils.helper_ui import create_inventory_display # Memanggil dari utils
    
    inv_display = create_inventory_display(p.get('inventory', []))
    
    # Keyboard untuk use item
    keyboard = []
    usable_items = [i for i in p.get('inventory', []) if i.get('type') in ['potion', 'consumable']]
    
    for i, item in enumerate(usable_items[:5]):  # Max 5 items
        keyboard.append([InlineKeyboardButton(
            text=f"Use: {item['name']}",
            callback_data=f"use_item_{item['id']}"
        )])
    
    keyboard.append([InlineKeyboardButton(text="🔙 Close", callback_data="close_inventory")])
    
    await message.answer(
        inv_display,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
        parse_mode="Markdown"
    )

@dp.message(GameState.exploring, F.text == "🏆 Quest")
async def quest_handler(message: Message):
    p = get_player(message.from_user.id)
    
    daily_quests = p.get('daily_quests', [])
    daily_stats = p.get('daily_stats', {})
    
    quests_with_progress = []
    for quest in daily_quests:
        progress = check_daily_quest_progress(p, quest['type'])
        completed = progress >= quest['target']
        quests_with_progress.append({
            **quest,
            'progress': progress,
            'completed': completed
        })
    
    quest_card = create_daily_quest_card(quests_with_progress)
    
    # Keyboard untuk claim rewards
    keyboard = []
    for i, q in enumerate(quests_with_progress):
        if q['completed'] and not q.get('claimed', False):
            keyboard.append([InlineKeyboardButton(
                text=f"✅ Claim: {q['title']}",
                callback_data=f"claim_quest_{i}"
            )])
    
    keyboard.append([InlineKeyboardButton(text="🔙 Close", callback_data="close_quests")])
    
    await message.answer(
        quest_card,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
        parse_mode="Markdown"
    )

# === MOVEMENT & EXPLORATION (ENHANCED) ===

@dp.message(F.text.in_(["⬆️ Utara", "⬅️ Barat", "Timur ➡️", "⬇️ Selatan"]))
async def move_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    current_state = await state.get_state()
    
    if current_state != GameState.exploring:
        return await message.answer("Kamu sedang tidak bisa bergerak saat ini.")
    
    player = get_player(user_id)
    
    # Track recent moves untuk easter egg
    recent_moves = player.get('recent_moves', [])
    recent_moves.append(message.text)
    if len(recent_moves) > 10:
        recent_moves = recent_moves[-10:]
    update_player(user_id, {'recent_moves': recent_moves})
    
    # Check easter eggs
    easter_egg = check_easter_egg(player, "movement_sequence")
    if easter_egg:
        await message.answer(easter_egg['message'], parse_mode="Markdown")
        # Apply rewards...
        return
    
    # Check random event trigger (10% chance)
    event = trigger_random_event(player.get('cycle', 1), player.get('location'))
    
    if event:
        await state.set_state(GameState.in_event)
        await state.update_data(current_event=event)
        
        event_msg = f"""
🎲 *RANDOM EVENT!*

*{event['name']}*
_{event['description']}_
"""
        await message.answer(event_msg, reply_markup=get_event_keyboard(event), parse_mode="Markdown")
        return
    
    # Normal movement processing (sekarang memakai exploration.py!)
    event_type, event_data, narration = process_move(user_id)
    
    # Update daily stats
    daily_stats = player.get('daily_stats', {})
    daily_stats['steps_today'] = daily_stats.get('steps_today', 0) + 1
    update_player(user_id, {'daily_stats': daily_stats})
    
    # Process event types dengan enhanced UI
    if event_type == "boss":
        # Boss warning dramatis
        boss_name = "SANG PENJAGA"
        warning = create_boss_warning(boss_name)
        
        await message.answer(warning, parse_mode="Markdown")
        await asyncio.sleep(2)  # Dramatic pause
        
        # Start boss combat
        p = get_player(user_id)
        puzzle = generate_battle_puzzle(p, 5, is_boss=True)
        
        await state.set_state(GameState.in_combat)
        await state.update_data(
            puzzle=puzzle, 
            current_stage=1, 
            target_stages=5,
            combat_start_hp=p['hp'],  # Track untuk flawless achievement
            current_combo=player.get('current_combo', 0)
        )
        
        combat_header = create_combat_header(puzzle['monster_name'], "BOSS", 1, 5)
        combat_msg = f"""
{combat_header}

🧩 *PUZZLE STAGE 1:*
`{puzzle['question']}`

{create_hp_bar(p['hp'], p['max_hp'])}
{create_mp_bar(p['mp'], p['max_mp'])}
"""
        
        msg = await message.answer(
            combat_msg, 
            parse_mode="Markdown",
            reply_markup=get_enhanced_combat_keyboard(p['mp'], player.get('has_companion', False))
        )
        
        asyncio.create_task(combat_timeout_task(msg, state, puzzle, user_id))
        
    elif event_type == "monster":
        # Regular combat dengan enhanced UI
        p = get_player(user_id)
        tier_level = min(5, max(1, (p['kills'] // 5) + 1))
        puzzle = generate_battle_puzzle(tier_level, is_boss=False)
        
        await state.set_state(GameState.in_combat)
        await state.update_data(
            puzzle=puzzle,
            current_stage=1,
            target_stages=1,
            combat_start_hp=p['hp'],
            current_combo=player.get('current_combo', 0)
        )
        
        combat_header = create_combat_header(puzzle['monster_name'], tier_level, 1, 1)
        
        # Show combo if active
        combo_text = create_combo_indicator(player.get('current_combo', 0))
        
        combat_msg = f"""
{narration}

{combat_header}

{combo_text}

🧩 *PUZZLE:*
`{puzzle['question']}`

{create_hp_bar(p['hp'], p['max_hp'])}
{create_mp_bar(p['mp'], p['max_mp'])}
"""
        
        msg = await message.answer(
            combat_msg,
            parse_mode="Markdown",
            reply_markup=get_enhanced_combat_keyboard(p['mp'], player.get('has_companion', False))
        )
        
        asyncio.create_task(combat_timeout_task(msg, state, puzzle, user_id))
        
    else:
        # Safe travel or NPC
        await message.answer(narration, reply_markup=get_main_reply_keyboard(player), parse_mode="Markdown")

# === COMBAT HANDLER (ENHANCED) ===

@dp.message(GameState.in_combat)
async def combat_answer_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    puzzle = data.get("puzzle")
    
    if not puzzle:
        return
    
    is_correct, is_timeout = validate_answer(
        message.text, 
        puzzle['answer'], 
        puzzle['generated_time'], 
        puzzle['timer']
    )
    
    p = get_player(user_id)
    
    if is_correct:
        # CORRECT ANSWER PATH
        current_stage = data.get("current_stage", 1)
        target_stages = data.get("target_stages", 1)
        current_combo = data.get("current_combo", 0) + 1
        
        # Update combo
        max_combo = max(p.get('max_combo_reached', 0), current_combo)
        update_player(user_id, {
            'current_combo': current_combo,
            'max_combo_reached': max_combo
        })
        
        if current_stage < target_stages:
            # Next stage
            tier_level = min(5, max(1, (p['kills'] // 5) + 1))
            new_puzzle = generate_battle_puzzle(tier_level, puzzle['is_boss'])
            
            await state.update_data(
                puzzle=new_puzzle,
                current_stage=current_stage + 1,
                current_combo=current_combo
            )
            
            combo_indicator = create_combo_indicator(current_combo)
            
            next_msg = f"""
✅ *BENAR!* {combo_indicator}

{create_combat_header(new_puzzle['monster_name'], puzzle.get('tier', 1), current_stage + 1, target_stages)}

🧩 `{new_puzzle['question']}`

{create_hp_bar(p['hp'], p['max_hp'])}
{create_mp_bar(p['mp'], p['max_mp'])}
"""
            
            msg = await message.answer(
                next_msg,
                parse_mode="Markdown",
                reply_markup=get_enhanced_combat_keyboard(p['mp'], p.get('has_companion', False))
            )
            
            asyncio.create_task(combat_timeout_task(msg, state, new_puzzle, user_id))
            
        else:
            # VICTORY!
            is_boss = puzzle.get('is_boss', False)
            tier = puzzle.get('tier', 1)
            
            # Calculate rewards dengan combo bonus
            base_reward = 500 if is_boss else (tier * 25)
            combo_bonus = int(base_reward * (current_combo * 0.1))  # 10% per combo
            total_gold = base_reward + combo_bonus
            
            base_exp = 1000 if is_boss else (tier * 50)
            exp_reward = base_exp + (current_combo * 20)
            
            # Roll loot drops
            loot_drops = roll_loot_drop(tier, is_boss)
            
            # Check flawless (untuk achievement)
            combat_start_hp = data.get('combat_start_hp', p['hp'])
            is_flawless = (p['hp'] == combat_start_hp)
            
            # Update player
            new_kills = 0 if is_boss else p['kills'] + 1
            new_cycle = p['cycle'] + 1 if is_boss else p['cycle']
            current_exp = p.get('exp', 0) + exp_reward
            current_level = p.get('level', 1)
            exp_needed = calculate_exp_needed(current_level)
            
            # Level up check
            level_up_msg = ""
            while current_exp >= exp_needed:
                current_level += 1
                current_exp -= exp_needed
                exp_needed = calculate_exp_needed(current_level)
                level_up_msg = create_level_up_animation(current_level - 1, current_level)
            
            updates = {
                'kills': new_kills,
                'gold': p['gold'] + total_gold,
                'cycle': new_cycle,
                'exp': current_exp,
                'level': current_level,
                'exp_needed': exp_needed,
                'current_combo': current_combo
            }
            
            if is_boss:
                updates['miniboss_slain'] = False
                updates['boss_kills'] = p.get('boss_kills', 0) + 1
                add_history(user_id, f"Menghancurkan Sang Penjaga. Memasuki Siklus {new_cycle}.")
                
                if is_flawless:
                    updates['flawless_boss_count'] = p.get('flawless_boss_count', 0) + 1
            
            # Add loot to inventory
            if loot_drops:
                inventory = p.get('inventory', [])
                for loot in loot_drops:
                    if loot.get('type') != 'gold':
                        inventory.append(loot)
                    else:
                        updates['gold'] = updates['gold'] + loot['value']
                updates['inventory'] = inventory
            
            # Update daily stats
            daily_stats = p.get('daily_stats', {})
            daily_stats['kills_today'] = daily_stats.get('kills_today', 0) + 1
            daily_stats['gold_earned_today'] = daily_stats.get('gold_earned_today', 0) + total_gold
            if is_flawless:
                daily_stats['perfect_combat_today'] = daily_stats.get('perfect_combat_today', 0) + 1
            updates['daily_stats'] = daily_stats
            
            # Update total gold earned (for achievements)
            updates['total_gold_earned'] = p.get('total_gold_earned', 0) + total_gold
            
            update_player(user_id, updates)
            
            # Check achievements
            updated_player = get_player(user_id)
            newly_unlocked = get_all_unlockable_achievements(updated_player)
            
            achievement_msgs = []
            for ach_id in newly_unlocked:
                ach_reward = award_achievement(updated_player, ach_id)
                if ach_reward:
                    ach_msg = create_achievement_notification(
                        ach_reward['title'],
                        ach_reward['description'],
                        ach_reward['rewards']
                    )
                    achievement_msgs.append(ach_msg)
            
            # Victory message
            combo_indicator = create_combo_indicator(current_combo)
            loot_display = create_loot_drop(loot_drops)
            
            victory_msg = f"""
🎉 *KEMENANGAN!* 🎉

{combo_indicator}

💰 Gold: +{total_gold} (Base: {base_reward} + Combo: {combo_bonus})
⭐ EXP: +{exp_reward}

{loot_display}

{create_hp_bar(p['hp'], p['max_hp'])}
{create_mp_bar(p['mp'], p['max_mp'])}
"""
            
            if level_up_msg:
                victory_msg += "\n" + level_up_msg
            
            await state.set_state(GameState.exploring)
            await message.answer(victory_msg, reply_markup=get_main_reply_keyboard(updated_player), parse_mode="Markdown")
            
            # Send achievement notifications
            for ach_msg in achievement_msgs:
                await message.answer(ach_msg, parse_mode="Markdown")
    
    else:
        # WRONG ANSWER PATH
        damage = puzzle.get('damage', 10)
        new_hp = p['hp'] - damage
        
        # Break combo
        update_player(user_id, {'current_combo': 0})
        
        if new_hp <= 0:
            stats = {
                'cycle': p.get('cycle', 1),
                'kills': p['kills'],
                'gold_lost': p['gold']
            }
            death_screen = create_death_screen(
                f"Dikalahkan oleh {puzzle['monster_name']}",
                stats
            )
            msg_text = reset_player_death(user_id, "death_combat")
            
            await state.set_state(GameState.exploring)
            await message.answer(
                death_screen + "\n\n" + msg_text,
                reply_markup=get_main_reply_keyboard(),
                parse_mode="Markdown"
            )
        else:
            update_player(user_id, {"hp": new_hp})
            
            label = "⏰ *WAKTU HABIS!*" if is_timeout else "❌ *SALAH!*"
            
            await message.answer(
                f"{label}\n\n*{puzzle['monster_name']}* menyerang!\n\n{create_hp_bar(new_hp, p['max_hp'])}",
                reply_markup=get_main_reply_keyboard(),
                parse_mode="Markdown"
            )
            
            await state.set_state(GameState.exploring)

# === SKILL HANDLERS ===

@dp.callback_query(F.data == "skill_reveal")
async def skill_reveal_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    player = get_player(user_id)
    data = await state.get_data()
    puzzle = data.get("puzzle")
    
    if not puzzle or player['mp'] < 10:
        return await callback.answer("🔮 MP tidak cukup! (Butuh 10 MP)", show_alert=True)
    
    update_player(user_id, {"mp": player['mp'] - 10})
    
    await callback.answer(
        f"👁️ REVELATIO!\n\nJawaban: {puzzle['answer']}",
        show_alert=True
    )

@dp.callback_query(F.data == "skill_timewarp")
async def skill_timewarp_handler(callback: CallbackQuery, state: FSMContext):
    """
    Skill Time Warp: Menambah waktu 15 detik ke puzzle saat ini.
    Biaya: 20 MP.
    """
    user_id = callback.from_user.id
    player = get_player(user_id)
    data = await state.get_data()
    puzzle = data.get("puzzle")
    
    if not puzzle or player['mp'] < 20:
        return await callback.answer("🔮 MP tidak cukup! (Butuh 20 MP)", show_alert=True)
    
    update_player(user_id, {"mp": player['mp'] - 20})
    
    puzzle['timer'] += 15
    await state.update_data(puzzle=puzzle)
    
    await callback.answer(
        "⚡ TIME WARP AKTIF!\n\nWaktu diperpanjang 15 detik.",
        show_alert=True
    )

@dp.callback_query(F.data == "skill_shield")
async def skill_shield_handler(callback: CallbackQuery, state: FSMContext):
    """
    Skill Shield: Menahan 50% damage dari serangan monster berikutnya.
    Biaya: 30 MP.
    """
    user_id = callback.from_user.id
    player = get_player(user_id)
    data = await state.get_data()
    puzzle = data.get("puzzle")
    
    if not puzzle or player['mp'] < 30:
        return await callback.answer("🔮 MP tidak cukup! (Butuh 30 MP)", show_alert=True)
    
    update_player(user_id, {"mp": player['mp'] - 30})
    
    original_damage = puzzle.get('damage', 10)
    puzzle['damage'] = int(original_damage * 0.5)
    await state.update_data(puzzle=puzzle)
    
    await callback.answer(
        "🛡️ SHIELD AKTIF!\n\nDamage monster berkurang 50%.",
        show_alert=True
    )

# === INVENTORY & MENU CALLBACK HANDLERS ===

@dp.callback_query(F.data.startswith("use_item_"))
async def use_item_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    item_id = callback.data.replace("use_item_", "")
    p = get_player(user_id)
    
    inventory = p.get('inventory', [])
    
    # Cari item di dalam tas pemain
    item_index = -1
    for i, item in enumerate(inventory):
        if item.get('id') == item_id:
            item_index = i
            break
            
    if item_index == -1:
        return await callback.answer("❌ Item tidak ditemukan atau sudah habis!", show_alert=True)
        
    # Ambil dan hapus 1 item dari inventory
    used_item = inventory.pop(item_index)
    effect = used_item.get('effect', '')
    
    updates = {'inventory': inventory}
    alert_msg = f"Memakai {used_item['name']}!\n"
    
    # Proses efek ramuan
    if effect.startswith("heal_"):
        amount = int(effect.split("_")[1])
        updates['hp'] = min(p['max_hp'], p['hp'] + amount)
        alert_msg += f"❤️ +{amount} HP"
    elif effect.startswith("mp_"):
        if effect == "mp_full":
            updates['mp'] = p['max_mp']
            alert_msg += "🔮 MP Pulih Sepenuhnya!"
        else:
            amount = int(effect.split("_")[1])
            updates['mp'] = min(p['max_mp'], p['mp'] + amount)
            alert_msg += f"🔮 +{amount} MP"
    
    # Simpan status baru ke database
    update_player(user_id, updates)
    
    # Hapus pesan inventory lama agar chat tetap rapi
    await callback.message.delete()
    
    # Munculkan pop-up di layar HP dan kirim pesan konfirmasi
    await callback.answer(alert_msg, show_alert=True)
    await callback.message.answer(f"✨ Kamu menenggak *{used_item['name']}*.\n{alert_msg}", parse_mode="Markdown")

@dp.callback_query(F.data.in_(["close_inventory", "close_quests"]))
async def close_menu_handler(callback: CallbackQuery):
    """Fungsi untuk tombol 'Close' di Inventory dan Quest"""
    await callback.message.delete()
    await callback.answer()


# === BOILERPLATE ===
async def main():
    auto_seed_content()
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
