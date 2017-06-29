from __future__ import print_function ## so people can maybe run it w/ py2
import os
import sys
from shutil import copy2
from shutil import rmtree


def print_and_install(module):
    try: import pip
    except ImportError:
        print("Please install pip to use this script.")
        exit(-1)

    print(module, "is missing. Installing via pip...")
    pip.main(['install', module])


def main():
    if sys.version_info[0] < 3:
        raise Exception("Please run this script with Python 3.")
    if os.geteuid() != 0:
        print("This script must be run with root privileges.")
        exit(-1)

    print("Checking dependencies...")
    try: import numpy
    except ImportError:
        print_and_install('numpy')

    try: import sounddevice
    except ImportError:
        print_and_install('sounddevice')

    print("Copying files...")
    path = '/opt/pynaural'
    if os.path.exists(path):
        rmtree(path)

    os.mkdir(path)
    file_queue = ['./main.py', './auxiliary.py', './beat_gen.py', './main.ui']
    for file in file_queue:
        copy2(file, path)

    print("Creating symlink...")
    try: os.remove('/usr/local/bin/pynaural')
    except:
        pass
    os.symlink('/opt/pynaural/main.py', '/usr/local/bin/pynaural')

    print("Successfully installed.")


if __name__ == '__main__':
    main()
