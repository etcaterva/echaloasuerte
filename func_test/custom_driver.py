from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


class CustomWebDriver(webdriver.Firefox):

    def is_element_present(self, css_selector):
        try:
            self.find_element_by_css_selector(css_selector)
            return True
        except NoSuchElementException:
            return False

    def is_element_visible(self, css_selector):
        try:
            return self.find_element_by_css_selector(css_selector).is_displayed()
        except NoSuchElementException:
            return False

    def check_condition(self, condition):
        """ Wait until a condition is satisfied with a timeout of 10 seconds """
        try:
            return WebDriverWait(self, 10).until(condition)
        except TimeoutException:
            return False