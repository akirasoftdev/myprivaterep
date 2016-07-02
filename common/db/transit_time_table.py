# -*- coding: utf-8 -*-


class TransitTimeTable(object):
    @classmethod
    def register(cls, cursor, src_id, dst_id, time):
        sql = """
        INSERT transit_time
        SET
            src_id = %s, dst_id = %s, time = %s
        """
        cursor.execute(sql, (src_id, dst_id, time))
        return cursor.lastrowid

    @classmethod
    def get(cls, cursor, src_id, dst_id):
        sql = """
        SELECT * FROM transit_time
        WHERE src_id = %s AND dst_id = %s
        """
        cursor.execute(sql, (src_id, dst_id))
        return cursor.fetchone()