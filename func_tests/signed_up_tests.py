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

        self.driver_signed_in = webdriver.Firefox()
        self.driver_signed_in.set_window_size(1366, 768)

        #if something is not found give it 3 seconds to load
        self.driver_signed_in.implicitly_wait(3)

        # Sign up in one of the browsers
        driver_signed_in = self.driver_signed_in
        driver_signed_in.get(self.base_url + "/accounts/login/")
        driver_signed_in.find_element_by_css_selector("#login #email").clear()
        driver_signed_in.find_element_by_css_selector("#login #email").send_keys("test@test.com")
        driver_signed_in.find_element_by_css_selector("#login #password").clear()
        driver_signed_in.find_element_by_css_selector("#login #password").send_keys("test")
        driver_signed_in.find_element_by_css_selector("#login #login-button").click()

    def tearDown(self):
        super(SanityWebapp,self).tearDown()

        self.driver_signed_in.quit()

    def favourites_test(self):
        """
        - Add a title to a draw
        - Store it in favorites
        - Is dynamically added by JS
        - Access to it through the favourites sections from the home screen (so it's added to the DB)
        - Remove the draw from favorites
        - Remove it dynamically with JS
        - Check from the home screen that it's not anymore in the favourites section
        """
        draw_title = "Testing favourites"
        driver_signed_in = self.driver_signed_in
        driver_signed_in.find_element_by_css_selector("#card-draw").click()

        # Change the name of the draw
        driver_signed_in.find_element_by_name("title").clear()
        driver_signed_in.find_element_by_name("title").send_keys(draw_title)

        # Toss
        driver_signed_in.find_element_by_id("toss").click()

        # Add to favourites
        driver_signed_in.find_element_by_id("fav-button").click()
        driver_signed_in.find_element_by_id("favourites").click()
        draw_id = driver_signed_in.find_element_by_id("id__id").get_attribute('value')

        # Check that it has been dynamically added
        link = driver_signed_in.find_element_by_xpath("//*[@id='favourites-panel']//a[contains(@href,'" + draw_id + "')]")
        link.click()

        # Check that is correctly stored in the DB
        driver_signed_in.get(self.base_url + "/")
        driver_signed_in.find_element_by_id("favourites").click()
        driver_signed_in.find_element_by_xpath("//*[@id='favourites-panel']//a[contains(@href,'" + draw_id + "')]").click()
        same_name = draw_title == driver_signed_in.find_element_by_name("title").get_attribute("value")
        self.assertTrue(same_name)

        # Remove from favourites
        driver_signed_in.find_element_by_id("fav-button").click()

        # Check that it has been dynamically removed
        is_present = self.is_element_present("xpath", "//*[@id='favourites-panel']//a[contains(@href,'" + draw_id + "')]")
        self.assertFalse(is_present)

        # Check that is correctly removed from the DB
        driver_signed_in.get(self.base_url + "/")
        driver_signed_in.find_element_by_id("favourites").click()
        is_present = self.is_element_present("xpath", "//*[@id='favourites-panel']//a[contains(@href,'" + draw_id + "')]")
        self.assertFalse(is_present)

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
        driver_signed_in.find_element_by_id("publish").click()
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

    @skip("Promps can not be tested so far by selenium in python")
    def public_draw_password_test(self):
        """
        - Create a public draw (Privacy: password protected)
        - Setting a custom title
        - The draw is in the list "Recently created"
        - The draw can be accessed by non-register users by using the password
        - Only the owner can toss
        """
        driver_signed_in = self.driver_signed_in
        driver = self.driver
        driver_signed_in.find_element_by_id("public-draw").click()
        driver_signed_in.find_element_by_css_selector("#public-draw-dropdown .public-draw-create").click()
        driver_signed_in.find_element_by_css_selector("#dice-draw").click()
        driver_signed_in.find_element_by_name("title").clear()
        driver_signed_in.find_element_by_name("title").send_keys("Public draw test")
        driver_signed_in.find_element_by_id("next").click()
        driver_signed_in.find_element_by_id("public-mode-selected").click()
        time.sleep(1)
        driver_signed_in.find_element_by_css_selector("div.slider-tick.position-2").click()
        driver_signed_in.find_element_by_id("draw-password").clear()
        driver_signed_in.find_element_by_id("draw-password").send_keys("123456")
        driver_signed_in.find_element_by_id("save-change-privacy").click()
        driver_signed_in.find_element_by_id("publish").click()
        draw_id = driver_signed_in.find_element_by_id("id__id").get_attribute('value')
        driver_signed_in.find_element_by_id("toss").click()

        # Access the draw using the password
        driver.find_element_by_id("public-draw").click()
        driver.find_element_by_css_selector("#public-draw-dropdown .public-draw-join").click()
        driver.find_element_by_xpath("//tr[@data-draw_id='{0}']".format(draw_id)).click()

        #  password should be introduced here (and test that the title has been changed)

        # Check the spectator can not toss
        toss_status = driver.find_element_by_id("toss").get_attribute('disabled')
        self.assertNotEqual("disabled", toss_status)

        # Check the spectator can see the result
        results = driver.find_elements_by_class_name("result")
        self.assertEqual(1, len(results))

    def public_draw_invite_test(self):
        """
        - Create a public draw (Privacy: only invited)
        - The draw is in the list "Recently created"
        - The draw can be accessed by invited users
        - Only the owner can toss
        """
        # Create guest user
        self.remove_user("test_guest@test.com")
        self.test_user = User(
            'test_guest@test.com',
        )
        self.test_user.set_password("test")
        self.db.create_user(self.test_user)

        # Guest signs in
        driver = self.driver
        driver.get(self.base_url + "/accounts/login/")
        driver.find_element_by_css_selector("#login #email").clear()
        driver.find_element_by_css_selector("#login #email").send_keys("test_guest@test.com")
        driver.find_element_by_css_selector("#login #password").clear()
        driver.find_element_by_css_selector("#login #password").send_keys("test")
        driver.find_element_by_css_selector("#login #login-button").click()

        driver_signed_in = self.driver_signed_in
        driver_signed_in.find_element_by_id("public-draw").click()
        driver_signed_in.find_element_by_css_selector("#public-draw-dropdown .public-draw-create").click()
        driver_signed_in.find_element_by_css_selector("#dice-draw").click()
        driver_signed_in.find_element_by_name("title").clear()
        driver_signed_in.find_element_by_name("title").send_keys("Public draw test")
        driver_signed_in.find_element_by_id("next").click()
        driver_signed_in.find_element_by_id("public-mode-selected").click()
        time.sleep(1)
        driver_signed_in.find_element_by_css_selector("div.slider-tick.position-3").click()
        driver_signed_in.find_element_by_id("save-change-privacy").click()

        driver_signed_in.find_element_by_id("invite-emails-tokenfield").send_keys("test_guest@test.com")
        driver_signed_in.find_element_by_id("publish").click()
        draw_id = driver_signed_in.find_element_by_id("id__id").get_attribute('value')
        driver_signed_in.find_element_by_id("toss").click()

        driver.get(self.base_url + "/draw/dice/" + draw_id)

        # Check the spectator can not toss
        toss_status = driver.find_element_by_id("toss").get_attribute('disabled')
        self.assertNotEqual("disabled", toss_status)

        # Check the spectator can see the result
        results = driver.find_elements_by_class_name("result")
        self.assertEqual(1, len(results))
