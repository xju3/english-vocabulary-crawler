import os.path
import sys

import yt_dlp

from ai.cv_img_word_extractor import extract_single_frame, extract_largest_font_words
from ai.ollama_prose import ollama_compose_prose
from common.config import yt_options
from common.env import Environment
from db.opus_manager import OpusManager, OpusStatus
from publisher.xhs.cmd import list_dir_files
import subprocess


def dl_insta_video(env,  code, path):
    options = yt_options(f'{path}')
    with yt_dlp.YoutubeDL(options) as ydl:
        url = env.config.insta_opus_url(code)
        return ydl.download([url])

# merge multiple videos to one
def merge_video_files(logger, path, opus_id):
    files = list_dir_files(path, ext=".mp4")
    if len(files) == 0:
        logger.error("no video files found")
        return
    cmd = 'ffmpeg '
    for file in files:
        file_name = f'{path}/{file}'
        cmd += f' -i \'{file_name}\''
    cmd += " -filter_complex \""
    movie_idx = 0
    while movie_idx < len(files):
        cmd += f" [{movie_idx}:v]scale=640:640:force_original_aspect_ratio=decrease:eval=frame,pad=640:640:-1:-1:color=black[v{movie_idx}];"
        movie_idx += 1
    file_idx = 0
    while file_idx < len(files):
        cmd += f' [v{file_idx}][{file_idx}:a] '
        file_idx += 1
    cmd += f' concat=n={len(files)}:v=1:a=1[v][a]\"'
    cmd += f' -map [v]  -map [a] -vcodec libx264 -y {path}/{opus_id}.mp4'
    logger.debug(cmd)
    subprocess.call(cmd, shell=True)


def extract_info(env, opus):

    ans = None, None
    path = f'{env.config.opus_dir}/{opus.id}.{opus.code}'
    if not os.path.isdir(path):
        return ans

    video_files = list_dir_files(path, 'mp4')
    if len(video_files) == 0:
        env.logger.error("no video files found")
        return ans

    image_files = []
    for file in video_files:
        if (file == f'{opus.id}.mp4'):
            continue
        input_file = f'{path}/{file}'
        output_file = input_file.replace("mp4", "jpg")
        env.logger.debug(f"\n{input_file}\n{output_file}")
        image_files.append(output_file)
        extract_single_frame(input_file, output_file)

    if len(image_files) == 0:
        return ans

    words = []
    for image in image_files:
        ans = extract_largest_font_words(image)
        if len(ans) == 0:
            env.logger.error(f"no words found: {image}")
            continue
        word = " ".join(ans)
        env.logger.debug(word)
        words.append(word)

    prose = None
    if len(words) > 0:
        prose = ollama_compose_prose(words)

    return words, prose


class SaiLingoVocDownloader:

    def __init__(self):
        self.env = Environment(app=1)
        self.opus_manager = OpusManager()
        self.config = self.env.config
        self.logger = self.env.logger

    def run(self):
        failures = self.download(8)
        while failures != 0:
            failures = self.download(failures)

    def download(self, count):
        failures = 0
        items = self.opus_manager.get_items_for_downloading(count)
        for opus in items:
            self.opus_manager.set_opus_status(opus.code, OpusStatus.downloaded)
            code = opus.code
            path = f'{self.config.opus_dir}/{opus.id}.{code}'
            try:
                dl_insta_video(self.env, code, path=path)
                merge_video_files(self.logger, path=path, opus_id=opus.id)
                if os.path.isdir(path) and len(list_dir_files(path, 'mp4')) > 0:
                    self.opus_manager.set_opus_status(opus.code, OpusStatus.downloaded)
                    words, prose = extract_info(self.env, opus)
                    if words is None or prose is None:
                        self.opus_manager.set_opus_status(opus.code, OpusStatus.no_contents)
                        self.logger.error("no words and prose.")
                        sys.exit(0)
                    self.opus_manager.update_extracted_info(opus.code, words, prose)
                else:
                    self.opus_manager.set_opus_status(opus.code, OpusStatus.no_resource)
                    failures += 1
            except Exception as e:
                self.logger.error(e)
        return failures