# -*- coding: utf-8 -*-


class AccessTable(object):
    @classmethod
    def register(cls, cursor, bukken_id, station_id, walk_time, bus_time):
        sql = 'select id from access where bukkenId = %s'
        cursor.execute(sql, bukken_id)
        row = cursor.fetchone()
        if row is not None:
            return row['id']
        sql = 'INSERT access SET bukkenId=%s,stationId=%s,walkTime=%s,busTime=%s'
        cursor.execute(sql, (bukken_id, station_id, walk_time, bus_time))
        return cursor.lastrowid

    @classmethod
    def count(cls, cursor):
        sql = 'select count(*) from access'
        cursor.execute(sql)
        row = cursor.fetchone()
        return row['count(*)']

    @classmethod
    def get(cls, cursor, id):
        sql = 'select bukkenId from access where id = %s'
        cursor.execute(sql, id)
        row = cursor.fetchone()
        if row is None:
            return None
        return row['bukkenId']

    @classmethod
    def clear_all(cls, cursor):
        sql = 'delete from access'
        cursor.execute(sql)

    @classmethod
    def delete_by_bukken_id(cls, cursor, bukken_id):
        sql = 'delete from access where bukkenId=%s'
        cursor.execute(sql, bukken_id)
