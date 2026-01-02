@echo off
cls
echo ==========================================
echo    Universal Discord RPC - Build Tool
echo ==========================================
echo.

echo [1/4] Membersihkan file build lama...
if exist build rd /s /q build
if exist dist rd /s /q dist

set ICON_ARG=
if exist icon.ico (
    set ICON_ARG=--icon="%~dp0icon.ico"
    echo [INFO] Ikon ditemukan: icon.ico
) else (
    echo [WARNING] icon.ico tidak ditemukan. Menggunakan ikon default.
)

echo.
echo [2/4] Menginstal library yang dibutuhkan (Harap tunggu...)...
python -m pip install -q --disable-pip-version-check -r requirements.txt

echo.
echo [3/4] Membuat file EXE (Mungkin butuh semenit...)...
python -m PyInstaller --log-level WARN --noconsole --onefile %ICON_ARG% --add-data "icon.ico;." --version-file="file_version_info.txt" --name "UniversalDiscordRPC" main.py

echo [4/4] Menyelesaikan proses akhir...
if not exist dist mkdir dist
copy config.json dist\ >nul

echo.
echo [Bonus] Membuat paket Rilis (ZIP)...
powershell -Command "Compress-Archive -Path 'dist\*' -DestinationPath 'UDRPC_v1.2_Release.zip' -Force"

echo.
echo ==========================================
echo    BUILD BERHASIL!
echo ==========================================
echo Lokasi EXE:   \dist\UniversalDiscordRPC.exe
echo Lokasi Rilis: \UDRPC_v1.2_Release.zip
echo.
echo TIP: Jika icon tetap tidak muncul, coba rename file .exe-nya atau copy ke folder Desktop.
echo.
pause