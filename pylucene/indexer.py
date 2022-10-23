import os,sys,glob
import lucene
from org.apache.lucene.store import FSDirectory
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from parser_utils.utils.musician_page_object import MusicianPageObject
import os
import re
import time

def create_index():
    index_path = File("/mnt/data/index").toPath()
    store = FSDirectory.open(index_path)
    config = IndexWriterConfig(StandardAnalyzer())
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)
    with open("/mnt/data/musicians") as f:
        for line in f:
            musician = MusicianPageObject.from_json(line)
            doc = Document()
            doc.add(Field("title", musician.title, TextField.TYPE_STORED))
            doc.add(Field("full_info", line, TextField.TYPE_STORED))
            writer.addDocument(doc)
    writer.commit()
    writer.close()

if __name__ == '__main__':

    lucene.initVM()
    start_time = time.time()
    create_index()
    print(str((time.time() - start_time)))