# -*- coding: utf-8 -*-
import unittest

from test.db_util import DbUtil

from common.db import StationTable


class StationTableTest(unittest.TestCase):
    def setUp(self):
        self.connection = DbUtil.connect()
        self.clearDb()

    def tearDown(self):
        self.clearDb()
        self.connection.close()

    def clearDb(self):
        with self.connection.cursor() as cursor:
            StationTable.clear_all(cursor)
        self.connection.commit()

    def test_clearAll(self):
        with self.connection.cursor() as cursor:
            StationTable.clear_all(cursor)
            num = StationTable.count(cursor)
            self.assertEqual(num, 0)

    def test_regsiterSucceeds(self):
        with self.connection.cursor() as cursor:
            # when:
            id = StationTable.register(cursor, "testStation", 1)

            # then:
            route = StationTable.get(cursor, id)
            self.assertEqual(route, 'testStation')

            cursor.close()
        self.connection.commit()

    def test_regsiterSucceedsTwice(self):
        with self.connection.cursor() as cursor:
            # given:
            StationTable.register(cursor, "testStation", 1)

            # when:
            id_second = StationTable.register(cursor, "testStation2", 1)

            # then:
            name = StationTable.get(cursor, id_second)
            self.assertEqual(name, 'testStation2')

            cursor.close()
        self.connection.commit()


if __name__ == '__main__':
    unittest.main()
