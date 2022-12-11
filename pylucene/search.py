import lucene
import re
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import FSDirectory
from java.io import File
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser, MultiFieldQueryParser
from org.apache.lucene.analysis.standard import StandardAnalyzer
from parser_utils.utils.musician_page_object import MusicianPageObject


def print_welcome_message():
    print("Welcome to Artist Searcher ...\n"
          "Start by typing query and we will provide you with top 10 results\n"
          "If you want to list only titles, use \"-l\" followed by query\n"
          "If you want to change number of results per query use -limit <NUMBER>\n"
          "If you want to quit, type \"-q\"")

def get_full_artist_info(file_name, file_position):
    """
    Returns full artist info from file
    :param file_name: file to read from
    :param file_position: position in file to start reading from
    :return: artist object
    """
    with open(file_name, "r", encoding="utf8") as f:
        f.seek(int(file_position))
        artist = MusicianPageObject.from_json(f.readline())
        return artist


def search(query, list_only=False, limit=10):
    """
    Searches for text in index and returns list of results
    :param query: query to search for
    :param list_only: if true, only titles will be returned
    :param limit: number of results to return
    """
    index_path = File("/mnt/data/index").toPath()
    store = FSDirectory.open(index_path)
    searcher = IndexSearcher(DirectoryReader.open(store))

    parser = MultiFieldQueryParser(["title", "discography", "awards"], StandardAnalyzer())
    query = MultiFieldQueryParser.parse(parser, query)
    scoreDocs = searcher.search(query, limit).scoreDocs

    if not scoreDocs:
        print("No results")

    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        if list_only:
            print(doc.get("title"))

        else:
            artist = get_full_artist_info(doc.get("file_path"), doc.get("file_position"))
            print(str(artist))


if __name__ == '__main__':
    lucene.initVM()
    limit = 10
    print_welcome_message()
    while True:
        query = input('Input: ')
        if query == "":
            print("Wrong input")
        elif query.startswith("-l "):
            search(query[3:], list_only=True, limit=limit)
        elif query.lower() == "-q":
            break
        elif query.startswith("-limit"):
            try:
                limit = int(query[7:])
            except Exception:
                limit = 10
                print("Error setting limit, limit will be set to 10")
        else:
            search(query, limit=limit)
