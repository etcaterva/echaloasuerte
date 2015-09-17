import os
from os.path import join
import django
from django.test import LiveServerTestCase
from selenium import webdriver
from echaloasuerte.settings.common import SITE_ROOT
from server.mongodb.driver import MongoDriver

BROWSERSTACK_KEY = os.environ.get('BROWSERSTACK_KEY')


class BrowserStackTest(LiveServerTestCase):

    def __init__(self, *args, **kwargs):
        super(BrowserStackTest, self).__init__(*args, **kwargs)
        django.setup()

    def wait(self, seconds=10):
        # Set up a default implicit wait for 10 seconds
        self.driver.implicitly_wait(seconds)

    def setUp(self):
        self.db = MongoDriver.instance()
        self.base_url = self.live_server_url
        if BROWSERSTACK_KEY:
            test_url = "http://davidnaranjo1:{0}@hub.browserstack.com:80/wd/hub".format(BROWSERSTACK_KEY)
            # Specify capabilities
            desired_cap = {'browser': 'Safari',
                           'browser_version': '8.0',
                           'os': 'OS X',
                           'os_version': 'Yosemite',
                           'resolution': '1024x768',
                           'browserstack.local': True,
                           'browserstack.debug': True
                           }
            self.driver = webdriver.Remote(command_executor=test_url, desired_capabilities=desired_cap)
        else:
            # PhantomJS (Silent mode)
            self.driver = webdriver.PhantomJS('C:/phantomjs/bin/phantomjs.exe')

            # Firefox (Graphic mode)
            #self.driver = webdriver.Firefox()
            self.driver.set_window_size(1000, 900)

    def tearDown(self):
        self.driver.quit()
