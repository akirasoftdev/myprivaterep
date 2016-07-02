# -*- coding: utf-8 -*-
from telnetlib import EC

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

class Utils(object):
    @classmethod
    def scrollAndClick(cls, driver, xpath):
        try:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            e = driver.find_element_by_xpath(xpath)
            driver.execute_script('window.scrollTo(0,' + str(e.location['y'] - 30) + ')')
            e.click()
        except TimeoutException:
            print(xpath)

    @classmethod
    def scrll_and_click_by_element(cls, driver, e):
        driver.execute_script('window.scrollTo(0,' + str(e.location['y'] - 30) + ')')
        e.click()
