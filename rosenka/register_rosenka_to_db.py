# -*- coding: utf-8 -*-
import codecs
import csv
import re
import sys

from common.db.rosen_price_table import RosenPriceTable
from common.db_cache.city_cache import CityCache
from common.db_cache.prefecture_cache import PrefectureCache
from common.db_cache.town_cache import TownCache
from common.db_connection_builder import DbConnectionBuilder
from common.parser import Parser
from rosenka import address_util
from rosenka.read_rosenka import ReadRosenka

WORK_DIR='work'

def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]


def create_key(prefecture, city, town):
    r = re.compile(u'(.*)[１-９]')
#    utown = town.decode('utf-8')
    m = r.search(town)
    if m is not None:
        town = m.group(1)
    return (prefecture, city, town)

def create_name(prefecture, city, town):
    key = create_key(prefecture, city, town)
    return key[0] + key[1] + key[2]


def read_pdf_list(connection):
    with codecs.open('pdf_list.csv', 'r', 'utf8', 'ignore') as f:
        reader = csv.reader(f)
        next(reader)
        cursor = connection.cursor()
        for row in reader:
            name = create_name(row[0], row[1], row[2])
            town_id = Parser.read_town_id(connection, name)
            if town_id is None:
                continue
            filename = row[3].rsplit('/', 1)[1]
            csv_file_name = filename.replace('.pdf', '.csv')
            mean = ReadRosenka.read(WORK_DIR + "/" + csv_file_name)
            if mean == 0:
                continue
            RosenPriceTable.register(cursor, mean, town_id)




def main():
    host_name = sys.argv[1]
    port_no = sys.argv[2]
    connection = DbConnectionBuilder.build(host_name, port_no)

    read_pdf_list(connection)

    connection.commit()
    connection.close()
    print()

if __name__ == "__main__":
    main()