# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase
from server.mongodb.driver import MongoDriver
from server.bom.user import User
from selenium import webdriver
import pyvirtualdisplay
import django

class SeleniumTest(LiveServerTestCase):
    """
    Base fixture for selenium tests
    It:
     -Initializes the web driver (self.driver)
     -Prepares a test user (self.test_user)
     -Starts a web server and loads home

    You just need to subclass this and write your
     selenium test usin self.driver ;)
    """

    def setUp(self):
        django.setup()
        self.db = MongoDriver.instance()

        self.display = pyvirtualdisplay.Display(
                visible=0,
                size=(1366, 768)
        )
        self.display.start()
        self.driver = webdriver.Firefox()
        self.driver.set_window_size(1366,768)
        self.driver.implicitly_wait(0.1)
        self.verificationErrors = []
        self.accept_next_alert = True

        super(SeleniumTest,self).setUp()
        self.base_url = self.live_server_url

        #delete user if exists
        self.remove_user("test@test.com")
        self.test_user = User(
            'test@test.com',
        )
        self.test_user.set_password("test")
        self.db.create_user(self.test_user)

        #load index
        self.driver.get(self.base_url + "/")

        #if something is not found give it 3 seconds to load
        self.driver.implicitly_wait(3)

    def tearDown(self):
        self.driver.quit()
        self.display.stop()
        self.assertEqual([], self.verificationErrors)
        super(SeleniumTest,self).tearDown()

    def remove_user(self, user_id):
        self.db._users.remove({ '_id' : user_id})

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException: return False
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
        finally: self.accept_next_alert = True

