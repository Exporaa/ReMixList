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
