from PyInstaller.utils.win32.versioninfo import VSVersionInfo, FixedFileInfo, StringFileInfo, StringTable, StringStruct, VarFileInfo, VarStruct

vs_version_info = VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=(1, 0, 0, 0),
        prodvers=(1, 0, 0, 0),
        mask=0x3f,
        flags=0x0,
        OS=0x4,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo(
            [
                StringTable(
                    '040904B0',
                    [
                        StringStruct('CompanyName', 'Alan Software'),
                        StringStruct('FileDescription', 'SpaceZero - System Junk Cleaner'),
                        StringStruct('FileVersion', '1.0.0.0'),
                        StringStruct('InternalName', 'SpaceZero'),
                        StringStruct('LegalCopyright', 'Copyright (C) 2026 Alan. All rights reserved.'),
                        StringStruct('OriginalFilename', 'SpaceZero.exe'),
                        StringStruct('ProductName', 'SpaceZero'),
                        StringStruct('ProductVersion', '1.0.0.0'),
                        StringStruct('Author', 'Alan')
                    ]
                )
            ]
        ),
        VarFileInfo([VarStruct('Translation', [1033, 1200])])
    ]
)

with open('version_info.py', 'w', encoding='utf-8') as f:
    f.write('vs_version_info = ' + repr(vs_version_info))

print("Version info generated successfully!")
