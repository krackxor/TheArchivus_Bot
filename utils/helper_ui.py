# utils/helper_ui.py

"""
Helper UI untuk membuat tampilan visual yang lebih menarik di Telegram (Mobile Friendly)
Terintegrasi penuh dengan GDD Final (Durability, Element, Skill, Artifacts, Energy, dan Debuffs)
"""
from game.logic.stats import calculate_total_stats
from game.items import get_item # Tambahkan ini untuk membaca item dari database

def create_hp_bar(current, maximum, length=10):
    """Membuat HP bar visual seperti game"""
    if maximum <= 0: maximum = 1
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
    return f"{bar} {int(current)}/{int(maximum)} ({percentage}%)"

def create_mp_bar(current, maximum, length=10):
    """Membuat MP bar visual"""
    if maximum <= 0: maximum = 1
    filled = int((current / maximum) * length)
    empty = length - filled
    bar = "🟦" * filled + "⬜" * empty
    percentage = int((current / maximum) * 100)
    return f"{bar} {int(current)}/{int(maximum)} ({percentage}%)"

def create_energy_bar(current, maximum, length=10):
    """Membuat Energy bar visual untuk status survival"""
    if maximum <= 0: maximum = 1
    filled = int((current / maximum) * length)
    empty = length - filled
    bar = "🟧" * filled + "⬜" * empty
    percentage = int((current / maximum) * 100)
    return f"{bar} {int(current)}/{int(maximum)} ({percentage}%)"

def create_exp_bar(current, needed, length=10):
    """Membuat EXP bar untuk progression"""
    if needed <= 0: needed = 1
    filled = int((current / needed) * length)
    empty = length - filled
    bar = "🟪" * filled + "⬜" * empty
    return f"{bar} {int(current)}/{int(needed)}"

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

def create_monster_card(monster_name, element, hp, max_hp):
    """UI Monster yang bersih dan minimalis"""
    monster_mana = max_hp // 2 
    
    return f"""🦇 *{monster_name}*
✨ Elemen: {element.capitalize()}
❤️ HP:   {create_hp_bar(hp, max_hp, 8)}
💧 Mana: {create_mp_bar(monster_mana, monster_mana, 8)}"""

def create_status_card(player):
    """Membuat status card komprehensif (Sudah menggunakan logic stat yang baru)"""
    stats = calculate_total_stats(player)
    
    base_p_atk = player.get('base_p_atk', 10)
    base_p_def = player.get('base_p_def', 5)
    
    bonus_atk = stats['p_atk'] - base_p_atk
    bonus_def = stats['p_def'] - base_p_def
    
    resin_txt = ""
    if player.get('active_resin') and player.get('resin_duration', 0) > 0:
        resin_txt = f"\n📜 *Mantra:* {player['active_resin']} ({player['resin_duration']} Turn)"
        
    debuff_txt = ""
    debuffs = player.get('debuffs', [])
    if debuffs:
        debuff_txt = f"\n⚠️ *STATUS BURUK:* {', '.join([d.upper() for d in debuffs])}"

    card = f"""━━━━━━━━━━━━━━━━━━━━
👤 *{player.get('username', 'Weaver')}*
🎖️ Class: {player.get('current_job', 'Novice Weaver')}
🔄 Cycle: {player.get('cycle', 1)} | Level: {player.get('level', 1)}
━━━━━━━━━━━━━━━━━━━━
⚔️ *Atk:* {base_p_atk} (+{bonus_atk}) = {stats['p_atk']}
🛡️ *Def:* {base_p_def} (+{bonus_def}) = {stats['p_def']}
⚖️ *Berat:* {stats['total_weight']} | 💨 *Speed:* {stats['speed']}
✨ *Elemen:* {stats['element'].capitalize()}{resin_txt}{debuff_txt}

❤️ HP:  {create_hp_bar(player.get('hp', 0), player.get('max_hp', 100), 8)}
🔮 MP:  {create_mp_bar(player.get('mp', 0), player.get('max_mp', 50), 8)}
⚡ EN:  {create_energy_bar(player.get('energy', 100), player.get('max_energy', 100), 8)}
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
        # Pengecekan cerdas untuk format dictionary atau string list
        if isinstance(item, dict) and item.get("type") == "gold":
            loot_text += f"💰 {item['value']} Gold\n"
        elif isinstance(item, dict):
            loot_text += f"🎁 {item.get('name', 'Unknown Item')}\n"
        elif isinstance(item, str):
            # Tarik nama asli dari item DB jika berupa string ID
            item_data = get_item(item)
            name = item_data['name'] if item_data else item.replace("_", " ").title()
            loot_text += f"🎁 {name}\n"
            
    return loot_text

def create_level_up_animation(old_level, new_level):
    return f"""✨✨✨✨✨✨✨✨✨✨
🎆 *LEVEL UP!* 🎆
{old_level} ➜ *{new_level}*

📈 Kekuatanmu bertambah!
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

def create_inventory_display(player):
    """Tampilan inventory yang mendukung sistem 8-slot dan format item string ID"""
    inventory = player.get('inventory', [])
    artifacts = player.get('artifacts', []) # Artefak yang didapat secara naratif
    
    if not inventory and not artifacts:
        return "🎒 *INVENTORY & ARTEFAK KOSONG*\nKumpulkan item untuk bertahan hidup."
    
    display = "🎒 *INVENTORY*\n━━━━━━━━━━━━━━━━━━━━\n"
    
    equip_types = ['weapon', 'armor', 'head', 'mask', 'gloves', 'boots', 'cloak', 'artifact']
    
    # Pisahkan item berdasarkan tipenya
    equips = []
    consumables = []
    
    for item_data in inventory:
        if isinstance(item_data, dict):
            consumables.append(item_data)
        elif isinstance(item_data, str):
            eq = get_item(item_data)
            if eq: equips.append(eq)
    
    if equips:
        display += "🛡️ *EQUIPMENT TERSIMPAN*\n"
        for e in equips:
            dur = e.get('durability', 50)
            max_dur = e.get('max_durability', 50)
            
            if dur <= 0: status_icon = "❌ (RUSAK)"
            elif dur <= 10: status_icon = "⚠️ (Retak)"
            else: status_icon = "✅"
                
            skill_info = f" | ⚡ Skill: {e['skill']['name']}" if e.get('skill') else ""
            stat_info = f"+{e.get('p_atk', 0)} Atk" if e.get('type') == 'weapon' else f"+{e.get('p_def', 0)} Def"
            
            display += f"• *{e['name']}* ({stat_info})\n  └ {status_icon} Durability: {dur}/{max_dur}{skill_info}\n"
        display += "\n"
        
    if consumables:
        display += "🧪 *CONSUMABLES & UTILITY*\n"
        item_counts = {}
        for c in consumables:
            name = c.get('name', 'Unknown Item')
            item_counts[name] = item_counts.get(name, 0) + 1
            
        for name, count in item_counts.items():
            display += f"• {name} (x{count})\n"
        display += "\n"
            
    if artifacts:
        display += "✨ *ARTEFAK AKTIF (PERMANEN)*\n"
        for art in artifacts:
            art_name = art.get('name') if isinstance(art, dict) else art
            display += f"• {art_name}\n"
            
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
