# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from crawler.athome.validate_bukken import ValidateBukken
from common.db.access_table import AccessTable
from common.db.bukken_table import BukkenTable
from common.db.price_table import PriceTable
from common.db_connection_builder import DbConnectionBuilder


def main():
    host_name = sys.argv[1]
    port_no = sys.argv[2]
    connection = DbConnectionBuilder.build(host_name, port_no)
    cursor = connection.cursor()

    bukkens = BukkenTable.get_ll(cursor)
    for bukken in bukkens:
        if not ValidateBukken.validate(0, bukken['layout'], 0, bukken['occupiedArea'], 0, 0, 0):
            print("%s %s" % (bukken['title'], bukken['url']))
            AccessTable.delete_by_bukken_id(cursor, bukken['id'])
            PriceTable.delete_by_bukken_id(cursor, bukken['id'])
            BukkenTable.delete(cursor, bukken['id'])
    connection.commit()
    connection.close()

if __name__  == "__main__":
    main()