@echo off
pyinstaller  -F pkgmaker.py --icon=ico/package.ico
rd/s/q build
rd/s/q __pycache__
del pkgmaker.spec
cd dist
ren pkgmaker.exe "PackageMaker v3.0.exe"
cd ..