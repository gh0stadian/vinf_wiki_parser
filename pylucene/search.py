import lucene
import re
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import FSDirectory
from java.io import File
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.analysis.standard import StandardAnalyzer
from parser_utils.utils.musician_page_object import MusicianPageObject


def search(text):
    index_path = File("/mnt/data/index").toPath()
    store = FSDirectory.open(index_path)
    searcher = IndexSearcher(DirectoryReader.open(store))
    query = QueryParser("full_info", StandardAnalyzer()).parse(text)

    scoreDocs = searcher.search(query, 50).scoreDocs
    if not scoreDocs:
        print("No results")

    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        json = doc.get("full_info")
        musician = MusicianPageObject.from_json(json)
        print(str(musician))


if __name__ == '__main__':
    lucene.initVM()

    while True:
        query = input('Input: ')
        if query == "":
            print("Wrong input")
        elif query.lower() == "-q":
            break
        else:
            search(query)
