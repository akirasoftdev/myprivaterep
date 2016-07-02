# -*- coding: utf-8 -*-
import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from common.db_connection_builder import DbConnectionBuilder


def list_duplicated_bukken_id(cursor):
    sql = 'select bukkenId from price group by bukkenId having count(bukkenId) > 1;'
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


def combine_price(cursor, bukken_id):
    sql = 'select * from price where bukkenId=%s'
    cursor.execute(sql, (bukken_id))
    rows = cursor.fetchall()
    latest_date = datetime.datetime(1970, 1, 1)
    price = 0
    id_of_latest_date = 0
    for row in rows:
        if row['latestDate'] > latest_date:
            price = row['price']
            id_of_latest_date = row['id']
    sql = 'update price set latestDate=%s, price=%s where id=%s'
    cursor.execute(sql, (latest_date,price, id_of_latest_date))
    for row in rows:
        if row['id'] != id_of_latest_date:
            sql = 'delete from price where id=%s'
            cursor.execute(sql, (row['id']))
    return


def main():
    host_name = sys.argv[1]
    port_no = sys.argv[2]
    connection = DbConnectionBuilder.build(host_name, port_no)
    cursor = connection.cursor()

    bukken_ids = list_duplicated_bukken_id(cursor)
    for bukken_id in bukken_ids:
        combine_price(cursor, bukken_id['bukkenId'])
    connection.commit()
    connection.close()

if __name__ == '__main__':
    main()