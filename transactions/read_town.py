#coding:utf-8
import codecs
import csv
import os
import re
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from common.db.city_table import CityTable
from common.db.town_table import TownTable
from common.db import PrefectureTable
from common.db_connection_builder import DbConnectionBuilder
from crawler.normalization import Normalization


class ReadTown(object):
    def __init__(self, host_name, port_no):
        self.connection = DbConnectionBuilder.build(host_name, port_no)
        self.cursor = self.connection.cursor()
        self.db_prefecutre_map = {}
        self.db_city_map = {}
        self.db_town_map = {}
        self.csv_city_map = {}

    def loadPrefecutreFile(self, file):
        with codecs.open(file, 'r', 'utf8', 'ignore') as f:
            for line in csv.reader(f):
                prefecture = line[0]
                city = Normalization.convert(line[1])
                town = Normalization.convert(line[2])
                self.csv_city_map[city] = city
                print("%s, %s, %s" % (prefecture, city, town))
                if prefecture in self.db_prefecutre_map:
                    prefectureId = self.db_prefecutre_map[prefecture]
                else:
                    raise
                if city == '千代田区' and town == '飯田橋':
                    print(city)

                if city in self.db_city_map:
                    cityId = self.db_city_map[city]
                else:
                    cityId = CityTable.register(self.cursor, city, prefectureId)
                    self.db_city_map[city] = cityId
                    print("NEW CITY")

                townId = TownTable.register(self.cursor, town, cityId)
                self.db_town_map[(cityId, town)] = townId

    def loadPrefecutresFromDb(self):
        rows = PrefectureTable.get_all(self.cursor)
        for row in rows:
            self.db_prefecutre_map[row['name']] = row['id']

    def loadCity(self, prefectureId):
        rows = CityTable.get_cities(self.cursor, prefectureId)
        for row in rows:
            self.db_city_map[row['name']] = row['id']

    def parseCity(city):
        r = re.compile('(.*市)(.*区)');
        m = r.search(city)
        if m is not None:
            return m.group(1)
        return city


    def main(self):
        self.loadPrefecutresFromDb()

        prefectures = [(6, '12CHIBA.CSV'), (7, '11SAITAM.CSV'), (8, '13TOKYO.CSV'), (9, '14KANAGA.CSV')]
        for (preId, file_name) in prefectures:
            self.db_city_map = {}
            self.loadCity(preId)
            self.db_town_map = {}
            self.loadPrefecutreFile(file_name)

        self.connection.commit()
        self.connection.close()

if __name__ == "__main__":
    host_name = sys.argv[1]
    port_no = sys.argv[2]
    ReadTown(host_name, port_no).main()