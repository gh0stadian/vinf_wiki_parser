from parser_utils.wiki_io import WikiIO
from parser_utils.parser import WikiParser


def main():
    wiki = WikiIO("data/raw/enwiki-latest-pages-articles-multistream16.xml-p20460153p20570392")
    parser = WikiParser("data/musicians_sample")


    for i in range(10000):
        chunk = wiki.get_chunk()
        parser.parse(chunk)


if __name__ == '__main__':
    main()
