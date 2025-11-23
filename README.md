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
  
<img width="690" height="915" alt="image" src="https://github.com/user-attachments/assets/4dab4881-2ffc-4e0c-8551-f7fe9f21739c" />


## ReMixList v1.1.

**Perubahan Logic:**
1. Interval Dinamis: Batas angka di kotak interval akan berubah otomatis tergantung satuan yang dipilih.
2. Pilih Detik/Menit -> Mentok di 59 (dan wrap/muter ke 0).
3. Pilih Jam -> Mentok di 23.
4. Pilih Hari -> Bebas (sampai 999).
5. Auto-Correct: Kalau lu lagi isi angka "90", terus lu ganti satuannya ke "Menit", angkanya otomatis turun ke "59" biar gak error.

## ReMixList v2.1
Fitur baru ReMixLIst v2.1 - Folder Master Edition
1. Tab System: Memecah aplikasi menjadi 2 mode: Shuffle Files (Acak File) dan Sort Folders (Urutkan Folder).
2. Folder Sorting: Fitur untuk menyusun urutan folder secara manual (Naik/Turun).
3. Sync Content: Opsi untuk menyamakan waktu file di dalam folder dengan waktu foldernya.
4. Drag & Drop: Integrasi library tkinterdnd2 agar user bisa menyeret folder langsung dari Windows Explorer.
5. Visual Numbering: Menambahkan nomor urut [1], [2] pada list folder.
6. Interval Folder: Jarak waktu antar Folder A ke Folder B.
7. Interval File: Jarak waktu antar Lagu 1 ke Lagu 2 (di dalam folder).
8. Folder Creation Date: Menambahkan opsi untuk mengubah Date Created pada folder itu sendiri.
9. Auto-Hop: Mencegah tabrakan waktu. Jika durasi total lagu dalam satu folder melebihi interval folder, waktu untuk folder berikutnya otomatis "loncat" ke slot waktu kosong selanjutnya.
10. Smart Sync: Menyempurnakan logika Date Created. Jika Date Modified "loncat" karena fitur Smart Interval, maka Date Created juga ikut loncat dengan durasi yang sama persis. Menjaga konsistensi timeline folder.

<img width="602" height="951" alt="image" src="https://github.com/user-attachments/assets/558ea593-d894-47c2-9c88-f9329de66155" />


    
**Cara pakai: Tinggal download yang (ReMixList.Exe) yang tertera, dan langsung pakai**
