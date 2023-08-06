
import subprocess, os, platform
import pathlib

if __name__ == '__main__':
    filepath = pathlib.Path(__file__).parent / 'builder.py'
    if platform.system() == 'Darwin':
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':
        os.startfile(filepath)
    else:
        subprocess.call(('xdg-open', filepath))
