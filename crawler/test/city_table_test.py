# -*- coding: utf-8 -*-
import unittest

from test.db_util import DbUtil

from common.db import CityTable


class CityTableTest(unittest.TestCase):
    def setUp(self):
        self.connection = DbUtil.connect()
        self.clearDb()

    def tearDown(self):
        self.clearDb()
        self.connection.close()

    def clearDb(self):
        with self.connection.cursor() as cursor:
            CityTable.delete_all(cursor)
        self.connection.commit()

    def test_clearAll(self):
        with self.connection.cursor() as cursor:
            CityTable.delete_all(cursor)
            num = CityTable.count(cursor)
            self.assertEqual(num, 0)

    def test_regsiterSucceeds(self):
        with self.connection.cursor() as cursor:
            # when:
            id = CityTable.register(cursor, 'city', 1)

            # then:
            route = CityTable.get_name(cursor, id)
            self.assertEqual(route, 'city')

            cursor.close()
        self.connection.commit()

    def test_regsiterSucceedsTwice(self):
        with self.connection.cursor() as cursor:
            # given:
            CityTable.register(cursor, 'city', 1)

            # when:
            id_second = CityTable.register(cursor, 'city2', 1)

            # then:
            name = CityTable.get_name(cursor, id_second)
            self.assertEqual(name, 'city2')

            cursor.close()
        self.connection.commit()


if __name__ == '__main__':
    unittest.main()
