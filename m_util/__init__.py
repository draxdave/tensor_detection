from .EVENT import EVENT
from .logger import Logger
import glob
import os
import shutil

logger = None


def init_logger(base_path):
    global logger
    logger = Logger(base_path)


def log(event):
    global logger
    logger.record(event)


def remove_files(path):
    files = glob.glob(path + '/*.*', recursive=True)

    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))


def clear_dir(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
