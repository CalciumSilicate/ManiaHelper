from .file_api import *
import subprocess


def a_speed(input_file, speed, out_file):
    try:
        cmd = "ffmpeg -y -i %s -filter_complex \"atempo=tempo=%s\" %s -loglevel quiet" % (input_file, speed, out_file)
        res = subprocess.call(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, shell=True)

        if res != 0:
            return False
        return True
    except Exception:
        return False
