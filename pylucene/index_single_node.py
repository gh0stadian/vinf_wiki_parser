import os, sys, glob
import lucene
from org.apache.lucene.store import FSDirectory
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField, StoredField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from parser_utils.utils.musician_page_object import MusicianPageObject
import os
import re
import time

DATA_FILE_NAME = "/mnt/data/musicians_sample"


def get_entities_from_file(path):
    """Returns a generator of entities from a file."""
    with open(path, "r", encoding="utf8") as f:
        while True:
            position = f.tell()
            line = f.readline()
            if not line:
                break
            yield position, line


def create_index():
    """Creates an index of musician pages."""
    index_path = File("/mnt/data/index").toPath()
    store = FSDirectory.open(index_path)
    config = IndexWriterConfig(StandardAnalyzer())
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    for file_position, entity in get_entities_from_file(DATA_FILE_NAME):
        musician = MusicianPageObject.from_json_sn(entity)
        doc = Document()
        doc.add(Field("title", musician.title, TextField.TYPE_STORED))
        doc.add(Field("about", str(musician.about), TextField.TYPE_NOT_STORED))
        doc.add(Field("discography", str(musician.discography), TextField.TYPE_NOT_STORED))
        doc.add(Field("awards", str(musician.awards), TextField.TYPE_NOT_STORED))
        doc.add(StoredField("file_path", DATA_FILE_NAME))
        doc.add(StoredField("file_position", file_position))
        writer.addDocument(doc)
    writer.commit()
    writer.close()


if __name__ == '__main__':
    lucene.initVM()
    start_time = time.time()
    create_index()
    print(str((time.time() - start_time)))
