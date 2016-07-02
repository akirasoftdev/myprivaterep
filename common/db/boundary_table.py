# -*- coding: utf-8 -*-


class BoundaryTable(object):
    @classmethod
    def register(cls, cursor, town_id, x, y, boundary):
        sql = """
        INSERT into boundary
           (townId, pos, boundary)
        VALUES (
            %s,
            GeomFromText('POINT(%s %s)'),
            %s);
        """
        cursor.execute(sql, (town_id, float(x), float(y), boundary))
        return cursor.lastrowid