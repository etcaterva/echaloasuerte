import os
from os.path import join
import django
from django.test import LiveServerTestCase
from selenium import webdriver
from echaloasuerte.settings.common import SITE_ROOT

LOCAL_TESTS = not os.environ['RUN_TESTS_LOCALLY']


class BrowserStackTest(LiveServerTestCase):

    def __init__(self, *args, **kwargs):
        super(BrowserStackTest, self).__init__(*args, **kwargs)
        django.setup()

    def wait(self, seconds=10):
        # Set up a default implicit wait for 10 seconds
        self.driver.implicitly_wait(seconds)

    def setUp(self):
        self.base_url = self.live_server_url
        test_url_file = join(SITE_ROOT, 'secret_tests.txt')
        try:
            test_url = open(test_url_file).read().strip()
        except IOError:
            print("Impossible to load secret_tests.txt")
        else:
            # Specify capabilities
            desired_cap = {
                'browser': 'Chrome',
                'browser_version': '44.0',
                'os': 'Windows',
                'os_version': '8.1',
                'resolution': '1440x900'
            }
            if LOCAL_TESTS:
                # Firefox
                # self.driver = webdriver.Firefox()

                # PhantomJS (Silent)
                self.driver = webdriver.PhantomJS('C:/phantomjs/bin/phantomjs.exe')
            else:
                desired_cap['browserstack.local'] = True
                desired_cap['browserstack.debug'] = True

                # BrowserStack
                self.driver = webdriver.Remote(command_executor=test_url, desired_capabilities=desired_cap)

    def tearDown(self):
        self.driver.quit()
