from playwright.sync_api import Page, expect
from .base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input          = page.get_by_label("Username")
        self.password_input          = page.get_by_label("Password")
        self.login_button            = page.get_by_role("button", name="Login")
        self.welcome_text            = page.get_by_text("Welcome back")
        self.error_message           = page.get_by_role("alert")
        self.forgot_password_link    = page.get_by_text("Forgot Password?")
        self.forgot_password_header  = page.get_by_role("heading", name="Forgot Password")
        self.username_required_error = page.get_by_text("Username is required")
        self.password_required_error = page.get_by_text("Password is required")
        self.password_incorrect_error = page.get_by_text("Password is incorrect")

    def navigate(self, base_url: str):
        self.navigate_to(base_url)

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def click_login(self):
        self.login_button.click()

    def click_forgot_password(self):
        self.forgot_password_link.click()

    def verify_page_loaded(self):
        expect(self.welcome_text).to_be_visible()
        expect(self.username_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.login_button).to_be_visible()
