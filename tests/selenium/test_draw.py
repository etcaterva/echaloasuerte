import os
from os.path import join
import django
from django.test import LiveServerTestCase
from selenium import webdriver
from echaloasuerte.settings.common import SITE_ROOT

LOCAL_TESTS = not os.environ['RUN_TESTS_LOCALLY']


class NormalDrawTest(LiveServerTestCase):

    def wait(self):
        self.driver.implicitly_wait(10)

    def setUp(self):
        django.setup()
        self.base_url = self.live_server_url
        self.wait_length = 10
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

            # Load starting page
            self.driver.get(self.base_url + "/")

    def tearDown(self):
        self.driver.quit()

    def test_coin(self):
        driver = self.driver
        driver.implicitly_wait(100)
        draw_box = driver.find_element_by_id("coin-draw")
        draw_box.click()
        self.wait()
        toss_btn = driver.find_element_by_id("toss")
        toss_btn.click()
        self.wait()
        results = driver.find_element_by_id("results")
        self.assertTrue(results)

    def test_random_number_test(self):
        driver = self.driver
        draw_box = driver.find_element_by_id("number-draw")
        draw_box.click()
        self.wait()
        toss_btn = driver.find_element_by_id("toss")
        toss_btn.click()
        self.wait()
        results = driver.find_element_by_id("results")
        self.assertTrue(results)

    def test_random_card(self):
        driver = self.driver
        draw_box = driver.find_element_by_id("card-draw")
        draw_box.click()
        self.wait()
        toss_btn = driver.find_element_by_id("toss")
        toss_btn.click()
        self.wait()
        results = driver.find_element_by_id("results")
        self.assertTrue(results)

    def test_random_item(self):
        driver = self.driver
        draw_box = driver.find_element_by_id("item-draw")
        draw_box.click()
        self.wait()
        driver.find_element_by_id("id_items-tokenfield").send_keys("a,b,c")
        toss_btn = driver.find_element_by_id("toss")
        toss_btn.click()
        self.wait()
        results = driver.find_element_by_id("results")
        self.assertTrue(results)

    def test_dice(self):
        driver = self.driver
        draw_box = driver.find_element_by_id("dice-draw")
        draw_box.click()
        self.wait()
        toss_btn = driver.find_element_by_id("toss")
        toss_btn.click()
        self.wait()
        results = driver.find_element_by_id("results")
        self.assertTrue(results)

    def test_link_sets(self):
        driver = self.driver
        draw_box = driver.find_element_by_id("link_sets-draw")
        draw_box.click()
        self.wait()
        driver.find_element_by_id("id_set_1-tokenfield").send_keys("1,2,3")
        driver.find_element_by_id("id_set_2-tokenfield").send_keys("a,b,c")
        toss_btn = driver.find_element_by_id("toss")
        toss_btn.click()
        self.wait()
        results = driver.find_element_by_id("results")
        self.assertTrue(results)

    def test_back_button(self):
        driver = self.driver
        driver.find_element_by_id("number-draw").click()
        self.wait()
        driver.find_element_by_class_name("back-arrow").click()
        self.wait()
        driver.find_element_by_id("number-draw")


