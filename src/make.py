import argparse
import glob
import os
import pathlib
import shutil
import subprocess
import time

from definitions import DIR_PIC, DIR_ROOT


def clear_build_files(root: os.PathLike, args: argparse.Namespace):
    # remove .spec file
    os.remove(os.path.join(root, f"{args.name}.spec"))
    # remove build and dist folder
    shutil.rmtree(os.path.join(root, "build"))
    shutil.rmtree(os.path.join(root, "dist"))


def clear_executables(root: os.PathLike):
    for filename in glob.glob('*.exe', root_dir=root):
        pathlib.Path(filename).unlink(True)


def build(root: os.PathLike, args: argparse.Namespace):
    if args.release:
        pathlib.Path(os.path.join(root, f"{args.name}")).unlink(True)

    subprocess.run(["pyinstaller",
                    "-F",
                    "-w",
                    "--uac-admin",
                    os.path.join(root, "src", "main.py"),
                    f"--icon={args.icon}",
                    f"-n{args.name}"
                    ])

    # move the executable to the root directory
    shutil.move(os.path.join(root, "dist", args.name), root)


parser = argparse.ArgumentParser()
parser.add_argument("-r", "--release", action='store_true')
parser.add_argument("-n", "--name", default=f"{int(time.time())}.exe")
parser.add_argument("-i",
                    "--icon",
                    default=os.path.join(DIR_PIC, "icon.ico"),
                    )
args = parser.parse_args()

if args.release:
    args.name = "OneClick-Drivers-Installer.exe"

build(DIR_ROOT, args)
clear_build_files(DIR_ROOT, args)
