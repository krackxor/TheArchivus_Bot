"""
Sistem NPC (Non-Playable Characters) - Data-Driven Edition
Mengatur pertemuan, dialog, dan logika interaksi. 
Semua teks & narasi (100 NPC) diambil dari game/data/npc_data.py
"""
import random
from game.data.npc_data import NPC_POOL, LORE_STORIES

def get_npc_encounter(cycle=1):
    """
    Menghasilkan data encounter NPC secara dinamis dari 100 kemungkinan.
    """
    npc_types = ["healer", "trickster", "scholar", "wanderer", "mercenary", "curse_eater", "collector", "guide", "beggar", "lore_keeper"]
    weights = [0.12, 0.12, 0.10, 0.10, 0.08, 0.08, 0.10, 0.10, 0.10, 0.10] 
    
    chosen_type = random.choices(npc_types, weights=weights, k=1)[0]
    
    # Mengambil satu data NPC secara acak dari 10 variasi di kategorinya
    npc_data = random.choice(NPC_POOL[chosen_type])
    name = npc_data.get("name", "Unknown Entity")
    narration = npc_data.get("narration", "...")

    # --- MEMBANGUN STRUKTUR ENCOUNTER BERDASARKAN TIPE ---
    
    if chosen_type == "healer":
        cost = npc_data["base_cost"] + (cycle * 5)
        heal = npc_data["base_heal"] + (cycle * 10)
        return {
            "id": "npc_healer", "name": name, "type": "healer",
            "narration": f"**{name}**\n\n{narration}",
            "choices": [
                {"text": f"Sembuhkan ❤️ ({cost} Gold)", "action": "heal", "cost": cost, "value": heal},
                {"text": "Abaikan dan Lari", "action": "leave"}
            ]
        }
        
    elif chosen_type == "trickster":
        bet = npc_data["base_bet"] + (cycle * 5)
        return {
            "id": "npc_trickster", "name": name, "type": "trickster",
            "narration": f"**{name}**\n\n{narration}",
            "choices": [
                {"text": f"🎲 Taruhan Nyawa (-{bet} Gold)", "action": "gamble", "cost": bet},
                {"text": "Tolak Taruhan", "action": "leave"}
            ]
        }
        
    elif chosen_type == "scholar":
        return {
            "id": "npc_scholar", "name": name, "type": "scholar",
            "narration": f"**{name}**\n\n{narration}",
            "choices": [
                {"text": "📖 Terima Ujian Kegilaan", "action": "quiz"},
                {"text": "Menghindar", "action": "leave"}
            ]
        }

    elif chosen_type == "mercenary":
        cost = npc_data["base_cost"] + (cycle * 20)
        return {
            "id": "npc_mercenary", "name": name, "type": "mercenary",
            "narration": f"**{name}**\n\n{narration}\n*(Buff Permanen ATK +2)*",
            "choices": [
                {"text": f"⚔️ Sewa Monster Ini (-{cost} Gold)", "action": "buy_buff", "cost": cost},
                {"text": "Terlalu Mahal", "action": "leave"}
            ]
        }

    elif chosen_type == "curse_eater":
        return {
            "id": "npc_curse_eater", "name": name, "type": "curse_eater",
            "narration": f"**{name}**\n\n{narration}",
            "choices": [
                {"text": "🩸 Berdarah (Tukar 20 HP -> 30 MP)", "action": "swap_hp_mp"},
                {"text": "Jangan Sentuh Aku", "action": "leave"}
            ]
        }

    elif chosen_type == "collector":
        reward = random.randint(40, 90)
        return {
            "id": "npc_collector", "name": name, "type": "collector",
            "narration": f"**{name}**\n\n{narration}",
            "choices": [
                {"text": f"💰 Jual Item Rongsok", "action": "sell_random", "value": reward},
                {"text": "Jauhi Dia", "action": "leave"}
            ]
        }
        
    elif chosen_type == "guide":
        return {
            "id": "npc_guide", "name": name, "type": "guide",
            "narration": f"**{name}**\n\n{narration}",
            "choices": [
                {"text": "🧭 Ikuti Petunjuknya", "action": "ask_direction"},
                {"text": "Aku Tidak Percaya", "action": "leave"}
            ]
        }

    elif chosen_type == "beggar":
        return {
            "id": "npc_beggar", "name": name, "type": "beggar",
            "narration": f"**{name}**\n\n{narration}",
            "choices": [
                {"text": "🍞 Lempar Makanan/Item", "action": "give_item"},
                {"text": "Biarkan Kelaparan", "action": "leave"}
            ]
        }

    elif chosen_type == "lore_keeper":
        return {
            "id": "npc_lore", "name": name, "type": "lore_keeper",
            "narration": f"**{name}**\n\n{narration}",
            "choices": [
                {"text": "👂 Dengarkan Kutukannya", "action": "listen_story"},
                {"text": "Tutup Telinga", "action": "leave"}
            ]
        }
        
    else: # wanderer
        return {
            "id": "npc_wanderer", "name": name, "type": "wanderer",
            "narration": f"**{name}**\n\n{narration}",
            "choices": [
                {"text": "✨ Pungut Barang Itu", "action": "accept_gift"},
                {"text": "Abaikan Saja", "action": "leave"}
            ]
        }

# --- RESOLUSI AKSI NPC ---
def resolve_npc_action(player, npc_data, action_choice):
    updates = {}
    result_msg = ""
    
    if action_choice == "leave":
        return "Kau berlalu. Sosok itu perlahan memudar tertelan kegelapan Archivus.", updates

    npc_type = npc_data["type"]

    # --- LOGIKA HEALER ---
    if npc_type == "healer" and action_choice == "heal":
        cost = npc_data["choices"][0]["cost"]
        heal = npc_data["choices"][0]["value"]
        if player.get("gold", 0) < cost:
            result_msg = "Gold tidak cukup. Ia menatapmu dengan jijik dan memudar."
        else:
            updates["gold"] = player.get("gold", 0) - cost
            updates["hp"] = min(player.get("max_hp", 100), player.get("hp", 100) + heal)
            result_msg = f"✨ *Proses yang menyakitkan.* Luka terikat kembali. Kamu memulihkan {heal} HP."

    # --- LOGIKA TRICKSTER (GAMBLE) ---
    elif npc_type == "trickster" and action_choice == "gamble":
        cost = npc_data["choices"][0]["cost"]
        if player.get("gold", 0) < cost:
            result_msg = "Ia tertawa mengejek. 'Miskin harta, miskin nyawa.' Ia menghilang."
        else:
            updates["gold"] = player.get("gold", 0) - cost
            roll = random.random()
            if roll < 0.45: # Kalah
                damage = random.randint(15, 30)
                updates["hp"] = max(1, player.get("hp", 100) - damage)
                result_msg = f"❌ *Kalah!* Kau merasakan jantungmu ditusuk dari dalam! (-{cost} Gold, -{damage} HP)!"
            elif roll < 0.85: # Menang Gold
                win = int(cost * 3)
                updates["gold"] = player.get("gold", 0) + win
                result_msg = f"🎉 *Selamat!* Koin berpihak padamu, meski kau merasa kotor. Memenangkan {win} Gold!"
            else: # Item Langka
                artifacts = player.get("artifacts", [])
                artifacts.append({"id": "gambler_coin", "name": "✨ The Cursed Coin", "type": "artifact", "effect": "better_loot"})
                updates["artifacts"] = artifacts
                result_msg = "🎁 Ia terdiam. 'Kau menang.' Ia menyerahkan artefak terkutuk [The Cursed Coin] kepadamu!"

    # --- LOGIKA MERCENARY (BUFF) ---
    elif npc_type == "mercenary" and action_choice == "buy_buff":
        cost = npc_data["choices"][0]["cost"]
        if player.get("gold", 0) < cost:
            result_msg = "Ia mendengus kasar. 'Pergilah sebelum kutebas kepalamu.'"
        else:
            updates["gold"] = player.get("gold", 0) - cost
            updates["base_atk"] = player.get("base_atk", 10) + 2
            result_msg = "⚔️ Latihan yang brutal dan berdarah. Ototmu mengeras. *Base Attack meningkat +2!*"

    # --- LOGIKA CURSE EATER ---
    elif npc_type == "curse_eater" and action_choice == "swap_hp_mp":
        if player.get("hp", 0) <= 25:
            result_msg = "Darahmu terlalu busuk. Ia memalingkan wajahnya darimu."
        else:
            updates["hp"] = player.get("hp") - 20
            updates["mp"] = min(player.get("max_mp", 50), player.get("mp", 0) + 30)
            result_msg = "🩸 *Tukar Guling.* Tubuhmu melemah, tapi pikiranmu terbakar sihir! (-20 HP, +30 MP)"

    # --- LOGIKA COLLECTOR ---
    elif npc_type == "collector" and action_choice == "sell_random":
        inv = player.get("inventory", [])
        sellable_items = [i for i in inv if i.get("type") in ["potion", "food", "material"]]
        
        if not sellable_items:
            result_msg = "Tidak ada barang di tasmu yang menarik baginya. Ia mendesis marah."
        else:
            item_to_sell = random.choice(sellable_items)
            inv.remove(item_to_sell)
            sell_price = npc_data["choices"][0]["value"]
            updates["inventory"] = inv
            updates["gold"] = player.get("gold", 0) + sell_price
            result_msg = f"💰 Ia merampas *{item_to_sell['name']}* darimu dan melempar {sell_price} Gold ke wajahmu!"

    # --- LOGIKA GUIDE ---
    elif npc_type == "guide" and action_choice == "ask_direction":
        if random.random() < 0.60:
            result_msg = "🧭 *Suaranya bergema:* 'Tiga langkah dari sini, kematian mengintip dari atap. Berlarilah.' (Petunjuk Akurat)"
        else:
            result_msg = "🧭 *Ia tersenyum miring:* 'Jalan di depan sangat aman...' Sayangnya kau tahu itu kebohongan. (Awas Jebakan!)"

    # --- LOGIKA BEGGAR ---
    elif npc_type == "beggar" and action_choice == "give_item":
        inv = player.get("inventory", [])
        food_potions = [i for i in inv if i.get("type") in ["potion", "food"]]
        
        if not food_potions:
            result_msg = "Kau merogoh tasmu yang kosong. Sosok itu menangis dan berubah menjadi debu."
        else:
            given_item = food_potions[0]
            inv.remove(given_item)
            updates["inventory"] = inv
            
            if random.random() < 0.70:
                updates["gold"] = player.get("gold", 0) + 100
                result_msg = f"🍞 Kau melempar *{given_item['name']}*. Ia memakannya bersama wadahnya. Sebagai gantinya, kau memungut koin miliknya. (+100 Gold)"
            else:
                stolen_gold = random.randint(30, 80)
                updates["gold"] = max(0, player.get("gold", 0) - stolen_gold)
                result_msg = f"🍞 Saat kau mendekat memberikan *{given_item['name']}*, ia menggigit tanganmu dan merampas emasmu! (-{stolen_gold} Gold)"

    # --- LOGIKA LORE KEEPER ---
    elif npc_type == "lore_keeper" and action_choice == "listen_story":
        chosen_story = random.choice(LORE_STORIES)
        unlocked_lores = player.get("unlocked_lores", [])
        
        if chosen_story not in unlocked_lores:
            unlocked_lores.append(chosen_story)
            updates["unlocked_lores"] = unlocked_lores
            updates["exp"] = player.get("exp", 0) + 100
            updates["max_mp"] = player.get("max_mp", 50) + 2
            bonus_text = "\n\n*(Mimpi Buruk Baru Terbuka! +100 EXP, +2 Max MP)*"
        else:
            updates["mp"] = min(player.get("max_mp", 50), player.get("mp", 0) + 15)
            bonus_text = "\n\n*(Mengulang penderitaan yang sama memulihkan +15 MP)*"

        result_msg = f"📖 *Suara Penuh Keputusasaan:*\n\n{chosen_story}{bonus_text}"

    # --- LOGIKA WANDERER ---
    elif npc_type == "wanderer" and action_choice == "accept_gift":
        if random.random() < 0.5:
            gold = random.randint(20, 50)
            updates["gold"] = player.get("gold", 0) + gold
            result_msg = f"✨ Koin emas terasa dingin di tanganmu. Ia pergi tanpa jejak. (+{gold} Gold)"
        else:
            inv = player.get("inventory", [])
            inv.append({"id": "buy_heal_30", "name": "Minor HP Potion", "type": "potion", "effect": "heal_30"})
            updates["inventory"] = inv
            result_msg = "✨ Kau mendapatkan [Minor HP Potion]. Saat kau melihat lagi, ia sudah hilang ditelan kabut."

    return result_msg, updates
