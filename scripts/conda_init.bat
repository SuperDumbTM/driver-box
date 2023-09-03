@echo off
set ENVNAME="dri-installer"

echo Creating conda enviroment %ENVNAME% with Python version 3.11
echo:
call conda create --name %ENVNAME% python=3.11 -y
timeout 2

echo Installing 'pywin32'.
echo:
call conda activate %ENVNAME% && call conda install pywin32 -y
timeout 2


echo Installing required Python packages.
echo:
call pip install -r ..\requirements-dev.txt

pause