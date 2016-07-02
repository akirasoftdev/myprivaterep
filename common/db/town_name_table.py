# -*- coding: utf-8 -*-


class TownNameTable(object):

    @classmethod
    def register(cls, cursor, city_name, city_id):
        sql = 'INSERT town_name SET name = %s, townId = %s'
        cursor.execute(sql, (city_name, city_id))
        return cursor.lastrowid

    @classmethod
    def count(cls, cursor):
        sql = 'select count(*) from town_name'
        cursor.execute(sql)
        row = cursor.fetchone()
        return row['count(*)']

    @classmethod
    def get_name(cls, cursor, town_id):
        sql = 'select name from town_name where townId = %s'
        cursor.execute(sql, town_id)
        row = cursor.fetchone()
        if row is None:
            return None
        return row['name']

    @classmethod
    def get_id(cls, cursor, name):
        sql = 'select city_id from town_name where name = %s'
        cursor.execute(sql, name)
        row = cursor.fetchone()
        if row is None:
            return None
        return row['city_id']

    @classmethod
    def get_all(cls, cursor):
        sql = 'select * from town_name'
        cursor.execute(sql)
        return cursor.fetchall()
