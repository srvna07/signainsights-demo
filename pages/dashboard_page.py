from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class DashboardPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        
    
        self.Sales_card = page.get_by_role("region", name="Sales")
        self.Revenue_by_month_card = page.get_by_role("region", name="Revenue By Month")
        self.Receivables_card = page.get_by_role("region", name="Receivables")
        self.Royalty_report_card = page.get_by_role("region", name="Royalty Report")

    def verify_dashboard_cards_visible(self):
            expect(self.Sales_card).to_be_visible()
            expect(self.Revenue_by_month_card).to_be_visible()
            expect(self.Receivables_card).to_be_visible()
            expect(self.Royalty_report_card).to_be_visible()
       