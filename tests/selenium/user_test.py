from server.bom import User
from tests.selenium.browserstack_base import BrowserStackTest

class UserTest(BrowserStackTest):
    """
    Test that all draw types can be accessed and generate results.
    """

    def remove_user(self, user_id):
        self.db._users.remove({'_id': user_id})

    def setUp(self):
        super(UserTest, self).setUp()

        # delete user if exists
        self.remove_user("test@test.com")
        self.test_user = User(
            'test@test.com',
        )
        self.test_user.set_password("test")
        self.db.create_user(self.test_user)

        # Load starting page
        self.driver.get(self.base_url + "/")

    def login(self):
        driver = self.driver
        self.driver.get(self.base_url + "/accounts/sigin/")
        email_input = driver.find_element_by_css_selector("#login #email")
        password_input = driver.find_element_by_css_selector("#login #password")
        email_input.clear()
        email_input.send_keys("test@test.com")
        password_input.clear()
        password_input.send_keys('test')
        driver.find_element_by_css_selector("#login #login-button").click()

    def test_login_in_dropdown(self):
        """ User login (from dropdown panel) """
        driver = self.driver
        login_button = driver.find_element_by_css_selector('#login-dropdown a')
        login_button.click()
        email_input = driver.find_element_by_css_selector("#login-dropdown #email")
        password_input = driver.find_element_by_css_selector("#login-dropdown #password")
        email_input.clear()
        email_input.send_keys("test@test.com")
        password_input.clear()
        password_input.send_keys('test')
        driver.find_element_by_css_selector("#login-dropdown #login-button").click()
        result = driver.find_elements_by_id('account-dropdown')
        self.assertNotEqual([], result)

    def test_login_in_screen(self):
        """ User login (from login screen) """
        driver = self.driver
        self.login()
        result = driver.find_elements_by_id('account-dropdown')
        self.assertNotEqual([], result)

    def test_change_alias(self):
        pass

    def test_change_password(self):
        pass

    def test_change_email(self):
        pass

    def test_change_avatar(self):
        pass

