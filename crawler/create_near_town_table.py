# -*- coding: utf-8 -*-
from common.db_connection_builder import DbConnectionBuilder

def find_town_id_list(cursor):
    sql = '''
    SELECT id FROM town
    '''
    cursor.execute(sql)
    return cursor.fetchall()


def query_partial(cursor, town_id):
    sql = '''
    SELECT
        s1.townId, s2.townId, GLENGTH(
            GEOMFROMTEXT(CONCAT('LineString(', X(s1.pos), ' ', Y(s1.pos), ",", X(s2.pos), ' ', Y(s2.pos), ')')))
        AS distance
    FROM
        (SELECT * FROM boundary WHERE townId = %(town_id)s) AS s1
    INNER JOIN boundary s2
    GROUP BY s1.townId, s2.townId
    HAVING distance = MIN(distance) AND distance < 0.0089831601679492 AND s1.townId <> s2.townId;
    '''
    cursor.execute(sql, {'town_id':town_id})
    return cursor.fetchall()


def insert_near_town(cursor, town_id, near_town_id, distance):
    sql = '''
    INSERT INTO near_town
    (townId, nearTownId, distance)
    VALUES (%(town_id)s, %(near_town_id)s, %(distance)s)
    '''
    cursor.execute(sql, {'town_id': town_id, 'near_town_id': near_town_id, 'distance': distance})


def main():
    connection = DbConnectionBuilder.build('127.0.0.1', 3306)
    town_id_list = find_town_id_list(connection.cursor())
    for town_id in town_id_list:
        near_town_list = query_partial(connection.cursor(), town_id['id'])
        print(near_town_list)
        for near_town in near_town_list:
            insert_near_town(connection.cursor(), near_town['townId'], near_town['s2.townId'], near_town['distance'])
    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()