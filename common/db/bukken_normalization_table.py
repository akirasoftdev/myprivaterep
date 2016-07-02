# -*- coding: utf-8 -*-


class BukkenNormalizationTable(object):
    @classmethod
    def find(cls, cursor, n_year, n_occupied, n_walk_time, n_rosen_price):
        sql = '''
        SELECT
            A.bukkenId AS bukkenId,
            B.townId AS townId,
            B.year AS year,
            B.occupiedArea AS occupiedArea,
            B.walkTime AS walkTime,
            B.price AS price,
            (pow(A.year - %(n_year)s, 2) +
            pow(A.occupiedArea - %(n_occupied)s, 2) +
            pow(A.walkTime - %(n_walk_time)s, 2) +
            pow(A.rosenPrice - %(n_rosen_price)s, 2)) AS DIFF
        FROM
            bukken_normalization AS A
        LEFT JOIN
            bukken AS B ON A.bukkenId = B.id
        ORDER BY DIFF ASC
        LIMIT 100
        '''
        params = {
            'n_year': n_year,
            'n_occupied': n_occupied,
            'n_walk_time': n_walk_time,
            'n_rosen_price': n_rosen_price
        }
        cursor.execute(sql, params)
        return cursor.fetchall()
