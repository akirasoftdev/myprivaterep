# -*- coding: utf-8 -*-
import re

from common.db.city_table import CityTable
from common.db.prefecture_table import PrefectureTable
from common.db.town_table import TownTable


class Parser:
    def __init__(self):
        pass

    @classmethod
    def read_town_id(cls, conn, address):
        prefecture = cls.read_prefecture(conn, address)
        print(repr(prefecture))
        if prefecture is None:
            print("failed to parse [prefecture]" + address)
            return None
        address_city = address[len(prefecture['name']):]
        print(repr(address_city))
        city = cls.read_city(conn, prefecture['id'], address_city)
        print(repr(city))
        if city is None:
            print("failed to parse [city]" + address)
            return None
        address_town = address_city[len(city['name']):]
        print(repr(address_town))
        town = cls.read_town(conn, city['id'], address_town)
        print(repr(town))
        if town is None:
            print("failed to parse [town]" + address)
            return None

        return town['id']

    @classmethod
    def read_prefecture(cls, conn, address):
        cursor = conn.cursor()
        rows = PrefectureTable.get_all(cursor)
        for row in rows:
            mo = re.match('^%s' % (row['name']), address)
            if mo:
                return row
        return None

    @classmethod
    def read_city(cls, conn, prefecture_id, address):
        cursor = conn.cursor()
        rows = CityTable.get_cities_order_by_len(cursor, prefecture_id)
        for row in rows:
            mo = re.match('^%s' % (row['name']), address)
            if mo:
                return row
        return None

    @classmethod
    def read_town(cls, conn, city_id, address):
        cursor = conn.cursor()
        rows = TownTable.get_towns_order_by_len(cursor, city_id)
        for row in rows:
            mo = re.match('^%s' % (row['name']), address)
            if mo:
                return row
        return None
