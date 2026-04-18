# game/logic/event_handler.py

import random
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from game.logic.states import GameState
from database import update_player, add_history
from game.puzzles.manager import generate_puzzle
from game.logic.menu_handler import get_main_reply_keyboard

# Import Data Master
try:
    from game.data.npcs.functional import FUNCTIONAL_NPCS
    from game.data.npcs.storytellers import STORY_NPCS, get_random_story_npc # Database barumu
    from game.data.environment.hazards import HAZARDS_DATA
except ImportError:
    FUNCTIONAL_NPCS = {}
    STORY_NPCS = {}
    HAZARDS_DATA = {}

# --- GENERATOR TOMBOL INTERAKSI ---

def get_event_interaction_kb(event_type, event_data):
    """Membuat tombol berdasarkan jenis event."""
    kb = []
    
    if event_type == "npc":
        cat = event_data.get("category")
        if cat == "story":
            # Ganti teks agar lebih imersif
            kb.append([InlineKeyboardButton(text="🤝 Sapa & Dekati", callback_data="evt_npc_story")])
        elif cat == "quiz":
            kb.append([InlineKeyboardButton(text="📜 Tantang Kecerdasan", callback_data="evt_npc_quiz")])
        elif cat == "functional":
            kb.append([InlineKeyboardButton(text="🤝 Lihat Penawaran", callback_data="evt_npc_func")])
        elif cat == "gamble":
            kb.append([InlineKeyboardButton(text="🎲 Adu Nasib (Judi)", callback_data="evt_npc_gamble")])
        
        kb.append([InlineKeyboardButton(text="🚶 Abaikan", callback_data="evt_ignore")])

    elif event_type == "landmark":
        kb.append([InlineKeyboardButton(text="🔍 Periksa Lokasi", callback_data="evt_landmark_search")])
        kb.append([InlineKeyboardButton(text="➡️ Lanjut Jalan", callback_data="evt_ignore")])

    elif event_type == "hazard":
        if not event_data.get("safe"):
            kb.append([InlineKeyboardButton(text="🎒 Gunakan Item Pemulih", callback_data="menu_consumables")])
        kb.append([InlineKeyboardButton(text="➡️ Bertahan & Lanjut", callback_data="evt_ignore")])

    return InlineKeyboardMarkup(inline_keyboard=kb) if kb else None

# --- LOGIKA EKSEKUSI INTERAKSI ---

async def handle_event_interaction(callback, state, player):
    """Pusat pemrosesan aksi saat tombol di klik"""
    data = callback.data
    user_id = player['user_id']

    # 1. INTERAKSI STORY (GACHA NPC STORYTELLER)
    if data == "evt_npc_story":
        # Ambil NPC acak dari database storytellers.py
        npc_list = list(STORY_NPCS.keys())
        if not npc_list:
            return await callback.answer("Sosok itu menghilang ditiup angin...")
            
        npc_id = random.choice(npc_list)
        npc = STORY_NPCS[npc_id]
        
        roll = random.randint(1, 100)
        greeting = random.choice(npc['dialog_greetings'])
        
        # --- OPSI A: KUIS (40%) ---
        if roll <= 40:
            tier = max(1, min(5, player.get('level', 1) // 10 + 1))
            puzzle = generate_puzzle(tier=tier)
            await state.set_state(GameState.in_event)
            await state.update_data(event_data=puzzle)
            
            text = (
                f"👴 **{npc['name']}**\n"
                f"_{greeting}_\n\n"
                f"\"{puzzle['question']}\"\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"💬 *Ketik jawabanmu...*"
            )
            await callback.message.edit_text(text, parse_mode="Markdown")

        # --- OPSI B: HADIAH ITEM (20%) ---
        elif roll <= 60:
            # Gacha item sederhana (Tenda atau Potion)
            gift_id = random.choice(["tenda", "potion_heal"])
            inventory = player.get('inventory', [])
            inventory.append(gift_id)
            update_player(user_id, {"inventory": inventory})
            
            text = (
                f"🎁 **HADIAH DARI {npc['name'].upper()}**\n"
                f"_{greeting}_\n\n"
                f"\"Perjalananmu masih panjang, Weaver. Bawalah ini.\"\n\n"
                f"📦 **Dapatkan: {gift_id.replace('_', ' ').title()}**"
            )
            await state.set_state(GameState.exploring)
            await callback.message.edit_text(text, reply_markup=get_main_reply_keyboard(player))

        # --- OPSI C: BERKAH / HEAL (20%) ---
        elif roll <= 80:
            heal_amt = 30
            new_hp = min(player.get('max_hp', 100), player['hp'] + heal_amt)
            update_player(user_id, {"hp": new_hp})
            
            text = (
                f"✨ **BERKAH {npc['name'].upper()}**\n"
                f"_{greeting}_\n\n"
                f"Sosok itu meletakkan tangannya di bahumu. Luka-lukamu perlahan menutup.\n\n"
                f"💖 **HP Pulih +{heal_amt}**"
            )
            await state.set_state(GameState.exploring)
            await callback.message.edit_text(text, reply_markup=get_main_reply_keyboard(player))

        # --- OPSI D: LORE / TIPS (20%) ---
        else:
            lore_text = random.choice(npc['lore_episodes'])
            text = (
                f"💬 **BISIKAN {npc['name'].upper()}**\n"
                f"_{greeting}_\n\n"
                f"\"{lore_text}\""
            )
            await state.set_state(GameState.exploring)
            await callback.message.edit_text(text, reply_markup=get_main_reply_keyboard(player))
        
        await callback.answer()

    # 2. INTERAKSI QUIZ UMUM
    elif data == "evt_npc_quiz":
        puzzle = generate_puzzle(tier=random.randint(1, 3))
        await state.set_state(GameState.in_event)
        await state.update_data(event_data=puzzle)
        await callback.message.edit_text(f"📜 **TEKA-TEKI**\n\n{puzzle['question']}", parse_mode="Markdown")

    # 3. INTERAKSI FUNCTIONAL
    elif data == "evt_npc_func":
        if not FUNCTIONAL_NPCS: return await callback.answer("Tidak ada penawaran.")
        npc = FUNCTIONAL_NPCS[random.choice(list(FUNCTIONAL_NPCS.keys()))]
        if player['gold'] >= npc['cost']:
            update_player(user_id, {"hp": min(player['max_hp'], player['hp'] + npc['value']), "gold": player['gold'] - npc['cost']})
            await callback.message.edit_text(f"✨ **{npc['name']}** menyembuhkanmu! (-{npc['cost']}G)")
        else:
            await callback.answer("Gold tidak cukup!", show_alert=True)

    # 4. INTERAKSI GAMBLE
    elif data == "evt_npc_gamble":
        bet = 50
        if player['gold'] >= bet:
            win = random.choice([True, False])
            new_gold = player['gold'] + bet if win else player['gold'] - bet
            update_player(user_id, {"gold": new_gold})
            await callback.message.edit_text(f"🎲 **HASIL JUDI**\n\n{'🎉 Menang! +50G' if win else '💀 Kalah! -50G'}")
        else:
            await callback.answer("Butuh 50 Gold!", show_alert=True)

    # 5. INTERAKSI LANDMARK
    elif data == "evt_landmark_search":
        total_gold = random.randint(20, 100) + (player.get('stats', {}).get('luck', 0) * 2)
        update_player(user_id, {"gold": player['gold'] + total_gold})
        await callback.message.edit_text(f"🔍 **PENCARIAN**\n\nKau menemukan pundi emas!\n💰 **+{total_gold} Gold**")

    # 6. IGNORE / CLOSE
    elif data == "evt_ignore":
        await state.set_state(GameState.exploring)
        try:
            await callback.message.delete()
            await callback.message.answer("🏃 Melanjutkan perjalanan...", reply_markup=get_main_reply_keyboard(player))
        except:
            await callback.message.edit_text("🏃 Kau lanjut melangkah.")
