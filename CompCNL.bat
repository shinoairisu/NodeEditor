@echo off
pyinstaller  -F cnl.py --icon=ico/node.ico
rd/s/q build
rd/s/q __pycache__
del cnl.spec
cd dist
ren cnl.exe "NodeEditor v3.0.exe"
cd ..