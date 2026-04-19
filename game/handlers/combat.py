# game/handlers/combat.py

import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

# === LOGIC & DATABASE ===
from database import get_player, update_player, reset_player_death
from game.logic.states import GameState
from game.logic.stats import calculate_total_stats
from game.logic.menu_handler import get_main_reply_keyboard, get_stance_keyboard

# === UI & CONSTANTS ===
from game.ui_constants import Icon, Text, get_text
from utils.helper_ui import (
    create_combat_header,
    create_combat_status,
    create_combo_indicator,
    create_death_screen,
    create_loot_summary
)

router = Router()

# ==============================================================================
# 1. CORE COMBAT UI (LOG & MENUS)
# ==============================================================================

def create_combat_action_log(lang, action_type, result_data):
    """Membuat log combat yang ringkas dan mudah dibaca."""
    damage = result_data.get('damage', 0)
    
    if action_type == "attack":
        return f"{Icon.ATTACK} {get_text(lang, 'CMD_ATTACK')} (-{damage} {Icon.HP})"
    elif action_type == "skill":
        skill_name = result_data.get('skill_name', 'Skill')
        return f"{Icon.SKILL} {skill_name} (-{damage} {Icon.HP})"
    elif action_type == "defend":
        mitigated = result_data.get('mitigated', 0)
        return f"{Icon.DEFENSE} {get_text(lang, 'CMD_DEFEND')} (Blokir {mitigated} DMG)"
    elif action_type == "dodge_success":
        return f"{Icon.DODGE} {get_text(lang, 'CMD_DODGE')} berhasil!"
    elif action_type == "dodge_fail":
        return f"❌ Gagal menghindar (-{damage} {Icon.HP})"
    elif action_type == "enemy_attack":
        return f"{Icon.MONSTER} Musuh menyerang (-{damage} {Icon.HP})"
    elif action_type == "poison":
        return f"{Icon.ST_POISON} Racun (-{damage} {Icon.HP})"
        
    return result_data.get('message', '')

# ==============================================================================
# 2. COMBAT RESOLUTION (MENANG / MATI)
# ==============================================================================

async def execute_end_of_turn(callback: CallbackQuery, state: FSMContext, user_id: int, 
                              p: dict, enemy_data: dict, full_log: str, 
                              current_combo: int, battle_msg_id: int):
    """Menangani akhir giliran: Apakah musuh mati, pemain mati, atau lanjut."""
    lang = p.get('lang', 'id')
    
    # --- PEMAIN MENANG ---
    if enemy_data.get('monster_hp', 0) <= 0:
        # (Mock) Menggunakan logika finalize_battle dari backend
        try:
            from game.logic.combat import finalize_battle
            p, loot, quest_notifs = finalize_battle(p, enemy_data)
        except ImportError:
            loot, quest_notifs = [], []
            p['gold'] = p.get('gold', 0) + enemy_data.get('gold_reward', 10)
            
        total_exp = enemy_data.get('exp_reward', 20)
        old_level = p.get('level', 1)
        p['exp'] += total_exp
        
        try:
            from game.systems.progression import calculate_level_from_exp
            new_level = calculate_level_from_exp(p['exp'])
        except ImportError:
            new_level = old_level
            
        level_up_msg = ""
        if new_level > old_level:
            p['level'] = new_level
            p['stat_points'] += 3
            level_up_msg = f"\n\n{Icon.LEVEL} **NAIK LEVEL {new_level}!**\n+3 Stat Points"
            
        update_player(user_id, p)
        
        # UI Kemenangan
        victory_text = (
            f"{Icon.SUCCESS} **MENANG!**\n"
            f"{Text.LINE}\n"
            f"**{enemy_data.get('monster_name', 'Musuh')}** telah tumbang!\n\n"
            f"{create_loot_summary(loot, enemy_data.get('gold_reward', 0), total_exp)}\n"
        )
        
        if current_combo > 1:
            victory_text += f"{create_combo_indicator(current_combo)}\n"
            
        if quest_notifs:
            victory_text += f"\n{Icon.QUEST} Progres Misi:\n"
            for notif in quest_notifs[:2]:  # Max 2 notif agar tidak spam
                victory_text += f"• {notif}\n"
                
        victory_text += level_up_msg
        
        await state.set_state(GameState.exploring)
        if battle_msg_id:
            try: await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=battle_msg_id)
            except: pass
            
        await callback.message.answer(victory_text, reply_markup=get_main_reply_keyboard(p))
        return

    # --- PEMAIN MATI ---
    elif p.get('hp', 0) <= 0:
        death_reason = f"Dibunuh oleh {enemy_data.get('monster_name', 'Entitas Gelap')}"
        death_msg = reset_player_death(user_id, death_reason)
        
        await state.set_state(GameState.exploring)
        if battle_msg_id:
            try: await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=battle_msg_id)
            except: pass
            
        await callback.message.answer(death_msg, reply_markup=get_main_reply_keyboard(p))
        return
        
    # --- PERTARUNGAN BERLANJUT ---
    else:
        await state.update_data(enemy_data=enemy_data, current_combo=current_combo)
        
        combat_ui = (
            f"{create_combat_header(enemy_data['monster_name'], enemy_data['monster_hp'], enemy_data.get('monster_max_hp', 100), enemy_data.get('is_boss', False))}\n"
            f"{Text.LINE}\n"
            f"{create_combat_status(p)}\n"
            f"{Text.LINE}\n"
            f"💬 {full_log}"
        )
        
        if current_combo > 1:
            combat_ui += f"\n{create_combo_indicator(current_combo)}"
            
        is_boss = enemy_data.get('is_boss', False)
        
        if battle_msg_id:
            try:
                await callback.message.edit_text(
                    text=combat_ui, 
                    reply_markup=get_stance_keyboard(is_boss)
                )
            except Exception:
                pass

# ==============================================================================
# 3. HANDLERS (MENANGKAP TOMBOL STANCE)
# ==============================================================================

@router.callback_query(GameState.in_combat, F.data.startswith("stance_"))
async def combat_action_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    action = callback.data.replace("stance_", "")
    
    data = await state.get_data()
    enemy_data = data.get("enemy_data", {})
    current_combo = data.get("current_combo", 0)
    battle_msg_id = data.get("battle_msg_id", callback.message.message_id)
    
    p = get_player(user_id)
    lang = p.get('lang', 'id')
    
    # --- JIKA PEMAIN KABUR ---
    if action == "run":
        if enemy_data.get('is_boss', False):
            return await callback.answer("❌ Kamu tidak bisa kabur dari BOSS!", show_alert=True)
            
        # Hitung peluang kabur (Agility check)
        escape_chance = 50 + (p.get('stats', {}).get('speed', 10) - enemy_data.get('speed', 10))
        import random
        
        if random.randint(1, 100) <= escape_chance:
            await state.set_state(GameState.exploring)
            try: await callback.message.delete()
            except: pass
            
            await callback.message.answer(
                f"🏃 **BERHASIL KABUR!**\nKamu melarikan diri ke dalam kegelapan...",
                reply_markup=get_main_reply_keyboard(p)
            )
            return
        else:
            action_log = "❌ Gagal melarikan diri!"
            enemy_dmg = max(1, enemy_data.get('p_atk', 10) - p.get('stats', {}).get('p_def', 5))
            p['hp'] -= enemy_dmg
            enemy_log = create_combat_action_log(lang, "enemy_attack", {"damage": enemy_dmg})
            full_log = f"{action_log}\n{enemy_log}"
            
            await execute_end_of_turn(callback, state, user_id, p, enemy_data, full_log, 0, battle_msg_id)
            return

    # --- JIKA PEMAIN MENYERANG/BERTAHAN ---
    # Di sini Anda bisa memanggil `process_turn(p, enemy_data, action)` dari backend logic Anda.
    # Untuk kelengkapan, ini adalah simulasi dasar logic:
    
    player_dmg = 0
    enemy_dmg = 0
    action_log = ""
    
    if action == "attack":
        player_dmg = max(1, p.get('stats', {}).get('p_atk', 10) - enemy_data.get('p_def', 5))
        enemy_data['monster_hp'] -= player_dmg
        current_combo += 1
        action_log = create_combat_action_log(lang, "attack", {"damage": player_dmg})
        
    elif action == "block":
        current_combo = 0
        action_log = create_combat_action_log(lang, "defend", {"mitigated": p.get('stats', {}).get('p_def', 5)})
        
    elif action == "dodge":
        current_combo = 0
        action_log = create_combat_action_log(lang, "dodge_success", {})
        
    # Giliran Musuh Menyerang (Jika masih hidup)
    enemy_log = ""
    if enemy_data.get('monster_hp', 0) > 0:
        if action == "block":
            enemy_dmg = max(1, (enemy_data.get('p_atk', 10) // 2) - p.get('stats', {}).get('p_def', 5))
        elif action == "dodge":
            enemy_dmg = 0 # Asumsi berhasil
        else:
            enemy_dmg = max(1, enemy_data.get('p_atk', 10) - p.get('stats', {}).get('p_def', 5))
            
        p['hp'] -= enemy_dmg
        if enemy_dmg > 0:
            enemy_log = create_combat_action_log(lang, "enemy_attack", {"damage": enemy_dmg})
            
    full_log = f"{action_log}\n{enemy_log}" if enemy_log else action_log
    
    # Resolusi Akhir Giliran
    await execute_end_of_turn(callback, state, user_id, p, enemy_data, full_log, current_combo, battle_msg_id)
