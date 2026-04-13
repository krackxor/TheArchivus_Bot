"""
Sistem NPC (Non-Playable Characters) - Mega Variation Edition
Mengatur pertemuan, dialog, dan logika interaksi yang lebih kompleks.
"""
import random

# --- GENERATOR NAMA NPC VARIATIF ---
PREFIXES = ["The Blind", "The Hollow", "The Wandering", "The Forgotten", "The Faceless", "The Cursed", "The Radiant", "The Silent", "The Crimson", "The Ancient"]
NOUNS = ["Seer", "Scribe", "Thief", "Weaver", "Archivist", "Merchant", "Oracle", "Scholar", "Butcher", "Specter"]

def generate_random_npc_name():
    return f"{random.choice(PREFIXES)} {random.choice(NOUNS)}"

# --- LOGIKA ENCOUNTER NPC ---
def get_npc_encounter(player, cycle=1):
    """
    Menghasilkan data encounter NPC dengan variasi yang sangat banyak.
    """
    # Menentukan tipe berdasarkan bobot (Sekarang lebih banyak tipe!)
    npc_types = ["healer", "trickster", "scholar", "wanderer", "mercenary", "curse_eater", "collector"]
    weights = [0.20, 0.20, 0.15, 0.15, 0.10, 0.10, 0.10] 
    chosen_type = random.choices(npc_types, weights=weights, k=1)[0]
    
    # 1. HEALER (The Blind Seer / Medic)
    if chosen_type == "healer":
        cost = random.randint(15, 25) + (cycle * 5)
        heal = random.randint(30, 50) + (cycle * 10)
        return {
            "id": "npc_healer",
            "name": "The Blind Seer",
            "type": "healer",
            "narration": f"Kamu bertemu dengan *The Blind Seer*. Matanya tertutup kain, namun ia tampak melihat setiap dosamu.\n\n*'Luka fisikmu mudah sembuh, Weaver. Tapi bagaimana dengan jiwamu?'*\n\nIa menawarkan bantuan pemulihan.",
            "choices": [
                {"text": f"Sembuhkan ❤️ ({cost} Gold)", "action": "heal", "cost": cost, "value": heal},
                {"text": "Abaikan dan Pergi", "action": "leave"}
            ]
        }
        
    # 2. TRICKSTER (The Memory Thief / Gambler)
    elif chosen_type == "trickster":
        bet = random.randint(40, 80) + (cycle * 5)
        return {
            "id": "npc_trickster",
            "name": "The Memory Thief",
            "type": "trickster",
            "narration": f"Seorang sosok licik memainkan koin perak di jarinya. *The Memory Thief* mendekat.\n\n*'Koin ini bisa memberimu takdir baru, atau menghapus keberadaanmu. Berani pasang {bet} Gold?'*",
            "choices": [
                {"text": f"🎲 Mainkan! (-{bet} Gold)", "action": "gamble", "cost": bet},
                {"text": "Bilang 'Tidak' pada Judi", "action": "leave"}
            ]
        }
        
    # 3. SCHOLAR (The Hollow Scribe / Quiz)
    elif chosen_type == "scholar":
        return {
            "id": "npc_scholar",
            "name": "The Hollow Scribe",
            "type": "scholar",
            "narration": "Ribuan buku melayang di sekitar *The Hollow Scribe*. Ia mencari satu lembar memori yang hilang.\n\n*'Pengetahuan adalah satu-satunya senjata yang tidak akan tumpul di sini. Uji dirimu, Weaver.'*",
            "choices": [
                {"text": "📖 Terima Ujian Lore", "action": "quiz"},
                {"text": "Lari dari Pelajaran", "action": "leave"}
            ]
        }

    # 4. MERCENARY (The Iron Soul / Combat Buff)
    elif chosen_type == "mercenary":
        cost = 100 + (cycle * 20)
        return {
            "id": "npc_mercenary",
            "name": "The Iron Soul",
            "type": "mercenary",
            "narration": f"Prajurit tua ini sedang mengasah pedangnya yang retak.\n\n*'Aku butuh biaya untuk perjalananku. Bayar aku {cost} Gold, dan aku akan membimbing pedangmu agar lebih mematikan.'*",
            "choices": [
                {"text": f"⚔️ Sewa Mentor (-{cost} Gold)", "action": "buy_buff", "cost": cost},
                {"text": "Terlalu Mahal", "action": "leave"}
            ]
        }

    # 5. CURSE EATER (The Sin Eater / Reset HP for MP)
    elif chosen_type == "curse_eater":
        return {
            "id": "npc_curse_eater",
            "name": "The Sin Eater",
            "type": "curse_eater",
            "narration": "Makhluk ini terlihat mengerikan, memakan bangkai monster. Ia menoleh padamu.\n\n*'Berikan aku darahmu (HP), dan aku akan memberimu napas sihir (MP)...'*",
            "choices": [
                {"text": "🩸 Tukar 20 HP jadi 30 MP", "action": "swap_hp_mp"},
                {"text": "Jangan Sentuh Aku", "action": "leave"}
            ]
        }

    # 6. COLLECTOR (The Scrap Merchant)
    elif chosen_type == "collector":
        reward = random.randint(50, 100)
        return {
            "id": "npc_collector",
            "name": "The Scrap Merchant",
            "type": "collector",
            "narration": "Ia membawa karung besar berisi rongsokan. \n\n*'Kau punya barang yang tidak berguna? Aku akan membelinya dengan harga tinggi!'*",
            "choices": [
                {"text": f"💰 Jual Item Acak (+{reward} Gold)", "action": "sell_random", "value": reward},
                {"text": "Barangku Terlalu Berharga", "action": "leave"}
            ]
        }
        
    else: # WANDERER (Common encounters)
        name = generate_random_npc_name()
        return {
            "id": "npc_wanderer",
            "name": name,
            "type": "wanderer",
            "narration": f"Kamu bertemu dengan {name}, seorang pengembara yang tampak damai di tengah kekacauan Archivus.\n\nIa menawarkan segenggam debu bercahaya kepadamu.",
            "choices": [
                {"text": "✨ Terima Cahayanya", "action": "accept_gift"},
                {"text": "Lanjutkan Jalan", "action": "leave"}
            ]
        }

# --- RESOLUSI AKSI NPC ---
def resolve_npc_action(player, npc_data, action_choice):
    updates = {}
    result_msg = ""
    
    if action_choice == "leave":
        return "Kamu memilih untuk meninggalkan NPC tersebut. Sosoknya perlahan menghilang tertutup kabut.", updates

    npc_type = npc_data["type"]

    # --- LOGIKA HEALER ---
    if npc_type == "healer" and action_choice == "heal":
        cost = npc_data["choices"][0]["cost"]
        heal = npc_data["choices"][0]["value"]
        if player.get("gold", 0) < cost:
            result_msg = "Goldmu tidak cukup. Seer itu menggeleng sedih dan memudar."
        else:
            updates["gold"] = player.get("gold", 0) - cost
            updates["hp"] = min(player.get("max_hp", 100), player.get("hp", 100) + heal)
            result_msg = f"✨ *Keajaiban!* Luka-lukamu menutup. Kamu memulihkan {heal} HP."

    # --- LOGIKA TRICKSTER (GAMBLE) ---
    elif npc_type == "trickster" and action_choice == "gamble":
        cost = npc_data["choices"][0]["cost"]
        if player.get("gold", 0) < cost:
            result_msg = "The Memory Thief tertawa. 'Miskin sekali...' Ia menghilang."
        else:
            updates["gold"] = player.get("gold", 0) - cost
            roll = random.random()
            if roll < 0.45: # Kalah
                damage = random.randint(15, 30)
                updates["hp"] = max(1, player.get("hp", 100) - damage)
                result_msg = f"❌ *Kalah!* Kamu tertipu. Kehilangan {cost} Gold dan terkena {damage} DMG!"
            elif roll < 0.85: # Menang Gold
                win = int(cost * 3)
                updates["gold"] = player.get("gold", 0) + win
                result_msg = f"🎉 *Jackpot!* Kamu memenangkan {win} Gold dari taruhanmu!"
            else: # Item Langka
                inv = player.get("inventory", [])
                inv.append({"id": "ancient_relic", "name": "Ancient Relic", "type": "artifact"})
                updates["inventory"] = inv
                result_msg = "🎁 *Luar Biasa!* Kamu mendapatkan [Ancient Relic] yang sangat langka!"

    # --- LOGIKA MERCENARY (BUFF) ---
    elif npc_type == "mercenary" and action_choice == "buy_buff":
        cost = npc_data["choices"][0]["cost"]
        if player.get("gold", 0) < cost:
            result_msg = "Prajurit itu tidak bekerja secara gratis."
        else:
            updates["gold"] = player.get("gold", 0) - cost
            updates["attack_buff"] = player.get("attack_buff", 0) + 5
            result_msg = "⚔️ Prajurit itu melatihmu. *Attack Permanent-mu meningkat +5!*"

    # --- LOGIKA CURSE EATER ---
    elif npc_type == "curse_eater" and action_choice == "swap_hp_mp":
        if player.get("hp", 0) <= 25:
            result_msg = "Darahmu terlalu tipis, Sin Eater menolak memakan jiwamu."
        else:
            updates["hp"] = player.get("hp") - 20
            updates["mp"] = min(player.get("max_mp", 100), player.get("mp", 0) + 30)
            result_msg = "🩸 *Pengorbanan.* Tubuhmu melemah, tapi energi sihirmu meluap! (-20 HP, +30 MP)"

    # --- LOGIKA COLLECTOR ---
    elif npc_type == "collector" and action_choice == "sell_random":
        inv = player.get("inventory", [])
        if not inv:
            result_msg = "Tasmu kosong. Collector itu mendesah bosan."
        else:
            sold_item = inv.pop(random.randint(0, len(inv)-1))
            updates["inventory"] = inv
            updates["gold"] = player.get("gold", 0) + npc_data["choices"][0]["value"]
            result_msg = f"💰 Kamu menjual *{sold_item['name']}* seharga {npc_data['choices'][0]['value']} Gold!"

    # --- LOGIKA WANDERER ---
    elif npc_type == "wanderer" and action_choice == "accept_gift":
        roll = random.random()
        if roll < 0.5:
            gold = random.randint(20, 50)
            updates["gold"] = player.get("gold", 0) + gold
            result_msg = f"✨ Kamu menerima {gold} Gold dari sang pengembara."
        else:
            inv = player.get("inventory", [])
            inv.append({"id": "mystery_pill", "name": "Mystery Pill", "type": "potion"})
            updates["inventory"] = inv
            result_msg = "✨ Kamu mendapatkan sebuah [Mystery Pill]!"

    return result_msg, updates
