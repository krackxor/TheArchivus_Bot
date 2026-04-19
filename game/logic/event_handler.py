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
        
        # Berikan teks tombol yang lebih sesuai dengan konteks NPC
        if cat == "scholar":
            kb.append([InlineKeyboardButton(text="📜 Jawab Tantangan", callback_data=f"pool_{cat}")])
        elif cat in ["healer", "mercenary", "trickster"]:
            kb.append([InlineKeyboardButton(text="💰 Bayar / Taruhan", callback_data=f"pool_{cat}")])
        elif cat in ["collector", "curse_eater", "beggar"]:
            kb.append([InlineKeyboardButton(text="🤝 Lakukan Pertukaran", callback_data=f"pool_{cat}")])
        else:
            kb.append([InlineKeyboardButton(text="🤝 Dekati Sosok Itu", callback_data=f"pool_{cat}")])
        
        kb.append([InlineKeyboardButton(text="🚶 Abaikan", callback_data="evt_ignore")])

    elif event_type == "deadly":
        event_id = event_data.get("id")
        kb.append([InlineKeyboardButton(text="🏃 Terjang Bahaya!", callback_data=f"exec_deadly_{event_id}")])
        kb.append([InlineKeyboardButton(text="🔄 Cari Jalan Lain", callback_data="evt_ignore")])

    elif event_type == "landmark":
        lm_id = event_data.get("id")
        kb.append([InlineKeyboardButton(text="🔍 Periksa Lokasi", callback_data=f"exec_landmark_{lm_id}")])
        kb.append([InlineKeyboardButton(text="➡️ Lanjut Jalan", callback_data="evt_ignore")])

    return InlineKeyboardMarkup(inline_keyboard=kb) if kb else None

# --- 2. LOGIKA EKSEKUSI INTERAKSI (THE ENGINE) ---

async def handle_event_interaction(callback, state, player):
    """Pusat pemrosesan aksi modular. Anti-Crash & Full Support 10 NPC Types."""
    data = callback.data
    user_id = player['user_id']
    
    # Ambil atribut pemain dengan fallback 0 agar TIDAK CRASH (KeyError)
    p_gold = player.get('gold', 0)
    p_hp = player.get('hp', 0)
    p_max_hp = player.get('max_hp', 100)
    p_mp = player.get('mp', 0)
    p_max_mp = player.get('max_mp', 50)
    p_inv = player.get('inventory', [])
    
    # A. MESIN NPC POOL (Mendukung 10 Kategori)
    if data.startswith("pool_"):
        category = data.split("_")[1]
        npc_list = NPC_POOL.get(category, NPC_POOL['wanderer'])
        npc = random.choice(npc_list)
        
        text = f"👤 **{npc['name']}**\n\n_{npc['narration']}_\n"
        quest_msgs = []
        npc_type = npc.get("type")
        
        # 1. HEALER
        if npc_type == "heal":
            cost = npc.get('cost', 0)
            if p_gold >= cost:
                player['hp'] = min(p_max_hp, p_hp + npc.get('value', 0))
                player['gold'] = p_gold - cost
                text += f"\n✨ **HP Pulih +{npc.get('value')}** (-{cost} Gold)"
            else: 
                return await callback.answer(f"Butuh {cost} Gold!", show_alert=True)

        # 2. TRICKSTER
        elif npc_type == "gamble":
            bet = npc.get('bet', 0)
            if p_gold >= bet:
                win = random.random() < npc.get('chance', 0.5)
                if win:
                    reward = bet * 2
                    player['gold'] = p_gold - bet + reward
                    text += f"\n🎲 **Kemenangan!** Emasmu bertambah. (+{reward - bet} Gold)"
                else:
                    player['gold'] = p_gold - bet
                    text += f"\n💀 **Kalah.** Emasmu ditelan kegelapan. (-{bet} Gold)"
            else: 
                return await callback.answer(f"Butuh {bet} Gold!", show_alert=True)

        # 3. MERCENARY (Buff Permanen)
        elif npc_type == "buff":
            cost = npc.get('cost', 0)
            if p_gold >= cost:
                player['gold'] = p_gold - cost
                stat_name = npc.get('stat', 'atk')
                val = npc.get('val', 0)
                # Map nama stat ke database
                stat_map = {"atk": "base_p_atk", "def": "base_p_def", "spd": "base_speed"}
                db_stat = stat_map.get(stat_name, "base_p_atk")
                player[db_stat] = player.get(db_stat, 10) + val
                text += f"\n💪 **Kekuatan Baru!** {stat_name.upper()} +{val} (-{cost} Gold)"
            else:
                return await callback.answer(f"Butuh {cost} Gold!", show_alert=True)

        # 4. CURSE EATER (Tukar HP ke MP)
        elif npc_type == "convert":
            hp_loss = npc.get('hp_loss', 0)
            mp_gain = npc.get('mp_gain', 0)
            if p_hp > hp_loss:
                player['hp'] = p_hp - hp_loss
                player['mp'] = min(p_max_mp, p_mp + mp_gain)
                text += f"\n🔮 **Sihir Mengalir!** HP -{hp_loss} | MP +{mp_gain}"
            else:
                return await callback.answer("HP-mu terlalu rendah untuk bertahan dari ini!", show_alert=True)

        # 5. COLLECTOR (Beli Rongsokan)
        elif npc_type == "buy":
            item = npc.get('item_wanted')
            price = npc.get('price', 0)
            sold = False
            
            if item == "any_potion":
                for i in p_inv:
                    if "potion" in i:
                        p_inv.remove(i)
                        player['gold'] = p_gold + price
                        text += f"\n💰 **Terjual!** {i.replace('_', ' ')} ditukar {price} Gold."
                        sold = True
                        break
            elif item in p_inv:
                p_inv.remove(item)
                player['gold'] = p_gold + price
                text += f"\n💰 **Terjual!** {item.replace('_', ' ')} ditukar {price} Gold."
                sold = True

            if not sold:
                return await callback.answer(f"Kau tidak punya barang yang ia inginkan.", show_alert=True)
            player['inventory'] = p_inv

        # 6. BEGGAR (Pengemis)
        elif npc_type == "request":
            item = npc.get('item_needed')
            luck_gain = npc.get('reward_luck', 0)
            if item in p_inv:
                p_inv.remove(item)
                player['base_luck'] = player.get('base_luck', 0) + luck_gain
                text += f"\n🍀 **Kebaikan Terbalas!** Keberuntunganmu meningkat +{luck_gain}."
                player['inventory'] = p_inv
            else:
                return await callback.answer(f"Kau tidak memiliki {item.replace('_', ' ')}.", show_alert=True)

        # 7. SCHOLAR (Kuis Lore)
        elif npc_type == "quiz":
            tier = max(1, min(5, player.get('level', 1) // 10 + 1))
            puzzle = generate_puzzle(tier=tier)
            await state.set_state(GameState.in_event)
            await state.update_data(event_data=puzzle)
            
            quiz_text = (
                f"👤 **{npc['name']}**\n_{npc['narration']}_\n\n"
                f"📜 **TANTANGAN KECERDASAN**\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"\"{puzzle['question']}\"\n\n"
                f"💬 *Ketik jawabanmu sekarang...*"
            )
            # Khusus Quiz, hentikan fungsi di sini karena butuh input teks pemain
            return await callback.message.edit_text(quiz_text, parse_mode="Markdown")

        # 8. GUIDE & LORE KEEPER
        elif npc_type in ["info", "lore"]:
            text += f"\n\n📜 *Sebuah pengetahuan telah terserap ke dalam benakmu.*"
            player, quest_msgs = update_quest_progress(player, "move_steps")

        # 9. WANDERER (Hadiah)
        elif npc_type == "gift":
            item = npc.get('gift_item')
            if item:
                p_inv.append(item)
                player['inventory'] = p_inv
                text += f"\n🎁 **Dapatkan:** {item.replace('_', ' ').title()}"

        # AKHIRI INTERAKSI NPC & RESET STATE
        await state.set_state(GameState.exploring)
        update_player(user_id, player)
        
        final_text = text + ("\n\n" + "\n".join(quest_msgs) if quest_msgs else "")
        try: await callback.message.delete()
        except: pass
        await callback.message.answer(final_text, reply_markup=get_main_reply_keyboard(player))

    # B. MESIN BAHAYA MAUT (Deadly Terrains)
    elif data.startswith("exec_deadly_"):
        event_id = data.replace("exec_deadly_", "")
        success, msg = process_deadly_interaction(player, event_id)
        
        await state.set_state(GameState.exploring)
        update_player(user_id, player)
        
        try: await callback.message.delete()
        except: pass
        await callback.message.answer(msg, reply_markup=get_main_reply_keyboard(player))

    # C. MESIN LOKASI (Landmarks)
    elif data.startswith("exec_landmark_"):
        lm_id = data.replace("exec_landmark_", "")
        res, msg = process_landmark_interaction(player, lm_id)
        
        if res == "ambush":
            # Jika ambush, biarkan battle handler yang bekerja (jangan reset state)
            await callback.message.edit_text(f"⚠️ {msg}")
        else:
            await state.set_state(GameState.exploring)
            update_player(user_id, player)
            try: await callback.message.delete()
            except: pass
            await callback.message.answer(msg, reply_markup=get_main_reply_keyboard(player))

    # D. ABAIKAN / LANJUT JALAN
    elif data == "evt_ignore":
        player, quest_msgs = update_quest_progress(player, "move_steps")
        update_player(user_id, player)
        
        await state.set_state(GameState.exploring)
        msg = "🏃 Kamu melangkah ke dalam kabut."
        if quest_msgs: 
            msg += "\n\n" + "\n".join(quest_msgs)
        
        try: await callback.message.delete()
        except: pass
        await callback.message.answer(msg, reply_markup=get_main_reply_keyboard(player))

    await callback.answer()
