# -*- coding: utf-8 -*-
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class PrefecturePage(object):
    @classmethod
    def check_param_and_open_summay(cls, url, driver, madori, area_array):
        driver.get(url)
        try:
            for area in area_array:
                cls.scroll_and_click(driver, area)
            ''' 築年数30年以内'''
            cls.scroll_and_click(driver, '//*[@id="search-area"]/div/div[5]/table/tbody/tr[6]/td/ul/li[9]/label/input')
            ''' 土地所有権 '''
            cls.scroll_and_click(driver, '//*[@id="search-options"]/div/table/tbody/tr[8]/td/ul/li[7]/label/input')
            ''' 間取 1R'''
            cls.scroll_and_click(driver, '//*[@id="search-area"]/div/div[5]/table/tbody/tr[2]/td/ul/li[%d]/label/input' % madori)

            cls.scroll_and_click(driver, '//*[@id="search-area"]/div/div[3]/div/div/p/a/img')

        except TimeoutException:
            print("Timeout Error")

    @classmethod
    def scroll_and_click(cls, driver, xpath):
        try:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            e = driver.find_element_by_xpath(xpath)
            driver.execute_script('window.scrollTo(0,' + str(e.location['y'] - 30) + ')')
            e.click()
        except TimeoutException:
            print(xpath)

