@echo off
setlocal enabledelayedexpansion
cls

:: ==========================================
::    geetRP - Build Tool
:: ==========================================

:: Initial variables
set "PROGRESS=0"
set "STAGE=Memulai..."
set "BAR=--------------------"

:: Jump to main logic
goto :main

:draw_bar
cls
echo ==========================================
echo    geetRP - Build Tool
echo ==========================================
echo.
echo  Progress: [!BAR!] !PROGRESS!%%
echo  Status  : !STAGE!
echo.
echo ==========================================
echo.
exit /b

:main
:: --- Step 1: Cleaning ---
set "PROGRESS=10"
set "STAGE=Membersihkan file build lama..."
set "BAR=##------------------"
call :draw_bar
if exist build rd /s /q build
if exist dist rd /s /q dist
timeout /t 1 >nul

:: --- Step 2: Dependencies ---
set "PROGRESS=30"
set "STAGE=Menginstal library yang dibutuhkan..."
set "BAR=######--------------"
call :draw_bar
python -m pip install -q --disable-pip-version-check -r requirements.txt

:: --- Step 3: PyInstaller & UPX ---
set "PROGRESS=50"
set "STAGE=Bundling aplikasi ke EXE (Harap tunggu)..."
set "BAR=##########----------"
call :draw_bar

set ICON_ARG=
if exist icon.ico (
    set ICON_ARG=--icon="%~dp0icon.ico"
)

:: UPX Detection for compression
set UPX_ARG=
if exist upx.exe (
    set UPX_ARG=--upx-dir="%~dp0."
    set "STAGE=Bundling + Kompresi UPX sedang berjalan..."
    call :draw_bar
) else (
    :: Check if upx is in PATH
    where upx >nul 2>&1
    if !errorlevel! equ 0 (
        set "STAGE=Bundling + Kompresi UPX (System PATH)..."
        call :draw_bar
    )
)

python -m PyInstaller --log-level WARN --noconfirm --onefile !ICON_ARG! !UPX_ARG! --add-data "icon.ico;." --version-file="file_version_info.txt" --name "geetRP" main.py >nul 2>&1

:: --- Step 4: Finalizing ---
set "PROGRESS=80"
set "STAGE=Menyalin konfigurasi rilis..."
set "BAR=################----"
call :draw_bar
if not exist dist mkdir dist
copy config.json dist\ >nul

:: --- Step 5: ZIP Release ---
set "PROGRESS=95"
set "STAGE=Membuat paket ZIP Rilis..."
set "BAR=###################-"
call :draw_bar
powershell -Command "Compress-Archive -Path 'dist\geetRP.exe', 'config.json', 'README.md' -DestinationPath 'geetRP-%VERSION%.zip' -Force"

:: --- Step 6: Done ---
set "PROGRESS=100"
set "STAGE=Selesai! Build Berhasil."
set "BAR=####################"
call :draw_bar

echo Lokasi EXE:   \dist\UniversalDiscordRPC.exe
echo Lokasi Rilis: \UDRPC_v1.5_Release.zip
echo.
if not exist upx.exe (
    where upx >nul 2>&1
    if !errorlevel! neq 0 (
        echo [TIP] Ingin ukuran EXE lebih kecil? Letakkan upx.exe di folder ini!
        echo.
    )
)
echo TIP: Jika icon tetap tidak muncul, coba rename file .exe-nya.
echo.
pause