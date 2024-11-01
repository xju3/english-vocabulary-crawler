import subprocess
from os import walk
import os
from pathlib import Path

from common.env import Environment

env = Environment()

def merge_video_files(path):
    local_file_path = Path.cwd().joinpath(path)
    video_list_file_path = local_file_path.joinpath("/list.txt")
    if not os.path.isfile(video_list_file_path):
        file_names = next(walk(path), (None, None, []))[2]
        with open(video_list_file_path, "w") as f:
            for line in file_names:
                f.write(f"{line}\n")
    cmd = f'ffmpeg -f contact -i {video_list_file_path} -c copy 1.mp4'
    env.logger.debug(cmd)
    subprocess.call(cmd, shell=True)