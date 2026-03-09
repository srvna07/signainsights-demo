from playwright.sync_api import Page, expect
from .base_page import BasePage


class SmokePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.nav_dashboard            = page.get_by_role("button", name="Dashboard",            exact=False)
        self.nav_user_management      = page.get_by_role("button", name="User Management",      exact=False)
        self.nav_insights             = page.get_by_role("button", name="Insights",             exact=False)
        self.nav_organizations        = page.get_by_role("button", name="Organizations",        exact=False)
        self.nav_report_registrations = page.get_by_role("button", name="Report Registrations", exact=False)
        self.user_menu                = page.get_by_role("button", name="Signed in as", exact=False)
        self.privacy_policy           = page.get_by_role("link",   name="Privacy Policy")
        self.terms                    = page.get_by_role("link",   name="Terms & Conditions")
        self.report_iframe            = page.locator("iframe").first

    def navigate_to_dashboard(self, base_url: str):
        self.navigate_to(f"{base_url.rstrip('/')}/dashboard")

    def navigate_to_insights(self, base_url: str):
        self.navigate_to(f"{base_url.rstrip('/')}/insights")

    def verify_all_sidebar_items_present(self):
        expect(self.nav_dashboard).to_be_visible()
        expect(self.nav_user_management).to_be_visible()
        expect(self.nav_insights).to_be_visible()
        expect(self.nav_organizations).to_be_visible()
        expect(self.nav_report_registrations).to_be_visible()

    def verify_user_menu_present(self):
        expect(self.user_menu).to_be_visible()

    def verify_footer_links_present(self):
        expect(self.privacy_policy).to_be_visible()
        expect(self.terms).to_be_visible()

    def verify_report_iframe_displayed(self):
        expect(self.report_iframe).to_be_visible()