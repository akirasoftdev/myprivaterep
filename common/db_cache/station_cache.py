# -*- coding: utf-8 -*-
from common.db.station_table import StationTable

class StationCache(object):

    def __init__(self, cursor):
        stations = StationTable.get_all(cursor)
        self.cache = {}
        for station in stations:
            key = station['line'] + '_' + station['name']
            if key in self.cache:
                if self.cache[key] == station['id']:
                    continue
                raise Exception(key)
            self.cache[key] = station['id']

    def get(self, cursor, name, line):
        key = line + '_' + name
        if key in self.cache:
            return self.cache[key]
        return None
