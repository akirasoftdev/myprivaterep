# -*- coding: utf-8 -*-
import datetime
import unittest

from test.db_util import DbUtil

from common.db import BukkenTable


class BukkenTableTest(unittest.TestCase):
    def setUp(self):
        self.connection = DbUtil.connect()
        self.clearDb()

    def tearDown(self):
        self.clearDb()
        self.connection.close()

    def clearDb(self):
        with self.connection.cursor() as cursor:
            BukkenTable.clear_all(cursor)
        self.connection.commit()

    def test_clearAll(self):
        with self.connection.cursor() as cursor:
            BukkenTable.clear_all(cursor)
            num = BukkenTable.count(cursor)
            self.assertEqual(num, 0)

    def test_regsiterSucceeds(self):
        with self.connection.cursor() as cursor:
            # when:
            id = BukkenTable.register(cursor, 'http://test.com', 'title')

            # then:
            row = BukkenTable.get(cursor, id)
            self.assertEqual(row['url'], 'http://test.com')

            cursor.close()
        self.connection.commit()

    def test_regsiterSucceedsTwice(self):
        with self.connection.cursor() as cursor:
            # given:
            BukkenTable.register(cursor, 'http://test.com', 'title')

            # when:
            id_second = BukkenTable.register(cursor, 'http://test2.com', 'title2')

            # then:
            row = BukkenTable.get(cursor, id_second)
            self.assertEqual(row['url'], 'http://test2.com')

            cursor.close()
        self.connection.commit()

    def test_updateAddress(self):
        with self.connection.cursor() as cursor:
            # given:
            id = BukkenTable.register(cursor, 'http://test.com', 'title')
            # when
            BukkenTable.update_address(cursor, id, 'address', 2, 3)
            # then
            row = BukkenTable.get(cursor, id)
            self.assertEqual(row['address'], 'address')
            self.assertEqual(row['prefectureId'], 2)
            self.assertEqual(row['cityId'], 3)

    def test_updateLandArea(self):
        with self.connection.cursor() as cursor:
            # given:
            id = BukkenTable.register(cursor, 'http://test.com', 'title')
            # when
            BukkenTable.update_landarea(cursor, id, 0.1)
            # then
            row = BukkenTable.get(cursor, id)
            self.assertEqual(row['landArea'], 0.1)

    def test_updateBuildingArea(self):
        with self.connection.cursor() as cursor:
            # given:
            id = BukkenTable.register(cursor, 'http://test.com', 'title')
            # when
            BukkenTable.update_buildingarea(cursor, id, 0.1)
            # then
            row = BukkenTable.get(cursor, id)
            self.assertEqual(row['buildingArea'], 0.1)

    def test_updateLayout(self):
        with self.connection.cursor() as cursor:
            # given:
            id = BukkenTable.register(cursor, 'http://test.com', 'title')
            # when
            BukkenTable.update_layout(cursor, id, '3LDK');
            # then
            row = BukkenTable.get(cursor, id)
            self.assertEqual(row['layout'], '3LDK')

    def test_updateBuildingYear(self):
        with self.connection.cursor() as cursor:
            # given:
            id = BukkenTable.register(cursor, 'http://test.com', 'title')
            # when
            BukkenTable.update_buildingyear(cursor, id, datetime.datetime.strptime('1970-08', '%Y-%m'))
            # then
            row = BukkenTable.get(cursor, id)
            self.assertEqual(row['year'].year, 1970)
            self.assertEqual(row['year'].month, 8)


if __name__ == '__main__':
    unittest.main()
