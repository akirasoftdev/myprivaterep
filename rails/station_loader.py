# -*- coding: utf-8 -*-
import re
import sys

from pymysql import IntegrityError
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from common.db_connection_builder import DbConnectionBuilder
from common.webdriver_builder import WebDriverBuilder

TOKYO_URL='http://transit.yahoo.co.jp/station/list?pref=13&prefname=%E6%9D%B1%E4%BA%AC&done=sta'
KANAGAWA_URL='http://transit.yahoo.co.jp/station/list?pref=14&prefname=%E7%A5%9E%E5%A5%88%E5%B7%9D&done=sta'
SAITAMA_URL='http://transit.yahoo.co.jp/station/list?pref=11&prefname=%E5%9F%BC%E7%8E%89&done=sta'
CHIBA_URL='http://transit.yahoo.co.jp/station/list?pref=12&prefname=%E5%8D%83%E8%91%89&done=sta'
URLS = [TOKYO_URL, KANAGAWA_URL, SAITAMA_URL, CHIBA_URL]

class StationLoader:
    def __init__(self, driver, connection):
        self._driver = driver
        self._connection = connection

    def run(self):
        for url in URLS:
            print(url)
            self._driver.get(url)
            self.read_lines()

    def register_station(self, yahoo_id, name, line, organization):
        sql = """
        INSERT INTO
            yahoo_station
            (yahoo_id, name, line, organization)
        VALUES
            (%s, %s, %s, %s)
        """
        cursor = self._connection.cursor()
        cursor.execute(sql, (yahoo_id, name, line, organization))
        return cursor.rowcount

    def read_stations(self, line_name, organization):
        xpath = '//*[@id="mdSearchSta"]/ul/li[1]/a'
        WebDriverWait(self._driver, 60).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        xpath = '//*[@id="mdSearchSta"]/ul/li[*]/a'
        station_elements = self._driver.find_elements_by_xpath(xpath)
        for station_element in station_elements:
            station_id = self.extract_station_id_from_href(station_element.get_attribute('href'))
            try:
                self.register_station(station_id, station_element.text, line_name, organization)
            except IntegrityError as e:
                if e.args[0] == 1062:
                    continue
                raise

    def extract_station_id_from_href(self, href):
        m = re.compile('/station/top/(\d+)/.*').search(href)
        if m is not None:
            return int(m.group(1))
        raise Exception(href)

    def read_lines(self):
        xpath = '//*[@id="mdSearchLine"]/ul/li[1]'
        WebDriverWait(self._driver, 60).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        xpath = '//*[@id="mdSearchLine"]/ul/li[*]/dl/dd/ul/li[*]/a'
        line_elements = self._driver.find_elements_by_xpath(xpath)
        lines = []
        for line_element in line_elements:
            organization = line_element.find_element_by_xpath('ancestor::li[*]/dl/dt').text
            lines.append({
                'organization': organization,
                'name': line_element.text,
                'href': line_element.get_attribute('href')
            })
        for line in lines:
            print(line['name'])
            self._driver.get(line['href'])
            self.read_stations(line['name'], line['organization'])

def main():
    host_name = sys.argv[1]
    port_no = sys.argv[2]
    driver_path = sys.argv[3]

    try:
        connection = DbConnectionBuilder.build(host_name, port_no)
        driver = WebDriverBuilder.build(driver_path)
        station = StationLoader(driver, connection)
        station.run()
        connection.commit()
        connection.close()

    finally:
#        driver.quit()
        pass

if __name__ == "__main__":
    main()
