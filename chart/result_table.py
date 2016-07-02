# -*- coding: utf-8 -*-
import numpy

class ResultTable(object):
    @classmethod
    def register(cls, cursor, build_no, average, relative_error):
        sql = 'INSERT result SET '
        sql = sql + 'build_no=%s,'
        sql = sql + 'total_error_rate=%s,'
        sql = sql + 'error_rate_1=%s,'
        sql = sql + 'error_rate_2=%s,'
        sql = sql + 'error_rate_3=%s,'
        sql = sql + 'error_rate_4=%s,'
        sql = sql + 'error_rate_5=%s,'
        sql = sql + 'error_rate_6=%s,'
        sql = sql + 'error_rate_7=%s,'
        sql = sql + 'error_rate_8=%s,'
        sql = sql + 'error_rate_9=%s,'
        sql = sql + 'error_rate_10=%s,'
        sql = sql + 'error_rate_over=%s'
        cursor.execute(sql, (build_no, str(average),
                             str(relative_error[0]),
                             str(relative_error[1]),
                             str(relative_error[2]),
                             str(relative_error[3]),
                             str(relative_error[4]),
                             str(relative_error[5]),
                             str(relative_error[6]),
                             str(relative_error[7]),
                             str(relative_error[8]),
                             str(relative_error[9]),
                             str(relative_error[10])))
        return

    @classmethod
    def readAll(cls, cursor):
        sql = 'SELECT * from result order by build_no asc limit 20'
        cursor.execute(sql)
        row = cursor.fetchall()
        return row

    @classmethod
    def read(cls, cursor, build_no):
        sql = 'SELECT * from result where build_no = %s'
        cursor.execute(sql, (build_no))
        return cursor.fetchone()
