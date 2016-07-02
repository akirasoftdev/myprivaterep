# -*- coding: utf-8 -*-
import unittest

from test.db_util import DbUtil

from common.db import RailwayRoutesTable


class RailwayroutesTableTest(unittest.TestCase):
    def setUp(self):
        self.connection = DbUtil.connect()
        self.clearDb()

    def tearDown(self):
        self.clearDb()
        self.connection.close()

    def clearDb(self):
        with self.connection.cursor() as cursor:
            RailwayRoutesTable.clear_all(cursor)
        self.connection.commit()

    def test_clearAll(self):
        with self.connection.cursor() as cursor:
            RailwayRoutesTable.clear_all(cursor)
            num = RailwayRoutesTable.count(cursor)
            self.assertEqual(num, 0)

    def test_regsiterSucceeds(self):
        with self.connection.cursor() as cursor:
            # when:
            id = RailwayRoutesTable.register(cursor, "testRoute")

            # then:
            route = RailwayRoutesTable.get(cursor, id)
            self.assertEqual(route, 'testRoute')

            cursor.close()
        self.connection.commit()

    def test_regsiterSucceedsTwice(self):
        with self.connection.cursor() as cursor:
            # given:
            RailwayRoutesTable.register(cursor, "testRoute")

            # when:
            id_second = RailwayRoutesTable.register(cursor, "testRoute2")

            # then:
            name = RailwayRoutesTable.get(cursor, id_second)
            self.assertEqual(name, 'testRoute2')

            cursor.close()
        self.connection.commit()


if __name__ == '__main__':
    unittest.main()
