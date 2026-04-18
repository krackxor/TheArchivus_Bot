# game/data/npcs/storytellers.py

"""
NPC Storyteller Database - The Archivus
Berisi NPC pencerita yang memberikan informasi sejarah (Lore) dan rahasia dunia.
"""

import random

STORY_NPCS = {
    "npc_chronicler": {
        "name": "The Last Chronicler",
        "role": "storyteller",
        "desc": "Pria tua dengan jubah yang dipenuhi tinta. Tangannya tidak berhenti menulis di udara kosong.",
        "dialog_greetings": [
            "Memori adalah satu-satunya mata uang yang tidak akan inflasi di sini.",
            "Kau ingin mendengar tentang awal mula kegelapan ini, Weaver?",
            "Catatanku tidak pernah bohong, hanya manusia yang sering salah membacanya."
        ],
        "lore_episodes": [
            "Dahulu, Archivus adalah perpustakaan cahaya, sebelum seseorang menumpahkan tinta kehampaan ke atasnya.",
            "Para Penjaga (Guardians) sebenarnya adalah Weaver yang gagal dan terjebak dalam siklus tanpa akhir.",
            "Jangan pernah mempercayai bayangan yang tidak mengikuti gerakan tubuhmu di area Abyss.",
            "Konon, jika kau berhasil mengumpulkan semua 'Pecahan Memori', kau bisa menjahit kembali takdir yang robek."
        ]
    },

    "npc_whispering_statue": {
        "name": "Patung Berbisik",
        "role": "storyteller",
        "desc": "Sebuah patung marmer retak yang air matanya mengalirkan darah kering.",
        "dialog_greetings": [
            "...mendekatlah... dengarkan bisikan dari masa lalu...",
            "...waktu hanyalah lingkaran yang berulang di tempat ini..."
        ],
        "lore_episodes": [
            "Ratu yang memimpin Crimson Throne bukanlah musuhmu, ia adalah tawanan yang paling malang.",
            "Di bawah danau beracun, terkubur pedang yang bisa membelah kabut paling pekat.",
            "Setiap kali kau mati, sebagian dari jiwamu tertinggal di sini, memperkuat dinding dimensi ini."
        ]
    },

    "npc_echo_of_weaver": {
        "name": "Gema Weaver Terdahulu",
        "role": "storyteller",
        "desc": "Bayangan transparan yang menyerupai dirimu, namun dengan perlengkapan yang sudah hancur.",
        "dialog_greetings": [
            "Aku adalah kau di masa lalu... atau mungkin di masa depan.",
            "Hati-hati, langkah yang kau ambil sekarang sudah pernah aku lalui seribu kali."
        ],
        "lore_episodes": [
            "Jika kau bertemu dengan pria bungkuk yang meminta roti, perhatikan matanya. Jika merah, berlarilah.",
            "Gunakan masker sebelum memasuki Mire, atau paru-parumu akan berubah menjadi lumpur hijau.",
            "Siklus (Cycle) ini akan terus menguat setiap kali kau berhasil membunuh Sang Penjaga."
        ]
    }
}

def get_story_npc(npc_id):
    """Mengambil data NPC pencerita berdasarkan ID."""
    return STORY_NPCS.get(npc_id)

def get_random_lore(npc_id):
    """
    Mengambil satu potongan cerita secara acak dari NPC tertentu.
    Digunakan untuk memberikan variasi dialog saat pemain 'Ngobrol'.
    """
    npc = STORY_NPCS.get(npc_id)
    if npc and "lore_episodes" in npc:
        return random.choice(npc["lore_episodes"])
    return "Sosok itu diam membisu, seolah sudah lupa cara berbicara."
