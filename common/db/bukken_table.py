# -*- coding: utf-8 -*-


class BukkenTable(object):
    @classmethod
    def register(cls, cursor, url, title, prefecture_id, city_id, town_id, address, layout, year,
                 occupied_area, building_floors, under_ground, room_floor, structure,
                 station_id, walk_time, price, last_modified):
        sql = '''
        INSERT
            bukken
        SET
            url=%(url)s,
            title=%(title)s,
            prefectureId=%(prefecture_id)s,
            cityId=%(city_id)s,
            townId=%(town_id)s,
            address=%(address)s,
            layout=%(layout)s,
            year=%(year)s,
            occupiedArea=%(occupied_area)s,
            buildingFloors=%(building_floors)s,
            underGround=%(under_ground)s,
            roomFloors=%(room_floor)s,
            structure=%(structure)s,
            stationId=%(stationId)s,
            walkTime=%(walk_time)s,
            price=%(price)s,
            lastModified=%(lastModified)s
            ON DUPLICATE KEY UPDATE
            lastModified=%(lastModified)s
        '''
        params = {
            'url': url,
            'title': title,
            'prefecture_id': prefecture_id,
            'city_id': city_id,
            'town_id': town_id,
            'address': address,
            'layout': layout,
            'year': year,
            'occupied_area': occupied_area,
            'building_floors': building_floors,
            'under_ground': under_ground,
            'room_floor': room_floor,
            'structure': structure,
            'stationId': station_id,
            'walk_time': walk_time,
            'price': price,
            'lastModified': last_modified
        }
        cursor.execute(sql, params)
        return cursor.lastrowid

    @classmethod
    def update_landarea(cls, cursor, rid, land_area):
        sql = 'select id from bukken where id = %s And landArea is null'
        cursor.execute(sql, rid)
        row = cursor.fetchone()
        if row is None:
            return row
        sql = 'update bukken set landArea=%s where id=%s'
        cursor.execute(sql, (land_area, rid))

    @classmethod
    def update_buildingarea(cls, cursor, rid, building_area):
        sql = 'select id from bukken where id = %s And buildingArea is null'
        cursor.execute(sql, rid)
        row = cursor.fetchone()
        if row is None:
            return
        sql = 'update bukken set buildingArea=%s where id=%s'
        cursor.execute(sql, (building_area, rid))
        return

    @classmethod
    def count(cls, cursor):
        sql = 'select count(*) from bukken'
        cursor.execute(sql)
        row = cursor.fetchone()
        return row['count(*)']

    @classmethod
    def get(cls, cursor, rid):
        sql = 'select url, title, address, prefectureId, cityId, landArea, buildingArea, layout, year, occupiedArea, walkTime, stationId, price from bukken where id = %s'
        cursor.execute(sql, rid)
        row = cursor.fetchone()
        if row is None:
            return None
        return row

    @classmethod
    def get_all(clsc, cursor):
        sql = 'select * from bukken'
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def clear_all(cls, cursor):
        sql = 'delete from bukken'
        cursor.execute(sql)

    @classmethod
    def get_duplicated_bukken(cls, cursor, city_id, address, building_floors, room_floors, occupied_area):
        sql = 'select * from bukken where cityId = %s and address = %s and buildingFloors = %s and roomFloors = %s and occupiedArea = %s'
        cursor.execute(sql, (city_id, address, building_floors, room_floors, occupied_area))
        row = cursor.fetchall()
        return row

    @classmethod
    def delete(cls, cursor, rid):
        sql = 'delete from bukken where id = %s'
        cursor.execute(sql, rid)
