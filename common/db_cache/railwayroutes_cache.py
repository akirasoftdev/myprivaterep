# -*- coding: utf-8 -*-
from common.db.railwayroutes_table import RailwayRoutesTable

class RailwayroutesCache(object):

    def __init__(self, cursor):
        self.cache = RailwayRoutesTable.get_all(cursor)

    def register(self, cursor, railway_routes):
        for d in self.cache:
            if d['name'] == railway_routes:
                return d['id']
        return RailwayRoutesTable.register(cursor, railway_routes)
