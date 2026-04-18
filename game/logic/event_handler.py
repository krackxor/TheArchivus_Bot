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

# --- 1. GENERATOR TOMBOL INTERAKSI ---

def get_event_interaction_kb(event_type, event_data):
    """Membuat tombol dinamis berdasarkan jenis event dan kategori."""
    kb = []
    
    if event_type == "npc":
        cat = event_data.get("category", "wanderer")
        # Callback pool_{cat} memicu interaksi dinamis dari NPC_POOL
        kb.append([InlineKeyboardButton(text="🤝 Dekati Sosok Itu", callback_data=f"pool_{cat}")])
        kb.append([InlineKeyboardButton(text="🚶 Abaikan", callback_data="evt_ignore")])

    elif event_type == "deadly":
        event_id = event_data.get("id")
        kb.append([InlineKeyboardButton(text="🏃 Terjang Bahaya!", callback_data=f"exec_deadly_{event_id}")])
        kb.append([InlineKeyboardButton(text="🔄 Cari Jalan Lain", callback_data="evt_ignore")])

    elif event_type == "landmark":
        lm_id = event_data.get("id")
        kb.append([InlineKeyboardButton(text="🔍 Periksa/Interaksi", callback_data=f"exec_landmark_{lm_id}")])
        kb.append([InlineKeyboardButton(text="➡️ Lanjut Jalan", callback_data="evt_ignore")])

    return InlineKeyboardMarkup(inline_keyboard=kb) if kb else None

# --- 2. LOGIKA EKSEKUSI INTERAKSI (THE ENGINE) ---

async def handle_event_interaction(callback, state, player):
    """Pusat pemrosesan aksi modular tanpa menyebabkan ValidationError."""
    data = callback.data
    user_id = player['user_id']
    
    # A. MESIN NPC POOL (10 Kategori NPC)
    if data.startswith("pool_"):
        category = data.split("_")[1]
        npc = random.choice(NPC_POOL.get(category, NPC_POOL['wanderer']))
        text = f"👤 **{npc['name']}**\n\n_{npc['narration']}_\n"
        quest_msgs = []

        # Eksekusi berdasarkan type fungsional di database
        npc_type = npc.get("type")
        
        if npc_type == "heal":
            if player['gold'] >= npc['cost']:
                player['hp'] = min(player.get('max_hp', 100), player['hp'] + npc['value'])
                player['gold'] -= npc['cost']
                text += f"\n✨ **HP Pulih +{npc['value']}**"
            else: 
                return await callback.answer("Gold tidak cukup!", show_alert=True)

        elif npc_type == "gamble":
            if player['gold'] >= npc['bet']:
                win = random.random() < npc['chance']
                reward = npc['bet'] * 2 if win else 0
                player['gold'] = player['gold'] - npc['bet'] + reward
                text += f"\n🎲 {'🎉 Menang!' if win else '💀 Kalah!'}"
            else: 
                return await callback.answer("Gold tidak cukup!", show_alert=True)

        elif npc_type == "lore":
            text += f"\n\n📜 **Lore:** _{random.choice(LORE_STORIES)}_"
            player, quest_msgs = update_quest_progress(player, "move_steps")

        elif npc_type == "gift":
            item = npc['gift_item']
            player.setdefault('inventory', []).append(item)
            text += f"\n🎁 **Dapatkan:** {item.replace('_', ' ').title()}"

        # Simpan perubahan
        update_player(user_id, player)
        
        final_text = text + ("\n\n" + "\n".join(quest_msgs) if quest_msgs else "")
        
        # PERBAIKAN: Hapus pesan lama dan kirim pesan baru untuk mengembalikan keyboard navigasi
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer(final_text, reply_markup=get_main_reply_keyboard(player))

    # B. MESIN BAHAYA MAUT (Deadly Terrains)
    elif data.startswith("exec_deadly_"):
        event_id = "_".join(data.split("_")[2:])
        success, msg = process_deadly_interaction(player, event_id)
        update_player(user_id, player)
        
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer(msg, reply_markup=get_main_reply_keyboard(player))

    # C. MESIN LOKASI (Landmarks)
    elif data.startswith("exec_landmark_"):
        lm_id = "_".join(data.split("_")[2:])
        res, msg = process_landmark_interaction(player, lm_id)
        
        if res == "ambush":
            await callback.message.edit_text(f"⚠️ {msg}")
            # Logika combat manual bisa dipicu di sini
        else:
            update_player(user_id, player)
            try:
                await callback.message.delete()
            except:
                pass
            await callback.message.answer(msg, reply_markup=get_main_reply_keyboard(player))

    # D. ABAIKAN / LANJUT (TRIGGER MOVE QUEST)
    elif data == "evt_ignore":
        player, quest_msgs = update_quest_progress(player, "move_steps")
        update_player(user_id, player)
        
        await state.set_state(GameState.exploring)
        msg = "🏃 Kamu melanjutkan perjalanan."
        if quest_msgs: 
            msg += "\n\n" + "\n".join(quest_msgs)
        
        # Hapus tombol inline dan munculkan kembali menu navigasi bawah
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer(msg, reply_markup=get_main_reply_keyboard(player))

    await callback.answer()
