# -*- coding: utf-8 -*-
import csv
import os
import re
import sys

from common.db.town_name_table import TownNameTable
from common.db.town_table import TownTable
from common.db_connection_builder import DbConnectionBuilder
from common.parser import Parser

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
print(sys.path)


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


def load_town_ids(conn):
    cursor = conn.cursor()
    towns = TownTable.get_all(cursor)
    return set(map(lambda x: x['id'], towns))


def main():
    town_map = {}
    host_name = sys.argv[1]
    port_no = sys.argv[2]
    connection = DbConnectionBuilder.build(host_name, port_no)
    town_ids = load_town_ids(connection)

    with open('pdf_list.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            name = create_name(row[0], row[1], row[2])
            town_id = Parser.read_town_id(connection, name)
            if town_id is not None:
                town_ids.discard(town_id)
                print('town_ids = ' + str(len(town_ids)))
                continue
            else:
                print("ERROR %s %s %s" % (row[0], row[1], row[2]))
                continue
    print_town_ids(connection, town_ids)


def print_town_ids(conn, town_ids):
    for town_id in list(town_ids):
        name = TownNameTable.get_name(conn.cursor(), town_id)
        print("{town_name}".format(town_name=name))


if __name__ == '__main__':
    main()
