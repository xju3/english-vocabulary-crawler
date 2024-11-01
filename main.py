import sys

from crawler.insta.dl import InstaDownloader
from crawler.insta.vocabulary import Vocabulary
from publisher.xhs.xiaohongshu import XiaoHongShu


def main():
    parameters = sys.argv[1:]

    if parameters is None or len(parameters) == 0 or parameters[0] == "1":
        insta_vocabulary = Vocabulary()
        insta_vocabulary.run()
        return

    if parameters[0] == "2":
        dl = InstaDownloader()
        dl.download()
        return

    if parameters[0] == "3":
        xhs = XiaoHongShu()
        xhs.publish()


if __name__ == '__main__':
    main()
