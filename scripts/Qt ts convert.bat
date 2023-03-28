@echo off

set /p fname=Enter the file name for the .ts file: 

cd ..\src\ui
call conda activate dri-installer
pylupdate5 .\main.py -ts "%fname%.ts"
pause