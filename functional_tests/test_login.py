from .base import FunctionalTestBase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from django.urls import reverse

class UserLoginTest(FunctionalTestBase):
    
    def test_user_login(self):
        self.browser.get(self.live_server_url)

        # User enters empty string
        username_input_box = self.browser.find_element(By.ID, "login-username")
        username_input_box.send_keys(Keys.ENTER)

        # User is able to see an error on the screen
        print(self.browser.page_source)
        error = self.browser.find_element(By.CLASS_NAME, "error")

        # User saw the error and reenter a valid input
        username_input_box.send_keys(self.sample_username)

        user_login_button = self.browser.find_element(By.ID, "login-button")
        user_login_button.click()

        self.assertEqual(self.browser.current_url, reverse("home_page"))
        