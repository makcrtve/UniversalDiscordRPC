# Universal Discord RPC (Stealth Mode)
Sebuah generator Discord Rich Presence (RPC) yang ringan dan dapat dikustomisasi sepenuhnya. Aplikasi ini berjalan secara otomatis di latar belakang untuk berbagai software, termasuk FL Studio, Ableton Live, CapCut, dan lainnya.
## ✨ Fitur Utama
- **Generic Fallback Mode**: Secara otomatis mendeteksi software apapun yang sedang Anda buka, meski tidak ada di daftar.
- **Smart Sticky Presence**: Status tetap aktif selama software masih berjalan, meskipun Anda sedang membuka folder atau berada di desktop.
- **Dynamic Icon Mapping**: Mendukung logo spesifik (seperti Brave/Chrome) menggunakan satu Master Application ID.
- **Integrasi System Tray**: Berjalan di area notifikasi (dekat jam), memudahkan kontrol tanpa memenuhi taskbar.
- **Exclusion List**: Cerdas mengabaikan proses sistem seperti Explorer agar status Discord tetap akurat.
- **Auto-Startup & Auto-Reload**: Sangat praktis, sekali pasang langsung jalan selamanya.
## 🚀 Cara Instalasi
### Opsi 1: Download File Siap Pakai (Rekomendasi)
1. Kunjungi halaman [Releases](https://github.com/makcrtve/UniversalDiscordRPC/releases).
2. Unduh file `UDRPC_v1.4_Release.zip` versi terbaru.
3. Ekstrak dan jalankan `UniversalDiscordRPC.exe`.
### Opsi 2: Build Sendiri (Developer)
1. Unduh source code dan jalankan `build.bat`. Script akan mengurus segalanya mulai dari instalasi library hingga pembuatan paket ZIP rilis.
## 🤝 Berkontribusi & Request
Jika ada software favorit Anda yang logo atau statusnya ingin dibuat lebih spesifik, silakan ajukan melalui [Software Request Template](https://github.com/makcrtve/UniversalDiscordRPC/issues/new/choose).
## ⚙️ Konfigurasi
Anda dapat menambahkan software yang ingin dideteksi dengan mengedit file `config.json`. 
Aplikasi ini mendukung variabel dinamis seperti:
- `{window_title}`: Menampilkan judul jendela/projek aktif.
- `{app_name}`: Menampilkan nama aplikasi yang diatur di konfigurasi.
- `{process_name}`: Menampilkan nama file `.exe` yang terdeteksi.
*Panduan lengkap pengisian variabel sudah tersedia di dalam file `config.json`.*
## 🛠️ Penggunaan & Kontrol
- **Mematikan Aplikasi**: Klik kanan ikon **Universal Discord RPC** di System Tray dan pilih **Exit**.
- **Auto-Startup**: Jalankan `install.bat` di dalam folder rilis untuk mendaftarkan aplikasi ke Windows Startup.
- **Troubleshooting**: Jika terjadi kendala, silakan periksa file `debug.log` yang ada di folder aplikasi.
## 📦 Dependensi
- `pypresence`
- `psutil`
- `pystray`
- `Pillow`
- `pyinstaller` (untuk proses build)
---
*Dibuat dengan ❤️ untuk para kreator oleh **makcrtve**.*
