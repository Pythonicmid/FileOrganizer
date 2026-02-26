@echo off
echo ============================================
echo   File Organizer Pro - PyInstaller Build
echo ============================================
echo.

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [INFO] Installing PyInstaller...
    pip install pyinstaller
)

echo [INFO] Building executable...
echo.

pyinstaller --onefile ^
            --windowed ^
            --name "FileOrganizerPro" ^
            file_organizer.py

echo.
IF %ERRORLEVEL% EQU 0 (
    echo ============================================
    echo   BUILD SUCCESSFUL!
    echo   Your .exe is in the "dist" folder.
    echo ============================================
    start "" "dist"
) ELSE (
    echo [ERROR] Build failed. Check the output above.
)

pause
