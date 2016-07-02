# -*- coding: utf-8 -*-


class AreaTable(object):
    @classmethod
    def register(cls, cursor, area, prefecture_id, city_id):
        sql = 'select id from area where name = %s and prefectureId = %s and cityId = %s'
        cursor.execute(sql, (sql, prefecture_id, city_id))
        row = cursor.fetchone()
        if row is not None:
            return row['id']
        sql = 'INSERT area SET name = %s, prefectureId = %s, cityId = %s'
        cursor.execute(sql, (area, prefecture_id, city_id))
        return cursor.lastrowid

    @classmethod
    def count(cls, cursor):
        sql = 'select count(*) from city'
        cursor.execute(sql)
        row = cursor.fetchone()
        return row['count(*)']

    @classmethod
    def get(cls, cursor, rid):
        sql = 'select name from city where id = %s'
        cursor.execute(sql, rid)
        row = cursor.fetchone()
        if row is None:
            return None
        return row['name']

    @classmethod
    def get_all(cls, cursor):
        sql = 'select * from city'
        cursor.execute(sql)
        return cursor.fetchall()


    @classmethod
    def clear_all(cls, cursor):
        sql = 'delete from city'
        cursor.execute(sql)
