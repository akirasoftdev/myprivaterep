# -*- coding: utf-8 -*-
import re

from common.db.town_name_table import TownNameTable
from crawler.athome.parser.address_parser import AddressParser

from common.db.town_table import TownTable


class TownCache(object):

    def __init__(self, cursor):
#        self.city_cache = city_cache
        self.town_cache = TownTable.get_all(cursor)
        self.town_name_cache = TownNameTable.get_all(cursor)

    def get_by_names(self, town_name, city_id):
        ret = []
        for town_name_row in filter(lambda x: x['name'] == town_name, self.town_name_cache):
            for x in self.town_cache:
                if x['id'] == town_name_row['townId'] and x['cityId'] == city_id:
                    ret.append(x)
        return ret

    def add_town_name(self, cursor, town_id, town_name):
        TownNameTable.register(cursor, town_name, town_id)

"""
    def find_town_id_address(self, address, city_id):
        if city_id not in self._town_map:
            raise Exception(city_id)
        city_name = self._cityCache.get_name_by_id(city_id)
        r = re.compile("^(%s)(.*)$" % city_name)
        m = r.search(address)
        address_without_city = m.group(2)
        print("address_without_city : %s" % (address_without_city))
        town_name = AddressParser.parse_town(address_without_city)
        print("town_name : %s" % (town_name))

        for row in self._cache:
            if row['name'] == town_name:
                return row['id']
        raise Exception(address)

    def find_town_id(self, town_name, city_id):
        if city_id not in self._town_map:
            raise Exception(city_id)
        town_list = self._town_map[city_id]
        for row in town_list:
            if row['name'] == town_name:
                return row['id']
        raise Exception(town_name)
"""
