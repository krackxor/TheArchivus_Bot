# game/logic/event_handler.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from game.logic.states import GameState
from game.puzzles.manager import generate_puzzle
import random

def get_event_interaction_kb(event_type, event_data):
    """
    Menghasilkan tombol interaksi berdasarkan tipe event yang dikirim exploration.py
    """
    kb = []
    
    if event_type == "npc":
        category = event_data.get("category")
        if category == "quiz":
            kb.append([InlineKeyboardButton(text="📜 Terima Tantangan", callback_data="npc_interact_quiz")])
        elif category == "story":
            kb.append([InlineKeyboardButton(text="👂 Dengarkan Cerita", callback_data="npc_interact_story")])
        elif category == "guide":
            kb.append([InlineKeyboardButton(text="🗺️ Tanya Jalan", callback_data="npc_interact_guide")])
        
        kb.append([InlineKeyboardButton(text="🚶 Abaikan", callback_data="npc_ignore")])

    elif event_type == "hazard":
        if not event_data.get("safe"):
            # Jika terkena hazard, beri tombol cepat ke tas
            kb.append([InlineKeyboardButton(text="🎒 Buka Tas (Obati)", callback_data="menu_consumables")])
        kb.append([InlineKeyboardButton(text="➡️ Lanjut", callback_data="close_popup")])

    elif event_type == "landmark":
        kb.append([InlineKeyboardButton(text="🔍 Periksa Lokasi", callback_data="npc_interact_landmark")])
        kb.append([InlineKeyboardButton(text="🚶 Lewati", callback_data="close_popup")])

    return InlineKeyboardMarkup(inline_keyboard=kb) if kb else None

async def handle_npc_interaction(callback, state, player):
    """
    Logika eksekusi saat tombol interaksi NPC diklik.
    """
    data = callback.data
    
    if data == "npc_interact_quiz":
        puzzle = generate_puzzle(tier=random.randint(1, 3))
        await state.set_state(GameState.in_event)
        await state.update_data(event_data=puzzle)
        
        text = (
            "📜 **TEKA-TEKI PENJAGA**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"*{puzzle['question']}*\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "💬 *Ketik jawabanmu sekarang...*"
        )
        await callback.message.edit_text(text, parse_mode="Markdown")

    elif data == "npc_interact_story":
        # Contoh interaksi storyteller (bisa nambah EXP/Intel sedikit)
        from database import update_player
        intel_gain = 2
        update_player(player['user_id'], {"intelligence": player.get("intelligence", 10) + intel_gain})
        
        text = (
            "📖 **CERITA KUNO**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Pria tua itu menceritakan tentang runtuhnya peradaban Weaver sebelum Archivus tercipta. "
            "Kau merasa sedikit lebih bijaksana.\n\n"
            "🧠 **Intelligence +2**"
        )
        await callback.message.edit_text(text, parse_mode="Markdown")

    elif data == "npc_interact_landmark":
        # Landmark bisa berisi Gold tersembunyi
        from database import update_player
        found_gold = random.randint(50, 200)
        update_player(player['user_id'], {"gold": player.get("gold", 0) + found_gold})
        
        await callback.message.edit_text(
            f"🔍 **EKSPLORASI LOKASI**\n\nKau menggeledah sudut reruntuhan dan menemukan pundi emas kuno!\n\n💰 **Gold +{found_gold}**",
            parse_mode="Markdown"
        )
