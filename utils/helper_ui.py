"""
Helper UI untuk membuat tampilan visual yang lebih menarik di Telegram (Mobile Friendly)
"""

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

def create_countdown_visual(seconds_left):
    """Membuat countdown timer yang dramatis"""
    if seconds_left > 40:
        return f"⏱️ `{seconds_left}s` 🟢"
    elif seconds_left > 20:
        return f"⏱️ `{seconds_left}s` 🟡"
    else:
        return f"⏱️ `{seconds_left}s` 🔴 *CEPAT!*"

def format_gold(amount):
    """Format gold dengan separator"""
    return f"💰 {amount:,}".replace(",", ".")

def format_damage(amount):
    """Format damage number dengan style"""
    if amount >= 50:
        return f"💥 *{amount}* DMG"
    elif amount >= 25:
        return f"⚔️ *{amount}* DMG"
    else:
        return f"🗡️ {amount} DMG"

def create_combat_header(monster_name, tier, stage, max_stage):
    """Header combat yang lebih dramatis dan responsif"""
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
    """Membuat status card yang comprehensive dan responsif"""
    card = f"""━━━━━━━━━━━━━━━━━━━━
👤 *{player.get('username', 'Weaver')}*
🔄 Cycle: {player.get('cycle', 1)} | Level: {player.get('level', 1)}
━━━━━━━━━━━━━━━━━━━━
❤️ HP: {create_hp_bar(player['hp'], player['max_hp'], 8)}
🔮 MP: {create_mp_bar(player['mp'], player['max_mp'], 8)}
⭐ EXP: {create_exp_bar(player.get('exp', 0), player.get('exp_needed', 100), 8)}
━━━━━━━━━━━━━━━━━━━━
💰 Gold: {player['gold']:,}
⚔️ Kills: {player.get('kills', 0)}
🏆 Streak: {player.get('win_streak', 0)}
📍 {player.get('location', 'The Whispering Hall')}
━━━━━━━━━━━━━━━━━━━━"""
    return card

def create_achievement_notification(title, description, reward):
    """Notifikasi achievement unlock yang exciting"""
    notif = f"""🎉 *ACHIEVEMENT UNLOCKED!* 🎉

🏆 *{title}*
_{description}_

🎁 Reward: {reward}"""
    return notif

def create_loot_drop(items):
    """Visualisasi loot drop dari monster"""
    if not items:
        return "💨 Tidak ada yang tersisa..."
    
    loot_text = "✨ *LOOT DROP!* ✨\n\n"
    for item in items:
        rarity_emoji = {
            "common": "⚪",
            "uncommon": "🟢",
            "rare": "🔵",
            "epic": "🟣",
            "legendary": "🟡"
        }
        emoji = rarity_emoji.get(item.get('rarity', 'common'), "⚪")
        loot_text += f"{emoji} {item['name']}\n"
    
    return loot_text

def create_level_up_animation(old_level, new_level):
    """Animasi level up yang epik"""
    return f"""✨✨✨✨✨✨✨✨✨✨
🎆 *LEVEL UP!* 🎆
{old_level} ➜ *{new_level}*

📈 Stats meningkat!
🔓 Skill baru tersedia!
✨✨✨✨✨✨✨✨✨✨"""

def create_boss_warning(boss_name):
    """Warning dramatis sebelum boss fight"""
    return f"""⚠️ ━━━━━━━━━━━━━━ ⚠️

        💀 *WARNING* 💀
        
      *{boss_name}*
        DETECTED
      
⚠️ ━━━━━━━━━━━━━━ ⚠️

Udara membeku...
Detak jantungmu melambat...
Ini adalah ujian sesungguhnya."""

def create_death_screen(cause, stats):
    """Death screen yang sinematik"""
    return f"""━━━━━━━━━━━━━━━━━━━━
        💀 *YOU DIED* 💀
━━━━━━━━━━━━━━━━━━━━

Cause of Death:
  {cause}
  
Your Legacy:
  🔄 Cycle: {stats.get('cycle', 1)}
  ⚔️ Kills: {stats.get('kills', 0)}
  💰 Gold Lost: {stats.get('gold_lost', 0)}
  
_"Archivus claims another soul..."_

━━━━━━━━━━━━━━━━━━━━"""

def create_combo_indicator(combo_count):
    """Indikator combo untuk multiple correct answers"""
    if combo_count >= 5:
        return f"🔥🔥🔥 *LEGENDARY COMBO x{combo_count}!* 🔥🔥🔥"
    elif combo_count >= 3:
        return f"⚡⚡ *COMBO x{combo_count}!* ⚡⚡"
    elif combo_count >= 2:
        return f"✨ Combo x{combo_count} ✨"
    else:
        return ""

def create_daily_quest_card(quests):
    """Card untuk daily quests"""
    card = "━━━━━━━━━━━━━━━━━━━━\n📋 *DAILY QUESTS*\n━━━━━━━━━━━━━━━━━━━━\n"
    for i, quest in enumerate(quests, 1):
        status = "✅" if quest.get('completed') else "⏳"
        card += f"{status} {quest['title']}\n"
        card += f"   Progress: {quest['progress']}/{quest['target']}\n"
        
        # Penanganan aman jika struktur reward berubah
        reward_gold = quest['reward'].get('gold', 0) if isinstance(quest['reward'], dict) else quest['reward']
        card += f"   Reward: {reward_gold} Gold\n\n"
    
    card += "━━━━━━━━━━━━━━━━━━━━"
    return card

def create_shop_item_preview(item):
    """Preview item di shop dengan detail"""
    rarity_colors = {
        "common": "⚪",
        "uncommon": "🟢",
        "rare": "🔵",
        "epic": "🟣",
        "legendary": "🟡"
    }
    
    rarity = item.get('rarity', 'common')
    emoji = rarity_colors.get(rarity, "⚪")
    
    preview = f"""{emoji} *{item['name']}* {emoji}
━━━━━━━━━━━━━━━━━━━━
💰 Price: {item['cost']} Gold

📖 Description:
{item.get('description', 'No description available')}

✨ Effect:
{item.get('effect_text', 'Unknown effect')}
━━━━━━━━━━━━━━━━━━━━"""
    return preview

def create_inventory_display(inventory):
    """Tampilan inventory yang organized"""
    if not inventory:
        return "🎒 Inventory kosong seperti jiwa yang terlupakan..."
    
    display = "🎒 *INVENTORY*\n\n"
    
    # Group by type
    weapons = [i for i in inventory if i.get('type') == 'weapon']
    potions = [i for i in inventory if i.get('type') == 'potion']
    artifacts = [i for i in inventory if i.get('type') == 'artifact']
    
    if weapons:
        display += "⚔️ *WEAPONS:*\n"
        for w in weapons:
            display += f"  • {w['name']} (+{w.get('damage', 0)} DMG)\n"
    
    if potions:
        display += "\n🧪 *POTIONS:*\n"
        for p in potions:
            display += f"  • {p['name']} x{p.get('quantity', 1)}\n"
    
    if artifacts:
        display += "\n🔮 *ARTIFACTS:*\n"
        for a in artifacts:
            display += f"  • {a['name']}\n"
    
    return display

def create_location_transition(old_loc, new_loc):
    """Animasi transisi lokasi"""
    return f"""🌫️ ━━━━━━━━━━━━━━ 🌫️

Kabut bergeser...
Realitas terdistorsi...

📍 {old_loc}
      ⬇️
📍 *{new_loc}*

_"Kau memasuki kedalaman baru..."_

🌫️ ━━━━━━━━━━━━━━ 🌫️"""

def create_puzzle_hint_display(question, hint, attempts_left):
    """Tampilan puzzle dengan hint system"""
    display = f"""🧩 *PUZZLE*
━━━━━━━━━━━━━━━━━━━━
{question}

💡 Hint: `{hint}`
🎯 Attempts: {attempts_left}/3
━━━━━━━━━━━━━━━━━━━━"""
    return display
