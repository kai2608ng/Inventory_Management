from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time

class UserLoginTest(StaticLiveServerTestCase):
    sample_username = "sky2608ng"
    options = Options()
    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    wait_time = 5

    def setUp(self):
        self.browser = webdriver.Firefox(options = self.options)

    def tearDown(self):
        self.browser.quit()

    def wait(self, fn):
        def modified_fn(*args, **kwargs):
            start_time = time.now()
            while(True):
                try:
                    fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.now() - start_time > self.wait_time:
                        raise e
                    time.sleep(0.5)

        return modified_fn

    def test_user_login(self):
        self.browser.get(self.live_server_url)

        username_input_box = self.browser.find_element(By.ID, "login-username")
        username_input_box.send_keys(self.sample_username)

        user_login_button = self.browser.find_element(By.ID, "login-button")
        user_login_button.click()
        