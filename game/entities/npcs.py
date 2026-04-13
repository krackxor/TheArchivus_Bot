"""
Sistem NPC (Non-Playable Characters)
Mengatur pertemuan, dialog, dan logika interaksi dengan karakter di Archivus.
"""
import random

# --- GENERATOR NAMA NPC ---
PREFIXES = ["The Blind", "The Hollow", "The Wandering", "The Forgotten", "The Faceless", "The Cursed"]
NOUNS = ["Seer", "Scribe", "Thief", "Weaver", "Archivist", "Merchant", "Oracle"]

def generate_random_npc_name():
    """Menghasilkan nama acak untuk NPC biasa"""
    return f"{random.choice(PREFIXES)} {random.choice(NOUNS)}"

# --- LOGIKA ENCOUNTER NPC ---
def get_npc_encounter(cycle=1):
    """
    Menghasilkan data encounter NPC secara acak beserta pilihan interaksinya.
    Digunakan saat pemain melangkah dan memicu event NPC.
    """
    npc_types = ["healer", "trickster", "scholar", "wanderer"]
    
    # Probabilitas bisa diatur, misalnya trickster lebih sering muncul
    weights = [0.3, 0.3, 0.2, 0.2] 
    chosen_type = random.choices(npc_types, weights=weights, k=1)[0]
    
    if chosen_type == "healer":
        cost = random.randint(15, 25) + (cycle * 5)
        heal = random.randint(30, 50) + (cycle * 10)
        return {
            "id": "npc_healer",
            "name": "The Blind Seer",
            "type": "healer",
            "narration": f"Kamu bertemu dengan The Blind Seer. Matanya tertutup kain lusuh, namun ia menatap tepat ke arah jiwamu.\n\n*'Luka-lukamu bercerita banyak, Weaver...'*\n\nIa menawarkan ramuan penenang seharga {cost} Gold untuk memulihkan {heal} HP.",
            "choices": [
                {"text": f"Sembuhkan (-{cost} Gold)", "action": "heal", "cost": cost, "value": heal},
                {"text": "Tolak dan Pergi", "action": "leave"}
            ]
        }
        
    elif chosen_type == "trickster":
        bet = random.randint(30, 60)
        return {
            "id": "npc_trickster",
            "name": "The Memory Thief",
            "type": "trickster",
            "narration": f"Sesosok bayangan tersenyum licik dari balik pilar runtuh. Itu adalah The Memory Thief.\n\n*'Ayo bermain permainan peluang, Weaver! Bertaruhlah {bet} Gold. Kau bisa menggandakannya, mendapatkan artefak, atau... kehilangan segalanya!'*",
            "choices": [
                {"text": f"Gamble! (-{bet} Gold)", "action": "gamble", "cost": bet},
                {"text": "Abaikan saja", "action": "leave"}
            ]
        }
        
    elif chosen_type == "scholar":
        return {
            "id": "npc_scholar",
            "name": "The Hollow Scribe",
            "type": "scholar",
            "narration": "Seorang Scribe tanpa wajah duduk tenang dikelilingi ribuan perkamen yang melayang.\n\n*'Hanya mereka yang mengingat sejarah yang dapat bertahan di Archivus. Mari uji ingatanmu, Weaver.'*\n\nJika benar, kau akan diberi hadiah. Jika salah, kau akan terkena kutukan (Damage).",
            "choices": [
                {"text": "Terima Ujian Lore", "action": "quiz"},
                {"text": "Menjauh perlahan", "action": "leave"}
            ]
        }
        
    else: # wanderer
        return {
            "id": "npc_wanderer",
            "name": generate_random_npc_name(),
            "type": "wanderer",
            "narration": "Kamu melihat sesama Weaver yang tampak lelah. Ia memberimu senyuman tipis dan mengulurkan tangannya yang bersinar sebelum memudar menjadi kabut debu.",
            "choices": [
                {"text": "Sentuh cahayanya", "action": "accept_gift"},
                {"text": "Biarkan saja", "action": "leave"}
            ]
        }

# --- RESOLUSI AKSI NPC ---
def resolve_npc_action(player, npc_data, action_choice):
    """
    Memproses hasil dari pilihan pemain terhadap NPC.
    Mengembalikan tuple: (Pesan Hasil, Dictionary Update untuk Database)
    """
    updates = {}
    result_msg = ""
    
    if action_choice == "leave":
        return "Kamu memilih untuk mengabaikannya dan melanjutkan perjalanan ke dalam kabut.", updates

    npc_type = npc_data["type"]

    if npc_type == "healer" and action_choice == "heal":
        cost = npc_data["choices"][0]["cost"]
        heal = npc_data["choices"][0]["value"]
        
        if player.get("gold", 0) < cost:
            result_msg = "Kamu tidak memiliki cukup Gold! The Blind Seer mendesah kecewa dan menghilang."
        else:
            new_hp = min(player.get("max_hp", 100), player.get("hp", 100) + heal)
            updates["gold"] = player.get("gold", 0) - cost
            updates["hp"] = new_hp
            result_msg = f"✨ Segar! Kamu membayar {cost} Gold dan memulihkan {heal} HP.\n(HP Saat ini: {new_hp}/{player.get('max_hp')})"

    elif npc_type == "trickster" and action_choice == "gamble":
        cost = npc_data["choices"][0]["cost"]
        
        if player.get("gold", 0) < cost:
            result_msg = "The Memory Thief tertawa meremehkan. 'Kau terlalu miskin untuk bermain denganku!' Ia pun menghilang."
        else:
            updates["gold"] = player.get("gold", 0) - cost  # Kurangi dulu uangnya
            roll = random.random()
            
            if roll < 0.4: # 40% Kalah (Jebakan)
                damage = random.randint(10, 25)
                updates["hp"] = max(1, player.get("hp", 100) - damage)
                result_msg = f"❌ Sial! Koinnya meledak menjadi bayangan gelap! Kamu kehilangan {cost} Gold dan terkena {damage} Damage."
            
            elif roll < 0.75: # 35% Menang Gold (Selamat dari Jebakan)
                win_amount = int(cost * 2.5)
                updates["gold"] = updates["gold"] + win_amount
                updates["trap_survived"] = player.get("trap_survived", 0) + 1 # Untuk achievement "The Lucky One"
                result_msg = f"🎉 Jackpot! The Memory Thief mendengus kesal. Kamu memenangkan {win_amount} Gold!"
            
            else: # 25% Dapat Item langka
                inventory = player.get("inventory", [])
                inventory.append({"id": "lucky_charm", "name": "Lucky Charm", "type": "artifact"})
                updates["inventory"] = inventory
                updates["trap_survived"] = player.get("trap_survived", 0) + 1 # Untuk achievement
                result_msg = "🎁 The Memory Thief tersenyum lebar. 'Kau sangat beruntung!' Ia memberimu sebuah artefak [Lucky Charm]."

    elif npc_type == "wanderer" and action_choice == "accept_gift":
        roll = random.random()
        if roll < 0.6: # 60% dapet Gold kecil
            found_gold = random.randint(15, 40)
            updates["gold"] = player.get("gold", 0) + found_gold
            result_msg = f"Cahaya itu berubah menjadi {found_gold} Gold di tanganmu. Teman sesama Weaver itu telah membantumu."
        else: # 40% dapet potion
            inventory = player.get("inventory", [])
            inventory.append({"id": "minor_potion", "name": "Minor Health Potion", "type": "potion"})
            updates["inventory"] = inventory
            result_msg = "Cahaya itu memadat menjadi botol kaca. Kamu mendapatkan 1x [Minor Health Potion]!"

    return result_msg, updates
