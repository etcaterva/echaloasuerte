from selenium.common.exceptions import StaleElementReferenceException
from func_test.browserstack_base import BrowserStackTest, init_browser
from selenium.webdriver.common.keys import Keys
from server.bom import User


class SharedDrawTest(BrowserStackTest):
    """
    Test shared draw functionalities.
    """

    def remove_user(self, user_id):
        self.db._users.remove({'_id': user_id})

    def setUp(self):
        super(SharedDrawTest, self).setUp()

        self.remove_user('test@test.com')
        test_user = User('test@test.com')
        test_user.set_password("test")
        self.db.create_user(test_user)
        self.test_user = test_user

        # Load starting page
        self.driver.get(self.base_url + "/")

    def tearDown(self):
        super(SharedDrawTest, self).tearDown()

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
        driver.is_element_visible('#invite-emails-tokenfield')
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
        driver_guest.find_element_by_css_selector('#chat-frame #chat-send').click()
        driver.find_element_by_css_selector('#chat-frame #chat-message-box').send_keys('Second chat message')
        driver.find_element_by_css_selector('#chat-frame #chat-send').click()

        # Check that messages are sent and alias is correct
        two_messages = driver.check_condition(
            lambda current_driver: len(current_driver.find_elements_by_css_selector('#chat-frame .chatline-details')) == 2
        )
        self.assertTrue(two_messages)
        details = [chatline.get_attribute('innerHTML') for chatline in driver.find_elements_by_css_selector('#chat-frame .chatline-details')]
        for chatline in details:
            if 'test' in chatline:
                owner_in_chat = True
            if 'Mr. Nobody' in chatline:
                guest_in_chat = True
        self.assertTrue(owner_in_chat)
        self.assertTrue(guest_in_chat)

        # Check that chat can be disables
        driver.find_element_by_id('edit-settings-button').click()
        driver.check_condition(
            lambda current_driver: current_driver.is_element_visible('#settings-chat-enabled')
        )
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

        # Edit draw
        driver.find_element_by_id('edit-settings-button').click()
        driver.check_condition(
            lambda current_driver: current_driver.is_element_visible('#edit-draw')
        )
        driver.find_element_by_id('edit-draw').click()
        driver.find_element_by_id('edit-draw-confirmation').click()
        range_min_input = driver.find_element_by_id('id_range_min')
        range_min_input.send_keys(Keys.UP)
        driver.find_element_by_id('edit-draw-save').click()

        # Check changes are appliedsend_keys(Keys.UP)
        def check_changes_applied(current_driver):
            checked_input = current_driver.find_element_by_id('id_range_min')
            try:
                return checked_input.get_attribute('value') == '1'
            except StaleElementReferenceException:
                # This exception rise if the page reloaded between finding the input and getting its value
                return current_driver.find_element_by_id('id_range_min').get_attribute('value') == '1'

        self.assertTrue(driver.check_condition(check_changes_applied))
        self.assertTrue(driver_guest.check_condition(check_changes_applied))

        # Invite another user
        driver.find_element_by_id('edit-settings-button').click()
        driver.check_condition(
            lambda current_driver: current_driver.is_element_visible('#invite')
        )
        driver.find_element_by_id('invite').click()
        url_invite = driver.find_element_by_css_selector('#settings-invite .url-share').get_attribute('value')
        self.assertEqual(url_draw, url_invite)
        driver.find_element_by_id('invite-emails-tokenfield').send_keys('iker_jimenez@test.com')
        driver.find_element_by_id('send-emails').click()

        # Check that the user has been invited
        def check_user_invited(current_driver):
            users_invited = [token.get_attribute('innerHTML') for token in current_driver.find_elements_by_css_selector('.token-label')]
            return 'iker_jimenez@test.com' in users_invited
        self.assertTrue(driver.check_condition(check_user_invited))

        driver_guest.quit()



