from playwright.sync_api import Page, expect
from .base_page import BasePage


class LandingPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.user_menu_button         = page.get_by_role("button", name="Signed in as Test User")
        self.logout_menu_item         = page.get_by_role("menuitem", name="Logout")
        self.logout_confirm_button    = page.get_by_role("button", name="Logout")
        self.nav_dashboard            = page.get_by_role("button", name="Dashboard",            exact=False)
        self.nav_user_management      = page.get_by_role("button", name="User Management",      exact=False)
        self.nav_insights             = page.get_by_role("button", name="Insights",             exact=False)
        self.nav_organizations        = page.get_by_role("button", name="Organizations",        exact=False)
        self.nav_report_registrations = page.get_by_role("button", name="Report Registrations", exact=False)
        self.privacy_policy_link      = page.get_by_role("link", name="Privacy Policy")
        self.terms_link               = page.get_by_role("link", name="Terms & Conditions")

    def navigate(self, base_url: str):
        self.navigate_to(f"{base_url.rstrip('/')}/dashboard")

    def click_sidebar_item(self, name: str):
        self.page.get_by_role("button", name=name, exact=False).click()

    def click_logout(self):
        self.user_menu_button.click()
        self.logout_menu_item.click()
        self.logout_confirm_button.click()

    def verify_page_loaded(self):
        expect(self.user_menu_button).to_be_visible()
        expect(self.nav_dashboard).to_be_visible()
        expect(self.nav_user_management).to_be_visible()
        expect(self.nav_insights).to_be_visible()
        expect(self.nav_organizations).to_be_visible()
        expect(self.nav_report_registrations).to_be_visible()
        expect(self.privacy_policy_link).to_be_visible()
        expect(self.terms_link).to_be_visible()

    def verify_url_contains(self, text: str):
        self.assert_url_contains(text)
