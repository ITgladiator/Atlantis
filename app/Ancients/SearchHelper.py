#! /usr/bin/env python
# ^_^ coding: utf-8 ^_^
import os.path
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from config import INDEX_DIR
from whoosh.qparser import QueryParser
from chineseAnalyzer import ChineseAnalyzer


analyzer = ChineseAnalyzer()


class MySchema(SchemaClass):
    id = NUMERIC(stored=True)
    title = TEXT(stored=True, analyzer=analyzer)
    content = TEXT(stored=True, analyzer=analyzer)
    tags = KEYWORD


class SearchHelper(object):
    def __init__(self):
        if not os.path.exists(INDEX_DIR):
            os.makedirs(INDEX_DIR)
        self.__schema = MySchema()

    def first_add_document(self, data_source):
        self.__ix = create_in(INDEX_DIR, self.__schema)
        self.__ix = open_dir(INDEX_DIR)
        self.__writer = self.__ix.writer()
        for item in data_source:
            # print type(item)
            self.__writer.add_document(**item)
        self.__writer.commit()

    def increment_add_document(self, data_source):
        self.__ix = open_dir(INDEX_DIR)
        self.__writer = self.__ix.writer()
        for item in data_source:
            # print type(item)
            self.__writer.add_document(**item)
        self.__writer.commit()

    def search(self, keyword):
        self.__ix = open_dir(INDEX_DIR)
        query_field = ['title', 'content']
        # keyword = kwargs.get('keyword')
        res_list = []
        with self.__ix.searcher() as searcher:
            for q in query_field:
                query = QueryParser(q, self.__schema).parse(keyword)
                result = searcher.search(query)
                if result:
                    for r in result:
                        res_list.append(int(r.fields().get('id')))
            # print format(res_list)
        return set(res_list)


