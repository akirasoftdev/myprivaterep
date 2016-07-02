# -*- coding: utf-8 -*-
import re


class TownTable(object):

    @classmethod
    def register(cls, cursor, town, city_id):
        sql = 'select id from town where name = %s and cityId = %s'
        cursor.execute(sql, (town, city_id))
        row = cursor.fetchone()
        if row is not None:
            return row['id']
        sql = 'INSERT town SET name = %s, cityId = %s'
        cursor.execute(sql, (town, city_id))
        return cursor.lastrowid

    @classmethod
    def count(cls, cursor):
        sql = 'select count(*) from town'
        cursor.execute(sql)
        row = cursor.fetchone()
        return row['count(*)']

    @classmethod
    def get(cls, cursor, rid):
        sql = 'select name from town where id = %s'
        cursor.execute(sql, (rid))
        row = cursor.fetchone()
        if row is None:
            return None
        return row['name']

    @classmethod
    def convert_name_if_needed(cls, name):
        r = re.compile("^大字(.+)")
        m = r.search(name)
        if m is not None:
            name = m.group(1)
        r = re.compile("^字(.+)")
        m = r.search(name)
        if m is not None:
            name = m.group(1)
        r = re.compile("^(.+)[イロハニホ]$")
        m = r.search(name)
        if m is not None:
            name = m.group(1)
        name = name.replace('ェ', 'エ')
        name = name.replace('靭', '靱')
        name = '五丁台' if name == '五町台' else name
        name = '将軍沢' if name == '将軍澤' else name
        name = '平沢' if name == '平澤' else name
        name = '大淵' if name == '大渕' else name
        name = '広野' if name == '廣野' else name
        name = '駒込' if name == '駒込経田' else name
        name = '小林' if name == '小林飛地' else name
        name = '棚沢' if name == '棚澤' else name
        name = '海沢' if name == '海澤' else name
        name = '子母口' if name == '子母口富士見台' else name
        name = '槇野地' if name == '槙野地' else name
        name = '瀬戸' if name == '瀬戸上灰毛' else name
        name = '木間ケ瀬' if name == '木間ケ瀬新田' else name
        return name

    @classmethod
    def get_id(cls, cursor, city_id, name):
        if name[0] == '字' or name[0] == '大':
            print(name)
        name = cls.convert_name_if_needed(name)
        print(name)

        sql = 'select id from town where name = %s'
        cursor.execute(sql, (name))
        row = cursor.fetchone()
        if row is not None:
            return row['id']
        return None

    @classmethod
    def get_all(cls, cursor):
        sql = 'select * from town'
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def get_towns(cls, cursor, city_id):
        sql = 'select * from town where cityId = %s'
        cursor.execute(sql, city_id)
        return cursor.fetchall()

    @classmethod
    def get_name_all(cls, cursor):
        sql = 'select name from town'
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def clear_all(cls, cursor):
        sql = 'delete from town'
        cursor.execute(sql)


    @classmethod
    def get_towns_order_by_len(cls, cursor, city_id):
        sql = '''
        select
            name, id, char_length(name) as name_len
        from
            town_name
        join
            (select * from town where cityId = %s) as B
        on
            town_name.townId = B.id
        order by name_len DESC
       '''
        cursor.execute(sql, city_id)
        return cursor.fetchall()
