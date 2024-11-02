import os
import subprocess
from os import walk
from pathlib import Path

from common.env import Environment

env = Environment()


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


def extract_single_frame(video_file, output_image_name, time="00:00:05"):
    command = [
        "ffmpeg",
        "-ss", time,
        "-i", video_file,
        "-frames:v", "1",
        '-y',
        output_image_name
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def merge_video_files(path):
    video_list_file_path = path.joinpath("/list.txt")
    if not os.path.isfile(video_list_file_path):
        files = list_dir_files(path, ext=".mp4")
        if len(files) == 0:
            env.logger.error("no video files found")
            return
        with open(video_list_file_path, "w") as f:
            for line in files:
                f.write(f"{line}\n")
    cmd = f'ffmpeg -f contact -i {video_list_file_path} -c copy -y 1.mp4'
    env.logger.debug(cmd)
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
