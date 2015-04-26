# -*- coding: utf-8 -*-
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from .selenium_base import SeleniumTest
from selenium.webdriver.common.action_chains import ActionChains
import time

class SanityWebapp(SeleniumTest):
    """ Basic sanity test for the web app"""

    def setUp(self):
        super(SanityWebapp,self).setUp()

    def tearDown(self):
        super(SanityWebapp,self).tearDown()

    def test_sanity(self):
        pass

    def test_change_language(self):
        driver = self.driver

        #TODO
        #driver.find_element_by_css_selector("span.fa.fa-flag").click()
        #driver.find_element_by_link_text(u"español (es)").click()
        #driver.find_element_by_id("change_language_but").click()
        #driver.find_element_by_css_selector("span.fa.fa-flag").click()
        #driver.find_element_by_link_text("English (en)").click()
        #driver.find_element_by_id("change_language_but").click()

        #driver.find_element_by_link_text("About us").click()

    def about_test(self):
        driver = self.driver
        driver.get(self.base_url + "/about.html")
        driver.find_element_by_class_name("team-member")

    def draw_tooltip_test(self):
        driver = self.driver
        # Check if it the help icon is visible when hovering
        draw = driver.find_element_by_id("number-draw")
        help_icon = driver.find_element_by_css_selector("#number-draw .fa-question")

        # Check if it has a title to show in the tooltip
        tooltip = help_icon.get_attribute("title")
        self.assertIsNotNone(tooltip)
        self.assertNotEqual("", tooltip)

        # Check if the tooltip is rendered
        ActionChains(driver).move_to_element(draw).perform()
        ActionChains(driver).move_to_element(help_icon).perform()
        driver.find_element_by_css_selector(".ui-tooltip")

    def user_sign_up_test(self):
        self.remove_user("test2@test.com")
        self.assertRaises(Exception, lambda: self.db.retrieve_user("test2@test.com"))

        driver = self.driver
        driver.find_element_by_css_selector("#account-dropdown > a.dropdown-toggle").click()
        driver.find_element_by_css_selector("#account-dropdown #sign-up-link").click()
        driver.find_element_by_css_selector("div.controls.col-xs-8 > #email").clear()
        driver.find_element_by_css_selector("div.controls.col-xs-8 > #email").send_keys("test2@test.com")
        driver.find_element_by_css_selector("div.controls.col-xs-8 > #password").clear()
        driver.find_element_by_css_selector("div.controls.col-xs-8 > #password").send_keys("test")
        driver.find_element_by_id("register-button").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profile-dropdown-link")))

    def user_sign_in_from_dropdown_test(self):
        driver = self.driver
        driver.find_element_by_css_selector("#account-dropdown > a.dropdown-toggle").click()
        driver.find_element_by_css_selector("#account-dropdown #email").clear()
        driver.find_element_by_css_selector("#account-dropdown #email").send_keys("test@test.com")
        driver.find_element_by_css_selector("#account-dropdown #password").clear()
        driver.find_element_by_css_selector("#account-dropdown #password").send_keys("test")
        driver.find_element_by_css_selector("#account-dropdown #login-button").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profile-dropdown-link")))

    def user_sign_in_screen_test(self):
        driver = self.driver
        driver.get(self.base_url + "/accounts/login/")
        driver.find_element_by_css_selector("#login #email").clear()
        driver.find_element_by_css_selector("#login #email").send_keys("test@test.com")
        driver.find_element_by_css_selector("#login #password").clear()
        driver.find_element_by_css_selector("#login #password").send_keys("test")
        driver.find_element_by_css_selector("#login #login-button").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profile-dropdown-link")))

    def user_sign_out_from_dropdown_test(self):
        self.user_sign_in_screen_test()
        driver = self.driver
        driver.find_element_by_css_selector("#account-dropdown > a.dropdown-toggle").click()
        driver.find_element_by_css_selector("#account-dropdown #sign-out").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-dropdown-link")))

    def user_sign_out_from_profile_test(self):
        self.user_sign_in_screen_test()
        driver = self.driver
        driver.get(self.base_url + "/accounts/profile/")
        driver.find_element_by_css_selector("#content #sign-out").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-dropdown-link")))