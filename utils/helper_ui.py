"""
Helper UI untuk membuat tampilan visual yang lebih menarik di Telegram (Mobile Friendly)
Terintegrasi penuh dengan GDD Final (Durability, Element, Skill)
"""
from game.systems.combat import calculate_equipment_stats

def create_hp_bar(current, maximum, length=10):
    """Membuat HP bar visual seperti game"""
    filled = int((current / maximum) * length)
    empty = length - filled
    
    # Warna berdasarkan persentase
    if current / maximum > 0.7:
        bar_char = "🟩"
    elif current / maximum > 0.3:
        bar_char = "🟨"
    else:
        bar_char = "🟥"
    
    bar = bar_char * filled + "⬜" * empty
    percentage = int((current / maximum) * 100)
    return f"{bar} {current}/{maximum} ({percentage}%)"

def create_mp_bar(current, maximum, length=10):
    """Membuat MP bar visual"""
    filled = int((current / maximum) * length)
    empty = length - filled
    bar = "🟦" * filled + "⬜" * empty
    percentage = int((current / maximum) * 100)
    return f"{bar} {current}/{maximum} ({percentage}%)"

def create_exp_bar(current, needed, length=10):
    """Membuat EXP bar untuk progression"""
    filled = int((current / needed) * length)
    empty = length - filled
    bar = "🟪" * filled + "⬜" * empty
    return f"{bar} {current}/{needed}"

def format_gold(amount):
    """Format gold dengan separator"""
    return f"💰 {amount:,}".replace(",", ".")

def create_combat_header(monster_name, tier, stage, max_stage):
    """Header combat yang dramatis dan responsif"""
    tier_emoji = {
        1: "⚪",
        2: "🟢", 
        3: "🔵",
        4: "🟣",
        5: "🔴",
        "BOSS": "💀",
        "MINI BOSS": "👹"
    }
    
    emoji = tier_emoji.get(tier, "⚪")
    
    header = f"""━━━━━━━━━━━━━━━━━━━━
{emoji} *{monster_name}* {emoji}
📊 Tier: {tier} | Wave: {stage}/{max_stage}
━━━━━━━━━━━━━━━━━━━━"""
    return header

def create_status_card(player):
    """Membuat status card yang komprehensif, membaca Durability & Element terbaru"""
    # Kalkulasi stat equipment (otomatis potong durability 0)
    stats = calculate_equipment_stats(player)
    
    base_atk = player.get('base_atk', 10)
    base_def = player.get('base_def', 0)
    bonus_atk = stats['atk'] - base_atk
    bonus_def = stats['def'] - base_def
    
    # Cek apakah ada buff Resin aktif
    resin_txt = ""
    if player.get('active_resin') and player.get('resin_duration', 0) > 0:
        resin_txt = f"\n📜 *Mantra Aktif:* {player['active_resin']} ({player['resin_duration']} Turn)"

    card = f"""━━━━━━━━━━━━━━━━━━━━
👤 *{player.get('username', 'Weaver')}*
🔄 Cycle: {player.get('cycle', 1)} | Level: {player.get('level', 1)}
━━━━━━━━━━━━━━━━━━━━
⚔️ *Atk:* {base_atk} (+{bonus_atk}) = {stats['atk']}
🛡️ *Def:* {base_def} (+{bonus_def}) = {stats['def']}
⚖️ *Berat:* {stats['weight']} | 💨 *Speed:* {stats['speed'].capitalize()}
✨ *Elemen:* {stats['element']}{resin_txt}

❤️ HP: {create_hp_bar(player['hp'], player['max_hp'], 8)}
🔮 MP: {create_mp_bar(player['mp'], player['max_mp'], 8)}
⭐ EXP: {create_exp_bar(player.get('exp', 0), player.get('exp_needed', 100), 8)}
━━━━━━━━━━━━━━━━━━━━
💰 Gold: {player.get('gold', 0):,}
💀 Kills: {player.get('kills', 0)}
📍 {player.get('location', 'The Whispering Hall')}
━━━━━━━━━━━━━━━━━━━━"""
    return card

def create_achievement_notification(title, description, reward):
    return f"🎉 *ACHIEVEMENT UNLOCKED!* 🎉\n\n🏆 *{title}*\n_{description}_\n\n🎁 Reward: {reward}"

def create_loot_drop(items):
    """Visualisasi loot drop dari monster"""
    if not items:
        return "💨 Tidak ada yang tersisa..."
    
    loot_text = "✨ *LOOT DROP!* ✨\n"
    for item in items:
        loot_text += f"🎁 {item['name']}\n"
    
    return loot_text

def create_level_up_animation(old_level, new_level):
    return f"""✨✨✨✨✨✨✨✨✨✨
🎆 *LEVEL UP!* 🎆
{old_level} ➜ *{new_level}*

📈 Stats meningkat!
✨✨✨✨✨✨✨✨✨✨"""

def create_boss_warning(boss_name):
    return f"""⚠️ ━━━━━━━━━━━━━━ ⚠️
        💀 *WARNING* 💀
        
      *{boss_name}*
        DETECTED
      
⚠️ ━━━━━━━━━━━━━━ ⚠️

Udara membeku...
Detak jantungmu melambat...
Ini adalah ujian sesungguhnya."""

def create_death_screen(cause, stats):
    return f"""━━━━━━━━━━━━━━━━━━━━
        💀 *YOU DIED* 💀
━━━━━━━━━━━━━━━━━━━━

Penyebab:
  {cause}
  
Legacy-mu:
  🔄 Cycle: {stats.get('cycle', 1)}
  ⚔️ Kills: {stats.get('kills', 0)}
  💰 Gold Lost: {stats.get('gold_lost', 0)}
  
_"Archivus menarik jiwa yang lain..."_
━━━━━━━━━━━━━━━━━━━━"""

def create_combo_indicator(combo_count):
    if combo_count >= 5: return f"🔥🔥🔥 *LEGENDARY COMBO x{combo_count}!* 🔥🔥🔥"
    elif combo_count >= 3: return f"⚡⚡ *COMBO x{combo_count}!* ⚡⚡"
    elif combo_count >= 2: return f"✨ Combo x{combo_count} ✨"
    return ""

def create_daily_quest_card(quests):
    card = "━━━━━━━━━━━━━━━━━━━━\n📋 *DAILY QUESTS*\n━━━━━━━━━━━━━━━━━━━━\n"
    for i, quest in enumerate(quests, 1):
        status = "✅" if quest.get('completed') else "⏳"
        card += f"{status} {quest['title']}\n"
        card += f"   Progress: {quest['progress']}/{quest['target']}\n"
        reward_gold = quest['reward'].get('gold', 0) if isinstance(quest['reward'], dict) else quest['reward']
        card += f"   Reward: {reward_gold} Gold\n\n"
    card += "━━━━━━━━━━━━━━━━━━━━"
    return card

def create_inventory_display(inventory):
    """Tampilan inventory yang membaca Durability dan tipe Equip"""
    if not inventory:
        return "🎒 *INVENTORY KOSONG*\nKumpulkan item untuk bertahan hidup."
    
    display = "🎒 *INVENTORY*\n━━━━━━━━━━━━━━━━━━━━\n"
    
    equip_types = ['weapon', 'shield', 'chest', 'head', 'gloves', 'boots']
    equips = [i for i in inventory if i.get('type') in equip_types]
    consumables = [i for i in inventory if i.get('type') == 'potion']
    
    if equips:
        display += "🛡️ *EQUIPMENT*\n"
        for e in equips:
            dur = e.get('durability', 0)
            max_dur = e.get('max_durability', 50)
            
            # Cek status barang
            if dur <= 0:
                status_icon = "❌ (RUSAK)"
            elif dur <= 10:
                status_icon = "⚠️ (Retak)"
            else:
                status_icon = "✅"
                
            skill_info = f" | ⚡ Skill: {e['skill']['name']}" if e.get('skill') else ""
            stat_info = f"+{e.get('bonus_atk')} Atk" if e.get('type') == 'weapon' else f"+{e.get('bonus_def')} Def"
            
            display += f"• *{e['name']}* ({stat_info})\n  └ {status_icon} Durability: {dur}/{max_dur}{skill_info}\n"
        display += "\n"
        
    if consumables:
        display += "🧪 *CONSUMABLES*\n"
        # Hitung kuantitas item yang sama
        item_counts = {}
        for c in consumables:
            name = c['name']
            item_counts[name] = item_counts.get(name, 0) + 1
            
        for name, count in item_counts.items():
            display += f"• {name} (x{count})\n"
            
    display += "━━━━━━━━━━━━━━━━━━━━\n_Gunakan Repair Kit untuk memperbaiki Equip._"
    return display

def create_location_transition(old_loc, new_loc):
    return f"""🌫️ ━━━━━━━━━━━━━━ 🌫️
Kabut bergeser...
Realitas terdistorsi...

📍 {old_loc}
     ⬇️
📍 *{new_loc}*

_"Kau memasuki kedalaman baru..."_
🌫️ ━━━━━━━━━━━━━━ 🌫️"""
