conda activate .\.conda;

pyinstaller .\src\main.py -cDF -n updater;

Move-Item -Path .\dist\updater.exe -Destination .\updater.exe -Force;