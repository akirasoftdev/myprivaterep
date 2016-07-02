# -*- coding: utf-8 -*-


class StationTable(object):

    @classmethod
    def count(cls, cursor):
        sql = 'select count(*) from yahoo_station'
        cursor.execute(sql)
        row = cursor.fetchone()
        return row['count(*)']

    @classmethod
    def get(cls, cursor, station_id):
        sql = 'select * from yahoo_station where id = %s'
        cursor.execute(sql, station_id)
        return cursor.fetchone()

    @classmethod
    def get_all(cls, cursor):
        sql = 'select * from yahoo_station'
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def clear_all(cls, cursor):
        sql = 'delete from yahoo_station'
        cursor.execute(sql)
