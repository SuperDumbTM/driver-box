@echo off


cd ..\src\ui\pyqt
call conda activate dri-installer
for %%f in (*.ui) do (
    echo converting "%%f" to python code "..\generated\%%~nf.py"
    pyuic5 "%%f" -o "..\generated\%%~nf.py"
)

pause