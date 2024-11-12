import sys
import os
from publisher.xhs.cmd import list_dir_files
from crawler.instagram.sai_lingo_voc import SaiLingoVoc
from common.env import Environment
from crawler.instagram.dl import SaiLingoVocDownloader
from publisher.xhs.publisher import Publisher
from ai.cv_img_word_extractor import merge_videos, save_list_to_file, mp4_to_mov

env = Environment()

def merge_video():
    opus_home = f"{env.config.opus_dir}"
    dirs = os.listdir(opus_home)
    for dir in dirs:
        path = f"{opus_home}/{dir}"
        if not os.path.isdir(path):
            continue
        files = list_dir_files(path, 'mp4')
        video_list_file_path = f"{path}/list.txt"
        for file in files:
            mp4_to_mov(f'{path}/{file}', f"{path}/{file}".replace(".mp4", ".mov"))

        # save_list_to_file(path, files, video_list_file_path)
        # merge_videos(video_list_file_path, f"{path}/all.mp4")



def main():
    parameters = sys.argv[1:]

    # search the posts and it's link on instagram
    if parameters is None or len(parameters) == 0 or parameters[0] == "1":
        insta_vocabulary = SaiLingoVoc()
        insta_vocabulary.run()
        return

    # download each post's resources, videos or pictures
    if parameters[0] == "2":
        dl = SaiLingoVocDownloader()
        dl.run()
        return

    # publish the downloaded contents.
    if parameters[0] == "3":
        xhs = Publisher()
        xhs.run()



if __name__ == '__main__':
    main()
