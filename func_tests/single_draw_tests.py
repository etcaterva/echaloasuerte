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
        driver.find_element_by_id("coin-draw").click()
        driver.find_element_by_id("img-coin").click()
        driver.find_element_by_id("img-coin").click()
        results = driver.find_elements_by_class_name("result")
        self.assertEqual(2, len(results))

    def random_number_test(self):
        driver = self.driver
        driver.find_element_by_id("number-draw").click()
        driver.find_element_by_id("toss").click()
        driver.find_element_by_id("toss").click()
        results = driver.find_elements_by_class_name("result")
        self.assertEqual(2, len(results))

    def card_test(self):
        driver = self.driver
        driver.find_element_by_id("card-draw").click()
        driver.find_element_by_id("toss").click()
        driver.find_element_by_id("toss").click()
        results = driver.find_elements_by_class_name("result")
        self.assertEqual(2, len(results))

    def random_item_test(self):
        driver = self.driver
        driver.find_element_by_id("item-draw").click()
        driver.find_element_by_id("id_items-tokenfield").clear()
        driver.find_element_by_id("id_items-tokenfield").send_keys("1,2,3")
        driver.find_element_by_id("toss").click()
        results = driver.find_elements_by_class_name("result")
        self.assertEqual(1, len(results))

    def dice_test(self):
        driver = self.driver
        driver.find_element_by_id("dice-draw").click()
        driver.find_element_by_id("toss").click()
        results = driver.find_elements_by_class_name("result")
        self.assertEqual(1, len(results))

    def link_sets_test(self):
        driver = self.driver
        driver.find_element_by_id("link_sets-draw").click()
        driver.find_element_by_id("id_set_1-tokenfield").send_keys("1,2,3")
        driver.find_element_by_id("id_set_2-tokenfield").send_keys("a,b,c")
        driver.find_element_by_id("toss").click()
        results = driver.find_elements_by_class_name("result")
        self.assertEqual(1, len(results))

    def back_button_test(self):
        driver = self.driver
        driver.find_element_by_id("number-draw").click()
        driver.find_element_by_class_name("back-arrow").click()
        driver.find_element_by_id("number-draw")


