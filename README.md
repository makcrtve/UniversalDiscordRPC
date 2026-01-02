# Universal Discord RPC (Stealth Mode)

A lightweight, customizable Discord Rich Presence (RPC) generator that works automatically in the background for any software, including FL Studio and Ableton Live.

## ✨ Features

- **Stealth Background Mode**: Runs silently with no windows or taskbar icons.
- **Auto-Startup**: Automatically starts when Windows launches (optional).
- **Auto-Reload**: No need to restart the application when updating `config.json`.
- **Intelligent Scanning**: Consumes **0% CPU** when idle and very low RAM (~20MB).
- **Multi-App Support**: Easily switch between different apps like FL Studio, Ableton, or Notepad with custom icons and states.
- **Custom Icon Support**: Build your own `.exe` with a custom icon.

## 🚀 Installation & Setup

### 1. Build the Executable
Run the `build.bat` file. This will create a `dist` folder containing `UniversalDiscordRPC.exe`.
> [!TIP]
> If you want a custom icon, put a file named `icon.ico` in the root folder before building.

### 2. Configure Your Apps
Edit `config.json` to add your software. You can specify multiple process names for a single app:
```json
{
  "name": "Ableton Live 12 Suite",
  "process_name": ["Ableton Live 12 Suite.exe", "Ableton Live 12.exe"],
  "client_id": "YOUR_CLIENT_ID",
  "large_image": "your_asset_key",
  "details_format": "Producing: {window_title}",
  "state_format": "Cooking in Ableton Live"
}
```

### 3. Enable Auto-Startup (Highly Recommended)
Inside the `dist` folder, run `install.bat`. 
This will register the program to Windows Startup so it runs silently every time you turn on your computer.

## 🛠️ Usage & Control

- **To Stop**: Open **Task Manager** (Ctrl+Shift+Esc), find `UniversalDiscordRPC.exe`, and select **End Task**.
- **To Uninstall (Remove from Startup)**: Press `Win+R`, type `shell:startup`, and delete the `UniversalDiscordRPC.lnk` file.
- **Troubleshooting**: If something isn't working, check the `debug.log` file generated in the program folder.

## 📦 Dependencies
- `pypresence`
- `psutil`
- `pyinstaller` (for building)

---
*Created with ❤️ for music producers and developers.*
