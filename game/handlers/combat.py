# game/handlers/combat.py
"""
CONTOH REFACTOR COMBAT HANDLER dengan UI yang lebih clean dan mobile-friendly
File ini adalah TEMPLATE - copy relevant parts ke combat.py asli
"""

import asyncio
import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from database import get_player, update_player
from game.logic.states import GameState
from game.logic.stats import calculate_total_stats
from game.logic.menu_handler import get_main_reply_keyboard, get_stance_keyboard

# UI BARU: Import constants untuk konsistensi
from game.ui_constants import Icon, Text, Lang
from utils.helper_ui import (
    create_combat_header,
    create_combat_status,
    create_combo_indicator,
    create_victory_screen,
    create_death_screen,
    create_loot_summary
)

router = Router()

# ==============================================================================
# CONTOH: REFACTOR COMBAT END SCREEN (Victory/Death)
# ==============================================================================

async def execute_end_of_turn_clean(message: Message, state: FSMContext, user_id: int, 
                                    p: dict, enemy_data: dict, full_log: str, 
                                    current_combo: int, battle_msg_id: int):
    """
    Versi CLEAN dari execute_end_of_turn dengan UI yang lebih ringkas
    """
    
    # --- PEMAIN MENANG ---
    if enemy_data['monster_hp'] <= 0:
        # Proses reward
        from game.logic.combat import finalize_battle
        p, loot, quest_notifs = finalize_battle(p, enemy_data)
        
        total_exp = enemy_data['exp_reward']
        old_level = p.get('level', 1)
        p['exp'] += total_exp
        
        from game.systems.progression import calculate_level_from_exp
        new_level = calculate_level_from_exp(p['exp'])
        
        level_up_msg = ""
        if new_level > old_level:
            p['level'] = new_level
            level_up_msg = f"\n\n{Icon.LEVEL} **NAIK LEVEL {new_level}!**"
        
        update_player(user_id, p)
        
        # UI BARU: Lebih ringkas dan terstruktur
        victory_text = (
            f"{Icon.WIN} **MENANG!**\n"
            f"{Text.LINE}\n"
            f"**{enemy_data['monster_name']}** kalah!\n\n"
            f"{create_loot_summary(loot, enemy_data['gold_reward'], total_exp)}\n"
        )
        
        # Tambah combo indicator jika ada
        if current_combo > 1:
            victory_text += f"{create_combo_indicator(current_combo)}\n"
        
        # Tambah quest notif jika ada
        if quest_notifs:
            victory_text += f"\n{Icon.QUEST} Progres misi:\n"
            for notif in quest_notifs[:2]:  # Max 2 notif
                victory_text += f"• {notif}\n"
        
        # Tambah level up jika ada
        victory_text += level_up_msg
        
        # Hapus battle message & reset state
        if battle_msg_id:
            try: 
                await message.bot.delete_message(chat_id=message.chat.id, message_id=battle_msg_id)
            except: 
                pass
        
        await state.set_state(GameState.exploring)
        await message.answer(
            victory_text, 
            reply_markup=get_main_reply_keyboard(p), 
            parse_mode="Markdown"
        )
        return

    # --- PEMAIN MATI ---
    elif p['hp'] <= 0:
        from database import reset_player_death
        death_reason = f"Dibunuh oleh {enemy_data['monster_name']}"
        reset_player_death(user_id, death_reason)
        
        # UI BARU: Death screen yang lebih clean
        death_text = create_death_screen(
            reason=death_reason,
            cycle=p.get('cycle', 1),
            kills=p.get('kills', 0)
        )
        
        await state.set_state(GameState.exploring)
        if battle_msg_id:
            try: 
                await message.bot.delete_message(chat_id=message.chat.id, message_id=battle_msg_id)
            except: 
                pass
        
        await message.answer(
            death_text, 
            reply_markup=get_main_reply_keyboard(p), 
            parse_mode="Markdown"
        )
        return
        
    # --- PERTARUNGAN BERLANJUT ---
    else:
        await state.update_data(enemy_data=enemy_data, current_combo=current_combo)
        
        # UI BARU: Combat screen yang lebih clean
        combat_ui = (
            f"{create_combat_header(enemy_data['monster_name'], enemy_data['monster_hp'], enemy_data.get('monster_max_hp', 100), enemy_data.get('is_boss', False))}\n"
            f"{Text.LINE}\n"
            f"{create_combat_status(p)}\n"
            f"{Text.LINE}\n"
            f"💬 {full_log}"
        )
        
        # Tambah combo indicator jika ada
        if current_combo > 1:
            combat_ui += f"\n{create_combo_indicator(current_combo)}"
        
        if battle_msg_id:
            try:
                await message.bot.edit_message_text(
                    chat_id=message.chat.id, 
                    message_id=battle_msg_id, 
                    text=combat_ui, 
                    parse_mode="Markdown", 
                    reply_markup=get_stance_keyboard(enemy_data.get('is_boss', False))
                )
            except Exception:
                new_battle_msg = await message.answer(
                    combat_ui, 
                    parse_mode="Markdown", 
                    reply_markup=get_stance_keyboard(enemy_data.get('is_boss', False))
                )
                await state.update_data(battle_msg_id=new_battle_msg.message_id)


# ==============================================================================
# CONTOH: COMBAT LOG YANG LEBIH RINGKAS
# ==============================================================================

def create_combat_action_log(action_type, result_data):
    """
    Membuat log combat yang ringkas dan mudah dibaca
    """
    if action_type == "attack":
        damage = result_data.get('damage', 0)
        return f"{Icon.ATTACK} Serang (-{damage} HP)"
    
    elif action_type == "skill":
        skill_name = result_data.get('skill_name', 'Skill')
        damage = result_data.get('damage', 0)
        return f"{Icon.SKILL} {skill_name} (-{damage} HP)"
    
    elif action_type == "defend":
        mitigated = result_data.get('mitigated', 0)
        return f"{Icon.DEFENSE} Bertahan (blokir {mitigated} damage)"
    
    elif action_type == "dodge_success":
        return f"{Icon.DODGE} Menghindar berhasil!"
    
    elif action_type == "dodge_fail":
        damage = result_data.get('damage', 0)
        return f"❌ Gagal menghindar (-{damage} HP)"
    
    elif action_type == "enemy_attack":
        damage = result_data.get('damage', 0)
        return f"👾 Musuh serang (-{damage} HP)"
    
    elif action_type == "poison":
        damage = result_data.get('damage', 0)
        return f"{Icon.POISON} Racun (-{damage} HP)"
    
    return result_data.get('message', '')


# ==============================================================================
# CONTOH: SKILL MENU YANG LEBIH CLEAN
# ==============================================================================

def get_skill_menu_keyboard_clean(player, player_stats):
    """
    Menu skill yang lebih clean dengan info MP cost yang jelas
    """
    from game.logic.skills import get_available_skills, get_effective_skill, get_cooldown_remaining
    
    available_skills = get_available_skills(player, player_stats)
    keyboard = []
    
    for skill_id in available_skills:
        skill = get_effective_skill(player, skill_id)
        if not skill: 
            continue
            
        cooldown = get_cooldown_remaining(player, skill_id)
        mp_cost = skill.get('mp_cost', 0)
        
        if cooldown > 0:
            # Skill masih cooldown
            btn_text = f"⏳ {skill['name']} ({cooldown} turn)"
            cb_data = "ignore_cooldown"
        else:
            # Skill ready
            btn_text = f"{Icon.SKILL} {skill['name']} (MP {mp_cost})"
            cb_data = f"useskill_{skill_id}"
            
        keyboard.append([InlineKeyboardButton(text=btn_text, callback_data=cb_data)])
    
    # Tambah info MP player di footer
    current_mp = player.get('mp', 0)
    max_mp = player.get('max_mp', 50)
    keyboard.append([
        InlineKeyboardButton(
            text=f"{Icon.MP} MP: {current_mp}/{max_mp}", 
            callback_data="show_mp_info"
        )
    ])
    
    keyboard.append([
        InlineKeyboardButton(text=f"{Icon.CLOSE} Tutup", callback_data="close_popup")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# ==============================================================================
# CONTOH: ITEM MENU YANG LEBIH CLEAN
# ==============================================================================

def get_combat_consumable_menu_clean(player):
    """
    Menu item yang lebih clean dengan stacking dan kategori
    """
    from game.items import get_item
    
    buttons = []
    inventory = player.get('inventory', [])
    
    # Kategorisasi dan hitung
    potions = {}
    for item_id in inventory:
        item = get_item(item_id)
        if item and item.get('type') == 'consumable':
            if item.get('effect_type') != "trigger_quiz":
                potions[item_id] = potions.get(item_id, 0) + 1
    
    if not potions:
        buttons.append([
            InlineKeyboardButton(text=Text.BAG_EMPTY, callback_data="close_popup")
        ])
    else:
        # Sort by type: heal > mana > energy
        priority = {'heal_hp': 0, 'restore_mp': 1, 'restore_energy': 2}
        sorted_items = sorted(
            potions.items(), 
            key=lambda x: priority.get(get_item(x[0]).get('effect_type', ''), 99)
        )
        
        for item_id, count in sorted_items:
            item = get_item(item_id)
            effect_type = item.get('effect_type', '')
            
            # Pilih ikon berdasarkan tipe
            if effect_type == 'heal_hp':
                icon = Icon.HP
            elif effect_type == 'restore_mp':
                icon = Icon.MP
            elif effect_type == 'restore_energy':
                icon = Icon.ENERGY
            else:
                icon = Icon.POTION
            
            btn_text = f"{icon} {item['name']} ({count}x)"
            buttons.append([
                InlineKeyboardButton(
                    text=btn_text, 
                    callback_data=f"combat_useitem_{item_id}"
                )
            ])
    
    # Footer info
    buttons.append([
        InlineKeyboardButton(
            text=f"{Icon.CLOSE} Tutup", 
            callback_data="close_popup"
        )
    ])
    
    return buttons


# ==============================================================================
# TIPS PENGGUNAAN
# ==============================================================================

"""
CARA MIGRASI KE UI BARU:

1. Import UI constants:
   from game.ui_constants import Icon, Text, Lang
   from utils.helper_ui import create_*

2. Ganti hardcoded emoji:
   "⚔️" -> Icon.ATTACK
   "💰" -> Icon.GOLD
   
3. Ganti separator:
   "━━━━━━━━━━━" -> Text.LINE
   
4. Pakai helper functions:
   create_combat_header()
   create_combat_status()
   create_loot_summary()
   
5. Buat log lebih ringkas:
   "Kamu menyerang musuh dengan pedang dan memberikan damage sebesar 50" 
   -> "⚔️ Serang (-50 HP)"

6. Konsistensi bahasa:
   "Attack" -> "Serang"
   "Defend" -> "Bertahan"
   "You" -> "Kamu"

7. Test di mobile:
   - Max 40 char per line
   - Pastikan tidak terpotong
   - Spacing cukup
"""
