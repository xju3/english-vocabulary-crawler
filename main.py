import sys
from crawler.instagram.sai_lingo_voc import SaiLingoVoc
from crawler.instagram.dl import SaiLingoVocDownloader
from publisher.xhs.publisher import Publisher


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
