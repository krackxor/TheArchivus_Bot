"""
Sistem NPC (Non-Playable Characters) - Mega Variation Edition
Mengatur pertemuan, dialog, dan logika interaksi yang kompleks.
Terintegrasi dengan array Artifact, Base Stats, Smart Inventory, dan Lore Chronicles.
"""
import random

# --- GENERATOR NAMA NPC VARIATIF ---
PREFIXES = ["The Blind", "The Hollow", "The Wandering", "The Forgotten", "The Faceless", "The Cursed", "The Radiant", "The Silent", "The Crimson", "The Ancient"]
NOUNS = ["Seer", "Scribe", "Thief", "Weaver", "Archivist", "Merchant", "Oracle", "Scholar", "Butcher", "Specter"]

def generate_random_npc_name():
    return f"{random.choice(PREFIXES)} {random.choice(NOUNS)}"

# --- DATABASE LORE & SEJARAH ARCHIVUS ---
LORE_STORIES = [
    # 1. Asal-usul Archivus
    "Dimensi ini dulunya adalah perpustakaan para Dewa. *The Archivus* dirancang untuk menyimpan semua kenangan, garis waktu, dan rahasia semesta yang terlalu berbahaya untuk diingat oleh manusia. Namun, sesuatu... atau seseorang, merobek pintunya.",
    # 2. Tentang Weaver (Pemain)
    "Kau bertanya apa itu 'Weaver'? Kita adalah penjahit realitas. Kita ditarik dari kematian kita sendiri untuk memperbaiki dimensi ini. Kau bukan yang pertama, temanku. Ribuan Weaver telah mati di sini. Kuburan yang kau temui? Itu adalah saudara-saudaramu.",
    # 3. Asal-usul Gold / Uang
    "Kau menggunakan koin emas untuk berbelanja, bukan? Tahukah kau apa itu sebenarnya? Itu bukan logam. Itu adalah pecahan waktu dari jiwa-jiwa yang membusuk di sini. Saat kau membayar sesuatu, kau menukar kenangan seseorang demi bertahan hidup.",
    # 4. Tentang Sang Penjaga (Main Boss)
    "Sang Penjaga yang kau buru... dia tidak terlahir sebagai monster. Namanya dulunya adalah Orion, Weaver Pertama. Dia mencoba membaca 'Kitab Akhir Zaman' sendirian. Pengetahuan itu meledakkan akalnya, mengubahnya menjadi penjaga gerbang yang cacat dan penuh amarah.",
    # 5. Tentang Rawa Tinta (The Inky Mire)
    "Rawa hijau beracun di distrik bawah itu dulunya adalah ruang arsip puisi. Namun, semua kebohongan dan sumpah palsu yang tertulis di dunia manusia menetes ke bawah, membusuk, dan berubah menjadi *Miasma* beracun yang kini membakar paru-parumu.",
    # 6. Tentang Artefak Jantung Penjaga
    "Jika suatu saat kau berhasil merobek dada Sang Penjaga, kau akan menemukan jantung yang membatu. Itu adalah artefak tertua. Barang siapa yang memegangnya, ia tidak akan bisa mati karena usia... tapi ia akan mati karena kesepian.",
    # 7. Pesan Motivasi Terakhir
    "Terkadang aku berpikir, apakah kita benar-benar hidup, atau kita hanyalah karakter dari sebuah buku tua yang sedang dibaca oleh entitas di luar sana? Jika kau berhasil mencapai *The Final Archive*, tolong... cari tahu siapa penulis takdir kita."
]

# --- LOGIKA ENCOUNTER NPC ---
def get_npc_encounter(cycle=1):
    """
    Menghasilkan data encounter NPC dengan 10 variasi penuh.
    """
    npc_types = ["healer", "trickster", "scholar", "wanderer", "mercenary", "curse_eater", "collector", "guide", "beggar", "lore_keeper"]
    weights = [0.12, 0.12, 0.10, 0.10, 0.08, 0.08, 0.10, 0.10, 0.10, 0.10] 
    chosen_type = random.choices(npc_types, weights=weights, k=1)[0]
    
    # 1. HEALER (The Blind Seer)
    if chosen_type == "healer":
        cost = random.randint(15, 25) + (cycle * 5)
        heal = random.randint(30, 50) + (cycle * 10)
        return {
            "id": "npc_healer", "name": "The Blind Seer", "type": "healer",
            "narration": f"Kamu bertemu dengan *The Blind Seer*. Matanya tertutup kain, namun ia tampak menilai jiwamu.\n\n*'Luka fisikmu mudah sembuh, Weaver. Tapi bagaimana dengan ingatanmu?'*\n\nIa menawarkan bantuan pemulihan.",
            "choices": [
                {"text": f"Sembuhkan ❤️ ({cost} Gold)", "action": "heal", "cost": cost, "value": heal},
                {"text": "Abaikan dan Pergi", "action": "leave"}
            ]
        }
        
    # 2. TRICKSTER (The Memory Thief)
    elif chosen_type == "trickster":
        bet = random.randint(40, 80) + (cycle * 5)
        return {
            "id": "npc_trickster", "name": "The Memory Thief", "type": "trickster",
            "narration": f"Sosok licik memainkan koin perak di jarinya. *The Memory Thief* tersenyum miring.\n\n*'Koin ini bisa memberimu takdir baru, atau menghapus keberadaanmu. Berani pasang {bet} Gold?'*",
            "choices": [
                {"text": f"🎲 Taruhan! (-{bet} Gold)", "action": "gamble", "cost": bet},
                {"text": "Tolak Taruhan", "action": "leave"}
            ]
        }
        
    # 3. SCHOLAR (The Hollow Scribe)
    elif chosen_type == "scholar":
        return {
            "id": "npc_scholar", "name": "The Hollow Scribe", "type": "scholar",
            "narration": "Ribuan perkamen melayang di sekitar *The Hollow Scribe*. Ia tampak mencari satu kata yang hilang.\n\n*'Pengetahuan adalah satu-satunya senjata abadi di Archivus. Uji pemahamanmu, Weaver.'*",
            "choices": [
                {"text": "📖 Terima Ujian Lore", "action": "quiz"},
                {"text": "Tolak Ujian", "action": "leave"}
            ]
        }

    # 4. MERCENARY (The Iron Soul)
    elif chosen_type == "mercenary":
        cost = 100 + (cycle * 20)
        return {
            "id": "npc_mercenary", "name": "The Iron Soul", "type": "mercenary",
            "narration": f"Prajurit tua dari dimensi runtuh ini sedang mengasah pedangnya.\n\n*'Beri aku {cost} Gold untuk bekal, dan aku akan mengajarimu cara memukul celah kelemahan musuh.'*",
            "choices": [
                {"text": f"⚔️ Sewa Mentor (-{cost} Gold)", "action": "buy_buff", "cost": cost},
                {"text": "Terlalu Mahal", "action": "leave"}
            ]
        }

    # 5. CURSE EATER (The Sin Eater)
    elif chosen_type == "curse_eater":
        return {
            "id": "npc_curse_eater", "name": "The Sin Eater", "type": "curse_eater",
            "narration": "Makhluk berwujud asap gelap ini menatapmu dengan lapar.\n\n*'Berikan aku darahmu yang hangat (HP), dan aku akan memberimu energi spiritual (MP)...'*",
            "choices": [
                {"text": "🩸 Tukar 20 HP jadi 30 MP", "action": "swap_hp_mp"},
                {"text": "Jangan Sentuh Aku", "action": "leave"}
            ]
        }

    # 6. COLLECTOR (The Scrap Merchant)
    elif chosen_type == "collector":
        reward = random.randint(40, 90)
        return {
            "id": "npc_collector", "name": "The Scrap Merchant", "type": "collector",
            "narration": "Ia menggendong karung besar berisi rongsokan dunia.\n\n*'Punya sisa ramuan atau makanan? Aku akan membelinya dengan harga tinggi!'*",
            "choices": [
                {"text": f"💰 Jual Item Konsumsi Acak", "action": "sell_random", "value": reward},
                {"text": "Tidak Ada Barang", "action": "leave"}
            ]
        }
        
    # 7. GUIDE (The Oracle)
    elif chosen_type == "guide":
        return {
            "id": "npc_guide", "name": "The Weeping Oracle", "type": "guide",
            "narration": "Seorang wanita bermata putih menunjuk ke arah kegelapan di depanmu.\n\n*'Jalan di depan bercabang, Weaver. Ada yang membawa pada harta, ada yang membawa pada kematian. Maukah kau mendengarkan bisikanku?'*",
            "choices": [
                {"text": "🧭 Minta Petunjuk Arah", "action": "ask_direction"},
                {"text": "Aku Percaya Instingku", "action": "leave"}
            ]
        }

    # 8. BEGGAR (The Starving Soul)
    elif chosen_type == "beggar":
        return {
            "id": "npc_beggar", "name": "The Starving Soul", "type": "beggar",
            "narration": "Sosok kurus kering merangkak mendekatimu, tangannya gemetar meraih ujung jubahmu.\n\n*'Tolong... setetes ramuan... atau sepotong roti... aku tidak ingin menghilang di tempat ini...'*",
            "choices": [
                {"text": "🍞 Berikan Item Konsumsi", "action": "give_item"},
                {"text": "Abaikan dan Pergi", "action": "leave"}
            ]
        }

    # 9. LORE KEEPER (The Fallen Weaver)
    elif chosen_type == "lore_keeper":
        return {
            "id": "npc_lore", "name": "The Fallen Weaver", "type": "lore_keeper",
            "narration": "Seorang Weaver yang tubuhnya perlahan berubah menjadi batu duduk bersila. Ia tersenyum damai melihatmu.\n\n*'Kau masih berjuang? Kemarilah, duduklah sejenak. Biar kuceritakan sejarah tempat yang terkutuk ini sebelum suaraku lenyap.'*",
            "choices": [
                {"text": "👂 Dengarkan Ceritanya", "action": "listen_story"},
                {"text": "Aku Tidak Punya Waktu", "action": "leave"}
            ]
        }
        
    # 10. WANDERER (Common encounters)
    else: 
        name = generate_random_npc_name()
        return {
            "id": "npc_wanderer", "name": name, "type": "wanderer",
            "narration": f"Kamu bertemu dengan {name}, seorang pengembara yang tampak damai di tengah kekacauan.\n\nIa menyodorkan sesuatu ke arahmu tanpa bicara.",
            "choices": [
                {"text": "✨ Terima Pemberiannya", "action": "accept_gift"},
                {"text": "Abaikan Saja", "action": "leave"}
            ]
        }

# --- RESOLUSI AKSI NPC ---
def resolve_npc_action(player, npc_data, action_choice):
    updates = {}
    result_msg = ""
    
    if action_choice == "leave":
        return "Kamu memilih berlalu. Sosok NPC tersebut perlahan memudar tertelan kabut.", updates

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
            result_msg = "The Memory Thief tertawa mengejek. 'Kembalilah saat kau punya uang.' Ia menghilang."
        else:
            updates["gold"] = player.get("gold", 0) - cost
            roll = random.random()
            if roll < 0.45: # Kalah
                damage = random.randint(15, 30)
                updates["hp"] = max(1, player.get("hp", 100) - damage)
                result_msg = f"❌ *Kalah!* Kamu tertipu. Kehilangan {cost} Gold dan terkena jebakan (-{damage} HP)!"
            elif roll < 0.85: # Menang Gold
                win = int(cost * 3)
                updates["gold"] = player.get("gold", 0) + win
                result_msg = f"🎉 *Jackpot!* Koin berpihak padamu. Memenangkan {win} Gold!"
            else: # Item Langka (Masuk ke array Artifacts)
                artifacts = player.get("artifacts", [])
                artifacts.append({"id": "gambler_coin", "name": "✨ The Gambler's Coin", "type": "artifact", "effect": "better_loot"})
                updates["artifacts"] = artifacts
                result_msg = "🎁 *Luar Biasa!* Sang Pencuri terkesiap. Ia menyerahkan artefak [The Gambler's Coin] kepadamu!"

    # --- LOGIKA MERCENARY (BUFF) ---
    elif npc_type == "mercenary" and action_choice == "buy_buff":
        cost = npc_data["choices"][0]["cost"]
        if player.get("gold", 0) < cost:
            result_msg = "Prajurit itu mendengus. 'Ilmu bertarung tidaklah gratis.'"
        else:
            updates["gold"] = player.get("gold", 0) - cost
            updates["base_atk"] = player.get("base_atk", 10) + 2
            result_msg = "⚔️ Latihan yang keras. Tanganmu kini lebih sigap. *Base Attack meningkat +2!*"

    # --- LOGIKA CURSE EATER ---
    elif npc_type == "curse_eater" and action_choice == "swap_hp_mp":
        if player.get("hp", 0) <= 25:
            result_msg = "Darahmu terlalu tipis, Sin Eater menolak jiwamu agar kau tidak mati sia-sia."
        else:
            updates["hp"] = player.get("hp") - 20
            updates["mp"] = min(player.get("max_mp", 50), player.get("mp", 0) + 30)
            result_msg = "🩸 *Pengorbanan.* Tubuhmu melemah, tapi energi sihirmu meluap! (-20 HP, +30 MP)"

    # --- LOGIKA COLLECTOR ---
    elif npc_type == "collector" and action_choice == "sell_random":
        inv = player.get("inventory", [])
        sellable_items = [i for i in inv if i.get("type") in ["potion", "food", "material"]]
        
        if not sellable_items:
            result_msg = "Tidak ada barang rongsok/konsumsi di tasmu. Collector itu mendesah kecewa."
        else:
            item_to_sell = random.choice(sellable_items)
            inv.remove(item_to_sell)
            sell_price = npc_data["choices"][0]["value"]
            updates["inventory"] = inv
            updates["gold"] = player.get("gold", 0) + sell_price
            result_msg = f"💰 Kamu menjual *{item_to_sell['name']}* ke Collector seharga {sell_price} Gold!"

    # --- LOGIKA GUIDE ---
    elif npc_type == "guide" and action_choice == "ask_direction":
        if random.random() < 0.60:
            result_msg = "🧭 *Oracle berkata:* 'Lima langkah dari sini, ada peti harta karun tertutup duri. Siapkan kuncimu.' (Petunjuk Akurat!)"
        else:
            result_msg = "🧭 *Oracle berkata:* 'Jalan di depan sangat aman...' Namun kau melihat senyum licik di wajahnya. (Hati-hati Jebakan!)"

    # --- LOGIKA BEGGAR ---
    elif npc_type == "beggar" and action_choice == "give_item":
        inv = player.get("inventory", [])
        food_potions = [i for i in inv if i.get("type") in ["potion", "food"]]
        
        if not food_potions:
            result_msg = "Kau merogoh tasmu, tapi tidak ada makanan atau ramuan. Sosok itu menangis kecewa."
        else:
            given_item = food_potions[0]
            inv.remove(given_item)
            updates["inventory"] = inv
            
            if random.random() < 0.70:
                updates["gold"] = player.get("gold", 0) + 100
                result_msg = f"🍞 Kamu memberikan *{given_item['name']}*. Ia menangis haru. 'Terima kasih... ambillah emas ini.' (+100 Gold)"
            else:
                stolen_gold = random.randint(30, 80)
                updates["gold"] = max(0, player.get("gold", 0) - stolen_gold)
                result_msg = f"🍞 Saat kamu memberikan *{given_item['name']}*, ia tiba-tiba merampas kantong emasmu dan kabur! (-{stolen_gold} Gold)"

    # --- LOGIKA LORE KEEPER ---
    elif npc_type == "lore_keeper" and action_choice == "listen_story":
        chosen_story = random.choice(LORE_STORIES)
        unlocked_lores = player.get("unlocked_lores", [])
        
        if chosen_story not in unlocked_lores:
            unlocked_lores.append(chosen_story)
            updates["unlocked_lores"] = unlocked_lores
            updates["exp"] = player.get("exp", 0) + 100
            updates["max_mp"] = player.get("max_mp", 50) + 2
            bonus_text = "\n\n*(Cerita Baru Terbuka! +100 EXP, +2 Max MP)*"
        else:
            updates["mp"] = min(player.get("max_mp", 50), player.get("mp", 0) + 15)
            bonus_text = "\n\n*(Mendengarkan ulang menenangkan pikiranmu. +15 MP)*"

        result_msg = f"📖 *Fallen Weaver bercerita:*\n\n{chosen_story}{bonus_text}"

    # --- LOGIKA WANDERER ---
    elif npc_type == "wanderer" and action_choice == "accept_gift":
        if random.random() < 0.5:
            gold = random.randint(20, 50)
            updates["gold"] = player.get("gold", 0) + gold
            result_msg = f"✨ Kamu menerima {gold} Gold dari pengembara itu."
        else:
            inv = player.get("inventory", [])
            inv.append({"id": "buy_heal_30", "name": "Minor HP Potion", "type": "potion", "effect": "heal_30"})
            updates["inventory"] = inv
            result_msg = "✨ Pengembara itu menyodorkan sebotol [Minor HP Potion] sebelum menghilang!"

    return result_msg, updates
