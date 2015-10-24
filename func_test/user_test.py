from server.bom import User
from func_test.browserstack_base import BrowserStackTest


class UserTest(BrowserStackTest):
    """
    Test that all draw types can be accessed and generate results.
    """

    def remove_user(self, user_id):
        self.db._users.remove({'_id': user_id})

    def setUp(self):
        super(UserTest, self).setUp()

        test_user = User('test@test.com')
        test_user.set_password("test")
        self.db.create_user(test_user)
        self.test_user = test_user

        # Load starting page
        self.driver.get(self.base_url + "/")

    def tearDown(self):
        super(UserTest, self).tearDown()

        self.db.remove_user(self.test_user.pk)

    def login(self):
        driver = self.driver
        self.driver.get(self.base_url + "/accounts/login/")
        email_input = driver.find_element_by_css_selector("#login #email")
        password_input = driver.find_element_by_css_selector("#login #password")
        email_input.clear()
        email_input.send_keys("test@test.com")
        password_input.clear()
        password_input.send_keys('test')
        driver.find_element_by_css_selector("#login #login-button").click()

    def test_login_dropdown(self):
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
        self.assertTrue(result)

    def test_login_in_screen(self):
        """ User login (from login screen) """
        driver = self.driver
        self.login()
        result = driver.find_elements_by_id('account-dropdown')
        self.assertTrue(result)

    def test_change_alias(self):
        driver = self.driver
        self.login()

        # Check that the user has his default alias
        alias = driver.find_element_by_id('account-dropdown').text.strip()
        self.assertEqual('test', alias)

        # Change the alias
        driver.get(self.base_url + '/accounts/profile')
        driver.find_element_by_id('profile-edit-alias').click()
        driver.find_element_by_id('user-alias').send_keys("Cool alias")
        driver.find_element_by_id('save-alias').click()

        # Check if the alias has changed
        alias_updated = self.check_condition(
            lambda driver: driver.find_element_by_id('account-dropdown').text.strip() == "Cool alias"
        )
        self.assertTrue(alias_updated)
        alias_in_table = driver.find_element_by_css_selector('#profile-edit-alias .user-settings-content').text.strip()
        self.assertEqual("Cool alias", alias_in_table)



    '''def test_change_password(self):
        driver = self.driver
        driver.get('/accounts/profile')

    def test_change_email(self):
        driver = self.driver
        driver.get('/accounts/profile')'''

