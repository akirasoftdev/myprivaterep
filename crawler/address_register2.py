# -*- coding: utf-8 -*-
import os
import re
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from common.db.bukken_table import BukkenTable
from common.db.city_table import CityTable
from common.db_connection_builder import DbConnectionBuilder
from common.db_cache.prefecture_cache import PrefectureCache
from common.db_cache.city_cache import CityCache
from common.db_cache.town_cache import TownCache

city_tables = []


def load_city_table(cursor, prefecture_id):
    cities = CityTable.get_cities(cursor, prefecture_id)
    for city in cities:
        city_tables.append(city['name'])


def exclude_city_name_from_address(address, city_rows):
    ret = ''
    for row in city_rows:
        city_name = row['name']
        r = re.compile('^%s(.*)$' % (city_name,))
        m = r.search(address)
        if m is None:
            continue
        address2 = m.group(1)
        if len(ret) > len(address2) or len(ret) == 0:
            ret = address2
    return ret


def exclude_tails(address):
#    address = address.replace('大字', '')

    r = re.compile(u'^([^０-９]*)')
    m = r.search(address)
    if m is not None:
        return m.group(1)

    return address

def main():
    host_name = sys.argv[1]
    port_no = sys.argv[2]
    connection = DbConnectionBuilder.build(host_name, port_no)
    cursor = connection.cursor()

    pref_cache = PrefectureCache(cursor)
    city_cache = CityCache(cursor, pref_cache)
    town_cache = TownCache(cursor, city_cache)

    count = 0
    error_count = 0
    rows = BukkenTable.get_all(cursor)
    for row in rows:
        bukken_id = row['id']
        address = row['address']
        city_id = row['cityId']
        city_rows = city_cache.get_by_id(city_id)
        town_adddress = exclude_city_name_from_address(address, city_rows)
        town2 = exclude_tails(town_adddress)
        town_rows = town_cache.get_by_names(town2, city_id)
        print(city_rows[0]['name'] + ' ' + town2)
        BukkenTable.update_town(cursor, town_rows[0]['id'], bukken_id)
    connection.commit()
    connection.close()

#        town_id = town_cache.find_town_id_by_address(address, row['cityId'])
#        print('town_id : %s' % (town_id))

"""
        price = TownPriceTable.get(cursor, town_id)
        if price is None:
            error_count += 1
            price = 0
        count += 1
        print("%d / %d (%f)" % (error_count, count, (error_count * 100 / count)))
        print("%d: %d" % (error_count, price))
"""


if __name__ == "__main__":
    main()