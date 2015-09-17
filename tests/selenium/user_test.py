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

    def test_sign_in_user(self):
        # Sign up in one of the browsers
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
        account_panel = driver.find_element_by_id('account-dropdown')
        self.assertTrue(account_panel)

