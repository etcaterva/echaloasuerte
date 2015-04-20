# -*- coding: utf-8 -*-
from .selenium_base import SeleniumTest
from selenium import webdriver
import time

class SanityWebapp(SeleniumTest):
    """ Basic sanity test for the web app"""

    def setUp(self):
        super(SanityWebapp,self).setUp()

        self.driver_signed_in = webdriver.Firefox()
        self.driver_signed_in.set_window_size(1366, 768)

        # Sign up in one of the browsers
        driver_signed_in = self.driver_signed_in
        driver_signed_in.get(self.base_url + "/accounts/login/")
        driver_signed_in.find_element_by_css_selector("#login #email").clear()
        driver_signed_in.find_element_by_css_selector("#login #email").send_keys("test@test.com")
        driver_signed_in.find_element_by_css_selector("#login #password").clear()
        driver_signed_in.find_element_by_css_selector("#login #password").send_keys("test")
        driver_signed_in.find_element_by_id("login-button").click()

    def tearDown(self):
        super(SanityWebapp,self).tearDown()

        self.driver_signed_in.quit()

    def public_draw_everyone_test(self):
        """
        - Create a public draw (Privacy: everyone)
        - The draw is in the list "Recently created"
        - The draw can be accessed by non-register users
        - Only the owner can toss
        """
        driver_signed_in = self.driver_signed_in
        driver = self.driver
        driver_signed_in.find_element_by_id("public-draw").click()
        driver_signed_in.find_element_by_css_selector("#public-draw-dropdown .public-draw-create").click()
        driver_signed_in.find_element_by_css_selector("#card-draw").click()
        driver_signed_in.find_element_by_id("next").click()
        driver_signed_in.find_element_by_name("next").click()
        draw_id = driver_signed_in.find_element_by_id("id__id").get_attribute('value')
        driver_signed_in.find_element_by_id("toss").click()

        driver.find_element_by_id("public-draw").click()
        driver.find_element_by_css_selector("#public-draw-dropdown .public-draw-join").click()
        driver.find_element_by_xpath("//tr[@data-draw_id='{0}']".format(draw_id)).click()

        # Check the spectator can not toss
        toss_status = driver.find_element_by_id("toss").get_attribute('disabled')
        self.assertNotEqual("disabled", toss_status)

        # Check the spectator can see the result
        results = driver.find_elements_by_class_name("result")
        self.assertEqual(1, len(results))
