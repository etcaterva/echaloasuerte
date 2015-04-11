from django.test import LiveServerTestCase
from server.mongodb.driver import MongoDriver
import django
from selenium import webdriver

class SanityWebapp(LiveServerTestCase):
    """ Basic sanity test for the web app"""
    def setUp(self):
        django.setup()
        self.db = MongoDriver.instance()
        self.selenium = webdriver.Firefox()
        self.selenium.maximize_window()

        super(SanityWebapp,self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(SanityWebapp,self).tearDown()

    def load_url(self, url):
        self.selenium.get("{0}{1}".format(
            self.live_server_url,
            url
        ))

    def sanity_test(self):
        self.load_url("/")

    def change_language_test(self):
        pass

    def user_login_test(self):
        pass

    def user_logout_test(self):
        pass

    def user_signup_test(self):
        pass
