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
from game.logic.event_handler import get_event_interaction_kb, handle_event_interaction

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
@dp.callback_query(F.data.in_(["close_popup", "ignore_cooldown"]))
async def popup_handler(callback: CallbackQuery, state: FSMContext):
    if callback.data == "ignore_cooldown":
        return await callback.answer("⏳ Skill ini belum siap digunakan!", show_alert=True)
    try: 
        await callback.message.delete()
    except: 
        pass

# === BLACKSMITH CALLBACK ===
@dp.callback_query(F.data == "menu_repair")
async def blacksmith_callback_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    p = get_player(user_id)
    
    # 1. Hitung biaya dan jumlah perbaikan
    new_durability, cost, count = process_repair_all(p)
    
    # 2. Validasi: Jika tidak ada barang yang perlu diperbaiki
    if count == 0: 
        return await callback.answer("⚒️ Aethelred: 'Gear-mu masih tajam dan kokoh. Pergi sana, jangan buang waktuku!'", show_alert=True)
    
    # 3. Validasi: Cek Emas
    if p.get('gold', 0) < cost: 
        return await callback.answer(f"❌ Emasmu tidak cukup! Aethelred butuh {cost} Gold untuk jasa reparasi ini.", show_alert=True)
        
    # 4. Eksekusi Perbaikan di Database
    # Penting: Setelah durabilitas diperbaiki, kita harus menghitung ulang total stats 
    # karena gear yang rusak memberikan penalti stat besar.
    p['equipment_durability'] = new_durability
    new_stats = calculate_total_stats(p)
    
    update_player(user_id, {
        "gold": p['gold'] - cost, 
        "equipment_durability": new_durability,
        "stats": new_stats
    })
    
    # 5. Visual Feedback (UI)
    repair_msg = (
        f"⚒️ **BENGKEL AETHELRED**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💬 *'Nah, sekarang benda ini bisa membelah kulit iblis lagi. Jaga baik-baik, Weaver.'*\n\n"
        f"🛠️ **Item Diperbaiki:** {count} buah\n"
        f"💰 **Biaya Jasa:** -{cost} Gold\n"
        f"✨ **Kondisi:** 100% (Semua Gear Kokoh)\n"
        f"📊 **Status:** Kekuatan tempurmu telah pulih!"
    )
    
    # Gunakan Keyboard Profile kembali agar pemain bisa langsung melihat stats yang pulih
    from game.logic.menu_handler import get_profile_main_menu
    p['gold'] -= cost # Update local variable untuk UI
    kb = get_profile_main_menu(p)
    
    try:
        await callback.message.edit_text(repair_msg, reply_markup=InlineKeyboardMarkup(inline_keyboard=kb), parse_mode="Markdown")
    except:
        await callback.message.answer(repair_msg, reply_markup=InlineKeyboardMarkup(inline_keyboard=kb), parse_mode="Markdown")
        
    await callback.answer("✅ Seluruh peralatan berhasil diperbaiki!")


# === SHOP PURCHASE CALLBACK ===
@dp.callback_query(F.data.startswith("buy_"))
async def shop_purchase_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    item_id = callback.data.replace("buy_", "")
    p = get_player(user_id)
    
    # 1. Proses pembelian (mengurangi gold & menambah inventory di variabel 'p')
    success, msg = process_purchase(p, item_id)
    
    if success:
        # 2. [QUEST UPDATE] Tambah progres quest belanja
        # Fungsi ini akan menambah angka 'current' dan memberikan gold/exp jika selesai
        quest_notif = update_quest_progress(p, "buy_items", 1)
        
        # 3. Update database dengan data terbaru dari variabel 'p'
        # Pastikan 'daily_quests' ikut dikirim agar progres tersimpan di MongoDB
        update_player(user_id, {
            "gold": p.get('gold'), 
            "inventory": p.get('inventory'),
            "daily_quests": p.get('daily_quests', [])
        })
        
        # 4. Notifikasi sukses
        # Jika quest selesai, tampilkan dalam alert agar lebih mencolok
        alert_mode = True if quest_notif else False
        success_msg = f"✅ Berhasil membeli {item_id.replace('_', ' ').title()}!{quest_notif}"
        
        await callback.answer(success_msg, show_alert=alert_mode)
        
        # 5. Refresh tampilan toko agar sisa Gold dan status tombol (💰/❌) terupdate
        try:
            # Menggunakan p terbaru yang sudah dipotong Gold-nya
            await callback.message.edit_reply_markup(
                reply_markup=get_shop_keyboard(p, location=p.get('location', 'The Whispering Hall'))
            )
        except Exception:
            # Abaikan jika tidak ada perubahan markup (Telegram Error)
            pass
    else:
        # Tampilkan alasan gagal (misal: emas tidak cukup)
        await callback.answer(msg, show_alert=True)
        

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


# === HELPER: QUEST PROGRESS TRACKER ===
def update_quest_progress(player: dict, goal_type: str, amount: int = 1) -> str:
    """
    Mengupdate progress quest harian pemain.
    Returns: Pesan notifikasi jika ada quest yang selesai.
    """
    player_quests = player.get('daily_quests', [])
    notif_msg = ""
    
    for q in player_quests:
        if q['status'] == "active" and q['goal_type'] == goal_type:
            q['current'] += amount
            # Cek apakah target tercapai
            if q['current'] >= q['goal_value']:
                q['current'] = q['goal_value']
                q['status'] = "completed"
                # Berikan Hadiah Langsung ke Player Object
                player['gold'] += q.get('reward_gold', 0)
                player['exp'] += q.get('reward_exp', 0)
                notif_msg += f"\n🎯 **QUEST SELESAI:** {q['icon']} {q['name']} (+{q['reward_gold']}G)"
                
    return notif_msg
    
# === INVENTORY & SHOP CALLBACKS ===
@dp.callback_query(F.data.startswith("menu_") | F.data.startswith("equip_") | F.data.startswith("unequip_") | F.data.startswith("useitem_") | F.data.startswith("buy_"))
async def inventory_button_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = callback.data
    p = get_player(user_id)
    p['stats'] = calculate_total_stats(p)

    # --- LOGIKA SHOP (BELI BARANG) ---
    if data.startswith("buy_"):
        item_id = data.replace("buy_", "")
        success, msg = process_purchase(p, item_id)
        if success:
            # [QUEST UPDATE] Tambah progres belanja
            quest_notif = update_quest_progress(p, "buy_items", 1)
            
            update_player(user_id, {
                "gold": p['gold'], 
                "inventory": p['inventory'],
                "daily_quests": p.get('daily_quests', []) # Simpan Progres Quest
            })
            
            await callback.answer(f"✅ Berhasil membeli {item_id.replace('_', ' ').title()}!{quest_notif}")
            try:
                # Refresh tampilan toko agar sisa gold terupdate
                await callback.message.edit_reply_markup(
                    reply_markup=get_shop_keyboard(p, location=p.get('location', 'The Whispering Hall'))
                )
            except: pass
        else:
            await callback.answer(msg, show_alert=True)
        return

    # --- LOGIKA NAVIGASI MENU ---
    if data == "menu_inventory":
        await callback.message.edit_text("🎒 **Isi Tas (Equipment):**", reply_markup=InlineKeyboardMarkup(inline_keyboard=get_inventory_menu(p)), parse_mode="Markdown")
    elif data == "menu_consumables":
        await callback.message.edit_text("🧪 **Daftar Ramuan:**", reply_markup=InlineKeyboardMarkup(inline_keyboard=get_consumable_menu(p)), parse_mode="Markdown")
    elif data == "menu_profile":
        await callback.message.edit_text("👕 **Equipment Terpakai:**", reply_markup=InlineKeyboardMarkup(inline_keyboard=get_profile_menu(p)), parse_mode="Markdown")
    elif data == "menu_main_profile":
        await callback.message.edit_text(generate_profile_text(p, p['stats']), reply_markup=InlineKeyboardMarkup(inline_keyboard=get_profile_main_menu(p)), parse_mode="Markdown")
    
    # --- LOGIKA PASANG/LEPAS GEAR ---
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
    
    # --- LOGIKA PENGGUNAAN ITEM (POTION/QUIZ) ---
    elif data.startswith("useitem_"):
        item_id = data.replace("useitem_", "")
        current_state = await state.get_state()
        
        try: await callback.message.delete()
        except: pass
        
        success, msg, p_new = use_consumable_item(p, item_id)
        if not success:
            return await callback.answer(msg, show_alert=True)

        # [QUEST UPDATE] Tambah progres penggunaan item
        quest_notif = update_quest_progress(p_new, "use_items", 1)

        # CEK: Pemicu Quiz (Buku/Scroll)
        item_data = get_item(item_id)
        if item_data and item_data.get("effect_type") == "trigger_quiz":
            from game.puzzles.manager import generate_puzzle
            puzzle = generate_puzzle(tier=item_data.get("tier", 2))
            await state.set_state(GameState.in_event)
            await state.update_data(event_data=puzzle)
            return await callback.message.answer(
                f"{quest_notif}\n📖 {msg}\n\n━━━━━━━━━━━━━━━━━━━━\n❓ **PERTANYAAN:**\n{puzzle['question']}\n━━━━━━━━━━━━━━━━━━━━\n*Ketik jawabanmu...*",
                parse_mode="Markdown"
            )

        # LOGIKA: Penggunaan di dalam Combat
        if current_state == GameState.in_combat:
            data_st = await state.get_data()
            enemy_data = data_st.get("enemy_data")
            
            m_dmg, m_log = apply_monster_turn(enemy_data, p_new)
            m_hpc, m_logs = apply_turn_status_effects(enemy_data, is_player=False)
            p_hpc, p_logs = apply_turn_status_effects(p_new, is_player=True)
            
            enemy_data['monster_hp'] = max(0, enemy_data['monster_hp'] + m_hpc)
            p_new['hp'] = max(0, p_new['hp'] + p_hpc)
            
            reduce_all_cooldowns(p_new)
            current_combo = data_st.get("current_combo", 0) + 1
            
            update_player(user_id, {
                "hp": p_new['hp'], 
                "mp": p_new['mp'], 
                "inventory": p_new['inventory'], 
                "active_effects": p_new.get('active_effects', []),
                "daily_quests": p_new.get('daily_quests', []), # Simpan Progres
                "skill_cooldowns": p_new.get('skill_cooldowns', {})
            })
            
            full_log = f"🎒 {msg}\n{quest_notif}\n👾 {m_log}\n" + " ".join(m_logs + p_logs)
            await execute_end_of_turn(callback.message, state, user_id, p_new, enemy_data, full_log, current_combo, data_st.get("battle_msg_id"))
        
        # LOGIKA: Penggunaan di luar Combat
        else:
            update_player(user_id, {
                'hp': p_new['hp'], 
                'mp': p_new['mp'], 
                'energy': p_new.get('energy', 100),
                'inventory': p_new['inventory'], 
                'active_effects': p_new.get('active_effects', []),
                'daily_quests': p_new.get('daily_quests', []) # Simpan Progres
            })
            await callback.message.answer(f"{msg}\n{quest_notif}", parse_mode="Markdown")


# === MOVEMENT & EXPLORATION ===
@dp.message(F.text.in_(["⬆️ Utara", "⬅️ Barat", "Timur ➡️", "⬇️ Selatan"]))
async def move_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    current_state = await state.get_state()
    
    # 1. CEK STATE: Mencegah jalan saat bertarung/event/istirahat
    if current_state in [GameState.in_combat, GameState.in_event, GameState.in_rest_area]:
        try: await message.delete() 
        except: pass
        warning_msg = await message.answer("⚠️ Selesaikan dulu urusanmu di depan sebelum bergerak maju!")
        await asyncio.sleep(2)
        try: await message.bot.delete_message(chat_id=message.chat.id, message_id=warning_msg.message_id)
        except: pass
        return
        
    try: await message.delete()
    except: pass
    
    # 2. CLEANUP: Hapus pesan eksplorasi sebelumnya agar chat tidak spam
    state_data = await state.get_data()
    last_expl_msg = state_data.get("last_expl_msg_id")
    if last_expl_msg:
        try: await message.bot.delete_message(chat_id=message.chat.id, message_id=last_expl_msg)
        except: pass

    # 3. PREPARASI DATA & STATS
    await state.set_state(GameState.exploring)
    tick_buffs(user_id) 
    p = get_player(user_id)
    
    # Sinkronisasi Stats
    p['stats'] = calculate_total_stats(p) 
    luck_bonus = p['stats'].get('luck', 0)
    intel_bonus = p.get('intelligence', 10)
    
    # 4. ENERGI CHECK
    current_energy = p.get('energy', 100)
    if current_energy <= 0:
        return await message.answer("😫 Kamu terlalu lelah untuk melangkah... Gunakan makanan atau istirahat di Rest Area!", 
                                   reply_markup=get_main_reply_keyboard(p))

    # 5. UPDATE PROGRES QUEST (Langkah Kaki) & ENERGI
    new_energy = current_energy - 1
    
    # Panggil helper quest untuk kategori "move_steps"
    quest_notif = update_quest_progress(p, "move_steps", 1)
    
    # Simpan perubahan energi dan quest ke database
    update_player(user_id, {
        "energy": new_energy,
        "daily_quests": p.get('daily_quests', [])
    })
    
    # 6. LOGIKA PERGERAKAN
    event_type, event_data, narration = process_move(user_id, luck=luck_bonus, intel=intel_bonus)
    
    # Gabungkan narasi dengan notifikasi quest jika ada yang selesai
    final_narration = f"{narration}\n{quest_notif}" if quest_notif else narration

    # 7. PENANGANAN HASIL EVENT
    if event_type in ["boss", "monster", "miniboss"]:
        is_boss = (event_type == "boss")
        is_miniboss = (event_type == "miniboss")
        tier_level = 5 if is_boss else min(5, max(1, (p.get('kills', 0) // 5) + 1))
        
        enemy_data = generate_battle_data(p, tier_level, is_boss=is_boss, is_miniboss=is_miniboss)
        await state.set_state(GameState.in_combat)
        
        # UI Battle
        safe_narration = final_narration.replace("**", "")
        combat_ui = render_live_battle(p, enemy_data, f"⚠️ <b>{safe_narration}</b>")
        sent_msg = await message.answer(combat_ui, parse_mode="HTML", reply_markup=get_stance_keyboard(is_boss))
        
        await state.update_data(
            battle_msg_id=sent_msg.message_id,
            enemy_data=enemy_data, 
            current_combo=0,
            last_expl_msg_id=None
        )

    elif event_type == "rest_area":
        await state.set_state(GameState.in_rest_area)
        kb = get_rest_area_keyboard()
        sent_msg = await message.answer(f"🏕️ **REST AREA**\n{final_narration}", reply_markup=kb, parse_mode="Markdown")
        await state.update_data(last_expl_msg_id=sent_msg.message_id)

    elif event_type == "event":
        await state.set_state(GameState.in_event)
        await state.update_data(event_data=event_data)
        sent_msg = await message.answer(f"❓ **MYSTERY EVENT**\n{final_narration}\n\n*Ketik jawabanmu di sini...*", parse_mode="Markdown")
        await state.update_data(last_expl_msg_id=sent_msg.message_id)

    else:
        # Eksplorasi Biasa
        sent_msg = await message.answer(f"{final_narration}\n\n⚡ Energi: {new_energy}/100", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
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
        # Tutup pop-up menu skill agar tidak menumpuk
        try: await callback.message.delete()
        except: pass
    
    # --- 1. SUB-MENU HANDLING ---
    if action == "item":
        kb = get_consumable_menu(p)
        if not kb or len(kb) <= 1: return await callback.answer("Tas ramuanmu kosong!", show_alert=True)
        return await callback.message.answer("🎒 **PILIH RAMUAN:**", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))

    if action == "skill":
        kb = get_skill_menu_keyboard(p, p['stats'])
        return await callback.message.answer("🔮 **DAFTAR MAGIC & SKILL:**", reply_markup=kb)

    # --- 2. PREPARASI DATA COMBAT ---
    state_data = await state.get_data()
    enemy_data = state_data.get("enemy_data")
    battle_msg_id = state_data.get("battle_msg_id")
    
    if not enemy_data:
        return await callback.answer("❌ Data musuh hilang. Gunakan tombol arah untuk memulai ulang.", show_alert=True)
        
    m_name = enemy_data.get('monster_name', 'Musuh')
    result_msg = ""
    current_combo = state_data.get("current_combo", 0)

    # --- 3. EKSEKUSI AKSI PEMAIN ---
    if action == "attack": 
        current_combo += 1
        res_type, p_val, status, p_log = execute_skill(p['stats'], enemy_data, "basic_attack", p)
        enemy_data['monster_hp'] -= p_val
        reduce_equipment_durability(user_id, target_slots=['weapon'], damage=1)
        
        m_dmg, m_log = apply_monster_turn(enemy_data, p)
        result_msg = f"⚔️ <b>SERANG:</b> {p_log}\n👾 <b>BALASAN:</b> {m_log}"
        
    elif action == "cast_skill" and skill_to_cast:
        eff_skill = get_effective_skill(p, skill_to_cast)
        if not eff_skill:
            return await callback.answer("❌ Skill tidak valid.", show_alert=True)
            
        mp_cost = eff_skill.get('mp_cost', 0)
        if p.get('mp', 0) < mp_cost:
            return await callback.answer(f"🔮 MP Tidak cukup! Butuh {mp_cost} MP.", show_alert=True)
            
        current_combo += 1
        p['mp'] -= mp_cost
        res_type, p_val, status, p_log = execute_skill(p['stats'], enemy_data, skill_to_cast, p)
        reduce_equipment_durability(user_id, target_slots=['weapon'], damage=2)
        
        if res_type == "damage":
            enemy_data['monster_hp'] -= p_val
            if status and status not in [e['type'] for e in enemy_data.get('monster_effects', [])]:
                enemy_data.setdefault('monster_effects', []).append({'type': status, 'value': int(p_val * 0.2) or 5})
        elif res_type == "heal":
            p['hp'] = min(p.get('max_hp', 100), p['hp'] + p_val)
        
        m_dmg, m_log = apply_monster_turn(enemy_data, p)
        result_msg = f"🌟 {p_log}\n👾 <b>BALASAN:</b> {m_log}"

    elif action == "block": 
        current_combo = 0 # Reset combo karena fokus bertahan
        heal_amount = int(p.get('max_hp', 100) * 0.10) # Nerf sedikit agar tidak OP
        p['hp'] = min(p.get('max_hp', 100), p['hp'] + heal_amount)
        
        m_dmg, m_log = apply_monster_turn(enemy_data, p)
        if m_dmg > 0:
            refund = int(m_dmg * 0.8) # Reduksi 80%
            p['hp'] += refund
            reduced_dmg = max(0, m_dmg - refund)
            reduce_equipment_durability(user_id, target_slots=['armor', 'head'], damage=1)
            result_msg = f"🛡️ <b>BERTAHAN:</b> (+{heal_amount} HP).\n👾 <b>TERTANGKIS:</b> {m_log} (-{reduced_dmg} HP)."
        else:
            result_msg = f"🛡️ <b>BERTAHAN:</b> (+{heal_amount} HP).\n👾 <b>MUSUH:</b> {m_log}"

    elif action == "dodge":
        base_dodge_chance = 0.40
        player_dodge_stat = p['stats'].get('dodge', 0.1) 
        # Penalti berat: Semakin banyak barang dibawa, semakin sulit menghindar
        weight_penalty = p['stats'].get('total_weight', 0) * 0.005 
        final_dodge_chance = min(0.90, max(0.10, base_dodge_chance + player_dodge_stat - weight_penalty))

        if random.random() < final_dodge_chance:
            current_combo += 1
            restore_mp = int(p.get('max_mp', 50) * 0.15)
            p['mp'] = min(p.get('max_mp', 50), p.get('mp', 0) + restore_mp)
            result_msg = f"💨 <b>PERFECT DODGE:</b> (+{restore_mp} MP).\n🎯 {m_name} menyerang angin!"
        else:
            current_combo = 0
            m_dmg, m_log = apply_monster_turn(enemy_data, p)
            if m_dmg > 0:
                refund = int(m_dmg * 0.2) # Gagal dodge tetap kena damage besar
                p['hp'] += refund
                reduced_dmg = m_dmg - refund
                reduce_equipment_durability(user_id, target_slots=['armor', 'head'], damage=1)
                result_msg = f"🧱 <b>GAGAL DODGE!</b> {m_log} (-{reduced_dmg} HP)."
            else:
                result_msg = f"🧱 <b>GAGAL DODGE!</b>\n👾 <b>MUSUH:</b> {m_log}"

    elif action == "run":
        chance = p['stats'].get('dodge', 0.1) + 0.30 
        if random.random() < chance:
            await state.set_state(GameState.exploring)
            update_player(user_id, {'current_combo': 0, 'skill_cooldowns': {}})
            try: await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=battle_msg_id)
            except: pass
            return await callback.message.answer("🏃💨 Kamu melarikan diri ke kegelapan.", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
        else:
            current_combo = 0
            m_dmg, m_log = apply_monster_turn(enemy_data, p)
            result_msg = f"🧱 <b>GAGAL KABUR!</b>\n👾 <b>BALASAN:</b> {m_log}"

    # --- 4. TICK STATUS EFFECTS & COOLDOWN ---
    m_hp_change, m_status_logs = apply_turn_status_effects(enemy_data, is_player=False)
    p_hp_change, p_status_logs = apply_turn_status_effects(p, is_player=True)
    
    enemy_data['monster_hp'] = max(0, enemy_data['monster_hp'] + m_hp_change)
    p['hp'] = max(0, p['hp'] + p_hp_change)
    
    # Kurangi cooldown hanya jika pemain melakukan aksi (bukan buka menu)
    reduce_all_cooldowns(p)
    
    # Sinkronisasi ke Database
    update_player(user_id, {
        "hp": p['hp'], "mp": p['mp'], 
        "inventory": p['inventory'], 
        "active_effects": p.get('active_effects', []),
        "skill_usages": p.get('skill_usages', {}),
        "skill_cooldowns": p.get('skill_cooldowns', {}),
        "last_skill_used": p.get('last_skill_used', None),
        "current_combo": current_combo
    })
    
    status_log_final = " ".join(m_status_logs + p_status_logs)
    full_log = f"{result_msg}\n{status_log_final}"

    # --- 5. FINALIZE TURN ---
    await execute_end_of_turn(callback.message, state, user_id, p, enemy_data, full_log, current_combo, battle_msg_id)


# === HELPER: FASE END OF TURN & CHECK DEATH ===
async def execute_end_of_turn(message: Message, state: FSMContext, user_id: int, p: dict, enemy_data: dict, full_log: str, current_combo: int, battle_msg_id: int):
    m_name = enemy_data.get('monster_name', 'Musuh')
    
    # --- SKENARIO 1: PEMAIN MENANG ---
    if enemy_data['monster_hp'] <= 0:
        tier = enemy_data.get('tier', 1)
        is_boss = enemy_data.get('is_boss', False)
        
        # Kalkulasi Reward (Ditambah bonus Combo)
        combo_bonus = 1 + (current_combo * 0.1)
        base_gold = 500 if is_boss else (int(tier) * 25)
        total_gold = int(base_gold * combo_bonus)
        
        base_exp = enemy_data.get('exp_reward', 15 * tier)
        total_exp = int(base_exp * combo_bonus)
        
        # ==========================================
        # === INTEGRASI QUEST (TAMBAHKAN INI) ===
        # ==========================================
        # 1. Update Progres Bunuh Monster
        quest_notif = update_quest_progress(p, "kill_monsters", 1)
        
        # 2. Update Progres Boss Slayer (Jika boss)
        if is_boss or enemy_data.get('is_miniboss'):
            quest_notif += update_quest_progress(p, "kill_boss", 1)
            
        # 3. Update Progres Kumpulkan Emas
        quest_notif += update_quest_progress(p, "earn_gold", total_gold)
        
        # 4. Update Progres Combo (Jika mencapai jumlah tertentu)
        quest_notif += update_quest_progress(p, "perform_combo", current_combo)
        # ==========================================

        # Proses Level Up
        new_exp = p.get('exp', 0) + total_exp
        old_level = p.get('level', 1)
        new_level = calculate_level_from_exp(new_exp)
        
        level_up_msg = ""
        if new_level > old_level:
            hp_gain = 15 + (new_level * 2)
            mp_gain = 5 + (new_level)
            new_max_hp = p.get('max_hp', 100) + hp_gain
            new_max_mp = p.get('max_mp', 50) + mp_gain
            p.update({'max_hp': new_max_hp, 'max_mp': new_max_mp, 'hp': new_max_hp, 'mp': new_max_mp, 'level': new_level})
            level_up_msg = f"\n\n🆙 <b>LEVEL UP!</b> ({old_level} ➜ {new_level})\n💖 Max HP +{hp_gain} | 💧 Max MP +{mp_gain}"

        # Proses Loot
        drops = process_loot(enemy_data.get('drops', []))
        inv = p.get('inventory', [])
        inv.extend(drops)
        
        # Finalisasi Data ke Database
        update_player(user_id, {
            'kills': p.get('kills', 0) + 1, 
            'gold': p['gold'] + total_gold, # p['gold'] sudah ditambah hadiah quest di helper
            'exp': p['exp'] + total_exp, 
            'level': p['level'],
            'hp': p['hp'],
            'max_hp': p.get('max_hp'),
            'max_mp': p.get('max_mp'),
            'inventory': inv,
            'daily_quests': p.get('daily_quests'), # Simpan progres quest terbaru!
            'current_combo': 0,
            'skill_cooldowns': {}
        })
        
        add_history(user_id, f"Menang melawan {m_name} (Combo x{current_combo})")
        
        if battle_msg_id:
            try: await message.bot.delete_message(chat_id=message.chat.id, message_id=battle_msg_id)
            except: pass
        
        await state.set_state(GameState.exploring)
        
        safe_drops = ", ".join(drops).replace("_", " ").title() if drops else "Hanya debu..."
        victory_text = (
            f"🎉 <b>KEMENANGAN!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👾 <b>{m_name}</b> telah tumbang!\n"
            f"⚔️ Combo Tertinggi: x{current_combo}\n\n"
            f"✨ EXP: +{total_exp}\n"
            f"💰 Gold: +{total_gold}\n"
            f"🎁 Drops: <i>{safe_drops}</i>"
            f"{quest_notif}" # Tampilkan notifikasi quest selesai di sini
            f"{level_up_msg}"
        )
        
        sent_msg = await message.answer(victory_text, reply_markup=get_main_reply_keyboard(p), parse_mode="HTML")
        await state.update_data(last_expl_msg_id=sent_msg.message_id)
        return

    # --- SKENARIO 2: PEMAIN MATI ---
    elif p['hp'] <= 0:
        death_text = reset_player_death(user_id, f"Dikalahkan oleh {m_name}")
        await state.set_state(GameState.exploring)
        
        if battle_msg_id:
            try: await message.bot.delete_message(chat_id=message.chat.id, message_id=battle_msg_id)
            except: pass
            
        await message.answer(f"💀 <b>ANDA MATI</b>\n\n{death_text}", reply_markup=get_main_reply_keyboard(p), parse_mode="HTML")
        return
        
    # --- SKENARIO 3: PERTARUNGAN LANJUT ---
    else:
        # Update state data untuk turn berikutnya
        await state.update_data(enemy_data=enemy_data, current_combo=current_combo)
        
        # Render UI Battle terbaru
        next_msg = render_live_battle(p, enemy_data, f"💬 {full_log}")
        
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
                await asyncio.sleep(e.retry_after)
            except Exception:
                # Fallback jika edit gagal (misal pesan dihapus user atau API error)
                new_battle_msg = await message.answer(next_msg, parse_mode="HTML", reply_markup=get_stance_keyboard(enemy_data.get('is_boss', False)))
                await state.update_data(battle_msg_id=new_battle_msg.message_id)


# === EVENT PUZZLE (NON-COMBAT / EKSPLORASI) ===
@dp.message(GameState.in_event)
async def event_puzzle_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    p = get_player(user_id)
    state_data = await state.get_data()
    event_data = state_data.get("event_data")
    
    # Ambil jawaban pemain
    player_answer = message.text.strip().lower()
    
    # Proses hasil event menggunakan sistem event
    success, reward_msg, loot = process_event_outcome(p, event_data, player_answer)
    
    if success:
        # [QUEST UPDATE] Tambah progres menjawab Quiz
        quest_notif = update_quest_progress(p, "answer_quiz", 1)
        
        # Tambahkan hadiah loot ke inventory jika ada
        if loot:
            p['inventory'].extend(loot)
        
        # Kalkulasi statistik kecerdasan & reward gold
        intel_gain = event_data.get('tier', 1) * 2
        new_intel = p.get("intelligence", 10) + intel_gain
        new_gold = p.get("gold", 0) + event_data.get("gold_reward", 50)
        
        # Update Database (Daily Quests wajib ikut agar tersimpan)
        update_player(user_id, {
            "inventory": p['inventory'],
            "intelligence": new_intel,
            "scholar_level": p.get("scholar_level", 0) + 1,
            "gold": new_gold,
            "daily_quests": p.get('daily_quests', [])
        })
        
        # Notifikasi Berhasil + Reward + Quest Progres
        success_final = (
            f"✅ **BERHASIL!**\n{reward_msg}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🧠 Intelligence +{intel_gain}\n"
            f"💰 Gold +{event_data.get('gold_reward', 50)}\n"
            f"{quest_notif}"
        )
        await message.answer(success_final, reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
        
    else:
        # Jika gagal, quest tidak bertambah
        await message.answer(f"❌ **GAGAL!**\n{reward_msg}", reply_markup=get_main_reply_keyboard(p), parse_mode="Markdown")
    
    # Kembalikan state ke menjelajah
    await state.set_state(GameState.exploring)
    

# === HELP SYSTEM ===
@dp.message(F.text == "/help")
async def help_handler(message: Message):
    help_text = (
        "📜 **ARCHIVUS PROTOCOL: GUIDANCE**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "Selamat datang di pusat bantuan, Weaver. Berikut adalah instruksi dasar untuk bertahan hidup:\n\n"
        
        "🧭 **EKSPLORASI & ENERGI**\n"
        "• Gunakan tombol arah untuk menjelajah.\n"
        "• Tiap langkah mengonsumsi **1 Energi**.\n"
        "• Jika Energi 0, gunakan **Makanan** atau temukan **Rest Area**.\n\n"
        
        "⚔️ **SISTEM PERTEMPURAN**\n"
        "• **Skill:** Serangan kuat menggunakan MP.\n"
        "• **Block:** Mitigasi damage & pulihkan sedikit HP.\n"
        "• **Dodge:** Peluang hindaran total & bonus MP.\n"
        "• **Combo:** Serangan beruntun meningkatkan bonus Gold/EXP.\n\n"
        
        "🎯 **MISI HARIAN (QUESTS)**\n"
        "• Selesaikan misi aktif untuk **Reward Besar**.\n"
        "• Progres dihitung otomatis saat bertarung, belanja, atau melangkah.\n\n"
        
        "🛠️ **GEAR & DURABILITAS**\n"
        "• Senjata/Armor yang rusak kehilangan **80% Stat**.\n"
        "• Perbaiki Gear di **Bengkel Aethelred** melalui menu Profil.\n\n"
        
        "🧠 **KECERDASAN (INTEL)**\n"
        "• Jawab Quiz dari item buku kuno untuk menaikkan Intel.\n"
        "• Intel tinggi membuka akses ke **Secret Room** & Event langka.\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🔮 *Ingatan adalah senjata terbaikmu di sini.*"
    )
    
    await message.answer(help_text, parse_mode="Markdown")


async def main():
    auto_seed_content()
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
