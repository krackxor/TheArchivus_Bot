# game/data/script.py

# Narasi Linear berdasarkan jumlah langkah (Step Counter)
# Tujuannya: Membangun siklus ketakutan yang tidak berulang
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
    # ... kau bisa teruskan sampai 1000
}

# Narasi saat memicu pertarungan (Monster Encounter)
MONSTER_WARNINGS = [
    "Sstt. Dia sudah di belakangmu.",
    "Ia bosan melihatmu bernapas.",
    "Berikan tanganmu. Dia lapar.",
    "Layar ini akan pecah. Dia keluar sekarang.",
    "Jangan berteriak. Tidak ada yang peduli."
]
