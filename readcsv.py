# -*- coding: utf-8 -*-

import codecs
import csv
import sys
from pymysql import IntegrityError

from common.db_connection_builder import DbConnectionBuilder


def insert_bukken(cursor, param):
    sql = """
    INSERT
        bukken
    SET
        id=%(id)s,
        url=%(url)s,
        title=%(title)s,
        address=%(address)s,
        prefectureId=%(prefectureId)s,
        cityId=%(cityId)s,
        landArea=%(landArea)s,
        buildingArea=%(buildingArea)s,
        layout=%(layout)s,
        year=%(year)s,
        buildingFloors=%(buildingFloors)s,
        roomFloors=%(roomFloors)s,
        numberOfHouse=%(numberOfHouse)s,
        occupiedArea=%(occupiedArea)s,
        underGround=%(underGround)s,
        structure=%(structure)s,
        townId=%(townId)s
    """
    cursor.execute(sql, param)


def delete_access_by_id(cursor, id):
    sql = """
    DELETE FROM
        access
    WHERE
        bukkenId=%s
    """
    cursor.execute(sql, id)


def delete_price_by_id(cursor, id):
    sql = """
    DELETE FROM
        price
    WHERE
        bukkenId=%s
    """
    cursor.execute(sql, (id, ))


def load_address_list_in_memory(connection):
    cursor = connection.cursor()

    count = 0
    error = 0

    with codecs.open('bukken.csv', 'r', 'utf8', 'ignore') as f:
        for line in csv.reader(f, delimiter=';'):
            if line[0] == 'id':
                continue
            data = {
                "id": line[0],
                "url": line[1],
                "title": line[2],
                "address": line[3],
                "prefectureId": line[4],
                "cityId": line[5],
                "landArea": line[6],
                "buildingArea": line[7],
                "layout": line[8],
                "year": line[9],
                "buildingFloors": line[10],
                "roomFloors": line[11],
                "numberOfHouse": line[12],
                "occupiedArea": line[13],
                "underGround": line[14],
                "structure": line[15],
                "townId": line[16]
            }
            try:
                count += 1
                insert_bukken(cursor, data)
            except IntegrityError as e:
                if e.args[0] == 1062:
                    error += 1
                    delete_access_by_id(cursor, line[0])
                    delete_price_by_id(cursor, line[0])
            print("rate - %f" % ((count - error) / count))
    connection.commit()
    connection.close()

host_name = sys.argv[1]
port_no = sys.argv[2]
connection = DbConnectionBuilder.build(host_name, port_no)

load_address_list_in_memory(connection)