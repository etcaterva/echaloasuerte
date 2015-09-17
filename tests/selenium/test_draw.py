from tests.selenium.browserstack_base import BrowserStackTest


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
        self.wait()
        toss_btn = driver.find_element_by_id("toss")
        toss_btn.click()
        self.wait()
        result = driver.find_elements_by_id("results")
        self.assertNotEqual([], result)

    def test_random_number_test(self):
        """Selenium: Random Number draw (normal draw)"""
        driver = self.driver
        draw_box = driver.find_element_by_id("number-draw")
        draw_box.click()
        self.wait()
        toss_btn = driver.find_element_by_id("toss")
        toss_btn.click()
        self.wait()
        result = driver.find_elements_by_id("results")
        self.assertNotEqual([], result)

    def test_random_card(self):
        """Selenium: Card draw (normal draw)"""
        driver = self.driver
        draw_box = driver.find_element_by_id("card-draw")
        draw_box.click()
        self.wait()
        toss_btn = driver.find_element_by_id("toss")
        toss_btn.click()
        self.wait()
        result = driver.find_elements_by_id("results")
        self.assertNotEqual([], result)

    def test_random_item(self):
        """Selenium: Random item draw (normal draw)"""
        driver = self.driver
        draw_box = driver.find_element_by_id("item-draw")
        draw_box.click()
        self.wait()
        driver.find_element_by_id("id_items-tokenfield").send_keys("a,b,c")
        toss_btn = driver.find_element_by_id("toss")
        toss_btn.click()
        self.wait()
        result = driver.find_elements_by_id("results")
        self.assertNotEqual([], result)

    def test_dice(self):
        """Selenium: Dice draw (normal draw)"""
        driver = self.driver
        draw_box = driver.find_element_by_id("dice-draw")
        draw_box.click()
        self.wait()
        toss_btn = driver.find_element_by_id("toss")
        toss_btn.click()
        self.wait()
        result = driver.find_elements_by_id("results")
        self.assertNotEqual([], result)

    def test_link_sets(self):
        """Selenium: Link sets draw (normal draw)"""
        driver = self.driver
        draw_box = driver.find_element_by_id("link_sets-draw")
        draw_box.click()
        self.wait()
        driver.find_element_by_id("id_set_1-tokenfield").send_keys("1,2,3")
        driver.find_element_by_id("id_set_2-tokenfield").send_keys("a,b,c")
        toss_btn = driver.find_element_by_id("toss")
        toss_btn.click()
        self.wait()
        result = driver.find_elements_by_id("results")
        self.assertNotEqual([], result)

    def test_back_button(self):
        """Selenium: Back button inside draws"""
        driver = self.driver
        driver.find_element_by_id("number-draw").click()
        self.wait()
        driver.find_element_by_class_name("back-arrow").click()
        self.wait()
        driver.find_element_by_id("number-draw")


