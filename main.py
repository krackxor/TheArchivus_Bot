import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from engine import process_move
from database import get_player, update_player, auto_seed_content, reset_player_death, add_history
from combat import generate_battle_puzzle, validate_answer
from states import GameState
from config import BOT_TOKEN
from shop import get_shop_keyboard, process_purchase
from skills import use_skill_reveal

dp = Dispatcher()

# --- KEYBOARDS ---

def get_main_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⬆️ Utara")],
            [KeyboardButton(text="⬅️ Barat"), KeyboardButton(text="Timur ➡️")],
            [KeyboardButton(text="⬇️ Selatan")],
            [KeyboardButton(text="📊 Status"), KeyboardButton(text="🛒 Toko")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Tentukan langkahmu, Weaver..."
    )

def get_combat_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔮 Revelatio (10 MP)", callback_data="use_skill", color="gold")]
    ])

def get_npc_interaction_keyboard(req):
    if req is None:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🧭 Ikuti Sarannya", callback_data="npc_follow", color="blue")],
            [InlineKeyboardButton(text="👣 Abaikan", callback_data="npc_ignore", color="red")]
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🤝 Beri {req['amount']} {req['name']}", callback_data="npc_accept", color="green")],
        [InlineKeyboardButton(text="👣 Abaikan", callback_data="npc_ignore", color="red")]
    ])

def get_quiz_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🏃‍♂️ Tolak Kuis")]],
        resize_keyboard=True,
        input_field_placeholder="Ketik jawabanmu atau tolak..."
    )

# --- BACKGROUND TIMERS ---

async def combat_timeout_task(message: Message, state: FSMContext, puzzle: dict, user_id: int):
    """Menangani timeout pertarungan, mendukung multi-stage (Gauntlet)"""
    await asyncio.sleep(puzzle['timer'])
    current_state = await state.get_state()
    data = await state.get_data()
    active_puzzle = data.get("puzzle", {})
    
    # Jika masih di stage puzzle yang SAMA saat waktu habis
    if current_state == GameState.in_combat and active_puzzle.get("generated_time") == puzzle["generated_time"]:
        p = get_player(user_id)
        damage = puzzle.get('damage', 10)
        new_hp = p['hp'] - damage
        
        await state.set_state(GameState.exploring)
        if new_hp <= 0:
            msg_text = reset_player_death(user_id, "death_combat")
            await message.answer(f"🌑 **MATI.**\n\n{msg_text}", reply_markup=get_main_reply_keyboard())
        else:
            update_player(user_id, {"hp": new_hp})
            await message.answer(
                f"⚠️ **WAKTU HABIS!**\n{puzzle['monster_name']} mendaratkan serangan telak: **-{damage} HP**.\n"
                f"Fokusmu hancur, pertarungan berakhir.", 
                reply_markup=get_main_reply_keyboard()
            )

# --- BASIC HANDLERS ---

@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    get_player(user_id, message.from_user.first_name)
    await state.set_state(GameState.exploring)
    await message.answer("📜 **The Archivus telah bangkit.**\nLangkahkan kakimu ke dalam sejarah tanpa akhir ini.", reply_markup=get_main_reply_keyboard())

# --- NPC LOGIC: MANUAL NAVIGATION ---

@dp.callback_query(F.data == "npc_follow")
async def npc_follow_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    npc_data = data.get("npc_data")
    if not npc_data: return
    
    dialog = npc_data['dialog']
    target_dir = "⬆️ Utara"
    if "Barat" in dialog: target_dir = "⬅️ Barat"
    elif "Timur" in dialog: target_dir = "Timur ➡️"
    elif "Selatan" in dialog: target_dir = "⬇️ Selatan"

    await state.set_state(GameState.traveling)
    await state.update_data(target_direction=target_dir, follow_step=0)

    text = (
        f"📍 **Navigasi Terkunci.**\n\n"
        f"Kamu memutuskan mengikuti petunjuk menuju **{target_dir}**.\n"
        f"Melangkahlah 5x ke arah tersebut untuk sampai."
    )
    await callback.message.edit_text(text)
    await callback.answer()

@dp.callback_query(F.data == "accept_mission")
async def accept_mission_handler(callback: CallbackQuery):
    await callback.message.edit_text("📜 **Misi Diterima.**\nLembaran sejarah Archivus mulai terbuka untukmu.")
    await callback.answer()

# --- CORE MOVE HANDLER (ENDLESS INTEGRATION) ---

@dp.message(F.text.in_(["⬆️ Utara", "⬅️ Barat", "Timur ➡️", "⬇️ Selatan"]))
async def move_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    current_state = await state.get_state()
    data = await state.get_data()

    # 1. LOGIKA MISI NAVIGASI (5 LANGKAH)
    if current_state == GameState.traveling:
        target_dir = data.get("target_direction")
        follow_step = data.get("follow_step", 0)

        if message.text != target_dir:
            await state.set_state(GameState.exploring)
            await state.update_data(target_direction=None, follow_step=0)
            update_player(user_id, {"mp": max(0, get_player(user_id)['mp'] - 10)})
            
            return await message.answer(
                "⚠️ **WEAVER KEHILANGAN BENANG.**\n"
                "Archivus tidak menoleransi keraguan. Dengan mengabaikan petunjuk, "
                "benang takdir yang baru saja terajut langsung terputus. MP -10",
                reply_markup=get_main_reply_keyboard()
            )

        follow_step += 1
        if follow_step < 5:
            await state.update_data(follow_step=follow_step)
            return await message.answer(f"Melangkah ke {target_dir}... ({follow_step}/5)\n{'👣' * follow_step}")
        else:
            await state.set_state(GameState.exploring)
            await state.update_data(target_direction=None, follow_step=0)
            npc_data = data.get("npc_data")

            if npc_data['is_liar']:
                p = get_player(user_id)
                tier_level = min(5, max(1, (p['kills'] // 5) + 1))
                puzzle = generate_battle_puzzle(tier_level, is_boss=False) 
                
                await state.set_state(GameState.in_combat)
                await state.update_data(puzzle=puzzle, current_stage=1, target_stages=1)
                
                res = (
                    "💀 **DIKHIANATI!**\n"
                    "Saran itu jebakan! Kamu sampai di ujung jalan yang buntu dan monster telah menunggumu.\n\n"
                    f"⚔️ **{puzzle['monster_name']}** (TIER {puzzle['tier']})\n"
                    f"🧩 `\"{puzzle['question']}\"`"
                )
                msg = await message.answer(res, reply_markup=get_combat_keyboard())
                asyncio.create_task(combat_timeout_task(msg, state, puzzle, user_id))
                return
            else:
                update_player(user_id, {"mp": min(get_player(user_id)['max_mp'], get_player(user_id)['mp'] + 20)})
                return await message.answer(
                    "😇 **TUJUAN TERCAPAI.**\nSaran itu benar. Kamu menemukan area yang lebih stabil. MP +20",
                    reply_markup=get_main_reply_keyboard()
                )

    # 2. LOGIKA JALAN NORMAL (GameState.exploring)
    if current_state == GameState.exploring:
        event_type, event_data, narration = process_move(user_id)
        
        if event_type == "npc_mission":
            text = f"📜 **{event_data['identity']}**\n*\"{event_data['dialog']}\"*"
            btn = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📜 Terima Misi", callback_data="accept_mission")]])
            return await message.answer(text, reply_markup=btn)

        elif event_type == "npc_quiz":
            await state.set_state(GameState.in_quiz)
            await state.update_data(quiz_data=event_data)
            text = f"❓ **{event_data['identity']}**\n*\"{event_data['dialog']}\"*"
            return await message.answer(text, parse_mode="Markdown", reply_markup=get_quiz_keyboard())

        elif event_type in ["boss", "mini_boss", "monster"]:
            p = get_player(user_id)
            is_boss = (event_type == "boss")
            target_stages = 5 if is_boss else (3 if event_type == "mini_boss" else 1)
            tier_level = min(5, max(1, (p['kills'] // 5) + 1))
            
            puzzle = generate_battle_puzzle(tier_level, is_boss)
            await state.set_state(GameState.in_combat)
            await state.update_data(puzzle=puzzle, current_stage=1, target_stages=target_stages)
            
            label = "⚠️ BOSS" if is_boss else ("🔥 MINI BOSS" if event_type == "mini_boss" else f"TIER {puzzle['tier']}")
            text = (
                f"{narration}\n\n"
                f"⚔️ **{puzzle['monster_name']}** ({label})\n"
                f"Tahap: 1/{target_stages} | ⏱ 60 detik\n\n"
                f"🧩 `\"{puzzle['question']}\"`"
            )
            msg = await message.answer(text, parse_mode="Markdown", reply_markup=get_combat_keyboard())
            asyncio.create_task(combat_timeout_task(msg, state, puzzle, user_id))
                
        elif event_type in ["npc_baik", "npc_jahat"]:
            await state.update_data(npc_data=event_data, current_npc_type=event_type)
            req = event_data['requirement']
            detail_req = "Dia menawarkan petunjuk jalan." if req is None else f"Dia meminta: **{req['amount']} {req['name']}**"
            text = (f"👤 **{event_data['identity']}**\n*\"{event_data['dialog']}\"*\n\n💎 {detail_req}")
            await message.answer(text, reply_markup=get_npc_interaction_keyboard(req))
            
        else:
            await message.answer(f"{narration}", reply_markup=get_main_reply_keyboard())

# --- COMBAT HANDLER (GAUNTLET SUPPORT) ---

@dp.message(GameState.in_combat)
async def combat_answer_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    puzzle = data.get("puzzle")
    if not puzzle: return

    is_correct, is_timeout = validate_answer(message.text, puzzle['answer'], puzzle['generated_time'], puzzle['timer'])
    p = get_player(user_id)

    if is_correct:
        current_stage = data.get("current_stage", 1)
        target_stages = data.get("target_stages", 1)
        
        if current_stage < target_stages:
            # Lanjut ke puzzle berikutnya (Gauntlet Mode)
            tier_level = min(5, max(1, (p['kills'] // 5) + 1))
            new_puzzle = generate_battle_puzzle(tier_level, puzzle['is_boss'])
            await state.update_data(puzzle=new_puzzle, current_stage=current_stage + 1)
            
            text = f"✅ **BENAR! Lanjut Tahap {current_stage + 1}/{target_stages}**\n\n🧩 `\"{new_puzzle['question']}\"`"
            msg = await message.answer(text, reply_markup=get_combat_keyboard())
            asyncio.create_task(combat_timeout_task(msg, state, new_puzzle, user_id))
        else:
            # Kemenangan Penuh
            reward = 500 if puzzle['is_boss'] else (100 if target_stages == 3 else 25)
            # Reset kill untuk loop jika Boss mati
            new_kills = 0 if puzzle['is_boss'] else p['kills'] + 1
            new_cycle = p['cycle'] + 1 if puzzle['is_boss'] else p['cycle']
            
            updates = {"kills": new_kills, "gold": p['gold'] + reward, "cycle": new_cycle}
            if puzzle['is_boss']:
                updates["miniboss_slain"] = False
                add_history(user_id, f"Menghancurkan Sang Penjaga. Memasuki Siklus {new_cycle}.")
            elif target_stages == 3:
                add_history(user_id, "Mengalahkan Letnan Kegelapan (Mini Boss).")
                
            update_player(user_id, updates)
            await state.set_state(GameState.exploring)
            await message.answer(f"🎉 **KEMENANGAN!** (+{reward} Gold)\nAncaman berhasil dilenyapkan.", reply_markup=get_main_reply_keyboard())
    else:
        damage = puzzle.get('damage', 5)
        new_hp = p['hp'] - damage
        if new_hp <= 0:
            msg_text = reset_player_death(user_id, "death_combat")
            await state.set_state(GameState.exploring)
            await message.answer(f"🌑 **MATI.**\n\n{msg_text}", reply_markup=get_main_reply_keyboard())
        else:
            update_player(user_id, {"hp": new_hp})
            label = "WAKTU HABIS!" if is_timeout else "SALAH!"
            await message.answer(f"❌ **{label}** HP -{damage}. Konsentrasimu terganggu!", reply_markup=get_main_reply_keyboard())
            await state.set_state(GameState.exploring)

# --- QUIZ HANDLER ---

@dp.message(GameState.in_quiz)
async def quiz_answer_handler(message: Message, state: FSMContext):
    if message.text == "🏃‍♂️ Tolak Kuis":
        await state.set_state(GameState.exploring)
        return await message.answer("Kamu mengabaikan tantangan The Memory Thief.", reply_markup=get_main_reply_keyboard())

    data = await state.get_data()
    quiz_data = data.get('quiz_data', {})
    correct_answer = quiz_data.get('requirement', {}).get('answer', '')
    p = get_player(message.from_user.id)

    if message.text.strip().lower() == correct_answer.lower():
        update_player(p['user_id'], {"mp": min(p['max_mp'], p['mp'] + 25), "gold": p['gold'] + 50})
        await message.answer("✅ **BENAR!** Ingatanmu tajam. (MP +25, Gold +50)", reply_markup=get_main_reply_keyboard())
    else:
        update_player(p['user_id'], {"mp": max(0, p['mp'] - 20)})
        await message.answer(f"❌ **SALAH!** Sejarah mencatat: {correct_answer}. (MP -20)", reply_markup=get_main_reply_keyboard())

    await state.set_state(GameState.exploring)

# --- TRANSACTION HANDLERS ---

@dp.callback_query(F.data == "npc_accept")
async def npc_accept_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    player = get_player(user_id)
    data = await state.get_data()
    npc_data = data.get("npc_data")
    if not npc_data: return

    req = npc_data['requirement']
    if req['type'] == "gold" and player['gold'] < req['amount']:
        return await callback.answer("❌ Gold tidak cukup!", show_alert=True)
    
    update_player(user_id, {"gold": player['gold'] - req['amount'] if req['type'] == "gold" else player['gold']})
    msg = "✅ **BERKAH.** Tubuhmu menguat!" if data.get("current_npc_type") == "npc_baik" else "❌ **DIRAMPOK!** Barangmu dibawa kabur."
    await callback.message.edit_text(msg)
    await callback.message.answer("Perjalanan berlanjut...", reply_markup=get_main_reply_keyboard())

@dp.callback_query(F.data == "npc_ignore")
async def npc_ignore_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GameState.exploring)
    await callback.message.edit_text("👣 Kamu mengabaikannya dan melangkah pergi.")
    await callback.message.answer("Perjalanan berlanjut...", reply_markup=get_main_reply_keyboard())

# --- STATUS & SHOP ---

@dp.message(GameState.exploring, F.text == "📊 Status")
async def status_handler(message: Message):
    p = get_player(message.from_user.id)
    text = (
        f"📊 **Status Weaver** | 🔄 Siklus: {p.get('cycle', 1)}\n"
        f
