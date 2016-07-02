# -*- coding: utf-8 -*-
import codecs
import csv
import os
import re
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
print(sys.path)
from common.db.city_table import CityTable
from common.db.posted_price_table import PostedPriceTable
from common.db.prefecture_table import PrefectureTable
from common.db_connection_builder import DbConnectionBuilder

koji_map = {}
prefecture_map = {}


def load_koji_map_in_memory():
    with codecs.open('kouji.csv', 'r', 'utf8', 'ignore') as f:
        for prefecture, city, price in csv.reader(f):
            print("%s, %s, %s" % (prefecture, city, price))
            if not prefecture in koji_map:
                koji_map[prefecture] = {}
            if not city in koji_map[prefecture]:
                koji_map[prefecture][city] = 0
                koji_map[prefecture][city] = int(price)


def load_prefectures(cursor):
    rows = PrefectureTable.get_all(cursor)
    for row in rows:
        prefecture_map[row['id']] = row['name']


def parse_city(city):
    r = re.compile('(.*市)(.*区)')
    m = r.search(city)
    if m is not None:
        return m.group(1)
    return city


def main():
    host_name = sys.argv[1]
    port_no = sys.argv[2]
    load_koji_map_in_memory()
    connection = DbConnectionBuilder.build(host_name, port_no)

    cursor = connection.cursor()
    load_prefectures(cursor)

    rows = CityTable.get_all(cursor)
    for row in rows:
        prefecture_name = prefecture_map[row['prefectureId']]
        city = row['name']
        cityId = row['id']
        if not city in koji_map[prefecture_name]:
            print("%s %s" % (prefecture_name, city))
            raise Exception(city)
        PostedPriceTable.register(cursor, koji_map[prefecture_name][city], cityId)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    main()