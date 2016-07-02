import codecs
import csv
import os
import sys

from normalization import Normalization

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from common.db.city_table import CityTable
from common.db import TownPriceTable
from common.db.town_table import TownTable
from common.db_connection_builder import DbConnectionBuilder


def verifyName(name):
    return len(name) > 0 and name != '東・西江見' and name != '（大字なし）'


def readFile(cursor, prefectureId, file_name):
    skip_header = True
    prices = {}
    with codecs.open(file_name, 'r', 'utf8', 'ignore') as f:
        for line in csv.reader(f):
            if skip_header:
                skip_header = False
                continue
            city = Normalization.convert(line[5])
            town = Normalization.convert(line[6])
            tubo = line[10]

            if verifyName(city) == False or verifyName(town) == False:
                print(line)
                continue

            if len(tubo) > 0:
                print("%s %s, 坪単価:%s" % (city, town, tubo))
                if (city, town) not in prices:
                    prices[(city, town)] = []
                prices[(city, town)].append(int(tubo))

    print("##### " , len(prices))
    for city, town in prices:
        cityId = CityTable.get_id(cursor, city)
        townId = TownTable.get_id(cursor, cityId, town)
        if townId == None:
            raise Exception("%s" % (town))
        ave = int(sum(prices[(city, town)]) / len(prices[(city, town)]))
        print("%s %s(%s) : %d" % (city, town, townId, ave))
        TownPriceTable.register(cursor, ave, townId)


def main():
    host_name = sys.argv[1]
    port_no = sys.argv[2]
    connection = DbConnectionBuilder.build(host_name, port_no)
    cursor = connection.cursor()

    prefectures = [
        (7, '11_Saitama Prefecture_20053_20154.csv'),
        (6, '12_Chiba Prefecture_20053_20154.csv'),
        (8, '13_Tokyo_20053_20154.csv'),
        (9, '14_Kanagawa Prefecture_20053_20154.csv')]
    for (preId, file_name) in prefectures:
        readFile(cursor, preId, file_name)
        connection.commit()
    connection.close()

if __name__ == "__main__":
    main()