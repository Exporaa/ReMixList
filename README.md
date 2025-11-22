# ReMixList
# ReMixList 🎵

**ReMixList** Jadi ini adalah aplikasi untuk mengacak urutan lagu pada pemutar musik yang hanya bisa mengurutkan lagu berdasarkan "Date Modified". Kalau pake music player, pastikan pakai settingan urutkan berdasarkan waktu biar lagu yang udah diubah tanggalnya bisa teracak otomatis

Aplikasi ini memanipulasi atribut waktu (*timestamp*) pada file audio secara otomatis, jadi playlist menjadi benar-benar acak tapi tetap rapi.

## Fitur Utama

* **Multi-Language Support:** Tersedia dalam 5 bahasa (English, Indonesia, Japanese, Chinese, Russian).
* **Smart Date Logic:** Validasi tanggal (otomatis mendeteksi jumlah hari dalam bulan & tahun kabisat).
* **GUI User Friendly:** Antarmuka modern berbasis Tkinter dengan Menu Bar.
* **Deep Scan:** Mendeteksi file lagu hingga ke dalam sub-folder.
* **Custom Interval:** Mengatur jarak waktu antar lagu (Detik, Menit, Jam, Hari).
* **Advanced Timestamp:** Mampu mengubah *Date Modified* dan *Date Created* (via Windows Kernel Access).

## ReMixList v2.1.

**Perubahan Logic:**
1. Interval Dinamis: Batas angka di kotak interval akan berubah otomatis tergantung satuan yang dipilih.
2. Pilih Detik/Menit -> Mentok di 59 (dan wrap/muter ke 0).
3. Pilih Jam -> Mentok di 23.
4. Pilih Hari -> Bebas (sampai 999).
5. Auto-Correct: Kalau lu lagi isi angka "90", terus lu ganti satuannya ke "Menit", angkanya otomatis turun ke "59" biar gak error.


<img width="690" height="977" alt="image" src="https://github.com/user-attachments/assets/2809aeae-e8ad-48d5-a38a-9f963257a36d" />

Cara pakai: Tinggal download yang (ReMixList.Exe) yang tertera, dan langsung pakai
