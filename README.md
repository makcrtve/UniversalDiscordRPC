# geetRPC (v1.5)
Sebuah generator Discord Rich Presence (RPC) yang ringan, cepat, dan otomatis. **geetRPC** berjalan di latar belakang untuk mendeteksi berbagai software secara cerdas, memberikan status Discord yang elegan dan profesional.

## ✨ Fitur Utama
- **Generic Fallback Mode**: Deteksi software otomatis melalui Master Application ID (**geetRPC**).
- **Local Media Metadata (Privacy First)**: Menampilkan Artis, Judul Lagu, dan Format File (FLAC/MP3) dari VLC, AIMP, dan foobar2000 tanpa upload data ke internet.
- **Smart Sticky Presence**: Status tetap melengket selama aplikasi ada di Taskbar. Tidak akan hilang saat Anda klik Desktop atau Explorer.
- **Dynamic Icon Mapping**: Logo spesifik (Brave, Chrome, Photoshop, dll) tetap muncul meski menggunakan satu Client ID pusat.
- **Integrasi System Tray**: Berjalan senyap di area notifikasi dengan menu kontrol yang simpel.
- **Optimasi Build & Size**: Dilengkapi Progress Bar di build script dan dukungan kompresi UPX untuk file EXE yang lebih ringan (~8MB).

## 🚀 Cara Instalasi
### Opsi 1: Download File Siap Pakai (Rekomendasi)
1. Kunjungi halaman [Releases](https://github.com/makcrtve/geetRPC/releases).
2. Unduh file `geetRPC-v1.5.zip`.
3. Ekstrak dan jalankan `geetRPC.exe`.

### Opsi 2: Build Sendiri (Developer)
1. Pastikan Python terinstal.
2. Jalankan `build.bat`. Script akan mengurus instalasi library, kompresi, hingga pembuatan ZIP secara otomatis dengan progress bar.

## 🤝 Berkontribusi & Request
Ingin software favorit Anda punya logo atau status khusus? Silakan ajukan melalui [Software Request Template](https://github.com/makcrtve/geetRPC/issues/new/choose).

## ⚙️ Konfigurasi
Edit file `config.json` untuk kustomisasi penuh. Variabel yang didukung:
- `{window_title}`: Judul jendela aktif.
- `{app_name}`: Nama aplikasi dari konfigurasi.
- `{artist}`: Nama penyanyi (Khusus Media Player).
- `{title}`: Judul lagu asli (Khusus Media Player).
- `{file_ext}`: Format file musik (Khusus Media Player).

## 🛠️ Kontrol & Tips
- **Auto-Startup**: Jalankan `install.bat` untuk mendaftarkan aplikasi agar jalan otomatis saat Windows menyala.
- **Manual Exit**: Klik kanan ikon di System Tray dan pilih **Exit**.
- **Build Ringan**: Letakkan [upx.exe](https://github.com/upx/upx/releases) di folder root sebelum menjalankan `build.bat` untuk mendapatkan ukuran EXE terkecil.

---
*Dibuat dengan ❤️ oleh **makcrtve** untuk komunitas kreator.*