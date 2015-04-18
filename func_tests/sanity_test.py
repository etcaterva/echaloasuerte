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

    def user_signup_test(self):
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

    def user_login_screen_test(self):
        self.user_signup_test()
        driver = self.driver
        driver.get(self.base_url + "/accounts/login/")
        driver.find_element_by_css_selector("#login #email").clear()
        driver.find_element_by_css_selector("#login #email").send_keys("test@test.com")
        driver.find_element_by_css_selector("#login #password").clear()
        driver.find_element_by_css_selector("#login #password").send_keys("test")
        driver.find_element_by_id("login-button").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profile-dropdown-link")))

    def user_logout_test(self):
        self.user_login_screen_test()
        driver = self.driver
        driver.find_element_by_css_selector("#account-dropdown > a.dropdown-toggle").click()
        driver.find_element_by_link_text("Sign out").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-dropdown-link")))


