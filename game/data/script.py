# game/data/script.py

# --- LINEAR DREAD STEPS (Fase Paranoid 1-100) ---
# Narasi yang memaksa user meragukan ruang di sekitarnya.
DESPAIR_STEPS = {
    1: "Kau kembali? Tidak ada yang merindukanmu di sini.",
    2: "Jari-jarimu kaku. Tinta mulai masuk ke nadimu.",
    3: "Berapa kali kau berkedip sejak langkah pertama?",
    4: "Layar ini terasa hangat. Seperti kulit manusia.",
    5: "Ada suara di belakangmu. Jangan menoleh.",
    6: "Kau yakin pintumu terkunci? Coba dengar engselnya.",
    7: "Kenapa kau masih di sini? Dunia aslimu sudah melupakanmu.",
    8: "Napasmu terdengar berat. Kau tidak sendirian di kamar itu.",
    9: "Sesuatu baru saja menyentuh tengkukmu.",
    10: "Lantai ini bergetar. Sesuatu merangkak di bawahmu.",
    11: "Cermin di dekatmu... pantulannya terlambat satu detik.",
    12: "Siapa yang berdiri di kegelapan belakangmu? Jangan cek.",
    13: "Layar ini mulai menghisap pantulan matamu.",
    14: "Kau mendengar detak jantung? Itu bukan milikmu.",
    15: "Sstt. Sesuatu baru saja berbisik di telinga kirimu.",
    16: "Jari yang kau pakai untuk menekan layar... itu bukan milikmu lagi.",
    17: "Bateraimu berkurang selaras dengan umurmu di sini.",
    18: "Jangan bernapas terlalu keras. Ia bisa mendengarmu.",
    19: "Ada sidik jari di layar yang bukan milikmu. Dari dalam.",
    20: "Dunia luar sudah berhenti. Hanya tersisa teks ini.",
    # Tambahkan sampai 1000 dengan eskalasi kengerian
}

# --- STALKING MODE (Paranoid Trigger) ---
# Pesan yang dikirim saat 'is_stalked' aktif. Menyerang psikis secara frontal.
STALKING_MESSAGES = [
    "Ia sedang menghitung berapa kali kau bernapas. Jangan salah hitung.",
    "Jangan matikan layar ini. Jika gelap, ia akan keluar.",
    "Kau merasa dingin di tengkuk? Itu adalah bibirnya yang mendekat.",
    "Bayanganmu di dinding baru saja tersenyum. Kau tidak melihatnya?",
    "Ada seseorang di bawah tempat tidurmu. Ia suka caramu bermain.",
    "Satu kedipan lagi, dan ia akan berada tepat di depan wajahmu.",
    "Jangan menoleh ke jendela. Ada mata yang sedang membandingkanmu."
]

# --- ENCOUNTER TRIGGER (Ambush) ---
# Kalimat eksekusi saat monster akhirnya menyerang.
MONSTER_WARNINGS = [
    "KAU TERLAMBAT MENOLIH!",
    "IA SUDAH BOSAN BERSEMBUNYI.",
    "GIGINYA SUDAH MENYENTUH KULITMU.",
    "RASAKAN TANGANNYA DI LEHERMU.",
    "TIDAK ADA LAGI RUANG UNTUK LARI.",
    "IA MEROBEK LAYARMU SEKARANG."
]
