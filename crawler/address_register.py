# -*- coding: utf-8 -*-
import codecs
import csv
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
print(sys.path)
from common.db.area_table import AreaTable
from common.db.prefecture_table import PrefectureTable
from common.db_cache.city_cache import CityCache
from common.db_connection_builder import DbConnectionBuilder

address_map = {}
prefecture_map = {}
city_map = {}


def load_address_list_in_memory():
    with codecs.open('address_list.csv', 'r', 'utf8', 'ignore') as f:
        for line in csv.reader(f):
            print("%s, %s, %s" % (line[0], line[1], line[2]))
            prefecture = line[0]
            city = line[1]
            area = line[2]
            if not prefecture in address_map:
                address_map[prefecture] = {}
            if not city in address_map[prefecture]:
                address_map[prefecture][city] = []
            if not area in address_map[prefecture][city]:
                address_map[prefecture][city].append(area)


def load_prefectures(cursor):
    rows = PrefectureTable.get_all(cursor)
    for row in rows:
        prefecture_map[row['name']] = row['id']


def main():
    load_address_list_in_memory()
    host_name = sys.argv[1]
    port_no = sys.argv[2]
    connection = DbConnectionBuilder.build(host_name, port_no)

    cursor = connection.cursor()
    load_prefectures(cursor)
    city_cache = CityCache(cursor)

    for preference in address_map:
        for city in address_map[preference]:
            cityId = city_cache.register(cursor, city, prefecture_map[preference])
            for area in address_map[preference][city]:
                AreaTable.register(cursor, area, prefecture_map[preference], cityId)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    main()