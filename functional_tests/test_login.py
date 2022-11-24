from .base import FunctionalTest
from django.urls import reverse
from selenium.webdriver.common.by import By
from unittest import skip

class UserLoginTest(FunctionalTest):
    invalid_username = "invalid_username"
    invalid_password = "invalid_password"
    sample_username = "sky2608ng"
    sample_password = "skyng123"

    new_username = "new_username"
    new_password = "new_password"
    new_repassword = new_password
    new_email = "new@email.com"

    @skip
    def test_user_login(self):
        self.browser.get(self.live_server_url)

        # User able to see the login template 
        username_input_box = self.browser.find_element(By.ID, "login-username")
        password_input_box = self.browser.find_element(By.ID, "login-password")
        login_button =  self.browser.find_element(By.ID, "login-button")

        # User key in its data and able to login
        self.wait_for(lambda: username_input_box.send_keys(self.sample_username))
        self.wait_for(lambda: password_input_box.send_keys(self.sample_password))
        self.wait_for(lambda: login_button.click())

        # User successfully login to its own home page
        self.assertEqual(self.browser.current_url, reverse("home_page", args = (self.sample_username, )))

    def test_user_create_new_user(self):
        self.browser.get(self.live_server_url)

        create_new_user_link = self.browser.find_element(By.ID, "create-new-user-link")
        create_new_user_link.click()

        # Go to Create new user web page
        self.assertIn(reverse("new_user_page"), self.browser.current_url)

        # User able to see the crete new user template
        username_input_box = self.browser.find_element(By.ID, "new-username")
        password_input_box = self.browser.find_element(By.ID, "new-password")
        repassword_input_box = self.browser.find_element(By.ID, "new-repassword")
        email_input_box = self.browser.find_element(By.ID, "new-email")
        create_new_user_button = self.browser.find_element(By.ID, "create-new-user-button")

        # User key in data
        self.wait_for(lambda: username_input_box.send_keys(self.new_username))
        self.wait_for(lambda: password_input_box.send_keys(self.new_password))
        self.wait_for(lambda: repassword_input_box.send_keys(self.new_repassword))
        self.wait_for(lambda: email_input_box.send_keys(self.new_email))

        # User click create new button
        self.wait_for(lambda: create_new_user_button.click())

        # Show account has created successfully 
        self.wait_for(lambda: self.browser.find_element(By.ID, "success-messages"))
        self.wait_for(lambda: self.browser.find_element(By.ID, "back-to-login-button").click())

        # User back to login page
        self.assertIn(reverse("login_page"), self.browser.current_url)