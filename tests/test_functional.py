from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import os

class TestRegistration(StaticLiveServerTestCase):
    fixtures = [os.path.join(os.path.dirname(__file__), 'sample_data.json')]

    def setUp(self):
        self.browser = webdriver.Firefox()
        super(TestRegistration, self).setUp()

    def tearDown(self):
        self.browser.quit()
        super(TestRegistration, self).tearDown()

    def test_open_register_page_from_index(self):
        self.browser.get(self.live_server_url + "/")
        register_link = self.browser.find_element_by_partial_link_text('Register')
        self.assertTrue(register_link.is_displayed())
        register_link.click()
        self.assertEqual(len(self.browser.find_elements_by_css_selector('input[value="Register"]')), 1)
