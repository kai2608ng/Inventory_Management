from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time
from user.models import User


class FunctionalTest(StaticLiveServerTestCase):
    sample_username = "sky2608ng"
    sample_password = "skyng123"
    options = Options()
    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    wait_time = 5

    def setUp(self):
        self.browser = webdriver.Firefox(options = self.options)
        User.objects.create_user(username = self.sample_username, password = self.sample_password)

    def tearDown(self):
        self.browser.quit()

    def wait(fn):
        def modified_fn(*args, **kwargs):
            start_time = time.time()
            while(True):
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > FunctionalTest.wait_time:
                        raise e
                    time.sleep(0.5)

        return modified_fn

    @wait
    def wait_for(self, fn):
        return fn()