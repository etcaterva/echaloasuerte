import os
import sys
import django

from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
import time
from server.mongodb.driver import MongoDriver
from server.bom.user import User

from sauceclient import SauceClient

USERNAME = os.environ.get('SAUCE_USERNAME')
ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY')
sauce = SauceClient(USERNAME, ACCESS_KEY)

browsers = [
    {"platform": "Mac OS X 10.9",
     "browserName": "chrome",
     "version": "35"},
    {"platform": "Windows 8.1",
     "browserName": "internet explorer",
     "version": "11"},
    {"platform": "Linux",
     "browserName": "firefox",
     "version": "37"}]


def on_platforms(platforms):
    def decorator(base_class):
        module = sys.modules[base_class.__module__].__dict__
        for i, platform in enumerate(platforms):
            d = dict(base_class.__dict__)
            d['desired_capabilities'] = platform
            name = "%s_%s" % (base_class.__name__, i + 1)
            module[name] = type(name, (base_class,), d)

    return decorator


@on_platforms(browsers)
class SauceTest(LiveServerTestCase):
    """
    Runs a test using travis-ci and saucelabs
    """

    def setUp(self):
        django.setup()
        self.db = MongoDriver.instance()
        self.base_url = self.live_server_url

        # delete user if exists
        self.remove_user("test@test.com")
        self.test_user = User(
            'test@test.com',
        )
        self.test_user.set_password("test")
        self.db.create_user(self.test_user)

        self.setUpSauce()

        #load index
        self.driver.get(self.base_url + "/")

        #if something is not found give it 10 seconds to load
        self.driver.implicitly_wait(10)



    def tearDown(self):
        self.tearDownSauce()

    def setUpSauce(self):
        self.desired_capabilities['name'] = self.id()
        self.desired_capabilities['tunnel-identifier'] = \
            os.environ['TRAVIS_JOB_NUMBER']
        self.desired_capabilities['build'] = os.environ['TRAVIS_BUILD_NUMBER']
        self.desired_capabilities['tags'] = \
            [os.environ['TRAVIS_PYTHON_VERSION'], 'CI']

        sauce_url = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub"
        self.driver = webdriver.Remote(
            desired_capabilities=self.desired_capabilities,
            command_executor=sauce_url % (USERNAME, ACCESS_KEY)
        )
        self.driver.implicitly_wait(5)

    def tearDownSauce(self):
        try:
            if sys.exc_info() == (None, None, None):
                sauce.jobs.update_job(self.driver.session_id, passed=True)
            else:
                sauce.jobs.update_job(self.driver.session_id, passed=False)
        finally:
            self.driver.quit()

    def remove_user(self, user_id):
        self.db._users.remove({'_id': user_id})

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to.alert()
        except NoAlertPresentException:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    """**************************
          Single Draw Tests
    ****************************"""

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

    """**************************
          Settings Panel Tests
    ****************************"""

    def update_privacy_test(self):
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

        password = "123456"

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

    """**************************
      Signed Up Tests
    ****************************"""

    def sign_in_user(self):
        # Sign up in one of the browsers
        driver_signed_in = self.driver
        driver_signed_in.get(self.base_url + "/accounts/login/")
        driver_signed_in.find_element_by_css_selector("#login #email").clear()
        driver_signed_in.find_element_by_css_selector("#login #email").send_keys("test@test.com")
        driver_signed_in.find_element_by_css_selector("#login #password").clear()
        driver_signed_in.find_element_by_css_selector("#login #password").send_keys("test")
        driver_signed_in.find_element_by_css_selector("#login #login-button").click()

    def sign_out_user(self):
        driver = self.driver
        driver.get(self.base_url + "/accounts/profile/")
        driver.find_element_by_css_selector("#content #sign-out").click()

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
        self.sign_in_user()
        draw_title = "Testing favourites"
        driver = self.driver
        driver.find_element_by_css_selector("#card-draw").click()

        # Change the name of the draw
        driver.find_element_by_name("title").clear()
        driver.find_element_by_name("title").send_keys(draw_title)

        # Toss
        driver.find_element_by_id("toss").click()

        # Add to favourites
        driver.find_element_by_id("fav-button").click()
        driver.find_element_by_id("favourites").click()
        draw_id = driver.find_element_by_id("id__id").get_attribute('value')

        # Check that it has been dynamically added
        link = driver.find_element_by_xpath("//*[@id='favourites-panel']//a[contains(@href,'" + draw_id + "')]")
        link.click()

        # Check that is correctly stored in the DB
        driver.get(self.base_url + "/")
        driver.find_element_by_id("favourites").click()
        driver.find_element_by_xpath("//*[@id='favourites-panel']//a[contains(@href,'" + draw_id + "')]").click()
        same_name = draw_title == driver.find_element_by_name("title").get_attribute("value")
        self.assertTrue(same_name)

        # Remove from favourites
        driver.find_element_by_id("fav-button").click()

        # Check that it has been dynamically removed
        is_present = self.is_element_present("xpath", "//*[@id='favourites-panel']//a[contains(@href,'" + draw_id + "')]")
        self.assertFalse(is_present)

        # Check that is correctly removed from the DB
        driver.get(self.base_url + "/")
        driver.find_element_by_id("favourites").click()
        is_present = self.is_element_present("xpath", "//*[@id='favourites-panel']//a[contains(@href,'" + draw_id + "')]")
        self.assertFalse(is_present)

    def public_draw_everyone_test(self):
        """
        - Create a public draw (Privacy: everyone)
        - The draw is in the list "Recently created"
        - The draw can be accessed by non-register users
        - Only the owner can toss
        """
        self.sign_in_user()
        driver = self.driver
        driver.find_element_by_id("public-draw").click()
        driver.find_element_by_css_selector("#public-draw-dropdown .public-draw-create").click()
        driver.find_element_by_css_selector("#card-draw").click()
        driver.find_element_by_id("next").click()
        driver.find_element_by_id("publish").click()
        driver.find_element_by_id("toss").click()
        draw_id = driver.find_element_by_id("id__id").get_attribute('value')

        self.sign_out_user()

        driver.find_element_by_id("public-draw").click()
        driver.find_element_by_css_selector("#public-draw-dropdown .public-draw-join").click()
        driver.find_element_by_xpath("//tr[@data-draw_id='{0}']".format(draw_id)).click()

        # Check the spectator can not toss
        toss_status = driver.find_element_by_id("toss").get_attribute('disabled')
        self.assertNotEqual("disabled", toss_status)

        # Check the spectator can see the result
        results = driver.find_elements_by_class_name("result")
        self.assertEqual(1, len(results))

    def public_draw_password_test(self):
        """
        - Create a public draw (Privacy: password protected)
        - Setting a custom title
        - The draw is in the list "Recently created"
        - The draw can be accessed by non-register users by using the password
        - Only the owner can toss
        """
        self.sign_in_user()
        driver = self.driver
        password = '123456'
        driver.find_element_by_id("public-draw").click()
        driver.find_element_by_css_selector("#public-draw-dropdown .public-draw-create").click()
        driver.find_element_by_css_selector("#dice-draw").click()
        driver.find_element_by_name("title").clear()
        driver.find_element_by_name("title").send_keys("Public draw test")
        driver.find_element_by_id("next").click()
        driver.find_element_by_id("public-mode-selected").click()
        time.sleep(1)
        driver.find_element_by_css_selector("div.slider-tick.position-2").click()
        driver.find_element_by_id("draw-password").clear()
        driver.find_element_by_id("draw-password").send_keys(password)
        driver.find_element_by_id("save-change-privacy").click()

        driver.find_element_by_id("publish").click()
        driver.find_element_by_id("toss").click()
        draw_id = driver.find_element_by_id("id__id").get_attribute('value')

        self.sign_out_user()

        # Access the draw using the password
        driver.find_element_by_id("public-draw").click()
        driver.find_element_by_css_selector("#public-draw-dropdown .public-draw-join").click()
        driver.find_element_by_xpath("//tr[@data-draw_id='{0}']".format(draw_id)).click()

        # Introduce password and submit the query
        driver.find_element_by_css_selector("#password-dialog #password").clear()
        driver.find_element_by_css_selector("#password-dialog #password").send_keys(password)
        driver.find_element_by_id("check-password").click()

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
        self.sign_in_user()
        # Create guest user
        self.remove_user("test_guest@test.com")
        self.test_user = User(
            'test_guest@test.com',
        )
        self.test_user.set_password("test")
        self.db.create_user(self.test_user)

        driver = self.driver
        driver.find_element_by_id("public-draw").click()
        driver.find_element_by_css_selector("#public-draw-dropdown .public-draw-create").click()
        driver.find_element_by_css_selector("#dice-draw").click()
        driver.find_element_by_name("title").clear()
        driver.find_element_by_name("title").send_keys("Public draw test")
        driver.find_element_by_id("next").click()
        driver.find_element_by_id("public-mode-selected").click()
        time.sleep(1)
        driver.find_element_by_css_selector("div.slider-tick.position-3").click()
        driver.find_element_by_id("save-change-privacy").click()

        driver.find_element_by_id("invite-emails-tokenfield").send_keys("test_guest@test.com ")
        driver.find_element_by_id("publish").click()
        driver.find_element_by_id("toss").click()
        draw_id = driver.find_element_by_id("id__id").get_attribute('value')

        self.sign_out_user()

        # Guest signs in
        driver.get(self.base_url + "/accounts/login/")
        driver.find_element_by_css_selector("#login #email").clear()
        driver.find_element_by_css_selector("#login #email").send_keys("test_guest@test.com")
        driver.find_element_by_css_selector("#login #password").clear()
        driver.find_element_by_css_selector("#login #password").send_keys("test")
        driver.find_element_by_css_selector("#login #login-button").click()

        driver.get(self.base_url + "/draw/dice/" + draw_id)

        # Check the spectator can not toss
        toss_status = driver.find_element_by_id("toss").get_attribute('disabled')
        self.assertNotEqual("disabled", toss_status)

        # Check the spectator can see the result
        results = driver.find_elements_by_class_name("result")
        self.assertEqual(1, len(results))