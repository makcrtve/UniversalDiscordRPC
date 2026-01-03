<div align="center">

# geetRP

### _Tampilkan Aktivitasmu di Discord dengan Elegan_

![Version](https://img.shields.io/badge/version-1.5.1-7289DA?style=for-the-badge&logo=discord&logoColor=white )
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-green?style=for-the-badge )](LICENSE)
![GitHub Repo stars](https://img.shields.io/github/stars/makcrtve/geetRP?style=for-the-badge)
![Platform](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white )
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/makcrtve/geetRP/total?style=for-the-badge)

<br/>

Generator Discord Rich Presence yang **ringan**, **cepat**, dan **sepenuhnya otomatis**.
Berjalan senyap di latar belakang untuk menampilkan status profesional dari berbagai aplikasi.

<br/>

[📦 **Download**](https://github.com/makcrtve/geetRP/releases ) · [🐛 **Report Bug**](https://github.com/makcrtve/geetRP/issues ) · [✨ **Request Software**](https://github.com/makcrtve/geetRP/issues/new/choose )

</div>

---

## ✨ Fitur Utama

<table>
<tr>
<td width="50%">

### 🎯 Generic Fallback Mode

Deteksi software otomatis melalui Master Application ID. **Software apapun** yang aktif akan langsung ditampilkan — meski tidak ada di daftar konfigurasi.

### 📌 Smart Sticky Presence

Status **tetap melengket** selama aplikasi terlihat di Taskbar. Tidak akan hilang saat Anda klik Desktop atau jendela Explorer.

### 🎨 Dynamic Icon Mapping

Logo spesifik untuk setiap aplikasi (Brave, Chrome, Photoshop, Microsoft Word, dll) muncul secara dinamis melalui satu Client ID pusat.

</td>
<td width="50%">

### 🔔 System Tray Integration

Berjalan **senyap** di area notifikasi. Tidak menggebrak taskbar Anda dengan window tambahan.

### 🚫 Smart Exclusion List

Otomatis mengabaikan proses sistem seperti Explorer, dwm.exe, dan aplikasi background lainnya yang tidak relevan.

### 🔄 Auto-Startup Ready

Sekali setup dengan `install.bat`, aplikasi akan **jalan otomatis** setiap Windows menyala.

</td>
</tr>
</table>

---

## 💻 System Requirements

| Komponen    | Requirement                         |
| :---------- | :---------------------------------- |
| **OS**      | Windows 10 / 11                     |
| **Discord** | Desktop App (bukan browser)         |
| **Python**  | 3.8+ _(hanya jika run dari source)_ |

---

## 🚀 Instalasi

### 📦 Opsi 1: Download Siap Pakai _(Rekomendasi)_

```
1. 📥 Kunjungi halaman Releases
2. 📁 Unduh file geetRP-v1.5.1.zip
3. ▶️ Ekstrak dan jalankan geetRP.exe
```

<div align="center">

[![Download Latest](https://img.shields.io/badge/Download-Latest%20Release-7289DA?style=for-the-badge&logo=github )](https://github.com/makcrtve/geetRP/releases )

</div>

Catatan v1.5.1: Perbaikan stabilitas—deteksi ganda instance, pemeriksaan keberadaan Discord, serta penanganan metadata musik yang lebih akurat. Tidak perlu menyunting config saat upgrade dari v1.5.0.

### 🛠️ Opsi 2: Build Sendiri _(Developer)_

```bash
# Clone repository
git clone https://github.com/makcrtve/geetRP.git
cd geetRP

# Install dependencies
pip install -r requirements.txt

# Jalankan langsung
python main.py

# Atau build executable
build.bat
```

> **💡 Tip:** Letakkan [upx.exe](https://github.com/upx/upx/releases ) di folder root sebelum menjalankan `build.bat` untuk mendapatkan ukuran EXE yang lebih kecil.

---

## ⚙️ Konfigurasi

Edit file `config.json` untuk menambah atau mengkustomisasi software yang ingin dideteksi.

### 📝 Variabel Dinamis

| Variabel         | Contoh Output            | Deskripsi                        |
| :--------------- | :----------------------- | :------------------------------- |
| `{window_title}` | `MySong.flp - FL Studio` | Judul jendela/projek aktif       |
| `{app_name}`     | `FL Studio`              | Nama aplikasi dari config        |
| `{process_name}` | `FL64.exe`               | Nama file `.exe` yang terdeteksi |
| `{artist}`       | `Taylor Swift`           | Nama penyanyi (media player)     |
| `{title}`        | `Cruel Summer`           | Judul lagu (media player)        |
| `{file_ext}`     | `FLAC`                   | Format file musik                |

### 📄 Contoh Konfigurasi

```json
{
  "polling_interval": 5,
  "apps": [
    {
      "name": "FL Studio",
      "process_name": ["FL64.exe"],
      "client_id": "1115529334594220116",
      "large_image": "fl-studio-icon",
      "details_format": "Editing: {window_title}",
      "state_format": "Cooking beats 🔥"
    }
  ]
}
```

---

## 🎮 Penggunaan & Kontrol

| Aksi                   | Cara                                         |
| :--------------------- | :------------------------------------------- |
| ▶️ **Menjalankan**     | Double-click `geetRP.exe`                    |
| ⏹️ **Mematikan**       | Klik kanan ikon di System Tray → **Exit**    |
| 🔄 **Auto-Startup**    | Jalankan `install.bat` sebagai Administrator |
| 🔍 **Troubleshooting** | Cek file `debug.log` di folder aplikasi      |

---

## ❓ FAQ

<details>
<summary><b>🔴 Rich Presence tidak muncul di Discord?</b></summary>
<br/>

**Checklist:**

- ✅ Pastikan Discord **Desktop App** berjalan (bukan versi browser)
- ✅ Aktifkan **"Display current activity"** di:
  `Discord Settings` → `Activity Privacy`
- ✅ Cek `debug.log` untuk melihat error messages
- ✅ Restart kedua aplikasi (Discord & geetRP)

</details>

<details>
<summary><b>🔴 Aplikasi tidak jalan saat startup Windows?</b></summary>
<br/>

**Solusi:**

1. Jalankan ulang `install.bat` sebagai **Administrator**
2. Verifikasi di `Task Manager` → Tab `Startup apps`
3. Pastikan entry "geetRP" berstatus **Enabled**

</details>

<details>
<summary><b>🔴 Software saya tidak terdeteksi?</b></summary>
<br/>

**Cara menambahkan:**

1. Buka **Task Manager** → Kolom "Name"
2. Catat nama process persis (contoh: `code.exe` untuk VS Code)
3. Tambahkan entry baru di `config.json`

</details>

<details>
<summary><b>🔴 Bagaimana cara mendapatkan logo custom?</b></summary>
<br/>

**Langkah:**

1. Buat aplikasi di [Discord Developer Portal](https://discord.com/developers/applications )
2. Upload gambar di bagian **Rich Presence** → **Art Assets**
3. Gunakan nama asset sebagai nilai `large_image` di config

</details>

---

## 📦 Dependensi

```
pypresence    # Discord RPC connection
psutil        # Process detection
pystray       # System tray integration
Pillow        # Image handling
pyinstaller   # Build executable
```

---

## 🤝 Berkontribusi

Kontribusi sangat diterima! Berikut caranya:

```
1. Fork repository ini
2. Buat branch fitur  →  git checkout -b feature/AmazingFeature
3. Commit perubahan   →  git commit -m "Add AmazingFeature"
4. Push ke branch     →  git push origin feature/AmazingFeature
5. Buat Pull Request
```

### 🎨 Software Request

Ingin logo atau status khusus untuk software favorit Anda?
Ajukan melalui **[Software Request Template](https://github.com/makcrtve/geetRP/issues/new/choose )**!

---

## 📋 Changelog

### v1.5.1 `Latest` — _3 Januari 2025_

```diff
+ ✨ Singleton kuat: cek mutex + proses duplikat
+ 🛡️ Discord gentle detection via registry
+ 🎵 Cache media: pid + title + size + mtime
+ 📂 Tray menu "Open Folder"
+ 🔧 Relative icon path di .spec
+ 📝 Nama output ZIP otomatis v1.5.1
```

### v1.5 — _Previous Release_

```diff
+ 🎉 Initial support for FL Studio, Ableton, CapCut, Office, browsers
+ 🔄 Smart sticky presence
+ 🎨 Dynamic icon mapping
+ 🔔 System tray integration
```

---

## 📄 License

Distributed under the **GPL v3 License**. See [`LICENSE`](LICENSE) for more information.

---

<div align="center">

### ⭐ Star repository ini jika bermanfaat!

<br/>

**Dibuat dengan ❤️ untuk para kreator oleh *[makcrtve](https://github.com/makcrtve)***

<br/>

</div>

