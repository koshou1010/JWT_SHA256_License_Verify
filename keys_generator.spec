# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(['keys_generator.py'],
             pathex=['C:\\side_projects\\enosim_aws\\tk_tools'],
             binaries=[],
             datas=[('.\\output','output'),
             ('.\\input','input') ,
             ('.\\img','img')],
             hiddenimports=[
                 'pkg_resources.py2_warn',  # only with minepez-Dev env
    ],
             hookspath=[],  
             runtime_hooks=[],
             excludes=['PyQt5','sqlite3','sqlite3','numpy','numpy','scipy','cryptography'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Keys_generator',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
            icon='.\\img\\favicon.ico'
           )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Keys_generator')
