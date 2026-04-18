# game/handlers/menu.py

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

# === IMPORTS UTAMA ===
from database import get_player, update_player
from game.logic.states import GameState
from game.logic.stats import calculate_total_stats
from game.logic.inventory_manager import equip_item, unequip_item, process_repair_all, use_consumable_item
from game.logic.menu_handler import (
    get_inventory_menu, get_profile_menu, get_consumable_menu, 
    get_profile_main_menu, generate_profile_text
)
from game.systems.shop import process_purchase, get_shop_keyboard
# Sinkronisasi dengan sistem Quest Modular
from game.data.quests import update_quest_progress
from game.items import get_item

# Inisialisasi Router
router = Router()

# ==============================================================================
# 1. BUKA MENU PROFIL (DARI TOMBOL BAWAH)
# ==============================================================================
@router.message(GameState.exploring, F.text == "📊 Profil & Tas")
async def profile_bag_handler(message: Message):
    user_id = message.from_user.id
    p = get_player(user_id)
    
    # Kalkulasi stat terbaru berdasarkan equipment yang sedang dipakai
    p['stats'] = calculate_total_stats(p)
    
    # Render teks dan tombol
    text = generate_profile_text(p, p['stats'])
    kb = get_profile_main_menu(p)
    
    await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=kb), parse_mode="Markdown")


# ==============================================================================
# 2. NAVIGASI ANTAR MENU (INLINE BUTTONS)
# ==============================================================================
@router.callback_query(F.data.in_(["menu_inventory", "menu_consumables", "menu_profile", "menu_main_profile", "close_menu_profile"]))
async def menu_navigation_handler(callback: CallbackQuery):
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
    
    elif data == "close_menu_profile":
        try:
            await callback.message.delete()
            await callback.answer("Menu ditutup")
        except Exception:
            await callback.message.edit_text("✨ Fokus kembali ke penjelajahan...")
            await callback.answer()


# ==============================================================================
# 3. EQUIP & UNEQUIP GEAR
# ==============================================================================
@router.callback_query(F.data.startswith("equip_") | F.data.startswith("unequip_"))
async def equipment_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    data = callback.data
    p = get_player(user_id)

    if data.startswith("equip_"):
        item_id = data.replace("equip_", "")
        success, msg = equip_item(p, item_id)
        
        # Simpan perubahan ke database
        update_player(user_id, {
            'inventory': p['inventory'], 
            'equipped': p['equipped'], 
            'current_job': p.get('current_job')
        })
        await callback.answer(msg)
        
        # Refresh tampilan tas
        await callback.message.edit_text("🎒 **Isi Tas:**", reply_markup=InlineKeyboardMarkup(inline_keyboard=get_inventory_menu(p)), parse_mode="Markdown")
        
    elif data.startswith("unequip_"):
        slot = data.replace("unequip_", "")
        success, msg = unequip_item(p, slot)
        
        # Simpan perubahan ke database
        update_player(user_id, {
            'inventory': p['inventory'], 
            'equipped': p['equipped'], 
            'current_job': p.get('current_job')
        })
        await callback.answer(msg)
        
        # Refresh tampilan gear terpakai
        await callback.message.edit_text("👕 **Equipment Terpakai:**", reply_markup=InlineKeyboardMarkup(inline_keyboard=get_profile_menu(p)), parse_mode="Markdown")


# ==============================================================================
# 4. BLACKSMITH (PERBAIKI GEAR)
# ==============================================================================
@router.callback_query(F.data == "menu_repair")
async def blacksmith_callback_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    p = get_player(user_id)
    
    # Hitung biaya dan jumlah perbaikan
    new_durability, cost, count = process_repair_all(p)
    
    if count == 0: 
        return await callback.answer("⚒️ Aethelred: 'Gear-mu masih tajam dan kokoh. Pergi sana!'", show_alert=True)
    
    if p.get('gold', 0) < cost: 
        return await callback.answer(f"❌ Emasmu tidak cukup! Butuh {cost} Gold.", show_alert=True)
        
    # Eksekusi Perbaikan
    p['gold'] -= cost
    p['equipment_durability'] = new_durability
    
    # Trigger Quest: Perawatan Gear (repair_gear)
    p, quest_msgs = update_quest_progress(p, "repair_gear", 1)
    
    # Update Stats terbaru
    p['stats'] = calculate_total_stats(p)
    
    update_player(user_id, {
        "gold": p['gold'], 
        "equipment_durability": new_durability,
        "active_quests": p.get('active_quests', [])
    })
    
    repair_msg = (
        f"⚒️ **BENGKEL AETHELRED**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💬 *'Nah, benda ini bisa membelah kulit iblis lagi.'*\n\n"
        f"🛠️ **Diperbaiki:** {count} buah\n"
        f"💰 **Biaya:** -{cost} Gold\n"
        f"✨ **Kondisi:** 100% (Gear Kokoh)\n"
    )
    
    if quest_msgs:
        repair_msg += "\n" + "\n".join(quest_msgs)
    
    kb = get_profile_main_menu(p)
    try:
        await callback.message.edit_text(repair_msg, reply_markup=InlineKeyboardMarkup(inline_keyboard=kb), parse_mode="Markdown")
    except Exception:
        pass
    await callback.answer("✅ Seluruh peralatan berhasil diperbaiki!")


# ==============================================================================
# 5. TOKO / PEMBELIAN BARANG (SHOP)
# ==============================================================================
@router.callback_query(F.data.startswith("buy_"))
async def shop_purchase_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    item_id = callback.data.replace("buy_", "")
    p = get_player(user_id)
    
    success, msg = process_purchase(p, item_id)
    
    if success:
        # Trigger Quest: Pelanggan Setia (buy_items)
        p, quest_msgs = update_quest_progress(p, "buy_items", 1)
        
        update_player(user_id, {
            "gold": p['gold'], 
            "inventory": p['inventory'],
            "active_quests": p.get('active_quests', [])
        })
        
        # Gabungkan pesan sukses toko dengan notifikasi quest
        full_msg = f"✅ Berhasil membeli {item_id.replace('_', ' ').title()}!"
        if quest_msgs:
            full_msg += "\n" + "\n".join(quest_msgs)
            
        await callback.answer(full_msg, show_alert=True if quest_msgs else False)
        
        # Refresh tampilan toko
        try:
            await callback.message.edit_reply_markup(
                reply_markup=get_shop_keyboard(p, location=p.get('location', 'The Whispering Hall'))
            )
        except Exception:
            pass
    else:
        await callback.answer(msg, show_alert=True)


# ==============================================================================
# 6. PENGGUNAAN ITEM (DI LUAR PERTEMPURAN)
# ==============================================================================
@router.callback_query(F.data.startswith("useitem_"))
async def use_item_handler(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    
    # Cegah penggunaan item jika sedang bertarung
    if current_state == GameState.in_combat:
        return await callback.answer("⚠️ Gunakan ramuan melalui tombol 🎒 Item di layar pertarungan!", show_alert=True)

    user_id = callback.from_user.id
    item_id = callback.data.replace("useitem_", "")
    p = get_player(user_id)
    
    try: await callback.message.delete()
    except: pass
    
    # Proses efek item
    success, msg, p_new = use_consumable_item(p, item_id)
    if not success:
        return await callback.answer(msg, show_alert=True)

    # Trigger Quest: Pecandu Ramuan (use_items)
    p_new, quest_msgs = update_quest_progress(p_new, "use_items", 1)

    # CEK SPESIAL: Pemicu Quiz (Buku / Scroll)
    item_data = get_item(item_id)
    if item_data and item_data.get("effect_type") == "trigger_quiz":
        from game.puzzles.manager import generate_puzzle
        puzzle = generate_puzzle(tier=item_data.get("tier", 2))
        
        await state.set_state(GameState.in_event)
        await state.update_data(event_data=puzzle)
        
        q_text = f"📖 {msg}\n"
        if quest_msgs: q_text += "\n".join(quest_msgs) + "\n"
        q_text += f"\n━━━━━━━━━━━━━━━━━━━━\n❓ **PERTANYAAN:**\n{puzzle['question']}\n━━━━━━━━━━━━━━━━━━━━\n*Ketik jawabanmu...*"
        
        return await callback.message.answer(q_text, parse_mode="Markdown")

    # Simpan status terbaru
    update_player(user_id, {
        'hp': p_new['hp'], 
        'mp': p_new['mp'], 
        'energy': p_new.get('energy', 100),
        'inventory': p_new['inventory'], 
        'active_effects': p_new.get('active_effects', []),
        'active_quests': p_new.get('active_quests', [])
    })
    
    final_alert = msg
    if quest_msgs:
        final_alert += "\n" + "\n".join(quest_msgs)
        
    await callback.message.answer(final_alert, parse_mode="Markdown")
