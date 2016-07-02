# -*- coding: utf-8 -*-


class CityNameTable(object):
    @classmethod
    def register(cls, cursor, city_name, city_id):
        sql = 'INSERT city_name SET name = %s, cityId = %s'
        cursor.execute(sql (city_name, city_id))
        return cursor.lastrowid

    @classmethod
    def count(cls, cursor):
        sql = 'select count(*) from city_name'
        cursor.execute(sql)
        row =  cursor.fetchone()
        return row['count(*)']

    @classmethod
    def get_name(cls, cursor, city_id):
        sql = 'select name from city_name where cityId = %s'
        cursor.execute(sql, (id))
        row = cursor.fetchone()
        if row is None:
            return None
        return row['name']

    @classmethod
    def get_id(cls, cursor, name):
        sql = 'select city_id from city_name where name = %s'
        cursor.execute(sql, (name))
        row = cursor.fetchone()
        if row is None:
            return None
        return row['city_id']

    @classmethod
    def get_rows_by_name(cls, cursor, name):
        sql = 'select city_id from city_name where name = %s'
        cursor.execute(sql, (name))
        return cursor.fetchall()

    @classmethod
    def get_all(cls, cursor):
        sql = 'select * from city_name'
        cursor.execute(sql)
        return cursor.fetchall()
