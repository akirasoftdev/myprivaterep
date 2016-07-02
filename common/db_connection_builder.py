# -*- coding: utf-8 -*-
import pymysql.cursors


class DbConnectionBuilder(object):

    @classmethod
    def build(cls, host_name, port_num):
        return pymysql.connect(host=host_name,
                               port=int(port_num),
                               user='iizuka',
                               password='ut43jjfjljsl',
                               db='fudosan',
                               charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)
