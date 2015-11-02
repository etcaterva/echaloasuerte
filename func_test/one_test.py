from func_test.browserstack_base import BrowserStackTest, init_browser
from selenium.webdriver.common.keys import Keys
from server.bom import User


class UserTest(BrowserStackTest):
    """
    Test that all draw types can be accessed and generate results.
    """

    def remove_user(self, user_id):
        self.db._users.remove({'_id': user_id})

    def setUp(self):
        super(UserTest, self).setUp()

        self.remove_user('test@test.com')
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

    def test_public_draw(self):
        self.login()
        driver = self.driver
        driver_guest = init_browser()

        driver.find_element_by_id('is-shared').click()
        driver.find_element_by_id("number-draw").click()

        # Give it a title
        title_input = driver.find_element_by_css_selector('#draw-title-container textarea')
        title_input.clear()
        title_input.send_keys('Test draw')

        # TODO Try draw

        driver.find_element_by_id("publish").click()

        # Invite another user
        driver.find_element_by_id('invite-emails-tokenfield').send_keys('invited_user@test.com')
        driver.find_element_by_id('send-emails').click()

        # Access the draw (as guest) through the link given
        url_draw = driver.find_element_by_css_selector('#invite-options .url-share').get_attribute('value')
        driver_guest.get(url_draw)
        title_in_guest = driver_guest.find_element_by_css_selector('#draw-title-container textarea').get_attribute('value')
        self.assertEqual('Test draw', title_in_guest)

        # TODO Check Facebook button

        # Access the draw (as owner)
        driver.find_element_by_id("go-to-draw").click()

        # Check that everything is right for guest
        self.assertTrue(driver_guest.is_element_present('#toss-disabled-button'))
        self.assertFalse(driver_guest.is_element_present('#shared-draw-toss'))
        self.assertFalse(driver_guest.is_element_present('#edit-settings-button'))
        self.assertTrue(driver_guest.is_element_present('#subscribe-button'))

        # Check that everything is right for owner
        self.assertFalse(driver.is_element_present('#toss-disabled-button'))
        self.assertTrue(driver.is_element_present('#shared-draw-toss'))
        self.assertTrue(driver.is_element_present('#edit-settings-button'))
        self.assertFalse(driver.is_element_present('#subscribe-button'))
        self.assertTrue(driver.is_element_present('#schedule-toss-button'))

        # Check that chat is disabled (since the guest is anonymous) and access it
        driver_guest.find_element_by_css_selector('#chat-frame .alias-chat').send_keys('Mr. Nobody')
        driver_guest.find_element_by_css_selector('#chat-frame #access-chat').click()

        driver_guest.find_element_by_css_selector('#chat-frame #chat-message-box').send_keys('First chat message')
        driver.find_element_by_css_selector('#chat-frame #chat-message-box').send_keys('Second chat message')

        # TODO Check that messages are sent and alias is correct
        '''two_messsages = self.check_condition(
            lambda driver: len(driver.find_elements_by_css_selector('.result')) == 2
        )'''

        # TODO disable chat
        driver.find_element_by_id('edit-settings-button').click()
        driver.find_element_by_id('settings-chat-enabled').click()
        driver.find_element_by_id('save-settings').click()
        chat_invisible_guest = driver_guest.check_condition(
            lambda driver: driver.is_element_visible('#chat-frame') == False
        )
        chat_invisible_owner = driver.check_condition(
            lambda driver: driver.is_element_visible('#chat-frame') == False
        )
        self.assertTrue(chat_invisible_guest)
        self.assertTrue(chat_invisible_owner)

        # Check that fields are readonly
        self.assertTrue(driver_guest.find_element_by_id('id_range_min').get_attribute('readonly'))

        # TODO edit draw
        driver.find_element_by_id('edit-settings-button').click()
        driver.find_element_by_id('edit-draw').click()
        driver.find_element_by_id('edit-draw-confirmation').click()
        range_min_input = driver.find_element_by_id('id_range_min')
        range_min_input.clear()
        range_min_input.send_keys(5)
        driver.find_element_by_id('edit-draw-save').click()

        # Check changes are applied
        def check_changes_applied(driver):
            range_min_input = driver.find_element_by_id('id_range_min')
            return range_min_input.get_attribute('readonly') and range_min_input.get_attribute('value') == '5'
        self.assertTrue(driver.check_condition(check_changes_applied))
        self.assertTrue(driver_guest.check_condition(check_changes_applied))

        # TODO invite people
        pass


