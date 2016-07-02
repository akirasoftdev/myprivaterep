# -*- coding: utf-8 -*-
import pymysql.cursors


class DbUtil(object):
    @classmethod
    def connect(cls):
        return pymysql.connect(host='localhost',
                               user='iizuka',
                               password='wUpo3j$lfdf',
                               db='house',
                               charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)
