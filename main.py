import sys

from crawler.insta.vocabulary import Vocabulary
from publisher.xhs.xiaohongshu import XiaoHongShu


def run_insta():
    insta_vocabulary = Vocabulary()
    insta_vocabulary.run()


def run_xhs():
    xhs = XiaoHongShu()
    xhs.run()


def main():
    parameters = sys.argv[1:]

    if parameters is None:
        run_insta()

    if parameters[0] == "1":
        run_insta()

    if parameters[0] == "2":
        run_xhs()


if __name__ == '__main__':
    main()
