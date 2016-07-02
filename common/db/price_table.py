# -*- coding: utf-8 -*-
import datetime


class PriceTable(object):

    @classmethod
    def register(cls, cursor, bukken_id, price):
        sql = 'replace price set bukkenId=%s,price=%s'
        cursor.execute(sql, (bukken_id, price))
        return cursor.lastrowid

    @classmethod
    def count(cls, cursor):
        sql = 'select count(*) from price'
        cursor.execute(sql)
        row = cursor.fetchone()
        return row['count(*)']

    @classmethod
    def get(cls, cursor, rid):
        sql = 'select price from price where id = %s'
        cursor.execute(sql, rid)
        row = cursor.fetchone()
        if row is None:
            return None
        return row['price']

    @classmethod
    def get_latest_date(cls, cursor, bukken_id):
        sql = 'select latestDate from price where bukkenId = %s order by latestDate desc'
        cursor.execute(sql, bukken_id)
        row = cursor.fetchone()
        if row is None:
            return None
        return row['latestDate']

    @classmethod
    def clear_all(cls, cursor):
        sql = 'delete from price'
        cursor.execute(sql)

    @classmethod
    def delete_by_bukken_id(cls, cursor, bukken_id):
        sql = 'delete from price where bukkenId = %s'
        cursor.execute(sql, (bukken_id))

    @classmethod
    def get_duplicated_bukken(cls, cursor):
        sql = 'select bukkenId from price group by bukkenId having count(bukkenId) > 1'
        cursor.execute(sql)
        bukkens = {}
        for prices in cursor.fetchall():
            sql = 'select id from price where bukkenId = %s'
            cursor.execute(sql, (prices['bukkenId']))
            bukkens[prices['bukkenId']] = []
            for a in cursor.fetchall():
                bukkens[prices['bukkenId']].append(a)
        return bukkens

    @classmethod
    def delete_by_id(cls, cursor, price_id):
        sql = 'delete from price where id = %s'
        cursor.execute(sql, (price_id))
