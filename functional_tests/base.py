from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time

class FunctionalTestBase(StaticLiveServerTestCase):
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