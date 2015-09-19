from os import environ
import django
from django.test import LiveServerTestCase
from selenium import webdriver
from server.mongodb.driver import MongoDriver

BROWSERSTACK_KEY = environ.get('BROWSERSTACK_KEY')


class BrowserStackTest(LiveServerTestCase):

    def __init__(self, *args, **kwargs):
        super(BrowserStackTest, self).__init__(*args, **kwargs)
        django.setup()

    def setUp(self):
        self.db = MongoDriver.instance()
        self.base_url = self.live_server_url
        if BROWSERSTACK_KEY:
            test_url = "http://davidnaranjo1:{0}@hub.browserstack.com:80/wd/hub".format(BROWSERSTACK_KEY)
            # Specify capabilities
            desired_cap = {'browser': 'Firefox',
                           'browser_version': '40.0',
                           'os': 'OS X',
                           'os_version': 'Yosemite',
                           'resolution': '1024x768',
                           'browserstack.local': True,
                           'browserstack.debug': True
                           }
            self.driver = webdriver.Remote(command_executor=test_url, desired_capabilities=desired_cap)
        else:
            # PhantomJS (Silent mode)
            self.driver = webdriver.PhantomJS()

            # Firefox (Graphic mode)
            # self.driver = webdriver.Firefox()

            self.driver.set_window_size(1000, 900)

        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()
