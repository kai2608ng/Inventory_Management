from .base import FunctionalTest
from selenium.webdriver.common.by import By
from django.urls import reverse

class UserHomeTest(FunctionalTest):
    def login(self):
        self.browser.get(self.live_server_url)
        # User able to see the login template [
        username_input_box = self.browser.find_element(By.ID, "login-username")
        password_input_box = self.browser.find_element(By.ID, "login-password")
        login_button =  self.browser.find_element(By.CLASS_NAME, "form-submit-button")


        # User key in its data and able to login
        self.wait_for(lambda: username_input_box.send_keys(self.sample_username))
        self.wait_for(lambda: password_input_box.send_keys(self.sample_password))
        self.wait_for(lambda: login_button.click())

    def test_home_page_displayed(self):
        self.login()

        self.wait_for(lambda: self.browser.find_element(By.CLASS_NAME, "add-store-container").click())
        self.assertIn(reverse('new_store_page', args = (self.sample_username, )), self.browser.current_url)

        store_name_input_box = self.browser.find_element(By.ID, "store-name")
        create_button = self.browser.find_element(By.CLASS_NAME, "form-submit-button")
        store_name_input_box.send_keys("Store1")
        create_button.click()

        self.assertIn(reverse('home_page', args = (self.sample_username)), self.browser.current_url)

        self.browser.find_element(By.CLASS_NAME, "store-content-container")

        