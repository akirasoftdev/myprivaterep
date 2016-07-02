# -*- coding: utf-8 -*-
import sys

from common.db_connection_builder import DbConnectionBuilder
from common.webdriver_builder import WebDriverBuilder
from rails.yahoo import YahooTransit


def read_stations(connection):
    sql = """
    SELECT * FROM yahoo_station group by id order by id
    """
    cursor = connection.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def read_transit_time(connection):
    sql = """
    SELECT src_id, dst_id FROM transit_time
    """
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    aa = set()
    for row in rows:
        aa.add((row['src_id'], row['dst_id']))
    return aa


def main():
    host_name = sys.argv[1]
    port_no = sys.argv[2]
    driver_path = sys.argv[3]

    try:
        connection = DbConnectionBuilder.build(host_name, port_no)
        stations = read_stations(connection)
        exclude_patterns = read_transit_time(connection)

        driver = WebDriverBuilder.build(driver_path)
        yahoo = YahooTransit(driver)
        yahoo.run(stations, exclude_patterns, connection)

        connection.close()

    finally:
#        driver.quit()
        pass



if __name__ == "__main__":
    main()
