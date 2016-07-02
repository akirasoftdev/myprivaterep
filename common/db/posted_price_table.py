# -*- coding: utf-8 -*-


class PostedPriceTable(object):

    @classmethod
    def register(cls, cursor, price, city_id):
        sql = 'select id from posted_price where cityId = %s'
        cursor.execute(sql, city_id)
        row = cursor.fetchone()
        if row is not None:
            return row['id']
        sql = 'INSERT posted_price SET price = %s, cityId = %s, date = %s'
        cursor.execute(sql, (price, city_id, '2016-06-16'))
        return cursor.lastrowid

    @classmethod
    def count(cls, cursor):
        sql = 'select count(*) from posted_price'
        cursor.execute(sql)
        row = cursor.fetchone()
        return row['count(*)']

    @classmethod
    def get(cls, cursor, rid):
        sql = 'select price from posted_price where id = %s'
        cursor.execute(sql, rid)
        row = cursor.fetchone()
        if row is None:
            return None
        return row['price']

    @classmethod
    def get_all(cls, cursor):
        sql = 'select * from posted_price'
        cursor.execute(sql)
        return cursor.fetchall()


    @classmethod
    def clear_all(cls, cursor):
        sql = 'delete from posted_price'
        cursor.execute(sql)
