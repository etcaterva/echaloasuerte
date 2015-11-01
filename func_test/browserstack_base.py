from os import environ

import django
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from server.mongodb.driver import MongoDriver


BROWSERSTACK_USERNAME = environ.get('BROWSERSTACK_USERNAME')
BROWSERSTACK_KEY = environ.get('BROWSERSTACK_KEY')
REPOSITORY_PATH = environ.get('TRAVIS_REPO_SLUG')


class BrowserStackTest(LiveServerTestCase):
    def __init__(self, *args, **kwargs):
        super(BrowserStackTest, self).__init__(*args, **kwargs)
        django.setup()

    def setUp(self):
        self.db = MongoDriver.instance()
        self.base_url = self.live_server_url
        if BROWSERSTACK_KEY:
            test_url = "http://{0}:{1}@hub.browserstack.com:80/wd/hub".format(
                BROWSERSTACK_USERNAME, BROWSERSTACK_KEY)
            # Specify capabilities
            desired_cap = {'browser': 'Firefox',
                           'browser_version': '40.0',
                           'os': 'OS X',
                           'os_version': 'Yosemite',
                           'resolution': '1024x768',
                           'browserstack.local': True,
                           'browserstack.debug': True
                           }
            self.driver = webdriver.Remote(command_executor=test_url,
                                           desired_capabilities=desired_cap)
        else:
            # PhantomJS (Silent mode)
            self.driver = webdriver.PhantomJS()

            # Firefox (Graphic mode)
            # self.driver = webdriver.Firefox()

            self.driver.set_window_size(1000, 900)
        self.driver.implicitly_wait(10)

    def is_element_present(self, css_selector):
        try:
            self.driver.find_element_by_css_selector(css_selector)
            return True
        except NoSuchElementException:
            return False

    def is_element_visible(self, css_selector):
        try:
            return self.driver.find_element_by_css_selector(
                css_selector).is_displayed()
        except NoSuchElementException:
            return False

    def check_condition(self, condition):
        """ Wait until a condition is satisfied with a timeout of 10 seconds """
        try:
            return WebDriverWait(self.driver, 10).until(condition)
        except TimeoutException:
            return False

    def tearDown(self):
        self.driver.quit()
