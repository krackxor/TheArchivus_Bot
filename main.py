import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

# === ROOT IMPORTS ===
from database import get_player, update_player, auto_seed_content, reset_player_death, add_history, tick_buffs
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
    create_death_screen, create_location_transition
)

dp = Dispatcher()

# === HELPER DURABILITY ===
def reduce_equipment_durability(user_id, damage_type):
    """Mengurangi durability barang. damage_type: 'weapon' atau 'armor'"""
    p = get_player(user_id)
    inventory = p.get('inventory', [])
    broken_items = []
    
    for item in inventory:
        if item.get('type') in ['weapon', 'shield', 'chest', 'head', 'gloves', 'boots']:
            if item.get('durability', 0) > 0:
                # Jika menyerang, senjata yang tumpul
                if damage_type == 'weapon' and item['type'] == 'weapon':
                    item['durability'] -= 1
                    if item['durability'] == 0:
                        broken_items.append(item['name'])
                
                # Jika diserang, semua armor & tameng retak
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

def get_enhanced_combat_keyboard(player, player_stats):
    """Combat keyboard Super Dinamis + QUICK ITEM!"""
    buttons = []
    player_mp = player.get('mp', 0)
    inventory = player.get('inventory', [])
    
    # 1. QUICK ITEM (Cek apakah punya Potion/Resin/Repair Kit di tas)
    hp_potion = next((item for item in inventory if item.get('effect', '').startswith('heal_')), None)
    mp_potion = next((item for item in inventory if item.get('effect', '').startswith('mp_')), None)
    resin = next((item for item in inventory if item.get('effect', '').startswith('resin_')), None)
    
    item_row = []
    if hp_potion: item_row.append(InlineKeyboardButton(text=f"🧪 {hp_potion['name']}", callback_data=f"combat_item_{hp_potion['id']}"))
    if mp_potion: item_row.append(InlineKeyboardButton(text=f"🔮 {mp_potion['name']}", callback_data=f"combat_item_{mp_potion['id']}"))
    if resin and len(item_row) < 2: item_row.append(InlineKeyboardButton(text=f"📜 Mantra", callback_data=f"combat_item_{resin['id']}"))
    if item_row: buttons.append(item_row)

    # 2. LOGIKA SKILL WEAPON (Dari equipment.py)
    weapon = next((i for i in inventory if i.get('type') == 'weapon' and i.get('durability', 0) > 0), None)
    if weapon and weapon.get('skill'):
        sk = weapon['skill']
        if player_mp >= sk['cost']:
            buttons.append([InlineKeyboardButton(text=f"⚔️ {sk['name']} ({sk['cost']} MP)", callback_data=f"skill_act_{sk['id']}")])

    # 3. LOGIKA TAMENG VS DODGE
    stance_row = []
    if player_stats.get("has_shield", False):
        # Jika pakai shield, cek skill shield-nya
        shield = next((i for i in inventory if i.get('type') == 'shield' and i.get('durability', 0) > 0), None)
        if shield and shield.get('skill'):
            sk = shield['skill']
            if player_mp >= sk['cost']:
                stance_row.append(InlineKeyboardButton(text=f"🛡️ {sk['name']} ({sk['cost']} MP)", callback_data=f"skill_act_{sk['id']}"))
        else:
            if player_mp >= 25: stance_row.append(InlineKeyboardButton(text="🛡️ Block (25 MP)", callback_data="skill_act_block_default"))
    else:
        if player_mp >= 15:
            dodge_ch = int(calculate_dodge_chance(player_stats) * 100)
            stance_row.append(InlineKeyboardButton(text=f"💨 Dodge ({dodge_ch}%) - 15 MP", callback_data="skill_act_dodge_default"))
    
    if stance_row: buttons.append(stance_row)

    # 4. SKILL UMUM
    util_row = [InlineKeyboardButton(text="👁️ Revelatio (10 MP)", callback_data="skill_reveal")]
    if player_mp >= 20: util_row.append(InlineKeyboardButton(text="⏳ Time Warp (20 MP)", callback_data="skill_timewarp"))
    buttons.append(util_row)
    
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
    warning_times = [30, 15, 5]
    for warning in warning_times:
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
        dmg_msg = ""
        
        # Logika gagal karena Timeout
        if action == "item":
            dmg_msg = f"\n❌ Ramuanmu pecah terjatuh karena kamu terlalu lambat! (-{final_dmg} HP)"
        elif action == "skill":
            dmg_msg = f"\n❌ Konsentrasimu buyar! Kamu terkena serangan saat merapal skill. (-{final_dmg} HP)"
        elif action == "dodge":
            dmg_msg = f"\n❌ Dodge Gagal! Kamu terlambat menghindar. (-{final_dmg} HP)"
        elif action == "block":
            final_dmg = int(raw_dmg * 0.2)
            dmg_msg = f"\n🛡️ Kamu menahan serangan dengan Tameng, namun telat merespons! (Menerima {final_dmg} DMG)"
        else:
            dmg_msg = f"\n❌ Kamu terlambat menyerang! (-{final_dmg} HP)"
            
        new_hp = p['hp'] - final_dmg
        await state.set_state(GameState.exploring)
        
        if new_hp <= 0:
            stats = {'cycle': p.get('cycle', 1), 'kills': p['kills'], 'gold_lost': p['gold']}
            death_msg = create_death_screen("Waktu habis di pertarungan", stats)
            msg_text = reset_player_death(user_id, "death_combat")
            await message.answer(death_msg + "\n\n" + msg_text, reply_markup=get_main_reply_keyboard(), parse_mode="Markdown")
        else:
            update_player(user_id, {"hp": new_hp, "current_combo": 0})
            
            # Kurangi Durability (Diserang)
            broken = reduce_equipment_durability(user_id, 'armor')
            broken_txt = f"\n🛡️ *CRACK!* Armormu hancur: {', '.join(broken)}!" if broken else ""
            
            await message.answer(
                f"⏰ *WAKTU HABIS!*\n*{puzzle['monster_name']}* menyerangmu!{dmg_msg}{broken_txt}\n{create_hp_bar(new_hp, p['max_hp'])}", 
                reply_markup=get_main_reply_keyboard(), parse_mode="Markdown"
            )

# === COMMAND HANDLERS ===
@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.first_name
    player = get_player(user_id, username)
    await state.set_state(GameState.exploring)
    
    welcome_msg = f"━━━━━━━━━━━━━━━━━━━━\n📜 *THE ARCHIVUS* 📜\n━━━━━━━━━━━━━━━━━━━━\nSelamat datang, {username}\n \nKau telah memasuki dimensi\ntanpa ujung ini sebagai\n*Weaver* - penenun takdir.\n \nBertahanlah, pecahkan\nmisteri, dan catatkan\nnamamu dalam sejarah...\n━━━━━━━━━━━━━━━━━━━━\nCycle: {player.get('cycle', 1)} | Level: {player.get('level', 1)}\n{create_hp_bar(player['hp'], player['max_hp'])}\n{create_mp_bar(player['mp'], player['max_mp'])}\n🔮 Ketik /help untuk panduan"
    await message.answer(welcome_msg, reply_markup=get_main_reply_keyboard(player), parse_mode="Markdown")

@dp.message(F.text == "/help")
async def help_handler(message: Message):
    help_text = "📖 *PANDUAN THE ARCHIVUS*\n\n🎮 *Cara Bermain:*\n• Gunakan tombol arah untuk menjelajah\n• Jawab teka-teki kilat (< 10 detik) untuk CRITICAL HIT!\n• Gunakan Shield/Dodge dengan bijak."
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
    if current_state != GameState.exploring:
        return await message.answer("Kamu sedang tidak bisa bergerak saat ini.")
    
    # Proses Buff & Durasi Mantra
    tick_buffs(user_id) 
    
    player = get_player(user_id)
    event_type, event_data, narration = process_move(user_id)
    
    if event_type == "boss" or event_type == "monster":
        p = get_player(user_id)
        p_stats = calculate_equipment_stats(p)
        
        tier_level = 5 if event_type == "boss" else min(5, max(1, (p['kills'] // 5) + 1))
        puzzle = generate_battle_puzzle(p, tier_level, is_boss=(event_type == "boss"))
        
        # Inisialisasi Combat State (Default = Attack)
        await state.set_state(GameState.in_combat)
        await state.update_data(
            puzzle=puzzle, 
            current_stage=1, 
            target_stages=5 if event_type == "boss" else 1,
            combat_start_hp=p['hp'], 
            current_combo=player.get('current_combo', 0),
            action_type="attack",
            pending_item=None,
            active_skill_id=None
        )
        
        combat_header = create_combat_header(puzzle['monster_name'], "BOSS" if event_type == "boss" else tier_level, 1, 5 if event_type == "boss" else 1)
        combo_text = create_combo_indicator(player.get('current_combo', 0))
        
        # Info Element Monster
        elem_txt = f"\nElemen Monster: *{puzzle['monster_element']}*"
        
        combat_msg = f"{narration}\n\n{combat_header}\n{combo_text}{elem_txt}\n🧩 *PUZZLE:*\n`{puzzle['question']}`\n\n{create_hp_bar(p['hp'], p['max_hp'])}\n{create_mp_bar(p['mp'], p['max_mp'])}"
        
        msg = await message.answer(
            combat_msg, 
            parse_mode="Markdown",
            reply_markup=get_enhanced_combat_keyboard(p, p_stats)
        )
        asyncio.create_task(combat_timeout_task(msg, state, puzzle, user_id))
    else:
        await message.answer(narration, reply_markup=get_main_reply_keyboard(player), parse_mode="Markdown")

# === COMBAT LOGIC (UPDATE ACTION TURN & DURABILITY) ===
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
    
    result_msg = ""
    dmg_msg = ""
    broken_txt = ""
    
    current_combo = data.get("current_combo", 0)
    
    if is_correct:
        # --- LOGIKA JAWABAN BENAR (AKSI BERHASIL) ---
        is_critical = time_taken < 10.0
        crit_msg = "\n💥 *CRITICAL HIT!*" if is_critical else ""
        
        if action == "attack":
            current_combo += 1
            # Kurangi Durability Senjata
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
                    updates['resin_duration'] = 3 # Tahan 3 turn
                    result_msg = f"📜 Kamu mengoleskan Mantra {elemen}! Senjatamu kini memancarkan sihir selama 3 turn."
                elif effect == "repair_all":
                    for equip in updates['inventory']:
                        if equip.get('type') in ['weapon', 'shield', 'chest', 'head', 'gloves', 'boots']:
                            equip['durability'] = equip.get('max_durability', 50)
                    result_msg = "⚒️ Semua equip-mu kembali mulus 100%!"
                    
                update_player(user_id, updates)
                p = get_player(user_id) # Refresh
            else:
                result_msg = "❌ Gagal menggunakan item (Tidak ditemukan)."

        elif action == "dodge":
            current_combo += 1 # Bonus Perfect Dodge
            result_msg = f"💨 *PERFECT DODGE!* Kamu menghindar dan membalas serangan! (+1 Combo)"
            
        elif action == "block":
            result_msg = f"🛡️ Kamu menangkis, lalu mendorong musuh mundur!"
            
        elif action == "skill":
            skill_id = data.get("active_skill_id")
            # --- CONTOH IMPLEMENTASI EFEK SKILL (Bisa ditambah nanti) ---
            if skill_id == "skl_iaido":
                result_msg = f"🗡️ *IAIDO STRIKE!* Serangan kilat membelah udara!"
            elif skill_id == "skl_pointblank":
                result_msg = f"💥 *POINT BLANK!* Ledakan shotgun membuat musuh terpental!"
            else:
                result_msg = f"🔥 *SKILL ACTIVATED!* Serangan sihirmu sukses!"
                
            broken = reduce_equipment_durability(user_id, 'weapon')
            if broken: result_msg += f"\n⚠️ Senjatamu hancur: {', '.join(broken)}!"

        # Update Combo Status
        update_player(user_id, {'current_combo': current_combo, 'max_combo_reached': max(p.get('max_combo_reached', 0), current_combo)})
        
        # Transisi Next Stage / Menang (Khusus jika aksinya bukan sekadar block/item)
        # Jika player asyik heal, musuh nggak mati-mati. Jadi kalau pakai item, monster tidak mati di turn itu.
        if action in ["attack", "skill", "dodge"]:
            current_stage = data.get("current_stage", 1)
            target_stages = data.get("target_stages", 1)
            
            if current_stage < target_stages:
                tier_level = min(5, max(1, (p['kills'] // 5) + 1))
                new_puzzle = generate_battle_puzzle(p, tier_level, puzzle['is_boss'])
                await state.update_data(puzzle=new_puzzle, current_stage=current_stage + 1, current_combo=current_combo, action_type="attack")
                
                combo_ind = create_combo_indicator(current_combo)
                next_msg = f"✅ *BENAR!*\n{result_msg}\n{combo_ind}\n\n{create_combat_header(new_puzzle['monster_name'], puzzle.get('tier', 1), current_stage + 1, target_stages)}\n🧩 `{new_puzzle['question']}`\n{create_hp_bar(p['hp'], p['max_hp'])}"
                msg = await message.answer(next_msg, parse_mode="Markdown", reply_markup=get_enhanced_combat_keyboard(p, p_stats))
                asyncio.create_task(combat_timeout_task(msg, state, new_puzzle, user_id))
            else:
                # WIN STATE
                tier = puzzle.get('tier', 1)
                base_reward = 500 if puzzle.get('is_boss') else (tier * 25)
                total_gold = base_reward + int(base_reward * (current_combo * 0.1))
                
                new_cycle = p['cycle'] + 1 if puzzle.get('is_boss') else p['cycle']
                update_player(user_id, {'kills': p['kills']+1, 'gold': p['gold']+total_gold, 'current_combo': current_combo, 'cycle': new_cycle})
                
                await state.set_state(GameState.exploring)
                await message.answer(f"🎉 *KEMENANGAN!*\n{result_msg}\n\n💰 Gold: +{total_gold}", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
        else:
            # Jika player cuma Heal/Block, kirim soal baru dari monster yang sama (Lanjut ronde)
            new_puzzle = generate_battle_puzzle(p, puzzle.get('tier', 1), puzzle['is_boss'])
            await state.update_data(puzzle=new_puzzle, action_type="attack")
            
            next_msg = f"✅ *AMAN!*\n{result_msg}\n\nNamun *{puzzle['monster_name']}* masih menyerang!\n🧩 `{new_puzzle['question']}`\n{create_hp_bar(p['hp'], p['max_hp'])}"
            msg = await message.answer(next_msg, parse_mode="Markdown", reply_markup=get_enhanced_combat_keyboard(p, p_stats))
            asyncio.create_task(combat_timeout_task(msg, state, new_puzzle, user_id))

    else:
        # --- LOGIKA JAWABAN SALAH (AKSI GAGAL & KENA SERANG) ---
        raw_damage = puzzle.get('damage', 10)
        final_damage = raw_damage
        
        if action == "block":
            final_damage = int(raw_damage * 0.2)
            dmg_msg = f"🛡️ Kamu menahan serangan dengan Tameng, namun posisimu goyah! (Menerima {final_damage} DMG)"
        elif action == "dodge":
            chance = calculate_dodge_chance(p_stats)
            if random.random() < chance:
                final_damage = 0
                dmg_msg = "💨 Kamu panik tapi berhasil menghindar berkat kecepatanmu! (Menerima 0 DMG)"
            else:
                dmg_msg = f"❌ Dodge Gagal! Kamu terkena serangan telak. (Menerima {final_damage} DMG)"
        elif action == "item":
            # Item hilang karena diganggu musuh
            item_id = data.get("pending_item")
            inventory = p.get('inventory', [])
            inventory = [i for i in inventory if i.get('id') != item_id]
            update_player(user_id, {'inventory': inventory})
            dmg_msg = f"❌ Gagal! Itemmu jatuh saat monster menyerang! (Menerima {final_damage} DMG)"
        elif action == "skill":
            dmg_msg = f"❌ Skill Gagal! Kamu kehilangan fokus dan terkena serangan. (Menerima {final_damage} DMG)"
        else:
            dmg_msg = f"❌ Kamu terlambat menangkis! (Menerima {final_damage} DMG)"
            
        new_hp = p['hp'] - final_damage
        update_player(user_id, {'current_combo': 0, 'hp': new_hp})
        
        # Kurangi Durability Armor (Karena diserang)
        if final_damage > 0:
            broken = reduce_equipment_durability(user_id, 'armor')
            if broken: dmg_msg += f"\n🛡️ *CRACK!* Armormu hancur: {', '.join(broken)}!"
        
        if new_hp <= 0:
            msg_text = reset_player_death(user_id, "death_combat")
            await state.set_state(GameState.exploring)
            await message.answer(f"💀 Dikalahkan oleh {puzzle['monster_name']}\n\n{msg_text}", reply_markup=get_main_reply_keyboard(), parse_mode="Markdown")
        else:
            await state.set_state(GameState.exploring)
            await message.answer(f"❌ *SALAH!*\n{dmg_msg}\n\n{create_hp_bar(new_hp, p['max_hp'])}", reply_markup=get_main_reply_keyboard(), parse_mode="Markdown")

# === STANCE & SKILL HANDLERS (ACTION TURN) ===
@dp.callback_query(GameState.in_combat, F.data.startswith("combat_item_"))
async def combat_item_stance_handler(callback: CallbackQuery, state: FSMContext):
    item_id = callback.data.replace("combat_item_", "")
    await state.update_data(action_type="item", pending_item=item_id)
    await callback.answer("🧪 Rencana: Gunakan Item.\nSelesaikan puzzle untuk meminumnya dengan aman!", show_alert=True)

@dp.callback_query(GameState.in_combat, F.data.startswith("skill_act_"))
async def combat_skill_stance_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    p = get_player(user_id)
    skill_id = callback.data.replace("skill_act_", "")
    
    # Deteksi Dodge / Block default
    if skill_id == "dodge_default":
        if p['mp'] < 15: return await callback.answer("🔮 MP tidak cukup! (Butuh 15)", show_alert=True)
        update_player(user_id, {"mp": p['mp'] - 15})
        await state.update_data(action_type="dodge")
        return await callback.answer("💨 Rencana: Dodge.\nJawab puzzle untuk Perfect Dodge!", show_alert=True)
        
    if skill_id == "block_default":
        if p['mp'] < 25: return await callback.answer("🔮 MP tidak cukup! (Butuh 25)", show_alert=True)
        update_player(user_id, {"mp": p['mp'] - 25})
        await state.update_data(action_type="block")
        return await callback.answer("🛡️ Rencana: Block.\nMenahan 80% damage di turn ini.", show_alert=True)

    # Cari data skill dari inventory
    skill_cost = 20 # Default fallback
    for item in p.get('inventory', []):
        if item.get('skill', {}).get('id') == skill_id:
            skill_cost = item['skill']['cost']
            break
            
    if p['mp'] < skill_cost: return await callback.answer(f"🔮 MP tidak cukup! (Butuh {skill_cost})", show_alert=True)
    update_player(user_id, {"mp": p['mp'] - skill_cost})
    
    await state.update_data(action_type="skill", active_skill_id=skill_id)
    await callback.answer(f"⚔️ Rencana: Gunakan Skill!\nSelesaikan puzzle untuk merapal!", show_alert=True)

@dp.callback_query(GameState.in_combat, F.data == "skill_reveal")
async def skill_reveal_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    player = get_player(user_id)
    data = await state.get_data()
    puzzle = data.get("puzzle")
    
    if not puzzle or player['mp'] < 10:
        return await callback.answer("🔮 MP tidak cukup! (Butuh 10 MP)", show_alert=True)
    
    update_player(user_id, {"mp": player['mp'] - 10})
    await callback.answer(f"👁️ REVELATIO!\n\nJawaban: {puzzle['answer']}", show_alert=True)

@dp.callback_query(GameState.in_combat, F.data == "skill_timewarp")
async def skill_timewarp_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    player = get_player(user_id)
    data = await state.get_data()
    puzzle = data.get("puzzle")
    
    if not puzzle or player['mp'] < 20:
        return await callback.answer("🔮 MP tidak cukup! (Butuh 20 MP)", show_alert=True)
    
    update_player(user_id, {"mp": player['mp'] - 20})
    puzzle['timer'] += 15
    await state.update_data(puzzle=puzzle)
    await callback.answer("⏳ TIME WARP AKTIF!\n\nWaktu diperpanjang 15 detik.", show_alert=True)


# === INVENTORY OUT OF COMBAT ===
@dp.callback_query(F.data.startswith("use_item_"))
async def use_item_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    item_id = callback.data.replace("use_item_", "")
    p = get_player(user_id)
    
    inventory = p.get('inventory', [])
    
    item_index = -1
    for i, item in enumerate(inventory):
        if item.get('id') == item_id:
            item_index = i
            break
            
    if item_index == -1:
        return await callback.answer("❌ Item tidak ditemukan atau sudah habis!", show_alert=True)
        
    used_item = inventory.pop(item_index)
    effect = used_item.get('effect', '')
    
    updates = {'inventory': inventory}
    alert_msg = f"Memakai {used_item['name']}!\n"
    
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
    elif effect.startswith("resin_"):
        elemen = effect.split("_")[1]
        updates['active_resin'] = elemen
        updates['resin_duration'] = 3
        alert_msg += f"📜 Senjatamu dialiri sihir {elemen} selama 3 pertarungan!"
    elif effect == "repair_all":
        for equip in updates['inventory']:
            if equip.get('type') in ['weapon', 'shield', 'chest', 'head', 'gloves', 'boots']:
                equip['durability'] = equip.get('max_durability', 50)
        alert_msg += "⚒️ Semua senjatamu kembali tajam dan armormu utuh!"
    
    update_player(user_id, updates)
    
    await callback.message.delete()
    await callback.answer(alert_msg, show_alert=True)
    await callback.message.answer(f"✨ Kamu menggunakan *{used_item['name']}*.\n{alert_msg}", parse_mode="Markdown")


@dp.callback_query(F.data.in_(["close_inventory", "close_quests"]))
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
