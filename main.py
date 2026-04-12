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

# --- KEYBOARDS ---

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

def get_npc_interaction_keyboard(req):
    """Membangun tombol berdasarkan permintaan acak NPC (Gold atau Item)"""
    label = f"🤝 Beri {req['amount']} {req['name']}"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=label, callback_data="npc_accept")],
        [InlineKeyboardButton(text="👣 Abaikan & Pergi", callback_data="npc_ignore")]
    ])

# --- HANDLERS ---

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
    # Tambahkan tampilan inventory jika sudah ada di database
    inv_list = ", ".join(p.get("inventory", [])) if p.get("inventory") else "Kosong"
    
    text = (
        f"📊 **Buku Catatan Weaver**\n"
        f"❤️ HP: {p['hp']}/{p['max_hp']} | 🔮 MP: {p['mp']}/{p['max_mp']}\n"
        f"💰 Gold: {p['gold']} | 💀 Kills: {p['kills']}\n"
        f"🎒 Tas: `{inv_list}`"
    )
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_nav_keyboard())
    await callback.answer()

# --- MOVE HANDLER (NPC & MONSTER) ---

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
        if await state.get_state() == GameState.in_combat:
            p = get_player(user_id)
            if puzzle.get("is_boss"):
                update_player(user_id, {"hp": 1, "gold": int(p['gold'] * 0.5)})
                await state.set_state(GameState.exploring)
                await msg.answer("💥 **THE KEEPER MENGHANCURKANMU!**\nHP sisa 1, Gold hilang 50%!", reply_markup=get_nav_keyboard())
            else:
                new_hp = p['hp'] - 35
                if new_hp <= 0:
                    pesan = reset_player_death(user_id, "death_combat")
                    await state.set_state(GameState.exploring)
                    await msg.answer(f"⌛ **WAKTU HABIS.**\n\n*{pesan}*", reply_markup=get_nav_keyboard())
                else:
                    update_player(user_id, {"hp": new_hp})
                    await msg.answer(f"⚠️ **TERLALU LAMA!** HP -35 (Sisa: {new_hp}).")
                
    elif event_type in ["npc_baik", "npc_jahat"]:
        # Simpan data NPC ke state agar bisa diakses di handler tombol
        await state.update_data(npc_data=event_data, current_npc_type=event_type)
        req = event_data['requirement']
        
        text = (
            f"👣 Kamu melangkah ke {arah}.\n{narration}\n\n"
            f"👤 **{event_data['identity']}** menghadangmu:\n"
            f"*\"{event_data['dialog']}\"*\n\n"
            f"Dia meminta: **{req['amount']} {req['name']}**"
        )
        await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_npc_interaction_keyboard(req))
    else:
        await callback.message.edit_text(f"👣 {narration}", reply_markup=get_nav_keyboard())
    
    await callback.answer()

# --- NPC INTERACTION HANDLERS ---

@dp.callback_query(F.data == "npc_accept")
async def npc_accept_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    player = get_player(user_id)
    data = await state.get_data()
    npc_data = data.get("npc_data")
    req = npc_data['requirement']
    npc_type = data.get("current_npc_type")

    # VALIDASI KEPEMILIKAN
    if req['type'] == "gold":
        if player['gold'] < req['amount']:
            await callback.answer(f"❌ Gold tidak cukup!", show_alert=True)
            return
        update_player(user_id, {"gold": player['gold'] - req['amount']})
    else:
        # Cek inventory (Item)
        inventory = player.get("inventory", [])
        if req['id'] not in inventory:
            await callback.answer(f"❌ Kamu tidak memiliki {req['name']}!", show_alert=True)
            return
        inventory.remove(req['id'])
        update_player(user_id, {"inventory": inventory})

    # LOGIKA HASIL (JUDI BUTA)
    if npc_type == "npc_baik":
        # Hadiah: Max HP +20 dan Reset HP ke penuh
        update_player(user_id, {"max_hp": player['max_hp'] + 20, "hp": player['max_hp'] + 20})
        pesan = f"😇 **KEBERUNTUNGAN!**\n\nSetelah menerima {req['name']}, sosok itu membacakan mantra kuno. Tubuhmu terasa lebih kuat dari sebelumnya! (Max HP +20)"
    else:
        pesan = f"💀 **KAMU TERTIPU!**\n\nDia mengambil {req['name']}-mu, tertawa licik, dan menghilang ke dalam bayangan. Kamu baru saja kehilangan aset berharga sia-sia."

    await callback.message.edit_text(f"{pesan}\n\nLanjutkan perjalananmu.", reply_markup=get_nav_keyboard())
    await callback.answer()

@dp.callback_query(F.data == "npc_ignore")
async def npc_ignore_handler(callback: CallbackQuery):
    await callback.message.edit_text("👣 Kamu mengabaikannya. Kehati-hatian adalah kunci bertahan hidup di Archivus.", reply_markup=get_nav_keyboard())
    await callback.answer()

# --- COMBAT HANDLER ---

@dp.message(GameState.in_combat)
async def combat_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    puzzle = data.get("puzzle")
    is_correct, is_timeout = validate_answer(message.text, puzzle['answer'], puzzle['generated_time'], puzzle['timer'])

    if is_correct:
        p = get_player(user_id)
        reward = 100 if puzzle.get("is_boss") else 10
        update_player(user_id, {"kills": p['kills'] + 1, "gold": p['gold'] + reward})
        await state.set_state(GameState.exploring)
        await message.answer(f"{'🏆' if reward > 10 else '✅'} **BENAR!** (+{reward} Gold)", reply_markup=get_nav_keyboard())
    else:
        p = get_player(user_id)
        if puzzle.get("is_boss"):
            update_player(user_id, {"hp": 1, "gold": int(p['gold'] * 0.5)})
            await state.set_state(GameState.exploring)
            await message.answer("💥 **GAGAL!** HP sisa 1 dan separuh Gold hilang!", reply_markup=get_nav_keyboard())
        else:
            new_hp = p['hp'] - 35
            if new_hp <= 0:
                pesan = reset_player_death(user_id, "death_combat")
                await state.set_state(GameState.exploring)
                await message.answer(f"🌑 **MATI.**\n\n*{pesan}*", reply_markup=get_nav_keyboard())
            else:
                update_player(user_id, {"hp": new_hp})
                label = "WAKTU HABIS!" if is_timeout else "SALAH!"
                await message.answer(f"❌ **{label}** HP -35. Jawab lagi!")

# --- BOILERPLATE ---
async def main():
    auto_seed_content()
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
