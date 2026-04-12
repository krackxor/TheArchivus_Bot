import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from engine import process_move
from database import get_player, update_player, auto_seed_content, reset_player_death
from combat import generate_battle_puzzle, validate_answer
from states import GameState
from config import BOT_TOKEN
from shop import get_shop_keyboard, process_purchase
from skills import use_skill_reveal

dp = Dispatcher()

def get_nav_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬆️ Utara", callback_data="move_utara")],
        [InlineKeyboardButton(text="⬅️ Barat", callback_data="move_barat"), InlineKeyboardButton(text="Timur ➡️", callback_data="move_timur")],
        [InlineKeyboardButton(text="⬇️ Selatan", callback_data="move_selatan")],
        [InlineKeyboardButton(text="📊 Cek Status", callback_data="check_status"), InlineKeyboardButton(text="🛒 Toko", callback_data="open_shop")]
    ])

def get_combat_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔮 Revelatio (10 MP)", callback_data="use_skill")]
    ])

@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    get_player(user_id, message.from_user.first_name)
    await state.set_state(GameState.exploring)
    
    text = (
        f"📜 **Selamat Datang di The Archivus, {message.from_user.first_name}.**\n\n"
        "Dunia ini telah kehilangan ceritanya. Kamu adalah seorang Weaver, "
        "satu-satunya yang bisa menyusun kembali realita lewat kata-kata.\n\n"
        "Pilih arah jalanmu di bawah ini untuk mulai menjelajah."
    )
    await message.answer(text, parse_mode="Markdown", reply_markup=get_nav_keyboard())

@dp.callback_query(GameState.exploring, F.data == "check_status")
async def status_handler(callback: CallbackQuery):
    p = get_player(callback.from_user.id)
    text = (
        f"📊 **Buku Catatan Weaver**\n"
        f"❤️ HP: {p['hp']}/{p['max_hp']} | 🔮 MP: {p['mp']}/{p['max_mp']}\n"
        f"💰 Gold: {p['gold']} | 💀 Kills: {p['kills']}"
    )
    await callback.message.edit_text(text, reply_markup=get_nav_keyboard())
    await callback.answer()

# --- TOKO HANDLERS ---
@dp.callback_query(GameState.exploring, F.data == "open_shop")
async def open_shop_handler(callback: CallbackQuery):
    player = get_player(callback.from_user.id)
    text = f"⚖️ **Toko Sang Pedagang Buta**\n\n💰 *Gold: {player['gold']}*\n\n\"Nyawa bisa dibeli jika kamu punya koin yang tepat...\""
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_shop_keyboard())
    await callback.answer()

@dp.callback_query(GameState.exploring, F.data == "close_shop")
async def close_shop_handler(callback: CallbackQuery):
    await callback.message.edit_text("👣 Kamu melangkah menjauh. Ke mana sekarang?", reply_markup=get_nav_keyboard())
    await callback.answer()

@dp.callback_query(GameState.exploring, F.data.startswith("buy_"))
async def buy_item_handler(callback: CallbackQuery):
    is_success, pesan = process_purchase(callback.from_user.id, callback.data)
    player = get_player(callback.from_user.id)
    text = f"{pesan}\n\n💰 *Sisa Gold: {player['gold']}*\n\n\"Ada lagi?\""
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_shop_keyboard())
    await callback.answer()

# --- SKILL HANDLER ---
@dp.callback_query(GameState.in_combat, F.data == "use_skill")
async def skill_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    puzzle = data.get("puzzle")

    success, message, new_hint = use_skill_reveal(user_id, puzzle)
    
    if not success:
        await callback.answer(message, show_alert=True)
        return

    puzzle['current_hint'] = new_hint
    await state.update_data(puzzle=puzzle)
    
    text = (
        f"⚔️ **{puzzle['monster_name']} MUNCUL!**\n"
        f"🔥 `\"{puzzle['question']}\"`\n\n"
        f"💡 Petunjuk: `{new_hint}`"
    )
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_combat_keyboard())
    await callback.answer(message)

# --- MOVE HANDLER (SUPPORT BOSS) ---
@dp.callback_query(GameState.exploring, F.data.startswith("move_"))
async def move_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    arah = callback.data.split("_")[1].capitalize()
    event_type, event_data, narration = process_move(user_id)
    
    if event_type == "monster":
        player = get_player(user_id)
        puzzle = generate_battle_puzzle(player['kills'])
        puzzle['current_hint'] = "_" * len(puzzle['answer'])
        
        await state.set_state(GameState.in_combat)
        await state.update_data(puzzle=puzzle)
        
        text = (
            f"👣 Kamu melangkah ke {arah}.\n{narration}\n\n"
            f"⚔️ **{puzzle['monster_name']} MUNCUL!**\n"
            f"Waktu: **{puzzle['timer']} detik**\n"
            f"🔥 `\"{puzzle['question']}\"`\n\n"
            f"💡 Petunjuk: `{puzzle['current_hint']}`"
        )
        msg = await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_combat_keyboard())
        
        await asyncio.sleep(puzzle['timer'])
        current_state = await state.get_state()
        
        if current_state == GameState.in_combat:
            p = get_player(user_id)
            is_boss = puzzle.get("is_boss", False)
            
            if is_boss:
                # Hukuman BOSS: HP sisa 1, Gold hilang 50%
                new_hp = 1
                new_gold = int(p['gold'] * 0.5)
                update_player(user_id, {"hp": new_hp, "gold": new_gold})
                await state.set_state(GameState.exploring)
                await msg.answer(f"💥 **THE KEEPER MENGHANCURKANMU!**\nHP tersisa 1 dan separuh Gold-mu dicuri!", reply_markup=get_nav_keyboard())
            else:
                new_hp = p['hp'] - 35
                if new_hp <= 0:
                    pesan_mati = reset_player_death(user_id, "death_combat")
                    await state.set_state(GameState.exploring)
                    await msg.answer(f"⌛ **WAKTU HABIS.**\n\n*{pesan_mati}*", reply_markup=get_nav_keyboard())
                else:
                    update_player(user_id, {"hp": new_hp})
                    await msg.answer(f"⚠️ **TERLALU LAMA!** HP -35 (Sisa: {new_hp}). Jawab!")
                
    elif event_type in ["npc_baik", "npc_jahat"]:
        text = f"👣 {narration}\n\n👤 **{event_data['identity']}**:\n*\"{event_data['dialog']}\"*"
        await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_nav_keyboard())
    else:
        await callback.message.edit_text(f"👣 {narration}", reply_markup=get_nav_keyboard())
    
    await callback.answer()

@dp.message(GameState.in_combat)
async def combat_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    puzzle = data.get("puzzle")
    is_boss = puzzle.get("is_boss", False)
    
    is_correct, is_timeout = validate_answer(message.text, puzzle['answer'], puzzle['generated_time'], puzzle['timer'])

    if is_correct:
        p = get_player(user_id)
        reward_gold = 100 if is_boss else 10
        update_player(user_id, {"kills": p['kills'] + 1, "gold": p['gold'] + reward_gold})
        await state.set_state(GameState.exploring)
        
        prefix = "🏆 **THE KEEPER TUMBANG!**" if is_boss else "✅ **BENAR!**"
        await message.answer(f"{prefix}\nKamu mendapatkan {reward_gold} Gold.", reply_markup=get_nav_keyboard())
    else:
        p = get_player(user_id)
        if is_boss:
            new_hp = 1
            new_gold = int(p['gold'] * 0.5)
            update_player(user_id, {"hp": new_hp, "gold": new_gold})
            await state.set_state(GameState.exploring)
            await message.answer(f"💥 **GAGAL MENGALAHKAN PENJAGA!**\nHP tersisa 1 dan separuh Gold-mu hilang!", reply_markup=get_nav_keyboard())
        else:
            new_hp = p['hp'] - 35
            if new_hp <= 0:
                pesan_mati = reset_player_death(user_id, "death_combat")
                await state.set_state(GameState.exploring)
                await message.answer(f"🌑 **MATI.**\n\n*{pesan_mati}*", reply_markup=get_nav_keyboard())
            else:
                update_player(user_id, {"hp": new_hp})
                label = "WAKTU HABIS!" if is_timeout else "SALAH!"
                await message.answer(f"❌ **{label}** HP -35 (Sisa: {new_hp}). Jawab lagi!")

async def main():
    auto_seed_content()
    bot = Bot(token=BOT_TOKEN)
    print("👁️ The Archivus telah bangkit. Bot sedang mendengarkan...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
