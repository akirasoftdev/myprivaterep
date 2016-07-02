# -*- coding: utf-8 -*-


class RosenPriceTable(object):

    @classmethod
    def register(cls, cursor, price, town_id):
        sql = 'select id from rosen_price where townId = %s'
        cursor.execute(sql, town_id)
        row = cursor.fetchone()
        if row is not None:
            return row['id']
        sql = 'INSERT rosen_price SET price = %s, townId = %s'
        cursor.execute(sql, (price, town_id))
        return cursor.lastrowid

    @classmethod
    def count(cls, cursor):
        sql = 'select count(*) from rosen_price'
        cursor.execute(sql)
        row = cursor.fetchone()
        return row['count(*)']

    @classmethod
    def get(cls, cursor, rid):
        sql = 'select price from rosen_price where townId = %s'
        cursor.execute(sql, rid)
        row = cursor.fetchone()
        if row is None:
            return None
        return row['price']

    @classmethod
    def getAll(cls, cursor):
        sql = 'select * from rosen_price'
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def clearAll(cls, cursor):
        sql = 'delete from rosen_price'
        cursor.execute(sql)
