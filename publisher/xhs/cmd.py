import os
import subprocess

from common.env import Environment

env = Environment()


# get dir files by extension
def list_dir_files(path, ext=None):
    if not os.path.isdir(path):
        return []
    files_and_folders = os.listdir(path)
    # Filter only files (optional)
    if ext is None:
        return [f for f in files_and_folders if os.path.isfile(os.path.join(path, f))]
    else:
        return [f for f in os.listdir(path) if
                f.endswith(ext) and os.path.isfile(os.path.join(path, f))]

