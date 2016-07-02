# -*- coding: utf-8 -*-
import re

from common.db.city_name_table import CityNameTable
from common.db.city_table import CityTable


class CityCache(object):

    def __init__(self, cursor):
#        self.prefecture_cache = prefecture_cache
        self.city_cache = CityTable.get_all(cursor)
        self.city_name_cache = CityNameTable.get_all(cursor)

#    def register(self, cursor, city_name, prefecture_id):
#        city_name_rows = CityNameTable.get_rows_by_name(cursor, city_name)
#        if city_name_rows is None:
#            return
#        for city_name_row in city_name_rows:
#            city_row = CityTable.get_row_by_id(city_name_row['cityId'])
#            if city_row['prefectureId'] == prefecture_id:
#                return
#        city_id = CityTable.register(cursor, prefecture_id)
#        CityNameTable.register(city_name, city_id)
#        self.city_cache = CityTable.get_all(cursor)
#        self.city_name_cache = CityNameTable.get_all(cursor)

    def get_by_names(self, city_name, prefecture_id):
        ret = []
        for city_name_row in filter(lambda x: x['name'] == city_name, self.city_name_cache):
            for x in self.city_cache:
                if x['id'] == city_name_row['cityId'] and x['prefectureId'] == prefecture_id:
                    ret.append(x)
        if len(ret) > 0:
            return ret
        raise Exception("not found city id, " + city_name)

    def get_all(self, prefecture_id=None):
        cities = []
        for city_name in self.city_name_cache:
            city_info = {}
            city_info['name'] = city_name['name']
            city = None
            for x in self.city_cache:
                if x['id'] == city_name['cityId']:
                    city = x
                    break
            if prefecture_id and prefecture_id != city['prefectureId']:
                continue
            city_info['prefectureId'] = city['prefectureId']
            city_info['id'] = city['id']
            cities.append(city_info)
        return cities

    def get_by_id(self, city_id):
        return list(filter(lambda x: x['cityId'] == city_id, self.city_name_cache))

"""
    def find_city_id_by_address(self, address, prefecture_id):
        for city in self.prefecture_id_and_cities[prefecture_id]:
            r = re.compile("^(%s).*" % (city['name']))
            m = r.search(address)
            if m is not None:
                return city['id']
        raise Exception(address)
"""
"""
    def get_address(self, city_id):
        prefid = self.city_id_map[city_id]['prefectureId']
        prefname = self.prefecture_cache.get_name_by_id(prefid)
        cityname = self.get_name_by_id(city_id)
        return cityname
"""
"""
    def find_city_id(self, city_name, prefecture_id):
        for city in self.prefecture_id_and_cities[prefecture_id]:
            if city['name'] == city_name:
                return city['id']
        raise Exception(city_name)
"""
