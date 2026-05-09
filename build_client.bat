@echo off
pip install pyinstaller
pyinstaller --onefile --windowed --icon=app_icon.ico client_receiver.py
echo.
echo EXE created in: dist\client_receiver.exe
pause
