#Tested in python3
#To run on OSX:
#
#
# brew install python
# pip3 install selenium
#
# 
# To run:
# python3 simpletest.py
#

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pathlib import Path


class WebDriverPythonBasics(unittest.TestCase):

    def setUp(self):
        driverpath = Path(__file__).parent.parent.parent
        if 'src' == driverpath.name:
            driverpath = driverpath.parent
        driverpath = driverpath.joinpath('resources/driver/chromedriver')
        self.browser = webdriver.Chrome(str(driverpath))



    def test_saucelabs_homepage_header_displayed(self):
        self.browser.get("http://localhost:5000/")
        element = self.browser.find_element_by_name("login");
        element.send_keys("Duck")
        element = self.browser.find_element_by_name("password");
        element.send_keys("PasseMot0")
        element.send_keys(Keys.RETURN)
        
        assert "No results found." not in self.browser.page_source

        mesPhotosElem = self.browser.find_element_by_id('MesPhotos')
        time.sleep(5)
        mesPhotosElem.send_keys(Keys.RETURN)

        # assert "No results found." not in self.browser.page_source
        # time.sleep(2)

        # self.assertTrue(element.is_displayed());
        # element.click();
        # pricing_link = self.browser.find_element(By.XPATH, '//a[text()="Pricing"]');
        # self.assertTrue(pricing_link.is_displayed());
        # pricing_link.click();
        time.sleep(20)



    def tearDown(self):
        self.browser.close()

if __name__ == '__main__':
        unittest.main()



