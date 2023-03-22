import os
import sys
import subprocess
import shutil
import time

from definitions import DIR_ROOT, DIR_PIC

name = str(int(time.time()))

subprocess.run(
    ["pyinstaller", "-F", "-w", "--uac-admin",
     os.path.join(DIR_ROOT, "src", "main.py"),
     "--icon=" + os.path.join(DIR_PIC, "icon.ico"),
     f"-n{name}"]
)

shutil.move(os.path.join(DIR_ROOT, "dist", f"{name}.exe"), DIR_ROOT)
os.remove(os.path.join(DIR_ROOT, f"{name}.spec"))
shutil.rmtree(os.path.join(DIR_ROOT, "build"))
shutil.rmtree(os.path.join(DIR_ROOT, "dist"))
