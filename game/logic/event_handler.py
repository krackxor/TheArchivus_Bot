# game/logic/event_handler.py

import random
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from game.logic.states import GameState
from database import update_player
from game.logic.menu_handler import get_main_reply_keyboard

# --- IMPORT DATA MASTER MODULAR ---
from game.data.npc_data import NPC_POOL, LORE_STORIES
from game.data.environment.hazards import process_hazard_interaction
from game.data.environment.deadly import process_deadly_interaction
from game.data.environment.landmarks import process_landmark_interaction
from game.data.quests import update_quest_progress
from game.puzzles.manager import generate_puzzle

# --- 1. GENERATOR TOMBOL INTERAKSI ---

def get_event_interaction_kb(event_type, event_data):
    """Membuat tombol dinamis berdasarkan jenis event dan kategori."""
    kb = []
    
    if event_type == "npc":
        cat = event_data.get("category", "wanderer")
        # Pemetaan kategori ke tombol yang sesuai
        if cat == "quiz":
            kb.append([InlineKeyboardButton(text="📜 Tantang Kecerdasan", callback_data="evt_npc_quiz")])
        else:
            # Gunakan prefix 'pool_' untuk kategori NPC fungsional/gacha
            kb.append([InlineKeyboardButton(text="🤝 Dekati Sosok Itu", callback_data=f"pool_{cat}")])
        
        kb.append([InlineKeyboardButton(text="🚶 Abaikan", callback_data="evt_ignore")])

    elif event_type == "deadly":
        event_id = event_data.get("id")
        # Pastikan event_id disertakan dengan jelas
        kb.append([InlineKeyboardButton(text="🏃 Terjang Bahaya!", callback_data=f"exec_deadly_{event_id}")])
        kb.append([InlineKeyboardButton(text="🔄 Cari Jalan Lain", callback_data="evt_ignore")])

    elif event_type == "landmark":
        lm_id = event_data.get("id")
        # Landmark menggunakan prefix 'exec_landmark_'
        kb.append([InlineKeyboardButton(text="🔍 Periksa Lokasi", callback_data=f"exec_landmark_{lm_id}")])
        kb.append([InlineKeyboardButton(text="➡️ Lanjut Jalan", callback_data="evt_ignore")])

    return InlineKeyboardMarkup(inline_keyboard=kb) if kb else None

# --- 2. LOGIKA EKSEKUSI INTERAKSI (THE ENGINE) ---

async def handle_event_interaction(callback, state, player):
    """Pusat pemrosesan aksi modular tanpa menyebabkan ValidationError."""
    data = callback.data
    user_id = player['user_id']
    
    # A. MESIN NPC POOL (Heal, Gamble, Lore, Gift)
    if data.startswith("pool_"):
        category = data.split("_")[1]
        npc_list = NPC_POOL.get(category, NPC_POOL['wanderer'])
        npc = random.choice(npc_list)
        
        text = f"👤 **{npc['name']}**\n\n_{npc['narration']}_\n"
        npc_type = npc.get("type")
        
        if npc_type == "heal":
            if player['gold'] >= npc.get('cost', 0):
                player['hp'] = min(player.get('max_hp', 100), player['hp'] + npc['value'])
                player['gold'] -= npc['cost']
                text += f"\n✨ **HP Pulih +{npc['value']}**"
            else: 
                return await callback.answer("Gold tidak cukup!", show_alert=True)

        elif npc_type == "gamble":
            if player['gold'] >= npc.get('bet', 0):
                win = random.random() < npc['chance']
                reward = npc['bet'] * 2 if win else 0
                player['gold'] = player['gold'] - npc['bet'] + reward
                text += f"\n🎲 {'🎉 Menang!' if win else '💀 Kalah!'}"
            else: 
                return await callback.answer("Gold tidak cukup!", show_alert=True)

        elif npc_type == "lore":
            text += f"\n\n📜 **Lore:** _{random.choice(LORE_STORIES)}_"
            player, _ = update_quest_progress(player, "move_steps")

        elif npc_type == "gift":
            item = npc['gift_item']
            player.setdefault('inventory', []).append(item)
            text += f"\n🎁 **Dapatkan:** {item.replace('_', ' ').title()}"

        # Akhiri interaksi dan reset state ke penjelajahan
        await state.set_state(GameState.exploring)
        update_player(user_id, player)
        
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer(text, reply_markup=get_main_reply_keyboard(player))

    # B. KHUSUS: MESIN QUIZ
    elif data == "evt_npc_quiz":
        tier = max(1, min(5, player.get('level', 1) // 10 + 1))
        puzzle = generate_puzzle(tier=tier)
        
        await state.set_state(GameState.in_event)
        await state.update_data(event_data=puzzle)
        
        text = (
            f"📜 **TANTANGAN KECERDASAN**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"\"{puzzle['question']}\"\n\n"
            f"💬 *Ketik jawabanmu sekarang...*"
        )
        await callback.message.edit_text(text, parse_mode="Markdown")

    # C. MESIN BAHAYA MAUT (Deadly Terrains)
    elif data.startswith("exec_deadly_"):
        # Ambil ID dengan memotong prefix
        event_id = data.replace("exec_deadly_", "")
        success, msg = process_deadly_interaction(player, event_id)
        
        await state.set_state(GameState.exploring)
        update_player(user_id, player)
        
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer(msg, reply_markup=get_main_reply_keyboard(player))

    # D. MESIN LOKASI (Landmarks)
    elif data.startswith("exec_landmark_"):
        # Ambil ID dengan memotong prefix
        lm_id = data.replace("exec_landmark_", "")
        res, msg = process_landmark_interaction(player, lm_id)
        
        if res == "ambush":
            # Jika ambush, biarkan battle handler atau UI combat yang bekerja
            await callback.message.edit_text(f"⚠️ {msg}")
        else:
            await state.set_state(GameState.exploring)
            update_player(user_id, player)
            try:
                await callback.message.delete()
            except:
                pass
            await callback.message.answer(msg, reply_markup=get_main_reply_keyboard(player))

    # E. ABAIKAN / LANJUT JALAN
    elif data == "evt_ignore":
        # Setiap langkah yang diabaikan tetap menghitung progres quest langkah
        player, quest_msgs = update_quest_progress(player, "move_steps")
        update_player(user_id, player)
        
        await state.set_state(GameState.exploring)
        msg = "🏃 Kamu melanjutkan perjalanan."
        if quest_msgs: 
            msg += "\n\n" + "\n".join(quest_msgs)
        
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer(msg, reply_markup=get_main_reply_keyboard(player))

    await callback.answer()
