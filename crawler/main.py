# -*- coding: utf-8 -*-
import sys

from bukken_summary_routine import BukkenSummaryRoutine
from common.db_connection_builder import DbConnectionBuilder
from common.webdriver_builder import WebDriverBuilder
from context import Context
from madori_routine import MaroriRoutine
from prefecture_routine import PrefectureRoutine


def bukken_summary_callback(context, prefectureId):
    BukkenSummaryRoutine.do(context, prefectureId)


def prefectures_callback(context, prefecture_id, url, area):
    MaroriRoutine.do(context, prefecture_id, url, area, bukken_summary_callback)


def main():
    host_name = sys.argv[1]
    port_no = sys.argv[2]
    driver_path = sys.argv[3]
    context = Context();
    context.load()
    context.connection = DbConnectionBuilder.build(host_name, port_no)
    context.driver = WebDriverBuilder.build(driver_path)

    PrefectureRoutine.do(context, prefectures_callback)

    context.connection.close()
    context.driver.quit()
    context.clear_condition().save()

if __name__ == "__main__":
    main()
