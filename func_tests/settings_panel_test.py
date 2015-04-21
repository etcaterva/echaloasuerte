# -*- coding: utf-8 -*-
from unittest import skip
from .selenium_base import SeleniumTest
from selenium import webdriver
import time
from server.bom.user import User

class SanityWebapp(SeleniumTest):
    """ Basic sanity test for the web app"""

    def setUp(self):
        super(SanityWebapp,self).setUp()

        # Sign up as owner
        driver = self.driver
        driver.get(self.base_url + "/accounts/login/")
        driver.find_element_by_css_selector("#login #email").clear()
        driver.find_element_by_css_selector("#login #email").send_keys("test@test.com")
        driver.find_element_by_css_selector("#login #password").clear()
        driver.find_element_by_css_selector("#login #password").send_keys("test")
        driver.find_element_by_css_selector("#login #login-button").click()

        # Create a public draw
        driver.find_element_by_id("public-draw").click()
        driver.find_element_by_css_selector("#public-draw-dropdown .public-draw-create").click()
        driver.find_element_by_css_selector("#card-draw").click()
        driver.find_element_by_id("next").click()
        driver.find_element_by_id("publish").click()
        self.draw_id = driver.find_element_by_id("id__id").get_attribute('value')

    def tearDown(self):
        super(SanityWebapp, self).tearDown()

        self.driver.quit()

    def update_privacy_to_password_test(self):
        password = "123456"
        driver = self.driver

        # Check that by default the draw is open to everyone
        draw = self.db.retrieve_draw(self.draw_id)
        self.assertEqual("Public", draw.shared_type)
        self.assertEqual("", draw.password)

        # Change privacy to password protected
        driver.find_element_by_id("public-draw-options").click()
        time.sleep(1)
        driver.find_element_by_id("privacy").click()
        driver.find_element_by_css_selector("div.slider-tick.position-2").click()
        driver.find_element_by_id("draw-password").clear()
        driver.find_element_by_id("draw-password").send_keys(password)
        driver.find_element_by_id("save-change-privacy").click()
        driver.find_element_by_css_selector("#settings-privacy button.close").click()
        time.sleep(1)

        # Check that the configuration has changed
        draw = self.db.retrieve_draw(self.draw_id)
        self.assertEqual("Public", draw.shared_type)
        self.assertEqual(password, draw.password)

        # Change privacy to only with invitation
        driver.find_element_by_id("public-draw-options").click()
        time.sleep(1)
        driver.find_element_by_id("privacy").click()
        driver.find_element_by_css_selector("div.slider-tick.position-3").click()
        driver.find_element_by_id("save-change-privacy").click()
        driver.find_element_by_css_selector("#settings-privacy button.close").click()

        # Check that the configuration has changed
        draw = self.db.retrieve_draw(self.draw_id)
        self.assertEqual("Invite", draw.shared_type)
        self.assertEqual("", draw.password)
        pass