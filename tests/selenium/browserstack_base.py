import os
from os.path import join
import django
from django.test import LiveServerTestCase
from selenium import webdriver
from echaloasuerte.settings.common import SITE_ROOT
from server.mongodb.driver import MongoDriver

LOCAL_TESTS = os.environ.get('RUN_TESTS_LOCALLY')


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
        test_url_file = join(SITE_ROOT, 'secret_tests.txt')
        try:
            key = open(test_url_file).read().strip()
        except IOError:
            print("Impossible to load secret_tests.txt")
        else:
            test_url = "http://davidnaranjo1:{0}@hub.browserstack.com:80/wd/hub".format(key)
            # Specify capabilities
            desired_cap = {'browser': 'Safari',
                           'browser_version': '8.0',
                           'os': 'OS X',
                           'os_version': 'Yosemite',
                           'resolution': '1024x768'
                           }
            if LOCAL_TESTS is None:
                desired_cap['browserstack.local'] = True
                desired_cap['browserstack.debug'] = True

                # BrowserStack
                self.driver = webdriver.Remote(command_executor=test_url, desired_capabilities=desired_cap)
            else:
                if LOCAL_TESTS == "silent":
                    # PhantomJS (Silent)
                    self.driver = webdriver.PhantomJS('C:/phantomjs/bin/phantomjs.exe')
                else:
                    # Firefox
                    self.driver = webdriver.Firefox()
                self.driver.set_window_size(1000, 900)

    def tearDown(self):
        self.driver.quit()
