# -*- coding: utf-8 -*-


class PrefectureTable(object):
    @classmethod
    def register(cls, cursor, prefecture):
        sql = 'select id from prefecture where name = %s'
        cursor.execute(sql, prefecture)
        row = cursor.fetchone()
        if row is not None:
            return row['id']
        sql = 'INSERT prefecture SET name=%s'
        cursor.execute(sql, (prefecture))
        return cursor.lastrowid

    @classmethod
    def count(cls, cursor):
        sql = 'select count(*) from prefecture'
        cursor.execute(sql)
        row = cursor.fetchone()
        return row['count(*)']

    @classmethod
    def get(cls, cursor, rid):
        sql = 'select name from prefecture where id = %s'
        cursor.execute(sql, rid)
        row = cursor.fetchone()
        if row is None:
            return None
        return row['name']

    @classmethod
    def get_all(cls, cursor):
        sql = 'select * from prefecture'
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def clear_all(cls, cursor):
        sql = 'delete from prefecture'
        cursor.execute(sql)
