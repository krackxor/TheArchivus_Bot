# game/puzzles/lore.py

import random

# --- DATABASE TEKA-TEKI DUNIA ARCHIVUS ---
LORE_DATA = [
    # === 1. ELEMEN & COUNTER (STRATEGI) - [20 DATA] ===
    {"q": "Api menari di ujung jarimu, namun entitas air menghalangi jalanmu. Elemen apa yang harus kau tenun?", "a": "petir"},
    {"q": "Musuh berbaju besi berat menertawakan pedang tajammu. Serangan tipe apa yang bisa menghancurkannya?", "a": "blunt"},
    {"q": "Kegelapan menyelimuti musuhmu. Cahaya apa yang paling ditakuti oleh bayangan?", "a": "holy"},
    {"q": "Jika musuhmu membeku dalam es, elemen apa yang akan mencairkan pertahanan mereka?", "a": "api"},
    {"q": "Monster terbang dengan sayap lebar sulit dipukul. Elemen apa yang bisa menjatuhkannya ke tanah?", "a": "angin"},
    {"q": "Tubuh musuhmu terbuat dari tanah keras. Kekuatan apa yang bisa membelahnya?", "a": "air"},
    {"q": "Zirah petir melindungi musuhmu. Elemen apa yang bisa meredam aliran energinya?", "a": "tanah"},
    {"q": "Serangan fisik tak mempan pada tubuh transparan. Kekuatan apa yang harus digunakan?", "a": "magic"},
    {"q": "Cahaya suci menyilaukanmu. Kekuatan purba apa yang bisa menelan cahaya tersebut?", "a": "dark"},
    {"q": "Musuh menggunakan pelindung angin. Serangan tipe apa yang bisa menembus pusarannya?", "a": "pierce"},
    {"q": "Entitas tumbuhan merambat sangat cepat. Elemen apa yang akan menghentikan pertumbuhannya?", "a": "api"},
    {"q": "Musuh memiliki regenerasi tinggi. Efek status apa yang bisa menghentikan pemulihannya?", "a": "burn"},
    {"q": "Lawanmu menggunakan refleksi sihir. Serangan tipe apa yang paling aman digunakan?", "a": "fisik"},
    {"q": "Energi netral sulit di-counter. Stat apa yang paling berpengaruh menahan serangan murni?", "a": "m_def"},
    {"q": "Musuh dengan kecepatan kilat sulit dibidik. Efek status apa yang bisa memperlambatnya?", "a": "slow"},
    {"q": "Serangan elemen apa yang paling efektif melawan naga di puncak gunung es?", "a": "api"},
    {"q": "Tipe senjata apa yang paling efektif melawan musuh bertipe 'Beast'?", "a": "slash"},
    {"q": "Jika musuh terkena status 'Drenched', serangan elemen apa yang damage-nya akan berlipat?", "a": "petir"},
    {"q": "Pelindung api yang sangat panas hanya bisa dipadamkan dengan elemen...?", "a": "air"},
    {"q": "Zirah suci sangat kuat. Elemen apa yang bisa memberikan 'Corruption' padanya?", "a": "dark"},

    # === 2. MONSTER & BEASTIARY - [20 DATA] ===
    {"q": "Aku merayap di langit-langit, memiliki delapan kaki dan membenci api. Siapakah aku?", "a": "spider"},
    {"q": "Gelar bagi monster raksasa yang hanya hancur jika 'Core' di dadanya pecah?", "a": "golem"},
    {"q": "Aku tidak bernapas dan tak memiliki darah. Senjata tajam hanya melewatiku. Siapakah aku?", "a": "ghost"},
    {"q": "Monster menyerupai peti harta karun untuk menjebak Weaver yang serakah?", "a": "mimic"},
    {"q": "Aku adalah mayat yang bangkit karena kutukan, membenci cahaya suci. Siapakah aku?", "a": "zombie"},
    {"q": "Makhluk kecil berwarna hijau, licik, dan sering menyerang berkelompok?", "a": "goblin"},
    {"q": "Singa bersayap dengan ekor kalajengking yang mematikan disebut?", "a": "manticore"},
    {"q": "Anjing berkepala tiga yang menjaga gerbang kehampaan?", "a": "cerberus"},
    {"q": "Ular raksasa dengan banyak kepala yang tumbuh kembali saat dipotong?", "a": "hydra"},
    {"q": "Setengah manusia setengah kuda yang ahli dalam memanah?", "a": "centaur"},
    {"q": "Setan kecil bersayap yang sering mencuri MP milik Weaver?", "a": "imp"},
    {"q": "Makhluk penghuni rawa yang tubuhnya terbuat dari lumpur hidup?", "a": "slime"},
    {"q": "Burung api legendaris yang bangkit dari abunya sendiri?", "a": "phoenix"},
    {"q": "Monster laut raksasa dengan tentakel yang mampu menghancurkan kapal?", "a": "kraken"},
    {"q": "Manusia yang berubah saat bulan purnama tiba?", "a": "werewolf"},
    {"q": "Patung batu bersayap yang hanya bergerak saat tidak ada yang melihat?", "a": "gargoyle"},
    {"q": "Raja para monster terbang yang dikenal sebagai penguasa langit?", "a": "dragon"},
    {"q": "Makhluk penghisap darah yang takut pada bawang putih dan matahari?", "a": "vampire"},
    {"q": "Tengkorak hidup yang tetap bergerak meski tulang-tulangnya berserakan?", "a": "skeleton"},
    {"q": "Penghuni hutan yang menyerupai pohon dan sangat membenci api?", "a": "ent"},

    # === 3. RAHASIA JOB & SKILL - [20 DATA] ===
    {"q": "Job yang berfokus pada kecepatan dan serangan balik bayangan adalah?", "a": "assassin"},
    {"q": "Weaver yang mengorbankan HP untuk damage luar biasa disebut?", "a": "berserker"},
    {"q": "Stat apa yang harus ditingkatkan agar mantra sihirmu semakin kuat?", "a": "intelligence"},
    {"q": "Mantra penyembuhan dasar yang digunakan oleh para Novice?", "a": "heal"},
    {"q": "Job pertahanan dengan zirah berat dan perisai besar disebut?", "a": "knight"},
    {"q": "Keahlian pasif yang meningkatkan kemungkinan menghindar (Dodge) disebut?", "a": "agility"},
    {"q": "Kemampuan untuk mendeteksi kelemahan monster disebut?", "a": "scan"},
    {"q": "Job pengguna busur yang menyerang dari jarak jauh?", "a": "archer"},
    {"q": "Skill yang digunakan untuk memprovokasi musuh agar menyerang kita?", "a": "taunt"},
    {"q": "Statistik yang menentukan urutan giliran dalam pertempuran?", "a": "speed"},
    {"q": "Job pengelana yang bisa meniru skill musuh disebut?", "a": "mimicry"},
    {"q": "Keahlian menempa senjata di tengah perjalanan disebut?", "a": "smithing"},
    {"q": "Skill pamungkas yang hanya bisa digunakan saat HP sangat rendah?", "a": "limit break"},
    {"q": "Statistik yang meningkatkan kemungkinan 'Critical Hit'?", "a": "luck"},
    {"q": "Mantra yang memberikan perlindungan fisik pada seluruh anggota tim?", "a": "barrier"},
    {"q": "Job mistis yang mengandalkan kartu takdir untuk bertarung?", "a": "gambler"},
    {"q": "Skill untuk melarikan diri dari pertempuran monster biasa?", "a": "escape"},
    {"q": "Statistik yang menentukan kapasitas MP maksimal Weaver?", "a": "wisdom"},
    {"q": "Job yang mahir menggunakan berbagai jenis ramuan dan racun?", "a": "alchemist"},
    {"q": "Skill yang mengubah damage musuh menjadi pemulihan MP?", "a": "mana shield"},

    # === 4. MYSTERIES & LORE DEEP - [20 DATA] ===
    {"q": "Berapa jumlah 'Great Weaver' sebelum Cycle ini dimulai?", "a": "tiga"},
    {"q": "Apa nama pedang pertama yang ditempa dari tulang Dewa yang jatuh?", "a": "godslayer"},
    {"q": "Simbol yang terukir di punggung tangan setiap Weaver terpilih?", "a": "stigma"},
    {"q": "Siapa pengkhianat pertama yang membocorkan rahasia Archivus?", "a": "judas"},
    {"q": "Nama menara tertinggi yang menghubungkan bumi dan langit?", "a": "babel"},
    {"q": "Zat cair berwarna perak yang menjadi bahan dasar ramuan abadi?", "a": "mercury"},
    {"q": "Lembah terlarang tempat naga-naga kuno tidur selamanya?", "a": "dragonfall"},
    {"q": "Buku yang mencatat setiap dosa manusia di dunia Archivus?", "a": "codex"},
    {"q": "Bunga yang hanya mekar saat seorang Weaver besar gugur?", "a": "lycoris"},
    {"q": "Hutan yang menyesatkan siapapun yang tidak memiliki memori?", "a": "lost woods"},
    {"q": "Nama lautan darah yang mengelilingi istana terakhir?", "a": "styx"},
    {"q": "Artefak berbentuk jam pasir yang bisa mengulang waktu sesaat?", "a": "chronos"},
    {"q": "Siapa entitas yang tertidur di inti planet Archivus?", "a": "gaia"},
    {"q": "Gelar bagi mereka yang berhasil mencapai level 100?", "a": "ascended"},
    {"q": "Nama api purba yang digunakan Weaver untuk menempa dunia?", "a": "promethus"},
    {"q": "Satu-satunya tempat yang tidak bisa dijangkau oleh cahaya Weaver?", "a": "abyss"},
    {"q": "Kunci untuk membuka gerbang dimensi 'The Void'?", "a": "void key"},
    {"q": "Apa warna jubah yang dikenakan oleh sang Archivus Agung?", "a": "putih"},
    {"q": "Berapa lama satu 'Cycle' dunia Archivus bertahan dalam tahun?", "a": "seribu"},
    {"q": "Apa tujuan akhir dari setiap perjalanan seorang Weaver?", "a": "kebenaran"}
]

def get_puzzle():
    """Mengambil teka-teki acak dengan format UI yang rapi."""
    selected = random.choice(LORE_DATA)
    headers = ["📜 **BISIKAN KUNO**", "🧠 **PENGETAHUAN TEMPUR**", "🕯️ **TEKA-TEKI WEAVER**", "📖 **CATATAN LORE**"]
    return {
        "question": f"{random.choice(headers)}\n\n_\"{selected['q']}\"_",
        "answer": selected['a'].lower()
    }

def generate_lore_puzzle():
    """Legacy support."""
    return get_puzzle()
