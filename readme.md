Ini adalah **Master README** yang sangat lengkap dan detail. Dokumen ini tidak hanya berfungsi sebagai petunjuk instalasi, tetapi juga sebagai **"Alkitab" (Buku Panduan Utama)** bagi arsitektur kode dan *lore* dunia The Archivus. 

Dengan menyertakan aturan *class/job*, hierarki musuh, dan pedoman UI, Anda (atau developer lain) tidak akan pernah tersesat saat mengembangkan game ini.

Silakan salin seluruh teks di bawah ini dan jadikan sebagai file `README.md` di *root folder* (direktori paling luar) proyek Anda.

---

```markdown
# 📜 THE ARCHIVUS BOT

**The Archivus** adalah game *Text-Based RPG* (Role-Playing Game berbasis teks) interaktif di Telegram. Game ini memadukan elemen petualangan, manajemen sumber daya (Survival), sistem pertarungan taktis, dan narasi *psychological horror* yang pekat.

Pemain berperan sebagai "Weaver", entitas yang terjebak di dalam realitas yang terus membengkok, di mana setiap langkah menghabiskan energi dan setiap ruangan menyimpan bahaya atau teka-teki mematikan.

---

## ⚙️ CARA INSTALASI & MENJALANKAN BOT

1. **Persyaratan Sistem:** Pastikan Anda memiliki Python 3.9 atau lebih baru.
2. **Clone / Siapkan Direktori:** Buka terminal di folder proyek ini.
3. **Virtual Environment (Opsional tapi Disarankan):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk Linux/Mac
   venv\Scripts\activate     # Untuk Windows
   ```
4. **Instal Dependensi:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Konfigurasi Environment:** Buat file bernama `.env` di folder utama (sejajar dengan `main.py`) dan masukkan token bot Telegram Anda:
   ```env
   BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
   ADMIN_ID=123456789
   ```
6. **Jalankan Game:**
   ```bash
   python main.py
   ```

---

## 📂 ARSITEKTUR KODE (DIRECTORY STRUCTURE)

Proyek ini dibangun dengan prinsip **Modular & Scalable**. Logika murni, tampilan UI, dan data statis dipisah secara ketat agar kode tidak berantakan saat jumlah senjata atau monster mencapai ratusan.

```text
TheArchivus_Bot/
├── main.py                 # (ENTRY POINT) Otak utama bot, inisialisasi aiogram dan router.
├── config.py               # Pemuat variabel .env dan pengaturan global.
├── database.py             # Handler SQLite/JSON untuk CRUD data pemain.
├── requirements.txt        # Daftar pustaka Python yang dibutuhkan.
│
├── docs/                   # (DOKUMENTASI) Panduan UI, standar kode, dan log pembaruan.
│   └── README_UI.md        # Panduan merender UI Telegram yang rapi di layar HP.
│
├── utils/                  # (ALAT BANTU) Fungsi-fungsi serbaguna.
│   └── helper_ui.py        # Pembuat visual seperti Progress Bar, format Gold, layar mati/menang.
│
└── game/                   # (INTI PERMAINAN) Semua aturan game ada di sini.
    ├── ui_constants.py     # Kamus Ikon (Icon.HP), Teks (Text.LINE), dan sistem Multi-Bahasa (i18n).
    │
    ├── handlers/           # (TELEGRAM ROUTERS) Menangkap pesan/klik dari pemain.
    │   ├── start.py        # Pendaftaran pemain baru (/start).
    │   ├── menu.py         # Navigasi profil, tas (inventory), dan ganti bahasa.
    │   ├── exploration.py  # Pergerakan arah (Utara, Selatan) dan trigger Random Encounter.
    │   └── combat.py       # Pilihan aksi bertarung (Serang, Skill, Bertahan, Kabur).
    │
    ├── logic/              # (KALKULATOR MATEMATIS) Dilarang ada teks balasan Telegram di sini.
    │   ├── stats.py        # Menghitung damage, defense, dan stat akhir dari equipment.
    │   ├── states.py       # Pengatur status pemain (Sedang Jalan, Sedang Tarung, dll).
    │   └── menu_handler.py # Merakit susunan tombol (InlineKeyboard/ReplyKeyboard).
    │
    ├── systems/            # (GAME MECHANICS) Fitur loop permainan.
    │   ├── shop.py         # Logika transaksi ekonomi dan perbaikan senjata (Blacksmith).
    │   ├── progression.py  # Logika perolehan EXP, Level Up, dan pembagian Stat Points.
    │   └── events.py       # Pemicu teka-teki, jebakan, atau dialog.
    │
    ├── items/              # (DATABASE BARANG) Objek yang bisa masuk ke Tas.
    │   ├── equipment/      # Senjata (weapons.py), Zirah (armors.py), Aksesoris.
    │   └── consumables/    # Obat (hp.py), Pemulih MP (mp.py), Makanan (food.py).
    │
    ├── entities/           # (DATABASE MAKHLUK HIDUP)
    │   └── monsters.py     # Stat dasar, drop item, dan AI logic musuh & boss.
    │
    └── data/               # (DATABASE LORE & NARASI)
        ├── environment/    # Data cuaca, bahaya area (hazards), dan deskripsi landmark.
        ├── npcs/           # Skrip dialog dan interaksi NPC.
        ├── quests.py       # Daftar syarat dan hadiah Misi Harian/Utama.
        └── script.py       # Narasi pemicu paranoid, bisikan psikologis, dan teks ambush.
```

---

## 🗺️ PETA DUNIA & LORE (WORLD LOCATIONS)

Dunia dibagi menjadi 3 tipe zona utama yang bisa dijelajahi pemain:

**1. Zona Peradaban (Titik Awal & Upgrade)**
* **Desa (The Village):** Area awal berselimut kabut. Tempat mencari material dasar.
* **Kota (The City):** Pusat perdagangan. Terdapat *Shop* lengkap, Blacksmith kelas atas, dan Papan Misi tingkat tinggi.

**2. Zona Berlindung (Safe Havens)**
* **Penginapan (The Inn):** Tempat aman untuk memulihkan 100% HP/MP/Energy dengan membayar Gold. Bebas dari serangan musuh.
* **Cafe (Kedai Singgah):** Area remang-remang untuk berinteraksi dengan NPC (Storytellers, Gamblers) dan memicu Misi Rahasia atau menebak Teka-teki (Quiz).

**3. Zona Berbahaya (Danger Zones)**
* **Hutan (The Forest):** Jalur rimbun yang menipu kompas pemain. Dipenuhi monster buas.
* **Dungeon:** Labirin bawah tanah. Menguras banyak Energi. Berisi jebakan teka-teki mematikan dan harta karun kelas elit.
* **Castile (The Grand Castle):** Kastil penguasa yang membusuk. Zona *End-Game* tempat *Final Boss* berada.

---

## ⚔️ SISTEM PERMAINAN (GAME MECHANICS)

### A. Sistem Kelas (Jobs/Classes)
Pemain dapat berevolusi dari *Novice* menjadi salah satu dari 3 *Job* spesifik pada Level 10:
* **🛡️ Vanguard:** Fokus pada fisik, ketahanan (*Defense*), dan *Counter-Attack*.
* **🧪 Survivor:** Fokus pada *Evasion*, manipulasi racun, dan meracik item (Crafting/Synthesis).
* **🔮 Arcanist:** Rentan secara fisik namun memiliki serangan *Magic* (*Mind Blast*, *Ultima*) area-of-effect yang mematikan.

### B. Hierarki Musuh (Entity Tiers)
* **Tier F & E (Fodder/Minion):** Musuh biasa tanpa strategi khusus (ex: *Infected Villager*, *Rabid Hound*).
* **Tier D & C (Elites):** Musuh yang menargetkan kelemahan pemain dan memiliki status pasif (ex: *Crimson Head*, *Void Lurker*).
* **Tier B (Miniboss / Stalker):** Musuh yang menjaga pintu masuk ke area krusial. Beberapa bertipe *Stalker* (mengikuti pemain antar ruangan).
* **Tier A & S (Main Boss / Lord):** Penguasa area dengan pertarungan multi-fase dan mekanik pemusnah massal (ex: *Omen Weapon*, *The Fallen Archivist*).

### C. Narasi & Teka-teki (Puzzles)
Game tidak hanya tentang *grinding*, tapi juga bertahan dari serangan psikologis (*script.py*). Di area seperti *Dungeon* atau *Castile*, pemain akan dikunci di ruangan dan harus menebak urutan patung, mencampur reagen racun, atau memutar waktu di dalam layar obrolan Telegram untuk bertahan hidup.

---

## 🎨 PEDOMAN PENGEMBANGAN UI (MANDATORY)

Bagi siapa pun yang menulis kode di folder `game/handlers/`, patuhi aturan UI dari `helper_ui.py` dan `ui_constants.py`:
1.  **Dilarang Hardcode Emoji/Teks:** Selalu gunakan `Icon.HP` atau `Text.LINE` dari `ui_constants.py`, bukan emoji manual ("❤️").
2.  **Gunakan UI Helper:** Untuk membuat garis nyawa, gunakan `create_hp_bar(current, max)` dari `helper_ui.py`. Jangan menulis logika kalkulasi persentase bar di dalam handler.
3.  **Mobile First:** Jaga agar teks tidak melebihi ~40 karakter per baris. Pesan panjang harus dipecah menjadi paragraf dengan spasi `\n\n` agar nyaman dibaca di layar HP.

---
*Game Master: Studio Khoirul | Engineer: Khoirul Anwar*
```
