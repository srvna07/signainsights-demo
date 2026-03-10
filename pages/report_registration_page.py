from playwright.sync_api import Page, Locator, expect
from .base_page import BasePage


class ReportRegistrationPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.report_registration        = page.get_by_role("button", name=" Report Registrations")
        self.new_report_btn = page.get_by_role("button", name="New Report")
        self.search_input   = page.get_by_placeholder("Search")
        self.rows_per_page  = page.get_by_role("combobox", name="Rows per page:")
        self.next_page_btn  = page.get_by_role("button", name="Go to next page")
        self.prev_page_btn  = page.get_by_role("button", name="Go to previous page")

        self.page_heading   = page.get_by_role("heading", name="Report Registration")

    def _dialog(self) -> Locator:
        return self.page.get_by_role("dialog")

    def _row(self, report_name: str) -> Locator:
        return self.page.get_by_role("row", name=report_name)

    def navigate_to_report_registration(self):
        self.report_registration.click()

    def search(self, report_name: str):
        self.search_input.fill(report_name)

    def clear_search(self):
        self.search_input.clear()

    def click_new_report(self):
        self.new_report_btn.click()

    def click_edit(self, report_name: str):
        self._row(report_name).get_by_role("button", name="Edit").click()

    def click_delete(self, report_name: str):
        self._row(report_name).get_by_role("button", name="Delete").click()

    def click_preview(self, report_name: str):
        self._row(report_name).get_by_role("button", name="Preview").click()

    def confirm_delete(self):
        self._dialog().get_by_role("button", name="Delete", exact=True).click()

    def confirm_update(self):
        self._dialog().get_by_role("button", name="Update", exact=True).click()

    def confirm_create(self):
        self._dialog().get_by_role("button", name="Create", exact=True).click()

    def fill_report_name(self, value: str):
        self._dialog().get_by_label("Report Name *").fill(value)

    def fill_menu(self, value: str):
        self._dialog().get_by_label("Menu *").fill(value)

    def fill_workspace_id(self, value: str):
        self._dialog().get_by_label("WorkSpaceId *").fill(value)

    def fill_report_id(self, value: str):
        self._dialog().get_by_label("ReportId *").fill(value)

    def fill_dataset_id(self, value: str):
        self._dialog().get_by_label("DatasetId *").fill(value)

    def select_role(self, *role_names: str):
        self.page.get_by_role("combobox", name="Role").click()
        for role in role_names:
            self.page.get_by_role("option", name=role).click()

    def select_organization(self, org_name: str):
        self.page.get_by_role("combobox", name="Organization").click()
        self.page.get_by_role("combobox", name="Organization").fill(org_name)
        option = self.page.get_by_role("option", name=org_name, exact=True)
        option.wait_for(state="visible")
        option.click()

    def set_rows_per_page(self, count: int):
        self.rows_per_page.click()
        self.page.get_by_role("option", name=str(count), exact=True).click()

    def go_to_next_page(self):
        self.next_page_btn.click()

    def go_to_previous_page(self):
        self.prev_page_btn.click()

    def create_report(self, report_name: str, menu_name: str, workspace_id: str,
                      report_id: str, dataset_id: str, organization: str, roles: list = None):
        self.navigate_to()
        self.click_new_report()
        self.fill_report_name(report_name)
        self.fill_menu(menu_name)
        self.fill_workspace_id(workspace_id)
        self.fill_report_id(report_id)
        self.fill_dataset_id(dataset_id)
        self.select_role(*(roles or ["Admin", "HR"]))
        self.select_organization(organization)
        self.confirm_create()

    def edit_report(self, report_name: str, new_name: str, additional_roles: list = None):
        self.click_edit(report_name)
        self.fill_report_name(new_name)
        if additional_roles:
            self.select_role(*additional_roles)
        self.confirm_update()

    def delete_report(self, report_name: str):
        self.click_delete(report_name)
        self.confirm_delete()

    def verify_report_visible(self, report_name: str):
        expect(self.page.get_by_text(report_name)).to_be_visible()

    def verify_report_not_visible(self, report_name: str):
        expect(self.page.get_by_text(report_name)).not_to_be_visible()

    def verify_search_result(self, report_name: str):
        expect(self.page.get_by_text(report_name).first).to_be_visible()

    def verify_heading_visible(self):
        expect(self.page_heading).to_be_visible()

    def verify_heading_not_visible(self):
        expect(self.page_heading).not_to_be_visible()

    def verify_nav_not_visible(self):
        expect(self.report_registration).not_to_be_visible()