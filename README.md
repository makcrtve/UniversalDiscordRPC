# Universal Discord RPC (Stealth Mode)

A lightweight, customizable Discord Rich Presence (RPC) generator that works automatically in the background for any software, including FL Studio and Ableton Live.

## ✨ Features

- **System Tray Integration**: Runs in the background with a tray icon for easy control.
- **Stealth Background Mode**: No active windows or taskbar icons.
- **Auto-Startup**: Automatically starts when Windows launches (optional).
- **Auto-Reload**: No need to restart the application when updating `config.json`.
- **Intelligent Scanning**: Consumes **0% CPU** when idle and very low RAM (~20MB).
- **Multi-App Support**: Easily switch between different apps like FL Studio, Ableton, or CapCut with custom icons and states.
- **Smart Title Detection**: Deep scanning of process trees to find active project names.

## 🚀 Installation & Setup

### 1. Build the Executable
Run the `build.bat` file. This will automatically install dependencies and create a `dist` folder containing `UniversalDiscordRPC.exe`.
> [!TIP]
> If you want a custom icon, put a file named `icon.ico` in the root folder before building.

### 2. Configure Your Apps
Edit `config.json` to add your software. Use variables like `{window_title}`, `{app_name}`, or `{process_name}`:
```json
{
  "name": "CapCut",
  "process_name": ["CapCut.exe"],
  "client_id": "YOUR_CLIENT_ID",
  "large_image": "capcutlogo",
  "details_format": "Producing: {window_title}",
  "state_format": "Cooking..."
}
```

### 3. Enable Auto-Startup (Highly Recommended)
Inside the `dist` folder, run `install.bat`. 
This will register the program to Windows Startup so it runs silently every time you turn on your computer.

## 🛠️ Usage & Control

- **To Stop**: Right-click the **Universal Discord RPC** icon in the **System Tray** and select **Exit**.
- **Alternative Stop**: Open **Task Manager**, find `UniversalDiscordRPC.exe`, and select **End Task**.
- **To Uninstall (Remove from Startup)**: Press `Win+R`, type `shell:startup`, and delete the `UniversalDiscordRPC.lnk` file.
- **Troubleshooting**: If something isn't working, check the `debug.log` file generated in the program folder.

## 📦 Dependencies
- `pypresence`
- `psutil`
- `pystray`
- `Pillow`
- `pyinstaller` (for building)

---
*Created with ❤️ for creators by makcrtve.*
