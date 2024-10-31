import sys

from crawler.insta.vocabulary import Vocabulary


def main():
    parameter = sys.argv[1:]

    if len(parameter) == 0 or parameter[0] == "1":
        insta_vocabulary = Vocabulary()
        insta_vocabulary.run()

    if len(parameter) > 0:
        if (parameter[0] == "2"):
            pass

        if (parameter[0] == "3"):
            pass


if __name__ == '__main__':
    main()
