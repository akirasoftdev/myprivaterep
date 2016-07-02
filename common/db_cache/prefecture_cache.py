# -*- coding: utf-8 -*-
from common.db.prefecture_table import PrefectureTable


class PrefectureCache(object):

    def __init__(self, cursor):
        self.cache = PrefectureTable.get_all(cursor)
        self.id_name_map = {}
        self.name_id_map = {}
        for row in self.cache:
            self.id_name_map[row['id']] = row['name']
            self.name_id_map[row['name']] = row['id']

    def register(self, cursor, prefecture):
        for d in self.cache:
            if d['name'] == prefecture:
                return d['id']
        return PrefectureTable.register(cursor, prefecture);

    def get_by_id(self, id):
        return self.id_name_map

    def get_by_name(self, name):
        return self.name_id_map[name]
