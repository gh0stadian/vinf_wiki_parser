from parser_utils.wiki_io import WikiIO
from parser_utils.parser import WikiParser


def main():
    wiki = WikiIO("data/raw/test_data.xml")
    parser = WikiParser("data/musicians_sample")


    for i in range(10000):
        chunk = wiki.get_chunk()
        parser.parse(chunk)


if __name__ == '__main__':
    main()
