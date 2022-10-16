from wiki_io import WikiIO
from parser import WikiParser


def main():
    wiki = WikiIO("data/raw/enwiki-20221001-pages-articles-multistream6.xml-p958046p1483661")
    parser = WikiParser()

    # TODO UNCOMMENT AND SET UNLIMITED
    for i in range(500):
        chunk = wiki.get_chunk()
        parser.parse(chunk)
    return


if __name__ == '__main__':
    main()
