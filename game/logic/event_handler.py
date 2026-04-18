# game/logic/event_handler.py

import random
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from game.logic.states import GameState
from database import update_player, add_history
from game.puzzles.manager import generate_puzzle

# Import Data Master (Gunakan try-except agar tidak crash jika file belum ada)
try:
    from game.data.npcs.functional import FUNCTIONAL_NPCS
    from game.data.npcs.gamblers import GAMBLERS
    from game.data.environment.hazards import HAZARDS_DATA
except ImportError:
    FUNCTIONAL_NPCS = {}
    GAMBLERS = {}
    HAZARDS_DATA = {}

# --- GENERATOR TOMBOL INTERAKSI ---

def get_event_interaction_kb(event_type, event_data):
    """Membuat tombol berdasarkan jenis event yang muncul dari exploration.py"""
    kb = []
    
    if event_type == "npc":
        cat = event_data.get("category")
        if cat == "quiz":
            kb.append([InlineKeyboardButton(text="📜 Tantang Kecerdasan", callback_data="evt_npc_quiz")])
        elif cat == "functional":
            kb.append([InlineKeyboardButton(text="🤝 Lihat Penawaran", callback_data="evt_npc_func")])
        elif cat == "gamble":
            kb.append([InlineKeyboardButton(text="🎲 Adu Nasib (Judi)", callback_data="evt_npc_gamble")])
        elif cat == "story":
            kb.append([InlineKeyboardButton(text="👂 Dengarkan Lore", callback_data="evt_npc_story")])
        
        kb.append([InlineKeyboardButton(text="🚶 Abaikan", callback_data="evt_ignore")])

    elif event_type == "landmark":
        kb.append([InlineKeyboardButton(text="🔍 Periksa Lokasi", callback_data="evt_landmark_search")])
        kb.append([InlineKeyboardButton(text="➡️ Lanjut Jalan", callback_data="evt_ignore")])

    elif event_type == "hazard":
        # Jika terluka, beri tombol cepat ke tas
        if not event_data.get("safe"):
            kb.append([InlineKeyboardButton(text="🎒 Gunakan Item Pemulih", callback_data="menu_consumables")])
        kb.append([InlineKeyboardButton(text="➡️ Bertahan & Lanjut", callback_data="evt_ignore")])

    return InlineKeyboardMarkup(inline_keyboard=kb) if kb else None

# --- LOGIKA EKSEKUSI INTERAKSI ---

async def handle_event_interaction(callback, state, player):
    """Pusat pemrosesan aksi saat tombol di klik"""
    data = callback.data
    user_id = player['user_id']

    # 1. INTERAKSI QUIZ
    if data == "evt_npc_quiz":
        puzzle = generate_puzzle(tier=random.randint(1, 3))
        await state.set_state(GameState.in_event)
        await state.update_data(event_data=puzzle)
        
        text = (
            "📜 **TEKA-TEKI PENJAGA**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"*{puzzle['question']}*\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "💬 *Ketik jawabanmu...*"
        )
        await callback.message.edit_text(text, parse_mode="Markdown")

    # 2. INTERAKSI FUNCTIONAL (Heal/Trade)
    elif data == "evt_npc_func":
        # Ambil satu NPC fungsional acak
        npc_id = random.choice(list(FUNCTIONAL_NPCS.keys()))
        npc = FUNCTIONAL_NPCS[npc_id]
        
        if npc['action_type'] == "heal":
            if player['gold'] >= npc['cost']:
                new_hp = min(player.get('max_hp', 100), player['hp'] + npc['value'])
                update_player(user_id, {"hp": new_hp, "gold": player['gold'] - npc['cost']})
                await callback.message.edit_text(f"✨ **{npc['name']}** telah menyembuhkanmu!\n💰 -{npc['cost']} Gold")
            else:
                await callback.answer("❌ Gold tidak cukup!", show_alert=True)

    # 3. INTERAKSI GAMBLE (Simple Coinflip)
    elif data == "evt_npc_gamble":
        bet = 50
        if player['gold'] >= bet:
            win = random.choice([True, False])
            new_gold = player['gold'] + bet if win else player['gold'] - bet
            update_player(user_id, {"gold": new_gold})
            
            res_text = f"🎉 Menang! +{bet}G" if win else f"💀 Kalah! -{bet}G"
            await callback.message.edit_text(f"🎲 **HASIL JUDI**\n\n{res_text}\n💰 Sisa Gold: {new_gold}")
        else:
            await callback.answer("❌ Butuh minimal 50 Gold!", show_alert=True)

    # 4. INTERAKSI LANDMARK (Looting)
    elif data == "evt_landmark_search":
        found_gold = random.randint(20, 150)
        luck = player.get('stats', {}).get('luck', 0)
        
        # Bonus keberuntungan
        total_gold = found_gold + (luck * 2)
        update_player(user_id, {"gold": player.get('gold', 0) + total_gold})
        
        await callback.message.edit_text(
            f"🔍 **PENCARIAN**\n\nKau menemukan pundi emas tersembunyi!\n💰 **+{total_gold} Gold**"
        )

    # 5. IGNORE / CLOSE
    elif data == "evt_ignore":
        try:
            await callback.message.delete()
        except:
            await callback.message.edit_text("🏃 Kau memilih untuk tidak peduli dan lanjut melangkah.")
