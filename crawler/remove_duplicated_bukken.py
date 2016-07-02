# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from common.db.price_table import PriceTable
from common.db_connection_builder import DbConnectionBuilder


def main():
    host_name = sys.argv[1]
    port_no = sys.argv[2]
    connection = DbConnectionBuilder.build(host_name, port_no)
    cursor = connection.cursor()


    rows = PriceTable.get_duplicated_bukken(cursor)
    print('price-table rows count ' + str(len(rows)))
    for key,values in rows.items():
        print('key ' + str(key))
        for value in values:
            print(value)
            PriceTable.delete_by_id(cursor, value['id'])
            break

    """
    rows = BukkenTable.get_all(cursor)
    print('bukken-table rows count ' + len(rows))
    for row in rows:
        duplicated = BukkenTable.get_duplicated_bukken(cursor, row['cityId'], row['address'], row['buildingFloors'], row['roomFloors'], row['occupiedArea'])
        print('duplicated ' + len(duplicated))
        for drow in duplicated:
            AccessTable.delete_by_bukken_id(cursor, drow['id'])
            PriceTable.delete_by_bukken_id(cursor, drow['id'])
            BukkenTable.delete(cursor, drow['id'])
            print(row['address'])
    """
    connection.commit()
    connection.close()


if __name__ == "__main__":
    main()
