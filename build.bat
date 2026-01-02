@echo off
echo Cleaning old build files...
if exist build rd /s /q build
if exist dist rd /s /q dist

set ICON_ARG=
if exist icon.ico (
    set ICON_ARG=--icon="%~dp0icon.ico"
    echo [INFO] Icon found: icon.ico
) else (
    echo [WARNING] icon.ico tidak ditemukan. Menggunakan icon default.
)

echo.
echo Building Universal Discord RPC...
pyinstaller --noconsole --onefile %ICON_ARG% --name "UniversalDiscordRPC" main.py
echo.
echo Copying config.json to dist folder...
if not exist dist mkdir dist
copy config.json dist\
echo.
echo Build complete! Check the 'dist' folder for UniversalDiscordRPC.exe.
echo TIP: Jika icon tetap tidak muncul, coba rename file .exe-nya atau copy ke folder Desktop.
pause