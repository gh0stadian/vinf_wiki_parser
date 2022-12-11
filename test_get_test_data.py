from parser_utils.wiki_io import WikiIO
from parser_utils.parser import WikiParser


def main():
    wiki = WikiIO("data/raw/enwiki-latest-pages-articles-multistream16.xml-p20460153p20570392")
    parser = WikiParser("data/musicians_sample")
    data = ""

    for i in range(10000):
        chunk = wiki.get_chunk()
        data += parser.get_test_data(chunk)

    with open("data/raw/test_data.xml", "w", encoding="utf8") as f:
        f.write(data)


if __name__ == '__main__':
    main()
