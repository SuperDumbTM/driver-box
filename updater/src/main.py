import argparse
import os
import tempfile
import zipfile
from pathlib import Path

import requests
import tqdm

argparser = argparse.ArgumentParser(description='')

argparser.add_argument('-d', '--app-directory', type=str,
                       help='Root directory of driver-box')

argparser.add_argument('-v', '--version', type=str,
                       required=True, help='Version target')

argparser.add_argument('-t', '--binary-type', type=str,
                       required=True, help='Binary target')


def backup(root: Path):
    os.mkdir('.backup')
    for path in ('driver-box.exe', 'bin'):
        filepath = root.joinpath(path)
        if filepath.exists():
            filepath.rename(root.parent.joinpath('.backup').joinpath(path))


if __name__ == '__main__':
    print(r'''
     _      _                     _                                 _       _            
  __| |_ __(_)_   _____ _ __     | |__   _____  __  _   _ _ __   __| | __ _| |_ ___ _ __ 
 / _` | '__| \ \ / / _ \ '__|____| '_ \ / _ \ \/ / | | | | '_ \ / _` |/ _` | __/ _ \ '__|
| (_| | |  | |\ V /  __/ | |_____| |_) | (_) >  <  | |_| | |_) | (_| | (_| | ||  __/ |   
 \__,_|_|  |_| \_/ \___|_|       |_.__/ \___/_/\_\  \__,_| .__/ \__,_|\__,_|\__\___|_|   
                                                         |_|                             
''')

    args = argparser.parse_args()
    if args.app_directory:
        os.chdir(args.app_directory)

    root = Path(args.app_directory or os.getcwd())

    print('+', '-'*26, '+')
    print('|{:^14s}{:^14s}|'.format('Version', args.version))
    print('|{:^14s}{:^14s}|'.format('Binary', args.binary_type))
    print('+', '-'*26, '+')
    print()

    filename = f'driver-box.{args.binary_type}.zip'
    resp = requests.get('https://github.com/SuperDumbTM/driver-box/releases/download/'
                        f'v{args.version}/{filename}',
                        stream=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        fpath = tmpdir.joinpath(filename)

        print(f'Downloading: {filename}')
        with (tqdm.tqdm(total=int(resp.headers['Content-Length']), unit="B", unit_scale=True) as progress,
                open(fpath, 'wb') as f):
            for chunk in resp.iter_content(1024):
                f.write(chunk)
                progress.update(len(chunk))
                progress.display()

        print(f'\nUnpacking...')
        with zipfile.ZipFile(fpath, 'r') as z:
            for archive in tqdm.tqdm(z.filelist, unit='B'):
                z.extract(archive.filename, str(tmpdir))

        print('Updating...')
        for path in ('driver-box.exe', 'bin'):
            filepath = root.joinpath(path)

            if filepath.exists():
                filepath.unlink()
            if tmpdir.joinpath(path).exists():
                tmpdir.joinpath(path).rename(root.joinpath(path))

    input("Press any key to continue...")
