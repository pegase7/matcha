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
        self.browser.get("http://www.python.org")
        self.assertIn("Python", self.browser.title)
        elem = self.browser.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in self.browser.page_source
        
        elem2 = self.browser.find_element_by_class_name('docs-meta')
        print('elem2', elem2, elem2.text)
        elem3 = self.browser.find_element_by_xpath("//input[@value='Search']")
        print('elem3', elem3)
        elem4 = self.browser.find_element_by_xpath("//button[@name='submit']")
        print('elem4', elem4)
        time.sleep(20)



    def tearDown(self):
        self.browser.close()

if __name__ == '__main__':
        unittest.main()



