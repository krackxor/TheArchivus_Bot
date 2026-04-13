"""
Kumpulan Puzzle Lore, Logika, dan Trivia Archivus
Berisi ratusan teka-teki untuk menguji pengetahuan dan ingatan para Weaver.
"""

import random

# --- DATABASE LOGIKA, SEJARAH & TRIVIA ---
LORE_PUZZLES = [
    # === KATEGORI: TEKA-TEKI LOGIKA (RIDDLES) ===
    {"q": "Aku punya lubang banyak, tapi bisa menampung air. Siapa aku?", "a": "spons"},
    {"q": "Semakin besar aku, semakin sedikit yang bisa kau lihat.", "a": "gelap"},
    {"q": "Jika kau mengucapkanku, kau akan merusakku. Siapa aku?", "a": "rahasia"},
    {"q": "Aku selalu datang tapi tak pernah tiba. Siapa aku?", "a": "besok"},
    {"q": "Aku tidak punya nyawa, tapi bisa mati. Siapa aku?", "a": "baterai"},
    {"q": "Punya leher tapi tak punya kepala, punya lengan tapi tak punya tangan.", "a": "baju"},
    {"q": "Aku bisa terbang tanpa sayap, menangis tanpa mata. Ke mana aku pergi, kegelapan mengikutiku.", "a": "awan"},
    {"q": "Semakin banyak kau ambil, semakin banyak yang kau tinggalkan. Apakah itu?", "a": "jejak"},
    {"q": "Aku punya kota tapi tak punya rumah, punya gunung tapi tak punya pohon, punya air tapi tak punya ikan.", "a": "peta"},
    {"q": "Apa yang bisa kau tangkap, tapi tidak bisa kau lempar?", "a": "pilek"},
    {"q": "Aku ringan seperti bulu, tapi raksasa pun tak bisa menahanku lama-lama. Siapakah aku?", "a": "napas"},
    {"q": "Aku milikmu, tapi orang lain lebih sering menggunakannya daripada dirimu. Apakah itu?", "a": "nama"},
    {"q": "Aku berjalan tanpa kaki, aku menangis tanpa air mata.", "a": "awan"},
    {"q": "Matahari membesarkanku, malam membunuhku. Aku ada di setiap benda yang terkena cahaya.", "a": "bayangan"},
    {"q": "Kau membeliku untuk makan, tapi kau tidak pernah memakanku. Apakah aku?", "a": "piring"},
    {"q": "Aku bisa pecah meskipun tidak pernah disentuh. Apakah aku?", "a": "janji"},

    # === KATEGORI: LORE ARCHIVUS (CUSTOM GAME) ===
    {"q": "Apa nama entitas pencatat memori di dimensi Archivus ini?", "a": "archivus"},
    {"q": "Mata uang yang digunakan oleh para Weaver di Archivus disebut pecahan...", "a": "memori"},
    {"q": "NPC pencuri yang menguji ingatanmu dengan judi disebut The Memory...?", "a": "thief"},
    {"q": "Gelar bagi petualang yang menenun takdir di dimensi Archivus adalah?", "a": "weaver"},
    {"q": "Siapa entitas raksasa yang menghadang di setiap akhir siklus (Cycle)? Sang...", "a": "penjaga"},
    {"q": "NPC tanpa mata yang bersedia menyembuhkan lukamu adalah The Blind...?", "a": "seer"},
    {"q": "Energi yang digunakan untuk mengeluarkan skill seperti Revelatio dan Time Warp adalah?", "a": "mp"},
    {"q": "Artefak dari Iblis Perjudian yang bisa melipatgandakan koinmu? Lucky...", "a": "charm"},
    {"q": "Syarat utama agar levelmu naik adalah dengan mengumpulkan...", "a": "exp"},
    {"q": "Status yang menandakan seberapa kuat kau bisa menahan serangan musuh adalah?", "a": "hp"},

    # === KATEGORI: RESIDENT EVIL TRIVIA ===
    {"q": "Tragedi kereta apa yang berujung pada hancurnya pegunungan Arklay? (Dua kata)", "a": "ecliptic express"},
    {"q": "Siapa pendiri yang dikhianati dan bangkit kembali berkat lintah raksasa? James...", "a": "marcus"},
    {"q": "Organisasi payung yang menciptakan virus mematikan itu bernama?", "a": "umbrella"},
    {"q": "Kota fiksi yang hancur lebur oleh penyebaran virus T adalah Raccoon...? (Satu kata)", "a": "city"},
    {"q": "Senjata biologis tak terbendung yang terus mengejar Jill Valentine? (Satu kata)", "a": "nemesis"},
    {"q": "Kapten tim Alpha S.T.A.R.S yang ternyata adalah seorang pengkhianat? Albert...", "a": "wesker"},
    {"q": "Polisi pemula yang bertahan hidup di hari pertamanya bekerja di RPD? Leon S...", "a": "kennedy"},
    {"q": "Adik dari Chris Redfield yang datang ke kota mencari kakaknya? Claire...", "a": "redfield"},
    {"q": "Virus mutasi mengerikan yang mengubah William Birkin menjadi monster adalah Virus...?", "a": "g"},
    {"q": "Nama fasilitas rahasia tempat penelitian virus Umbrella berada sering disebut lab...?", "a": "nest"},

    # === KATEGORI: RPG & FINAL FANTASY ===
    {"q": "Nama pedang raksasa milik Cloud Strife adalah? (Dua kata)", "a": "buster sword"},
    {"q": "Pusat dari energi Mako di dunia FF7 adalah kota?", "a": "midgar"},
    {"q": "Antagonis utama berambut perak dengan pedang Masamune di FF7 adalah?", "a": "sephiroth"},
    {"q": "Pangeran Lucis yang melakukan perjalanan bersama tiga sahabatnya adalah? (Satu kata)", "a": "noctis"},
    {"q": "Burung ikonik berwarna kuning yang sering ditunggangi di game RPG klasik? (Satu kata)", "a": "chocobo"},
    {"q": "Makhluk putih kecil bersayap kelelawar dengan pom-pom di kepalanya? (Satu kata)", "a": "moogle"},
    {"q": "Batu kristal yang memberikan kekuatan sihir di FF7 disebut?", "a": "materia"},
    {"q": "Senjata utama Sora di Kingdom Hearts yang berbentuk kunci? (Satu kata)", "a": "keyblade"},
    {"q": "Kota air ajaib yang merupakan kampung halaman Tidus di FF10 adalah?", "a": "zanarkand"},
    {"q": "Siapakah gadis penyihir penjual bunga yang tragis di FF7?", "a": "aerith"},

    # === KATEGORI: ACTION & SOULS-LIKE GAMES ===
    {"q": "Senjata ikonik dari sang hantu Tsushima adalah? (Satu kata)", "a": "katana"},
    {"q": "Siapa nama asli sang 'Ghost' yang menyelamatkan Tsushima? Jin...", "a": "sakai"},
    {"q": "Siapa dewa perang yang menghancurkan Olympus? (Dua kata)", "a": "kratos"},
    {"q": "Senjata rantai ikonik milik sang Dewa Perang adalah Blade of...? (Satu kata)", "a": "chaos"},
    {"q": "Nama putra Kratos yang melakukan perjalanan ke Jotunheim bersamanya?", "a": "atreus"},
    {"q": "Kapak es ajaib milik Kratos di mitologi Nordik bernama?", "a": "leviathan"},
    {"q": "Sebutan bagi pemain yang bangkit dari kematian di Dark Souls? Chosen...", "a": "undead"},
    {"q": "Sebutan bagi pemain di game Elden Ring yang mencari Erdtree? (Satu kata)", "a": "tarnished"},
    {"q": "Titik tempat pemain beristirahat dan memulihkan HP di Dark Souls disebut?", "a": "bonfire"},
    {"q": "Penyihir wanita dengan banyak tangan/wajah misterius di Elden Ring? (Satu kata)", "a": "ranni"},

    # === KATEGORI: ANIME & MANGA TRIVIA ===
    {"q": "Energi kehidupan yang digunakan para ninja di Naruto disebut?", "a": "chakra"},
    {"q": "Buah misterius yang memberikan kekuatan super di One Piece adalah Buah...?", "a": "iblis"},
    {"q": "Kekuatan tekad/ambisi misterius yang digunakan Luffy dkk disebut?", "a": "haki"},
    {"q": "Ras pejuang alien tempat Goku berasal disebut? (Satu kata)", "a": "saiyan"},
    {"q": "Kekuatan roh pelindung yang muncul di JoJo's Bizarre Adventure disebut?", "a": "stand"},
    {"q": "Siapa pahlawan botak yang bisa mengalahkan musuh dengan satu pukulan?", "a": "saitama"},
    {"q": "Makhluk raksasa pemakan manusia di seri Shingeki no Kyojin disebut?", "a": "titan"},
    {"q": "Sebutan untuk dewa kematian di seri Bleach adalah?", "a": "shinigami"},
    {"q": "Bentuk pelepasan kedua dari sebuah Zanpakuto di Bleach disebut?", "a": "bankai"},
    {"q": "Prinsip utama alkimia di Fullmetal Alchemist adalah pertukaran...? (Satu kata)", "a": "setara"}
]

def generate_lore_puzzle():
    """Mengambil pertanyaan logika atau sejarah dunia Archivus/Easter Eggs secara acak."""
    puzzle = random.choice(LORE_PUZZLES)
    return puzzle["q"], puzzle["a"]
