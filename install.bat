@echo off
set EXE_PATH=%~dp0dist\geetRP.exe

if not exist "%EXE_PATH%" (
    echo [ERROR] geetRP.exe tidak ditemukan di folder dist!
    echo Silakan jalankan build.bat terlebih dahulu.
    pause
    exit /b
)

echo Mengaktifkan Stealth Background Mode (Auto-Startup)...
"%EXE_PATH%" --install
echo.
echo Berhasil! Program akan otomatis jalan di background saat Windows nyala.
echo Kamu bisa menutup jendela ini sekarang.
pause
