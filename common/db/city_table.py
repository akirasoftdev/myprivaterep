# -*- coding: utf-8 -*-


class CityTable(object):
    @classmethod
    def register(cls, cursor, prefecture_id):
        sql = 'INSERT city SET prefectureId = %s'
        cursor.execute(sql, prefecture_id)
        return cursor.lastrowid

    @classmethod
    def count(cls, cursor):
        sql = 'select count(*) from city'
        cursor.execute(sql)
        row = cursor.fetchone()
        return row['count(*)']

    @classmethod
    def get_all(cls, cursor):
        sql = 'select * from city'
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def get_row_by_id(cls, cursor, city_id):
        sql = 'select * from city where cityId = %s'
        cursor.execute(sql, city_id)
        return cursor.fetchone()

    @classmethod
    def get_cities(cls, cursor, prefecture_id):
        sql = 'select * from city where prefectureId = %s'
        cursor.execute(sql, prefecture_id)
        return cursor.fetchall()

    @classmethod
    def get_cities_order_by_len(cls, cursor, prefecture_id):
        sql = '''
        select
            name, id, char_length(name) as name_len
        from
            city_name
        join
            (select * from city where prefectureId = %s) as B
        on
            city_name.cityId = B.id
        order by name_len DESC
       '''
        cursor.execute(sql, prefecture_id)
        return cursor.fetchall()


    @classmethod
    def delete_all(cls, cursor):
        sql = 'delete from city'
        cursor.execute(sql)
