# -*- coding: utf-8 -*-
import csv
import os
import re
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from page.prefecture_page import PrefecturePage
from common.webdriver_builder import WebDriverBuilder

urls = [
    ('tokyo', 'http://www.rosenka.nta.go.jp/main_h28/tokyo/tokyo/prices/city_frm.htm'),
    ('chiba', 'http://www.rosenka.nta.go.jp/main_h28/tokyo/chiba/prices/city_frm.htm'),
    ('kanagawa', 'http://www.rosenka.nta.go.jp/main_h28/tokyo/kanagawa/prices/city_frm.htm'),
    ('saitama', 'http://www.rosenka.nta.go.jp/main_h28/kanto/saitama/prices/city_frm.htm'),
]


def main():
    if os.path.exists('pdf_list.csv'):
        return
    chrome_path = sys.argv[3]
    driver = WebDriverBuilder.build(chrome_path)

    with open('pdf_list.csv', 'wb') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(['prefecture', 'city', 'town', 'pdf'])

        for p_name, url in urls:
            print(p_name)
            prefecture = PrefecturePage(driver, url)
            prefecture.do()
            data_list = prefecture.get()
            for data in data_list:
                base_url = re.compile('(.*)city_frm.htm$').search(url).group(1)
                pdf_url = base_url + 'pdf/' + data.town_id + ".pdf"
                writer.writerow([p_name, data.city_name.encode('utf-8'), data.town_name.encode('utf-8'), pdf_url])

    driver.quit()

if __name__ == '__main__':
    main()