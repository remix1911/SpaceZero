@echo off
chcp 65001 >nul

echo ===============================
echo    Build Script
echo ===============================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found!
    pause
    exit /b 1
)

echo Checking PyInstaller...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
)
echo PyInstaller ready
echo.

echo Building...
pyinstaller --onefile --windowed --clean --name=SpaceZero --add-data="lang.py;." --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=tkinter.messagebox --hidden-import=tkinter.filedialog --hidden-import=send2trash main.py

if %errorlevel% neq 0 (
    echo Build failed!
    pause
    exit /b 1
)

echo Build success!
echo Output: dist\SpaceZero.exe

echo.
echo Copying to current directory...
copy dist\SpaceZero.exe SpaceZero.exe >nul
echo Created: SpaceZero.exe

echo.
pause
