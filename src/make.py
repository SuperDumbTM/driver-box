import os
import sys
import subprocess
import shutil

from definitions import DIR_ROOT, DIR_PIC


subprocess.run(
    ["pyinstaller", "-F", "-w", "--uac-admin",
     os.path.join(DIR_ROOT, "src", "main.py"),
     "--icon=" + os.path.join(DIR_PIC, "icon.ico")]
)

shutil.move(os.path.join(DIR_ROOT, "dist", "main.exe"), DIR_ROOT)
os.remove(os.path.join(DIR_ROOT, "main.spec"))
shutil.rmtree(os.path.join(DIR_ROOT, "build"))
shutil.rmtree(os.path.join(DIR_ROOT, "dist"))