# -*- coding: utf-8 -*-
from .selenium_base import SeleniumTest
import time

class SanityWebapp(SeleniumTest):
    """ Basic sanity test for the web app"""

    def setUp(self):
        super(SanityWebapp,self).setUp()

    def tearDown(self):
        super(SanityWebapp,self).tearDown()

    def test_sanity(self):
        pass

    def coin_test(self):
        driver = self.driver
        driver.find_element_by_css_selector("div.draw-box-title.text-center").click()
        driver.find_element_by_id("img-coin").click()
        driver.find_element_by_id("img-coin").click()
        driver.find_element_by_id("ui-id-1").click()
        driver.find_element_by_id("ui-id-3").click()
    def random_number_test(self):
        driver = self.driver
        driver.find_element_by_xpath("//div[@id='content']/div[2]/div[2]/a/div/div").click()
        driver.find_element_by_name("toss").click()
        driver.find_element_by_name("toss").click()
        driver.find_element_by_id("ui-id-1").click()
        driver.find_element_by_id("ui-id-3").click()

    def card_test(self):
        driver = self.driver
        driver.find_element_by_xpath("//div[@id='content']/div[2]/div/a[2]/div/div").click()
        driver.find_element_by_name("toss").click()
        driver.find_element_by_name("toss").click()
        driver.find_element_by_id("ui-id-1").click()
        driver.find_element_by_id("ui-id-3").click()

    def random_item_test(self):
        driver = self.driver
        driver.find_element_by_xpath("//div[@id='content']/div[2]/div[2]/a[2]/div/div").click()
        driver.find_element_by_id("id_items-tokenfield").clear()
        driver.find_element_by_id("id_items-tokenfield").send_keys("1,2,3")
        driver.find_element_by_name("toss").click()
        driver.find_element_by_id("ui-id-1").click()

    def dice_test(self):
        driver = self.driver
        driver.find_element_by_xpath("//div[@id='content']/div[2]/div/a[3]/div/div").click()
        driver.find_element_by_name("toss").click()
        driver.find_element_by_id("ui-id-1").click()

    def link_sets_test(self):
        driver = self.driver
        driver.find_element_by_xpath("//div[@id='content']/div[2]/div[2]/a[3]/div").click()
        driver.find_element_by_id("id_set_1-tokenfield").send_keys("1,2,3")
        driver.find_element_by_id("id_set_2-tokenfield").send_keys("a,b,c")
        driver.find_element_by_name("toss").click()
        driver.find_element_by_id("ui-id-1").click()
        driver.find_element_by_id("ui-id-1").click()


