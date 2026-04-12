# 📜 The Archivus 
**An Endless Text-Based RPG Telegram Bot**

*"Kabut Archivus tidak memiliki ujung. Sejarah terus ditulis, dan nama-nama terus memudar."*

The Archivus adalah game Text-RPG berbasis Telegram yang mengusung genre *Endless Roguelite*. Dikembangkan dengan narasi sinematik yang gelap, pemain (disebut *Weaver*) harus bertahan hidup dari distorsi memori dengan memecahkan berbagai teka-teki logika, matematika, dan linguistik.

Dipersembahkan oleh **Studio Khoirul**.

---

## ✨ Fitur Utama (Core Features)

* **♾️ Endless Cycle System:** Game tidak pernah tamat. Kalahkan *Sang Penjaga* (Boss) untuk menaikkan siklus (New Game+) dengan tingkat kesulitan yang terus meningkat.
* **⚔️ Multi-Genre Combat:** Pertarungan melawan monster dilakukan dengan memecahkan *puzzle* dalam batas waktu (60 detik). Genre puzzle bervariasi:
  * *Linguistik* (Anagram & Word Scramble)
  * *Numerik* (Matematika Terdistorsi)
  * *Lore & History* (Pengetahuan dunia Archivus)
* **🗺️ Dynamic Locations:** Wilayah Archivus akan terus bergeser seiring dengan bertambahnya jumlah monster yang dibunuh pemain (Kills).
* **🎭 Hidden Identity NPCs:** Interaksi NPC tanpa label. Pemain harus menebak niat NPC dari gaya bahasanya:
  * **The Guide (Baik):** Memberikan pemulihan dan petunjuk arah yang benar.
  * **The Corrupted (Jahat):** Menyesatkan pemain ke dalam jebakan monster tier tinggi.
  * **The Memory Thief (Kuis):** Menguji ingatan pemain dengan taruhan HP/MP.
* **🧭 Manual Navigation:** Sistem navigasi 5-langkah yang mengikat (Traveling State). Salah melangkah berarti kehilangan energi mental (MP).
* **📖 Persistent Lore History:** Setiap pencapaian, kematian, dan perpindahan lokasi dicatat abadi di database sebagai "Sejarah Pemain".

---

## 🛠️ Prasyarat (Prerequisites)

Pastikan server (VPS Ubuntu) Anda telah menginstal komponen berikut:
* **Python 3.10+**
* **MongoDB** (Berjalan di `localhost:27017`)
* **Git**

---

## 🚀 Instalasi & Persiapan (Setup)

**1. Clone Repositori**
```bash
git clone [https://github.com/krackxor/TheArchivus_Bot.git](https://github.com/krackxor/TheArchivus_Bot.git)
cd TheArchivus_Bot
