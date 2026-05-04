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

echo Creating version info...
echo import sys > version_info.py
echo sys.path.insert(0, '.') >> version_info.py
echo from PyInstaller.utils.win32.versioninfo import VSVersionInfo, FixedFileInfo, StringFileInfo, StringTable, StringStruct, VarFileInfo, VarStruct >> version_info.py
echo >> version_info.py
echo vs_version_info = VSVersionInfo( >> version_info.py
echo     ffi=FixedFileInfo( >> version_info.py
echo         filevers=(1, 0, 0, 0), >> version_info.py
echo         prodvers=(1, 0, 0, 0), >> version_info.py
echo         mask=0x3f, >> version_info.py
echo         flags=0x0, >> version_info.py
echo         OS=0x4, >> version_info.py
echo         fileType=0x1, >> version_info.py
echo         subtype=0x0, >> version_info.py
echo         date=(0, 0) >> version_info.py
echo     ), >> version_info.py
echo     kids=[ >> version_info.py
echo         StringFileInfo( >> version_info.py
echo             [ >> version_info.py
echo                 StringTable( >> version_info.py
echo                     '040904B0', >> version_info.py
echo                     [ >> version_info.py
echo                         StringStruct('CompanyName', 'Alan Software'), >> version_info.py
echo                         StringStruct('FileDescription', 'SpaceZero - System Junk Cleaner'), >> version_info.py
echo                         StringStruct('FileVersion', '1.0.0.0'), >> version_info.py
echo                         StringStruct('InternalName', 'SpaceZero'), >> version_info.py
echo                         StringStruct('LegalCopyright', 'Copyright (C) 2026 Alan. All rights reserved.'), >> version_info.py
echo                         StringStruct('OriginalFilename', 'SpaceZero.exe'), >> version_info.py
echo                         StringStruct('ProductName', 'SpaceZero'), >> version_info.py
echo                         StringStruct('ProductVersion', '1.0.0.0'), >> version_info.py
echo                         StringStruct('Author', 'Alan') >> version_info.py
echo                     ] >> version_info.py
echo                 ) >> version_info.py
echo             ] >> version_info.py
echo         ), >> version_info.py
echo         VarFileInfo([VarStruct('Translation', [1033, 1200])]) >> version_info.py
echo     ] >> version_info.py
echo ) >> version_info.py

echo Building...
pyinstaller --onefile --windowed --clean --name=SpaceZero --version-file=version_info.py --add-data="lang.py;." --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=tkinter.messagebox --hidden-import=tkinter.filedialog --hidden-import=send2trash main.py

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