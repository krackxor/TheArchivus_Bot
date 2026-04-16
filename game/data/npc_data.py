# game/data/npc_data.py

"""
DATABASE NPC (Non-Playable Characters) - The Archivus
Total: 100 NPC (10 Kategori x 10 Variasi)
Tema: Psychological Horror & Despair
"""

NPC_POOL = {
    # =========================================================================
    # 1. HEALER (Pemulih)
    # Tugas/Mekanik : Memulihkan HP pemain.
    # Cost          : Gold (base_cost + scaling cycle).
    # Reward        : Heal HP (base_heal + scaling cycle).
    # Vibe          : Dokter bedah gila, makhluk parasit, atau perawat mengerikan.
    # =========================================================================
    "healer": [
        {"name": "The Blind Surgeon", "narration": "'Matamu terlihat lelah. Biarkan aku menjahitnya, dan kau akan merasa lebih baik...'", "base_cost": 15, "base_heal": 30},
        {"name": "The Leech Mother", "narration": "Ratusan lintah merayap di tubuhnya. 'Mereka haus, Weaver. Biarkan mereka menghisap rasa sakitmu.'", "base_cost": 20, "base_heal": 35},
        {"name": "The Flesh Weaver", "narration": "'Kulitmu robek. Aku punya kulit sisa dari Weaver sebelummu. Mau kutambal?'", "base_cost": 25, "base_heal": 40},
        {"name": "The Memory Stitcher", "narration": "'Aku tidak menyembuhkan luka. Aku hanya menghapus ingatan saat kau terluka. Harganya murah.'", "base_cost": 15, "base_heal": 25},
        {"name": "The Ash Doctor", "narration": "Ia menaburkan abu hangat ke lukamu. Tiba-tiba kau ingat abu itu berasal dari tulang manusia.", "base_cost": 30, "base_heal": 45},
        {"name": "The Silent Apothecary", "narration": "Ia tidak bicara. Ia hanya menyodorkan botol berisi cairan hitam kental yang berdenyut.", "base_cost": 20, "base_heal": 30},
        {"name": "The Tear Collector", "narration": "'Menangislah untukku, dan aku akan menutup lukamu dengan air matamu sendiri.'", "base_cost": 10, "base_heal": 20},
        {"name": "The Bone Setter", "narration": "*KRAK.* Ia mematahkan jarinya sendiri lalu tersenyum. 'Sekarang giliranmu.'", "base_cost": 35, "base_heal": 50},
        {"name": "The Hollow Nurse", "narration": "Wajahnya rata tanpa fitur. 'Waktunya minum obat... jangan dimuntahkan lagi.'", "base_cost": 15, "base_heal": 30},
        {"name": "The Blood Drinker", "narration": "'Beri aku emasmu, dan aku akan memuntahkan kembali darah yang hilang dari tubuhmu.'", "base_cost": 25, "base_heal": 40}
    ],

    # =========================================================================
    # 2. TRICKSTER (Penipu/Penjudi)
    # Tugas/Mekanik : Mengajak pemain bertaruh (Gacha).
    # Cost          : Gold (base_bet + scaling cycle).
    # Reward        : 45% Kalah (-HP), 40% Menang (+Gold 3x lipat), 15% Artefak Langka.
    # Vibe          : Penjudi iblis, pencuri jiwa, makhluk licik.
    # =========================================================================
    "trickster": [
        {"name": "The Coin Swallower", "narration": "'Masukkan koin ke dalam mulutku. Jika aku tersedak, kau menang. Jika tidak... kau milikku.'", "base_bet": 40},
        {"name": "The Fate Dealer", "narration": "Ia mengocok kartu yang terbuat dari kulit manusia. 'Pilih kartumu. Hidup, atau mati?'", "base_bet": 50},
        {"name": "The Grinning Man", "narration": "Senyumnya terlalu lebar, merobek pipinya sendiri. 'Ayo main tebak-tebakan nyawa!'", "base_bet": 30},
        {"name": "The Shadow Gambler", "narration": "'Pasang emasmu. Jika kalah, bayanganmu akan tinggal di sini bersamaku selamanya.'", "base_bet": 60},
        {"name": "The Handless Thief", "narration": "Ia tidak punya tangan, tapi kau merasa ada jemari dingin meraba lehermu. 'Taruhan?'", "base_bet": 45},
        {"name": "The Eye Taker", "narration": "'Koin emas mengkilap... persis seperti bola matamu. Berani bertaruh?'", "base_bet": 70},
        {"name": "The Liar", "narration": "'Aku pasti akan memberimu hadiah. Percayalah padaku. Kapan aku pernah berbohong?'", "base_bet": 20},
        {"name": "The Jester of Rot", "narration": "Tawanya terdengar seperti tulang berderak. 'Pilih tangan kanan atau kiri! Keduanya berdarah!'", "base_bet": 55},
        {"name": "The Soul Broker", "narration": "'Emas untuk nyawa. Nyawa untuk emas. Putar rodanya, Weaver!'", "base_bet": 80},
        {"name": "The Faceless Dealer", "narration": "Wajahnya memantulkan wajahmu sendiri yang sedang menangis. 'Pasang taruhanmu, pengecut.'", "base_bet": 40}
    ],

    # =========================================================================
    # 3. SCHOLAR (Pemberi Kuis)
    # Tugas/Mekanik : Menguji pengetahuan pemain tentang game ini.
    # Interaksi     : Memicu state Kuis Lore.
    # Vibe          : Pustakawan gila, pembaca pikiran, buku yang hidup.
    # =========================================================================
    "scholar": [
        {"name": "The Mad Scribe", "narration": "Ia menulis menggunakan kukunya yang berdarah. 'Jawab pertanyaanku, atau kujadikan kau tinta!'"},
        {"name": "The Blind Reader", "narration": "Matanya dijahit, tapi ia membaca pikiranmu. 'Pengetahuan adalah kutukan. Uji kutukanmu.'"},
        {"name": "The Torn Page", "narration": "Tubuhnya terbuat dari kertas yang terbakar. 'Bacakan sejarah yang terlupakan padaku.'"},
        {"name": "The Babbler", "narration": "Ia menggumamkan ribuan kata per detik. Tiba-tiba ia berhenti dan menatapmu. 'Giliranmu.'"},
        {"name": "The Ink Drinker", "narration": "Mulutnya hitam pekat. 'Aku memakan kata-kata. Buktikan kau punya kata yang lezat.'"},
        {"name": "The Dust Eater", "narration": "'Buku-buku ini sudah membusuk. Hanya memori yang tersisa. Apa kau ingat?'"},
        {"name": "The Forgotten Archivist", "narration": "Ia tidak punya nama. 'Jika kau tidak tahu sejarah, kau akan mengulanginya. Uji dirimu.'"},
        {"name": "The Mute Philosopher", "narration": "Ia memotong lidahnya sendiri, lalu menyodorkannya padamu sebagai pertanyaan."},
        {"name": "The Screaming Book", "narration": "Buku di tangannya menjerit kesakitan setiap kali halamannya dibalik. 'Baca!'"},
        {"name": "The Observer", "narration": "'Aku telah melihat ribuan Weaver mati. Tunjukkan padaku mengapa kau berbeda.'"}
    ],

    # =========================================================================
    # 4. MERCENARY (Mentor Tempur)
    # Tugas/Mekanik : Memberikan Buff Permanen (Base ATK).
    # Cost          : Sangat mahal (base_cost + scaling besar).
    # Reward        : Base ATK +2 secara permanen.
    # Vibe          : Prajurit yang disiksa, algojo, monster brutal.
    # =========================================================================
    "mercenary": [
        {"name": "The Broken Sword", "narration": "Pedangnya patah, tubuhnya penuh tombak. 'Bayar aku, kuajarkan cara mati dengan lambat.'", "base_cost": 100},
        {"name": "The Headless Knight", "narration": "Ia memegang kepalanya di tangan kiri. 'Pukulan yang baik adalah pukulan yang tak kau lihat.'", "base_cost": 120},
        {"name": "The Butcher", "narration": "Celemeknya basah oleh darah segar. 'Daging musuh sama lembutnya dengan dagingmu. Biar kutunjukkan.'", "base_cost": 90},
        {"name": "The Rust Eater", "narration": "'Emasmu bisa kubeli untuk mengasah senjatamu dengan karat.'", "base_cost": 110},
        {"name": "The Meat Shield", "narration": "Tubuhnya penuh bekas gigitan. 'Sakit itu hanya ilusi. Berikan koinmu, kuajarkan kebas.'", "base_cost": 130},
        {"name": "The Crimson Guard", "narration": "Armor miliknya terbuat dari darah yang mengeras. 'Kau terlalu lembek. Butuh latihan?'", "base_cost": 150},
        {"name": "The Executioner", "narration": "Kapak besarnya menyeret lantai. 'Leher yang putus tidak akan bisa berteriak.'", "base_cost": 140},
        {"name": "The Iron Husk", "narration": "Armor kosong yang bergerak sendiri. 'Kelemahanmu adalah dagingmu. Belajarlah menjadi besi.'", "base_cost": 160},
        {"name": "The Flagellant", "narration": "Ia terus mencambuk punggungnya sendiri. 'Rasa sakit adalah guru terbaik. Bayar aku.'", "base_cost": 80},
        {"name": "The Cowardly Vet", "narration": "'Aku selamat karena aku tahu cara lari. Tapi aku bisa mengajarimu cara memukul dari belakang.'", "base_cost": 100}
    ],

    # =========================================================================
    # 5. CURSE EATER (Tukar Darah)
    # Tugas/Mekanik : Menukar HP pemain menjadi MP.
    # Cost          : -20 HP.
    # Reward        : +30 MP.
    # Vibe          : Pemakan dosa, makhluk menjijikkan penuh penyakit.
    # =========================================================================
    "curse_eater": [
        {"name": "The Sin Swallower", "narration": "Perutnya bengkak dan berdenyut. 'Beri aku darah kotormu, aku akan memuntahkan sihir untukmu.'"},
        {"name": "The Vomiter", "narration": "Ia terus memuntahkan miasma hitam. 'Tukar... tukar nyawamu dengan manaku...'"},
        {"name": "The Plague Breath", "narration": "Napasnya membuat lenteramu redup. 'Sebagian jiwamu membusuk. Biarkan aku memakannya.'"},
        {"name": "The Miasma Drinker", "narration": "Ia meminum udara beracun dari sekitarnya. 'Kau butuh sihir? Berdarahlah untukku.'"},
        {"name": "The Rotten Mouth", "narration": "Giginya rontok saat ia tersenyum. 'Darah untuk Mana. Setara, bukan?'"},
        {"name": "The Curse Bloated", "narration": "Tubuhnya penuh nanah bercahaya biru. 'Tusuk aku, minumlah.'"},
        {"name": "The Leper Priest", "narration": "'Kesucian dicapai melalui penderitaan fisik. Tukarkan darahmu, Weaver.'"},
        {"name": "The Purger", "narration": "Ia memegang lintah raksasa. 'Makhluk ini akan mengubah darahmu menjadi sihir cair.'"},
        {"name": "The Hollow Vein", "narration": "Urat nadinya kosong dan transparan. 'Isi nadiku dengan HP-mu, kuberikan MP-ku padamu.'"},
        {"name": "The Sufferer", "narration": "Ia menangis tanpa henti. 'Sakit sekali... tolong bagi rasa sakitmu denganku.'"}
    ],

    # =========================================================================
    # 6. COLLECTOR (Pembeli Rongsok)
    # Tugas/Mekanik : Membeli item (Potion/Food) dari inventory pemain.
    # Cost          : Item konsumsi dari tas pemain.
    # Reward        : Gold dalam jumlah besar (40-90 Gold).
    # Vibe          : Pengumpul sampah, pemulung mayat, monster obsesif.
    # =========================================================================
    "collector": [
        {"name": "The Bone Hoarder", "narration": "Tasnya bergemerincing. 'Punya tulang ekstra? Tidak? Potion saja kalau begitu. Aku bayar mahal.'"},
        {"name": "The Nail Plucker", "narration": "Kukunya terbuat dari koin emas. 'Berikan barang rongsokanmu kepadaku.'"},
        {"name": "The Hair Weaver", "narration": "Ia menjahit jubah dari rambut manusia. 'Aku butuh barangmu. Harganya pantas.'"},
        {"name": "The Scavenger", "narration": "Berjalan merangkak, memakan debu. 'Sisa makananmu... potion bekasmu... jual padaku.'"},
        {"name": "The Trash Lord", "narration": "Duduk di atas gunungan sampah. 'Yang tak berguna bagimu adalah harta bagiku.'"},
        {"name": "The Eye Collector", "narration": "Stoples di tangannya penuh dengan bola mata. 'Ada yang mau dijual? Jangan menatapku begitu.'"},
        {"name": "The Tooth Fairy", "narration": "Bukan peri, melainkan monster besar berbaju compang-camping. 'Koin untuk barang bekasmu?'"},
        {"name": "The Rat King", "narration": "Ratusan tikus bergabung membentuk tubuhnya. 'KAMI LAPAR. KAMI BELI BARANGMU.'"},
        {"name": "The Magpie", "narration": "Makhluk bersayap cacat. 'Benda berkilau... atau ramuan... aku mau! Kubeli!'"},
        {"name": "The Corpse Looter", "narration": "Ia baru saja menggeledah tubuh Weaver lain. 'Hei, mau jual barang sebelum kau juga mati?'"}
    ],

    # =========================================================================
    # 7. GUIDE (Pemandu Arah)
    # Tugas/Mekanik : Memberi petunjuk mengenai jalan di depan.
    # Cost          : Gratis.
    # Reward        : 60% Petunjuk Benar, 40% Petunjuk Menyesatkan (Gaslighting).
    # Vibe          : Nabi palsu, orang gila, atau sosok yang tenggelam.
    # =========================================================================
    "guide": [
        {"name": "The Blind Point", "narration": "Jari telunjuknya terpotong, tapi ia menunjuk ke Utara. 'Ikuti bau darahnya, Weaver.'"},
        {"name": "The Weeping Compass", "narration": "Gadis kecil memegang kompas yang jarumnya berputar liar. 'Jalannya... jalannya membingungkan.'"},
        {"name": "The Liar's Post", "narration": "Pria berwajah dua. Satu tersenyum, satu menangis. 'Mau kutunjukkan jalan yang benar?'"},
        {"name": "The False Prophet", "narration": "'Aku melihat cahaya di ujung sana. Ya... cahaya yang membakar.'"},
        {"name": "The Lantern Bearer", "narration": "Lenteranya menggunakan jantung yang masih berdetak sebagai sumbu. 'Biar kuterangi masa depanmu.'"},
        {"name": "The Lost Soul", "narration": "'Aku sudah berjalan 100 tahun tapi selalu kembali ke sini. Biar kuberitahu arahnya.'"},
        {"name": "The Crawling Guide", "narration": "Ia tidak punya kaki, merangkak perlahan. 'Jalan yang aman ada di bawah tanah.'"},
        {"name": "The Stargazer", "narration": "Melihat ke atas meski tak ada langit. 'Bintang-bintang mengatakan kau akan mati di kiri.'"},
        {"name": "The Mute Pointer", "narration": "Ia hanya memiringkan kepalanya sampai tulang lehernya patah, menunjuk ke suatu arah."},
        {"name": "The Drowning Guide", "narration": "Air hitam terus keluar dari mulutnya. 'Tenggelamlah bersamaku, itu jalan pintas.'"}
    ],

    # =========================================================================
    # 8. BEGGAR (Pengemis)
    # Tugas/Mekanik : Meminta sedekah item dari pemain.
    # Cost          : 1 Item Potion/Food dari tas pemain.
    # Reward        : 70% Dapat +100 Gold, 30% Kerampokan (Kehilangan Gold).
    # Vibe          : Makhluk kelaparan, anak terlantar, jiwa yang menyedihkan.
    # =========================================================================
    "beggar": [
        {"name": "The Starving Husk", "narration": "Perutnya tembus pandang, kosong. 'Lapar... tolong... aku memakan lidahku sendiri kemarin.'"},
        {"name": "The Cold One", "narration": "Tubuhnya membeku. 'Ramuan... tolong... untuk menghangatkan jantungku yang mati.'"},
        {"name": "The Flesh Hungry", "narration": "Menatap tanganmu dengan air liur menetes. 'Roti... atau jarimu... kumohon.'"},
        {"name": "The Forgotten Child", "narration": "Suaranya seperti anak kecil, tapi wajahnya seperti orang tua. 'Ibu belum pulang... aku lapar.'"},
        {"name": "The Empty Belly", "narration": "Ia mencoba memakan batu. 'Tolong... berikan aku sesuatu yang bisa ditelan.'"},
        {"name": "The Thirsty Wretch", "narration": "Tenggorokannya kering kerontang. 'Potion... darah... apa saja yang cair... tolong.'"},
        {"name": "The Shivering Beggar", "narration": "Gemetar hebat hingga giginya retak. 'Sedekah untuk jiwa yang kedinginan ini?'"},
        {"name": "The Scraped Soul", "narration": "Mencakar dinding mencari lumut. 'Apakah kau punya sisa makanan, Weaver agung?'"},
        {"name": "The Hollowed Out", "narration": "Tubuhnya berlubang di bagian dada. 'Isi lubang ini... dengan makananmu.'"},
        {"name": "The Wretch", "narration": "Berlumuran lumpur tinta. 'Jangan tatap aku. Beri aku makan saja, lalu pergilah.'"}
    ],

    # =========================================================================
    # 9. LORE KEEPER (Pencerita Sejarah)
    # Tugas/Mekanik : Membuka Lore (Cerita) game.
    # Cost          : Gratis.
    # Reward        : Buka Cerita Baru -> +100 EXP & +2 Max MP. Cerita Lama -> +15 MP.
    # Vibe          : Tengkorak yang bicara, arwah raja masa lalu, nabi yang gila.
    # =========================================================================
    "lore_keeper": [
        {"name": "The Stone Mouth", "narration": "Patung batu yang bibirnya tiba-tiba bergerak lambat. 'Dengarkan kisah sebelum kau hancur.'"},
        {"name": "The Echoing Skull", "narration": "Tengkorak yang melayang pelan. 'Rahasianya ada di dinding. Mau kudongengkan?'"},
        {"name": "The Dying Breath", "narration": "Tubuhnya transparan, hampir menghilang. 'Waktuku habis. Bawa ingatanku bersamamu.'"},
        {"name": "The Mad Historian", "narration": "Mencabut rambutnya sendiri sambil tertawa. 'Semuanya bohong! Dewa itu bohong! Mau dengar?'"},
        {"name": "The Whisperer", "narration": "Hanya berupa suara di telingamu. 'Duduklah. Biar kuceritakan mengapa kita terjebak.'"},
        {"name": "The Last King", "narration": "Memakai mahkota dari duri karatan. 'Kerajaanku runtuh karena sebuah buku. Dengarkan.'"},
        {"name": "The First Weaver", "narration": "Tubuhnya menyatu dengan lantai marmer. 'Aku yang pertama mati di sini. Dengarkan pesanku.'"},
        {"name": "The Trapped Soul", "narration": "Terperangkap di dalam kristal hitam. 'Lepaskan aku dengan mendengar ceritaku.'"},
        {"name": "The Prophet of Ash", "narration": "Debu keluar dari mulutnya saat bicara. 'Sejarah adalah masa depan yang berulang.'"},
        {"name": "The Weeping Historian", "narration": "Menangis darah sambil memegang perkamen kosong. 'Buku ini tidak mau menceritakannya. Biar aku saja.'"}
    ],

    # =========================================================================
    # 10. WANDERER (Pengembara Misterius)
    # Tugas/Mekanik : Memberikan hadiah secara cuma-cuma.
    # Cost          : Gratis.
    # Reward        : 50% Dapat Gold, 50% Dapat HP Potion.
    # Vibe          : Bayangan yang lewat, doppelganger (kembaran), penguntit baik hati.
    # =========================================================================
    "wanderer": [
        {"name": "The Passing Shadow", "narration": "Bayangan gelap lewat tanpa suara, menjatuhkan sesuatu di dekat kakimu."},
        {"name": "The Silent Walker", "narration": "Ia berjalan melewati dan menembus tubuhmu. Meninggalkan rasa dingin dan sebuah benda."},
        {"name": "The Faceless Drifter", "narration": "Ia berdiri membelakangimu. Tiba-tiba ada benda di genggamanmu."},
        {"name": "The Smiling Man", "narration": "Ia tersenyum menatapmu. Senyum yang tidak akan pernah kau lupakan. Ia melempar sesuatu."},
        {"name": "The Tall One", "narration": "Tingginya menyentuh langit-langit. Ia menunduk dan memberikanmu hadiah dalam diam."},
        {"name": "The Observer", "narration": "Berdiri di sudut gelap, hanya matanya yang terlihat. Ia melempar sebuah koin."},
        {"name": "The Mirror", "narration": "Sosok yang perawakannya persis seperti dirimu berjalan berlawanan arah. Ia menjatuhkan sesuatu."},
        {"name": "The Twin", "narration": "'Jangan mati hari ini,' bisiknya pelan, menyelipkan sesuatu di sakumu."},
        {"name": "The Follower", "narration": "Ia sudah mengikutimu sejak lama. Ia maju, memberi barang, lalu menghilang."},
        {"name": "The Grateful Dead", "narration": "Mayat Weaver tiba-tiba bangkit, menyerahkan barangnya, lalu hancur menjadi debu."}
    ]
}

# =========================================================================
# LORE STORIES
# Kumpulan sejarah yang akan diceritakan oleh kategori "lore_keeper"
# =========================================================================
LORE_STORIES = [
    "Dimensi ini dulunya adalah perpustakaan para Dewa. *The Archivus* dirancang untuk menyimpan rahasia semesta yang terlalu berbahaya untuk diingat oleh manusia. Namun, seseorang merobek pintunya.",
    "Kau bertanya apa itu 'Weaver'? Kita adalah penjahit realitas yang ditarik dari kematian kita sendiri. Kuburan yang kau temui? Itu adalah saudara-saudaramu.",
    "Koin emas yang kau gunakan bukanlah logam. Itu adalah pecahan waktu dari jiwa-jiwa yang membusuk di sini. Saat kau berbelanja, kau menukar kenangan seseorang.",
    "Sang Penjaga yang kau buru dulunya adalah Orion, Weaver Pertama. Ia mencoba membaca 'Kitab Akhir Zaman' sendirian. Pengetahuan itu meledakkan akalnya.",
    "Rawa tinta hijau beracun di distrik bawah dulunya adalah ruang arsip puisi. Kebohongan manusia menetes ke bawah, membusuk menjadi Miasma beracun.",
    "Jika kau merobek dada Sang Penjaga, kau akan menemukan jantung yang membatu. Barang siapa yang memegangnya tidak akan bisa mati, tapi akan mati karena kesepian.",
    "Terkadang aku berpikir, apakah kita benar-benar hidup, atau kita hanyalah karakter dari sebuah game yang sedang dimainkan seseorang di luar sana lewat layar kaca?"
]
