# game/data/npc_data.py

"""
DATABASE NPC (Non-Playable Characters) - The Archivus
Total: 100 NPC (10 Kategori x 10 Variasi)
Tema: Psychological Horror & Despair
Fungsional: Mendukung sistem eksekusi otomatis di event_handler.py
"""

NPC_POOL = {
    # 1. HEALER (Pemulih HP)
    "healer": [
        {"name": "The Blind Surgeon", "type": "heal", "narration": "'Matamu terlihat lelah. Biarkan aku menjahitnya, dan kau akan merasa lebih baik...'", "cost": 15, "value": 30},
        {"name": "The Leech Mother", "type": "heal", "narration": "Ratusan lintah merayap di tubuhnya. 'Mereka haus, Weaver. Biarkan mereka menghisap rasa sakitmu.'", "cost": 20, "value": 35},
        {"name": "The Flesh Weaver", "type": "heal", "narration": "'Kulitmu robek. Aku punya kulit sisa dari Weaver sebelummu. Mau kutambal?'", "cost": 25, "value": 40},
        {"name": "The Memory Stitcher", "type": "heal", "narration": "'Aku tidak menyembuhkan luka. Aku hanya menghapus ingatan saat kau terluka.'", "cost": 15, "value": 25},
        {"name": "The Ash Doctor", "type": "heal", "narration": "Ia menaburkan abu hangat ke lukamu. Tiba-tiba kau ingat abu itu berasal dari tulang manusia.", "cost": 30, "value": 45},
        {"name": "The Silent Apothecary", "type": "heal", "narration": "Ia tidak bicara. Ia hanya menyodorkan botol berisi cairan hitam kental.", "cost": 20, "value": 30},
        {"name": "The Tear Collector", "type": "heal", "narration": "'Menangislah untukku, dan aku akan menutup lukamu dengan air matamu sendiri.'", "cost": 10, "value": 20},
        {"name": "The Bone Setter", "type": "heal", "narration": "*KRAK.* Ia mematahkan jarinya sendiri lalu tersenyum. 'Sekarang giliranmu.'", "cost": 35, "value": 50},
        {"name": "The Hollow Nurse", "type": "heal", "narration": "Wajahnya rata tanpa fitur. 'Waktunya minum obat... jangan dimuntahkan lagi.'", "cost": 15, "value": 30},
        {"name": "The Blood Drinker", "type": "heal", "narration": "'Beri aku emasmu, dan aku akan memuntahkan kembali darahmu.'", "cost": 25, "value": 40}
    ],

    # 2. TRICKSTER (Penjudi / Gacha)
    "trickster": [
        {"name": "The Coin Swallower", "type": "gamble", "narration": "'Masukkan koin ke dalam mulutku. Jika aku tersedak, kau menang.'", "bet": 40, "chance": 0.45},
        {"name": "The Fate Dealer", "type": "gamble", "narration": "Ia mengocok kartu dari kulit manusia. 'Pilih kartumu. Hidup, atau mati?'", "bet": 50, "chance": 0.5},
        {"name": "The Grinning Man", "type": "gamble", "narration": "Senyumnya terlalu lebar. 'Ayo main tebak-tebakan nyawa!'", "bet": 30, "chance": 0.4},
        {"name": "The Shadow Gambler", "type": "gamble", "narration": "'Pasang emasmu. Jika kalah, bayanganmu akan tinggal di sini bersamaku.'", "bet": 60, "chance": 0.48},
        {"name": "The Handless Thief", "type": "gamble", "narration": "Ia tidak punya tangan, tapi kau merasa ada jemari dingin meraba lehermu.", "bet": 45, "chance": 0.42},
        {"name": "The Eye Taker", "type": "gamble", "narration": "'Koin emas mengkilap... persis seperti bola matamu.'", "bet": 70, "chance": 0.35},
        {"name": "The Liar", "type": "gamble", "narration": "'Aku pasti akan memberimu hadiah. Percayalah padaku.'", "bet": 20, "chance": 0.3},
        {"name": "The Jester of Rot", "type": "gamble", "narration": "Tawanya terdengar seperti tulang berderak. 'Pilih tangan kanan atau kiri!'", "bet": 55, "chance": 0.45},
        {"name": "The Soul Broker", "type": "gamble", "narration": "'Emas untuk nyawa. Nyawa untuk emas. Putar rodanya, Weaver!'", "bet": 80, "chance": 0.5},
        {"name": "The Faceless Dealer", "type": "gamble", "narration": "Wajahnya memantulkan wajahmu sendiri. 'Pasang taruhanmu, pengecut.'", "bet": 40, "chance": 0.45}
    ],

    # 3. SCHOLAR (Kuis Lore)
    # Gunakan key 'quiz' untuk divalidasi oleh puzzle_manager.py
    "scholar": [
        {"name": "The Mad Scribe", "type": "quiz", "narration": "Ia menulis menggunakan kukunya yang berdarah. 'Jawab, atau kujadikan kau tinta!'", "reward": 200},
        {"name": "The Blind Reader", "type": "quiz", "narration": "Matanya dijahit. 'Pengetahuan adalah kutukan. Uji kutukanmu.'", "reward": 150},
        {"name": "The Torn Page", "type": "quiz", "narration": "Tubuhnya terbuat dari kertas terbakar. 'Bacakan sejarah yang terlupakan.'", "reward": 180},
        {"name": "The Babbler", "type": "quiz", "narration": "Ia menggumamkan ribuan kata per detik. Tiba-tiba ia berhenti. 'Giliranmu.'", "reward": 100},
        {"name": "The Ink Drinker", "type": "quiz", "narration": "Mulutnya hitam pekat. 'Buktikan kau punya kata yang lezat.'", "reward": 250},
        {"name": "The Dust Eater", "type": "quiz", "narration": "'Buku-buku ini sudah membusuk. Hanya memori yang tersisa.'", "reward": 120},
        {"name": "The Forgotten Archivist", "type": "quiz", "narration": "Ia tidak punya nama. 'Jika kau tidak tahu sejarah, kau akan mengulanginya.'", "reward": 300},
        {"name": "The Mute Philosopher", "type": "quiz", "narration": "Ia memotong lidahnya sendiri, menyodorkannya padamu sebagai pertanyaan.", "reward": 400},
        {"name": "The Screaming Book", "type": "quiz", "narration": "Buku di tangannya menjerit kesakitan. 'Baca!'", "reward": 220},
        {"name": "The Observer", "type": "quiz", "narration": "'Aku telah melihat ribuan Weaver mati. Mengapa kau berbeda?'", "reward": 500}
    ],

    # 4. MERCENARY (Buff Permanen)
    "mercenary": [
        {"name": "The Broken Sword", "type": "buff", "narration": "'Bayar aku, kuajarkan cara mati dengan lambat.'", "cost": 100, "stat": "atk", "val": 3},
        {"name": "The Headless Knight", "type": "buff", "narration": "'Pukulan yang baik adalah pukulan yang tak kau lihat.'", "cost": 120, "stat": "atk", "val": 4},
        {"name": "The Butcher", "type": "buff", "narration": "'Daging musuh sama lembutnya dengan dagingmu.'", "cost": 90, "stat": "atk", "val": 2},
        {"name": "The Rust Eater", "type": "buff", "narration": "'Emasmu bisa kubeli untuk mengasah senjatamu.'", "cost": 110, "stat": "atk", "val": 3},
        {"name": "The Meat Shield", "type": "buff", "narration": "'Sakit itu hanya ilusi. Berikan koinmu, kuajarkan kebas.'", "cost": 130, "stat": "def", "val": 5},
        {"name": "The Crimson Guard", "type": "buff", "narration": "Armor miliknya terbuat dari darah. 'Kau terlalu lembek.'", "cost": 150, "stat": "def", "val": 6},
        {"name": "The Executioner", "type": "buff", "narration": "Kapak besarnya menyeret lantai. 'Leher yang putus tidak akan berteriak.'", "cost": 140, "stat": "atk", "val": 5},
        {"name": "The Iron Husk", "type": "buff", "narration": "Armor kosong yang bergerak sendiri. 'Belajarlah menjadi besi.'", "cost": 160, "stat": "def", "val": 8},
        {"name": "The Flagellant", "type": "buff", "narration": "'Rasa sakit adalah guru terbaik. Bayar aku.'", "cost": 80, "stat": "atk", "val": 2},
        {"name": "The Cowardly Vet", "type": "buff", "narration": "'Aku selamat karena aku tahu cara lari. Bayar aku.'", "cost": 100, "stat": "spd", "val": 3}
    ],

    # 5. CURSE EATER (Tukar HP ke MP)
    "curse_eater": [
        {"name": "The Sin Swallower", "type": "convert", "narration": "'Beri aku darah kotormu, kuberikan sihir untukmu.'", "hp_loss": 20, "mp_gain": 15},
        {"name": "The Vomiter", "type": "convert", "narration": "'Tukar... tukar nyawamu dengan manaku...'", "hp_loss": 25, "mp_gain": 20},
        {"name": "The Plague Breath", "type": "convert", "narration": "'Sebagian jiwamu membusuk. Biarkan aku memakannya.'", "hp_loss": 15, "mp_gain": 10},
        {"name": "The Miasma Drinker", "type": "convert", "narration": "'Kau butuh sihir? Berdarahlah untukku.'", "hp_loss": 30, "mp_gain": 25},
        {"name": "The Rotten Mouth", "type": "convert", "narration": "Giginya rontok saat tersenyum. 'Darah untuk Mana. Setara.'", "hp_loss": 10, "mp_gain": 5},
        {"name": "The Curse Bloated", "type": "convert", "narration": "Tubuhnya penuh nanah bercahaya biru. 'Tusuk aku, minumlah.'", "hp_loss": 40, "mp_gain": 35},
        {"name": "The Leper Priest", "type": "convert", "narration": "'Tukarkan darahmu, Weaver.'", "hp_loss": 20, "mp_gain": 15},
        {"name": "The Purger", "type": "convert", "narration": "'Makhluk ini akan mengubah darahmu menjadi sihir cair.'", "hp_loss": 15, "mp_gain": 15},
        {"name": "The Hollow Vein", "type": "convert", "narration": "'Isi nadiku dengan HP-mu, kuberikan MP-ku padamu.'", "hp_loss": 35, "mp_gain": 30},
        {"name": "The Sufferer", "type": "convert", "narration": "'Sakit sekali... bagi rasa sakitmu denganku.'", "hp_loss": 10, "mp_gain": 10}
    ],

    # 6. COLLECTOR (Beli Rongsokan)
    "collector": [
        {"name": "The Bone Hoarder", "type": "buy", "narration": "'Punya tulang ekstra? Tidak? Potion saja kalau begitu.'", "item_wanted": "any_potion", "price": 100},
        {"name": "The Nail Plucker", "type": "buy", "narration": "Kukunya terbuat dari koin emas. 'Berikan barang rongsokanmu.'", "item_wanted": "scrap_metal", "price": 50},
        {"name": "The Hair Weaver", "type": "buy", "narration": "'Aku butuh barangmu. Harganya pantas.'", "item_wanted": "torn_fabric", "price": 30},
        {"name": "The Scavenger", "type": "buy", "narration": "'Sisa makananmu... potion bekasmu... jual padaku.'", "item_wanted": "empty_bottle", "price": 20},
        {"name": "The Trash Lord", "type": "buy", "narration": "'Yang tak berguna bagimu adalah harta bagiku.'", "item_wanted": "broken_hilt", "price": 60},
        {"name": "The Eye Collector", "type": "buy", "narration": "'Ada yang mau dijual? Jangan menatapku begitu.'", "item_wanted": "strange_eye", "price": 150},
        {"name": "The Tooth Fairy", "type": "buy", "narration": "Monster berbaju compang-camping. 'Koin untuk barang bekasmu?'", "item_wanted": "old_tooth", "price": 80},
        {"name": "The Rat King", "type": "buy", "narration": "'KAMI LAPAR. KAMI BELI BARANGMU.'", "item_wanted": "rotten_meat", "price": 40},
        {"name": "The Magpie", "type": "buy", "narration": "'Benda berkilau... aku mau!'", "item_wanted": "shiny_trinket", "price": 200},
        {"name": "The Corpse Looter", "type": "buy", "narration": "'Hei, mau jual barang sebelum kau juga mati?'", "item_wanted": "survivor_badge", "price": 120}
    ],

    # 7. GUIDE (Pemandu Arah)
    "guide": [
        {"name": "The Blind Point", "type": "info", "narration": "Jari telunjuknya terpotong, tapi menunjuk ke Utara. 'Ikuti bau darahnya.'"},
        {"name": "The Weeping Compass", "type": "info", "narration": "Gadis kecil memegang kompas yang berputar liar. 'Jalannya... membingungkan.'"},
        {"name": "The Liar's Post", "type": "info", "narration": "Pria berwajah dua. 'Mau kutunjukkan jalan yang benar?'"},
        {"name": "The False Prophet", "type": "info", "narration": "'Aku melihat cahaya di ujung sana. Cahaya yang membakar.'"},
        {"name": "The Lantern Bearer", "type": "info", "narration": "Lenteranya menggunakan jantung sebagai sumbu. 'Biar kuterangi masa depanmu.'"},
        {"name": "The Lost Soul", "type": "info", "narration": "'Aku sudah berjalan 100 tahun. Biar kuberitahu arahnya.'"},
        {"name": "The Crawling Guide", "type": "info", "narration": "Ia merangkak perlahan. 'Jalan yang aman ada di bawah tanah.'"},
        {"name": "The Stargazer", "type": "info", "narration": "Melihat ke atas meski tak ada langit. 'Bintang mengatakan kau mati di kiri.'"},
        {"name": "The Mute Pointer", "type": "info", "narration": "Ia memiringkan kepalanya sampai tulang lehernya patah, menunjuk arah."},
        {"name": "The Drowning Guide", "type": "info", "narration": "Air hitam keluar dari mulutnya. 'Tenggelamlah bersamaku.'"}
    ],

    # 8. BEGGAR (Pengemis Item)
    "beggar": [
        {"name": "The Starving Husk", "type": "request", "narration": "'Lapar... tolong...'", "item_needed": "bread_01", "reward_luck": 1},
        {"name": "The Cold One", "type": "request", "narration": "'Ramuan... untuk menghangatkan jantungku.'", "item_needed": "potion_heal", "reward_luck": 2},
        {"name": "The Flesh Hungry", "type": "request", "narration": "'Roti... atau jarimu... kumohon.'", "item_needed": "dried_meat", "reward_luck": 1},
        {"name": "The Forgotten Child", "type": "request", "narration": "'Ibu belum pulang... aku lapar.'", "item_needed": "apple_01", "reward_luck": 3},
        {"name": "The Empty Belly", "type": "request", "narration": "'Berikan aku sesuatu yang bisa ditelan.'", "item_needed": "bread_01", "reward_luck": 1},
        {"name": "The Thirsty Wretch", "type": "request", "narration": "'Apa saja yang cair... tolong.'", "item_needed": "water_bottle", "reward_luck": 1},
        {"name": "The Shivering Beggar", "type": "request", "narration": "'Sedekah untuk jiwa yang kedinginan ini?'", "item_needed": "mantel_bulu", "reward_luck": 5},
        {"name": "The Scraped Soul", "type": "request", "narration": "'Apakah kau punya sisa makanan?'", "item_needed": "bread_01", "reward_luck": 1},
        {"name": "The Hollowed Out", "type": "request", "narration": "'Isi lubang ini... dengan makananmu.'", "item_needed": "rotten_meat", "reward_luck": 1},
        {"name": "The Wretch", "type": "request", "narration": "'Jangan tatap aku. Beri aku makan saja.'", "item_needed": "bread_01", "reward_luck": 1}
    ],

    # 9. LORE KEEPER (Pembuka Cerita)
    "lore_keeper": [
        {"name": "The Stone Mouth", "type": "lore", "narration": "Patung batu yang bibirnya bergerak lambat. 'Dengarkan kisah sebelum hancur.'"},
        {"name": "The Echoing Skull", "type": "lore", "narration": "Tengkorak melayang pelan. 'Rahasianya ada di dinding.'"},
        {"name": "The Dying Breath", "type": "lore", "narration": "Waktuku habis. Bawa ingatanku bersamamu."},
        {"name": "The Mad Historian", "type": "lore", "narration": "Mencabut rambutnya sendiri. 'Semuanya bohong!'"},
        {"name": "The Whisperer", "type": "lore", "narration": "Hanya berupa suara di telingamu. 'Biar kuceritakan mengapa kita terjebak.'"},
        {"name": "The Last King", "type": "lore", "narration": "'Kerajaanku runtuh karena sebuah buku.'"},
        {"name": "The First Weaver", "type": "lore", "narration": "Tubuhnya menyatu dengan lantai. 'Aku yang pertama mati di sini.'"},
        {"name": "The Trapped Soul", "type": "lore", "narration": "Terperangkap di dalam kristal hitam. 'Lepaskan aku dengan mendengar ceritaku.'"},
        {"name": "The Prophet of Ash", "type": "lore", "narration": "Debu keluar dari mulutnya. 'Sejarah adalah masa depan yang berulang.'"},
        {"name": "The Weeping Historian", "type": "lore", "narration": "'Buku ini tidak mau menceritakannya. Biar aku saja.'"}
    ],

    # 10. WANDERER (Hadiah Gratis)
    "wanderer": [
        {"name": "The Passing Shadow", "type": "gift", "narration": "Bayangan gelap lewat tanpa suara, menjatuhkan sesuatu.", "gift_item": "old_coin"},
        {"name": "The Silent Walker", "type": "gift", "narration": "Ia menembus tubuhmu. Meninggalkan rasa dingin dan sebuah benda.", "gift_item": "potion_heal"},
        {"name": "The Faceless Drifter", "type": "gift", "narration": "Tiba-tiba ada benda di genggamanmu.", "gift_item": "gold_small"},
        {"name": "The Smiling Man", "type": "gift", "narration": "Senyum yang tidak akan kau lupakan. Ia melempar sesuatu.", "gift_item": "cursed_needle"},
        {"name": "The Tall One", "type": "gift", "narration": "Ia menunduk dan memberikanmu hadiah dalam diam.", "gift_item": "mana_shard"},
        {"name": "The Observer", "type": "gift", "narration": "Berdiri di sudut gelap. Ia melempar sebuah koin.", "gift_item": "gold_small"},
        {"name": "The Mirror", "type": "gift", "narration": "Sosok yang perawakannya persis seperti dirimu. Ia menjatuhkan sesuatu.", "gift_item": "identity_fragment"},
        {"name": "The Twin", "type": "gift", "narration": "'Jangan mati hari ini,' menyelipkan sesuatu di sakumu.", "gift_item": "luck_charm"},
        {"name": "The Follower", "type": "gift", "narration": "Ia sudah mengikutimu sejak lama. Ia maju, memberi barang.", "gift_item": "bread_01"},
        {"name": "The Grateful Dead", "type": "gift", "narration": "Mayat Weaver bangkit, menyerahkan barangnya, lalu hancur.", "gift_item": "rusty_key"}
    ]
}

LORE_STORIES = [
    "Dimensi ini dulunya adalah perpustakaan para Dewa. *The Archivus* dirancang untuk menyimpan rahasia semesta.",
    "Kita adalah penjahit realitas yang ditarik dari kematian kita sendiri. Kuburan itu? Itu adalah saudara-saudaramu.",
    "Koin emas yang kau gunakan bukanlah logam. Itu adalah pecahan waktu dari jiwa-jiwa yang membusuk.",
    "Sang Penjaga yang kau buru dulunya adalah Orion, Weaver Pertama. Ia mencoba membaca 'Kitab Akhir Zaman' sendirian.",
    "Rawa tinta hijau beracun dulunya adalah ruang arsip puisi. Kebohongan manusia menetes ke bawah, membusuk menjadi Miasma.",
    "Jika kau merobek dada Sang Penjaga, kau akan menemukan jantung yang membatu.",
    "Terkadang aku berpikir, apakah kita benar-benar hidup, atau kita hanyalah karakter dari sebuah game?"
]
