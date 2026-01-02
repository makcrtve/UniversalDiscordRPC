# Universal Discord RPC (Stealth Mode)

![Version](https://img.shields.io/badge/version-1.2-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-green.svg)](LICENSE)
![Stars](https://img.shields.io/github/stars/makcrtve/UniversalDiscordRPC?style=social)

Sebuah generator Discord Rich Presence (RPC) yang ringan dan dapat dikustomisasi sepenuhnya. Aplikasi ini berjalan secara otomatis di latar belakang untuk berbagai software, termasuk FL Studio, Ableton Live, CapCut, dan lainnya.

<!-- Uncomment jika sudah ada screenshot -->
<!-- ## 📸 Preview
![Discord RPC Demo](screenshots/demo.gif) -->

## ✨ Fitur Utama

| Fitur                          | Deskripsi                                                      |
| :----------------------------- | :------------------------------------------------------------- |
| 🎯 **Generic Fallback Mode**   | Otomatis mendeteksi software apapun, meski tidak ada di daftar |
| 📌 **Smart Sticky Presence**   | Status tetap aktif meski Anda di desktop atau folder           |
| 🎨 **Dynamic Icon Mapping**    | Logo spesifik per aplikasi via Discord Developer Portal        |
| 🔔 **System Tray Integration** | Berjalan di notification area, tidak memenuhi taskbar          |
| 🚫 **Exclusion List**          | Mengabaikan proses sistem (Explorer, dll)                      |
| 🔄 **Auto-Startup & Reload**   | Sekali setup, jalan selamanya                                  |

## 💻 System Requirements

- Windows 10/11
- Discord Desktop App (bukan browser)
- Python 3.8+ (hanya jika run dari source code)

## 🚀 Cara Instalasi

### Opsi 1: Download File Siap Pakai (Rekomendasi)

1. Kunjungi halaman [Releases](https://github.com/makcrtve/UniversalDiscordRPC/releases)
2. Unduh file `UDRPC_v1.4_Release.zip` versi terbaru
3. Ekstrak dan jalankan `UniversalDiscordRPC.exe`

### Opsi 2: Build Sendiri (Developer)

```bash
# Clone repository
git clone https://github.com/makcrtve/UniversalDiscordRPC.git
cd UniversalDiscordRPC

# Install dependencies
pip install -r requirements.txt

# Jalankan langsung
python main.py

# Atau build executable
build.bat
```

## ⚙️ Konfigurasi

Edit file `config.json` untuk menambah software yang ingin dideteksi.

### Variabel Dinamis

| Variabel         | Deskripsi                        |
| :--------------- | :------------------------------- |
| `{window_title}` | Judul jendela/projek aktif       |
| `{app_name}`     | Nama aplikasi dari config        |
| `{process_name}` | Nama file `.exe` yang terdeteksi |

### Contoh Konfigurasi

```json
{
  "polling_interval": 5,
  "apps": [
    {
      "name": "FL Studio",
      "process_name": ["FL64.exe"],
      "client_id": "YOUR_DISCORD_APP_ID",
      "large_image": "fl-studio-icon",
      "details_format": "Editing: {window_title}",
      "state_format": "Cooking..."
    }
  ]
}
```

## 🛠️ Penggunaan & Kontrol

| Aksi                | Cara                                         |
| :------------------ | :------------------------------------------- |
| **Mematikan**       | Klik kanan ikon di System Tray → Exit        |
| **Auto-Startup**    | Jalankan `install.bat` sebagai Administrator |
| **Troubleshooting** | Cek file `debug.log` di folder aplikasi      |

## ❓ FAQ

<details>
<summary><b>RPC tidak muncul di Discord?</b></summary>

- Pastikan Discord **Desktop App** berjalan (bukan browser)
- Aktifkan "Display current activity" di Discord Settings → Activity Privacy
- Cek `debug.log` untuk error messages
</details>

<details>
<summary><b>Aplikasi tidak jalan saat startup Windows?</b></summary>

- Jalankan ulang `install.bat` sebagai **Administrator**
- Cek Windows Task Manager → Startup apps
</details>

<details>
<summary><b>Software saya tidak terdeteksi?</b></summary>

- Tambahkan ke `config.json` dengan nama process yang benar
- Cari nama process di Task Manager → kolom "Name"
</details>

## 📦 Dependensi

```
pypresence
psutil
pystray
Pillow
pyinstaller  # untuk build
```

## 🤝 Contributing

Kontribusi sangat diterima! Berikut caranya:

1. **Fork** repository ini
2. Buat branch fitur (`git checkout -b feature/example`)
3. Commit perubahan (`git commit -m 'Add example'`)
4. Push ke branch (`git push origin feature/example`)
5. Buat **Pull Request**

### Software Request

Ingin logo/status spesifik untuk software favorit? Ajukan melalui [Software Request Template](https://github.com/makcrtve/UniversalDiscordRPC/issues/new/choose).

## 📋 Changelog

### v1.4 (2026-01-02)

- ✨ Improved security with path sanitization
- 🐛 Fixed potential crash on process detection
- 📝 Added type hints for better maintainability
- 🔧 Better exception handling throughout

### v1.2

- Initial public release
- System tray integration
- Auto-startup support

## 📄 License

Distributed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for more information.

---

<div align="center">

_Dibuat dengan ❤️ untuk para kreator oleh **[makcrtve](https://github.com/makcrtve)**._

⭐ Star repository ini jika bermanfaat!

</div>


