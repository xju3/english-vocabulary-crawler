import sys

from crawler.insta.vocabulary import Vocabulary


def main():
    parameters = sys.argv[1:]

    if len(parameters) == 0 or parameters[0] == "1":
        insta_vocabulary = Vocabulary()
        insta_vocabulary.run()

    if len(parameters) > 0:
        if (parameters[0] == "2"):
            pass

        if (parameters[0] == "3"):
            pass


if __name__ == '__main__':
    main()
