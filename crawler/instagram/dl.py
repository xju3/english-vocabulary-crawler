import os.path

import yt_dlp

from common.config import yt_options
from common.env import Environment
from db.opus_manager import OpusManager, OpusStatus
from publisher.xhs.cmd import list_dir_files

env = Environment()


def dl_insta_video(code, path):
    options = yt_options(f'{path}')
    with yt_dlp.YoutubeDL(options) as ydl:
        url = env.config.insta_opus_url(code)
        return ydl.download([url])


class SaiLingoVocDownloader:

    def __init__(self):
        self.opus_manager = OpusManager()

    def run(self):
        env.driver.quit()
        failures = self.download(5)
        while failures != 0:
            failures = self.download(failures)

    def download(self, count):
        failures = 0
        items = self.opus_manager.get_items_for_downloading(count)
        for opus in items:
            self.opus_manager.set_opus_status(opus.code, OpusStatus.downloaded)
            code = opus.code
            path = f'{env.config.opus_dir}/{code}'
            try:
                dl_insta_video(code, path=path)
                path = f'{env.config.opus_dir}/{opus.code}'
                if os.path.isdir(path) and len(list_dir_files(path, 'mp4')) > 0:
                    self.opus_manager.set_opus_status(opus.code, OpusStatus.downloaded)
                else:
                    self.opus_manager.set_opus_status(opus.code, OpusStatus.err)
                    failures += 1
            except Exception as e:
                env.logger.error(e)
        return failures

