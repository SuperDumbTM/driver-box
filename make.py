import os
import sys
import subprocess
import shutil

if getattr(sys, 'frozen', False):
    ROOTDIR = os.path.dirname(sys.executable)
elif __file__:
    ROOTDIR = os.path.dirname(__file__)

# file = input("to be compile file: ")
file = "OneClick-DriverInstaller.py"
LIB = os.path.join(ROOTDIR, "lib")
file = os.path.join(LIB, file)
flag = ["-F", "-w", "--uac-admin", file, "--icon=pic/icon.ico"]

subprocess.run(["pyinstaller"]+flag)

exe = (file.split("\\")[-1]).split(".")[0] + ".exe"
spec = (file.split("\\")[-1]).split(".")[0] + ".spec"

dist = os.path.join(ROOTDIR, "dist")
build = os.path.join(ROOTDIR, "build")
exe = os.path.join(dist, exe)

shutil.move(exe, ROOTDIR)
os.remove(spec)
shutil.rmtree(dist)
shutil.rmtree(build)
