# -*- coding: utf-8 -*-


class TownPriceTable(object):

    @classmethod
    def register(cls, cursor, price, town_id):
        sql = 'select id from town_price where townId = %s'
        cursor.execute(sql, town_id)
        row = cursor.fetchone()
        if row is not None:
            return row['id']
        sql = 'INSERT town_price SET price = %s, townId = %s'
        cursor.execute(sql, (price, town_id))
        return cursor.lastrowid

    @classmethod
    def count(cls, cursor):
        sql = 'select count(*) from town_price'
        cursor.execute(sql)
        row = cursor.fetchone()
        return row['count(*)']

    @classmethod
    def get(cls, cursor, id):
        sql = 'select price from town_price where townId = %s'
        cursor.execute(sql, (id))
        row = cursor.fetchone()
        if row is None:
            return None
        return row['price']

    @classmethod
    def get_all(cls, cursor):
        sql = 'select * from town_price'
        cursor.execute(sql)
        return cursor.fetchall()


    @classmethod
    def clear_all(cls, cursor):
        sql = 'delete from town_price'
        cursor.execute(sql)
