# -*- coding: utf-8 -*-
import unittest

from test.db_util import DbUtil

from common.db import PrefectureTable


class PrefectureTableTest(unittest.TestCase):
    def setUp(self):
        self.connection = DbUtil.connect()
        self.clearDb()

    def tearDown(self):
        self.clearDb()
        self.connection.close()

    def clearDb(self):
        with self.connection.cursor() as cursor:
            PrefectureTable.clear_all(cursor)
        self.connection.commit()

    def test_clearAll(self):
        with self.connection.cursor() as cursor:
            PrefectureTable.clear_all(cursor)
            num = PrefectureTable.count(cursor)
            self.assertEqual(num, 0)

    def test_regsiterSucceeds(self):
        with self.connection.cursor() as cursor:
            # when:
            id = PrefectureTable.register(cursor, 'prefecture')

            # then:
            route = PrefectureTable.get(cursor, id)
            self.assertEqual(route, 'prefecture')

            cursor.close()
        self.connection.commit()

    def test_regsiterSucceedsTwice(self):
        with self.connection.cursor() as cursor:
            # given:
            PrefectureTable.register(cursor, 'prefecture')

            # when:
            id_second = PrefectureTable.register(cursor, 'prefecture2')

            # then:
            name = PrefectureTable.get(cursor, id_second)
            self.assertEqual(name, 'prefecture2')

            cursor.close()
        self.connection.commit()


if __name__ == '__main__':
    unittest.main()
