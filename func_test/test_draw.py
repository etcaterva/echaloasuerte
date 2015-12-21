from selenium.webdriver.common.keys import Keys

from func_test.browserstack_base import BrowserStackTest


class NormalDrawTest(BrowserStackTest):
    """
    Test that all draw types can be accessed and generate results.
    """

    def setUp(self):
        super(NormalDrawTest, self).setUp()

        # Load starting page
        self.driver.get(self.base_url + "/")

    def test_coin(self):
        """Selenium: Coin draw (normal draw)"""
        driver = self.driver
        draw_box = driver.find_element_by_id("coin-draw")
        draw_box.click()

        # Toss with the button
        toss_btn = driver.find_element_by_id("create-and-toss")
        toss_btn.click()
        result = driver.find_elements_by_id("results")
        self.assertTrue(result)

        # Toss clicking the coin
        driver.find_element_by_id('img-coin').click()

        # Check if the results correspond with the edition
        results_rendered = driver.check_condition(
            lambda driver: len(driver.find_elements_by_css_selector('.result')) == 2
        )
        self.assertTrue(results_rendered)

    def test_random_number_test(self):
        """Selenium: Random Number draw (normal draw)"""
        driver = self.driver
        draw_box = driver.find_element_by_id("number-draw")
        draw_box.click()
        # Check the "allow repeated" checkbox is hidden
        self.assertTrue(driver.is_element_present('#div_id_allow_repeat'))
        self.assertFalse(driver.is_element_visible('#div_id_allow_repeat'))

        # Toss
        toss_btn = driver.find_element_by_id("create-and-toss")
        toss_btn.click()
        result = driver.find_elements_by_id("results")
        self.assertTrue(result)

        # Edit details
        number_of_results = driver.find_element_by_id('id_number_of_results')
        number_of_results.send_keys(Keys.UP)

        # Check the "allow repeated" checkbox is visible
        self.assertTrue(driver.is_element_visible('#div_id_allow_repeat'))

        # Toss
        toss_btn = driver.find_element_by_id("normal-draw-toss")
        toss_btn.click()

        # Check if the results correspond with the edition
        draw_updated = driver.check_condition(
            lambda driver: len(driver.find_elements_by_css_selector('.result')) == 2
        )
        self.assertTrue(draw_updated)

    def test_random_card(self):
        """Selenium: Card draw (normal draw)"""
        driver = self.driver
        draw_box = driver.find_element_by_id("card-draw")
        draw_box.click()
        toss_btn = driver.find_element_by_id("create-and-toss")
        toss_btn.click()
        result = driver.find_elements_by_id("results")
        self.assertTrue(result)

    def test_groups(self):
        """Selenium: Group draw (normal draw)"""
        driver = self.driver
        draw_box = driver.find_element_by_id("groups-draw")
        draw_box.click()
        driver.find_element_by_id("id_items-tokenfield").send_keys("a,b,c")
        toss_btn = driver.find_element_by_id("create-and-toss")
        toss_btn.click()
        result = driver.find_elements_by_id("results")
        self.assertTrue(result)

    def test_random_item(self):
        """Selenium: Random item draw (normal draw)"""
        driver = self.driver
        draw_box = driver.find_element_by_id("item-draw")
        draw_box.click()
        driver.find_element_by_id("id_items-tokenfield").send_keys("a,b,c")
        toss_btn = driver.find_element_by_id("create-and-toss")
        toss_btn.click()
        result = driver.find_elements_by_id("results")
        self.assertTrue(result)

    def test_dice(self):
        """Selenium: Dice draw (normal draw)"""
        driver = self.driver
        draw_box = driver.find_element_by_id("dice-draw")
        draw_box.click()
        toss_btn = driver.find_element_by_id("create-and-toss")
        toss_btn.click()
        result = driver.find_elements_by_id("results")
        self.assertTrue(result)

    def test_link_sets(self):
        """Selenium: Link sets draw (normal draw)"""
        driver = self.driver
        draw_box = driver.find_element_by_id("link_sets-draw")
        draw_box.click()
        driver.find_element_by_id("id_set_1-tokenfield").send_keys("1,2,3")
        driver.find_element_by_id("id_set_2-tokenfield").send_keys("a,b,c")
        toss_btn = driver.find_element_by_id("create-and-toss")
        toss_btn.click()
        result = driver.find_elements_by_id("results")
        self.assertTrue(result)

    def test_back_button(self):
        """Selenium: Back button inside draws"""
        driver = self.driver
        driver.find_element_by_id("number-draw").click()
        driver.find_element_by_class_name("back-arrow").click()
        result = driver.find_elements_by_id("number-draw")
        self.assertTrue(result)


