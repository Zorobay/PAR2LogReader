rmdir /s /q .\dist\
poetry run pyinstaller --onefile .\main.py
xcopy /s /i /q .\config\ .\dist\config
xcopy /s /i /q .\res\ .\dist\res