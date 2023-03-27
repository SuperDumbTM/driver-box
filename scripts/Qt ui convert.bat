@echo off


cd ..\src\ui
call conda activate dri-installer
for %%f in (*.ui) do (
    echo converting "%%f" to python code "%%~nf.py"
    pyuic5 "%%f" -o "%%~nf.py"
)

pause