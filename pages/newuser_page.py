from playwright.sync_api import Page, expect
from .base_page import BasePage


class NewUserPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.user_management_btn      = page.get_by_role("button", name=" User Management")
        self.new_user_btn             = page.get_by_role("button", name="New User")
        self.create_btn               = page.get_by_role("button", name="Create")
        self.update_btn               = page.get_by_role("button", name="Update")
        self.delete_btn               = page.get_by_role("button", name="Delete")
        self.search_input             = page.get_by_role("textbox", name="Search")

        self.first_name               = page.get_by_role("textbox", name="First Name")
        self.last_name                = page.get_by_role("textbox", name="Last Name")
        self.username                 = page.get_by_role("textbox", name="User Name")
        self.email                    = page.get_by_role("textbox", name="Email")
        self.dob                      = page.get_by_role("textbox", name="Date of Birth")
        self.phone                    = page.get_by_role("textbox", name="1 (702) 123-")
        self.address1                 = page.get_by_role("textbox", name="Address1")
        self.address2                 = page.get_by_role("textbox", name="Address2")
        self.country                  = page.get_by_role("textbox", name="Country")
        self.city                     = page.get_by_role("textbox", name="City")
        self.state                    = page.get_by_role("textbox", name="State")
        self.zip_code                 = page.get_by_role("textbox", name="Zip Code")

        self.role_dropdown            = page.get_by_role("combobox", name="Role")
        self.organization_dropdown    = page.get_by_role("combobox", name="Organization", exact=True)
        self.user_type_dropdown       = page.get_by_role("combobox", name="User Type")
        self.secondary_org_dropdown   = page.get_by_role("combobox", name="Secondary Organization")
        self.report_dropdown          = page.get_by_role("combobox", name="Select Report")

        self.success_message          = page.get_by_text("User created successfully")
        self.update_success_message   = page.get_by_text("User updated successfully")
        self.delete_success_message   = page.get_by_text("User deleted successfully")

        self.page_heading             = page.get_by_role("heading", name="User Management")

    def open_form(self):
        self.user_management_btn.click()
        self.new_user_btn.click()

    def fill_basic_info(self, first: str, last: str, username: str, email: str):
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.username.fill(username)
        self.email.fill(email)

    def fill_contact_info(self, dob: str, phone: str, address1: str, address2: str,
                          country: str, city: str, state: str, zipCode: str):
        self.dob.fill(dob)
        self.phone.fill(phone)
        self.address1.fill(address1)
        self.address2.fill(address2)
        self.country.fill(country)
        self.city.fill(city)
        self.state.fill(state)
        self.zip_code.fill(zipCode)

    def select_role(self, role_name: str):
        self.role_dropdown.click()
        self.page.get_by_role("option", name=role_name, exact=True).click()

    def select_organization(self, org_name: str):
        self.organization_dropdown.click()
        self.page.get_by_role("option", name=org_name, exact=True).click()

    def select_user_type(self, user_type: str):
        self.user_type_dropdown.click()
        self.page.get_by_role("option", name=user_type, exact=True).click()

    def select_secondary_orgs(self, *orgs: str):
        self.secondary_org_dropdown.click()
        for org in orgs:
            self.page.get_by_role("option", name=org, exact=True).click()

    def select_reports(self, *reports: str):
        self.report_dropdown.click()
        for report in reports:
            self.page.get_by_role("option", name=report).click()

    def open_reports_dropdown(self):
        self.report_dropdown.click()

    def close_reports_dropdown(self):
        self.page.keyboard.press("Escape")

    def submit_form(self):
        self.create_btn.click()

    def _clear_field(self, field):
        if field.input_value():
            field.clear()

    def _clear_multi_select(self, dropdown):
        clear_btn = dropdown.locator("..").get_by_role("button", name="Clear")
        if clear_btn.count() > 0:
            clear_btn.first.click()

    def search_user(self, username: str):
        self.search_input.click()
        self.search_input.fill(username)

    def edit_user(self, username: str):
        self.search_user(username)
        row = self.page.get_by_role("row", name=username).first
        row.wait_for(state="visible")
        row.get_by_role("button", name="Edit").click()

    def delete_user(self, username: str):
        self.search_user(username)
        row = self.page.get_by_role("row", name=username).first
        row.wait_for(state="visible")
        row.get_by_role("button", name="Delete").click()
        self.page.get_by_role("button", name="Delete").click()

    def update_user(self, update_data: dict):
        basic   = update_data["updated_basic"]
        contact = update_data["contact"]

        self._clear_field(self.first_name)
        self.first_name.fill(basic["firstName"])
        self._clear_field(self.last_name)
        self.last_name.fill(basic["lastName"])

        self.select_role(update_data["role"])
        self.select_organization(update_data["organization"])
        self.select_user_type(update_data["userType"])

        self._clear_multi_select(self.secondary_org_dropdown)
        self.select_secondary_orgs(*update_data["secondaryOrganizations"])

        self.dob.fill(contact["dob"])
        self.phone.fill(contact["phone"])
        for field_name in ["address1", "address2", "country", "city", "state"]:
            field = getattr(self, field_name)
            self._clear_field(field)
            field.fill(contact[field_name])
        self._clear_field(self.zip_code)
        self.zip_code.fill(contact["zipCode"])

        self._clear_multi_select(self.report_dropdown)
        self.select_reports(*update_data["reports"])

    def navigate_to_dashboard(self, base_url: str):
        self.navigate_to(f"{base_url.rstrip('/')}/dashboard")

    def verify_success(self):
        expect(self.success_message).to_be_visible()

    def verify_update_success(self):
        expect(self.update_success_message).to_be_visible()

    def verify_delete_success(self):
        expect(self.delete_success_message).to_be_visible()

    def verify_user_in_table(self, username: str):
        self.search_input.fill(username)
        expect(self.page.get_by_text(username, exact=False)).to_be_visible()

    def verify_user_not_in_table(self, username: str):
        expect(self.page.get_by_role("cell", name=username, exact=True)).not_to_be_visible()

    def verify_report_visible(self, report_name: str):
        expect(self.page.get_by_role("option", name=report_name)).to_be_visible()

    def verify_report_not_visible(self, report_name: str):
        expect(self.page.get_by_role("option", name=report_name)).not_to_be_visible()

    def verify_heading_visible(self):
        expect(self.page_heading).to_be_visible()

    def verify_heading_not_visible(self):
        expect(self.page_heading).not_to_be_visible()

    def verify_nav_not_visible(self):
        expect(self.user_management_btn).not_to_be_visible()

    def verify_user_type_option_visible(self, user_type: str):
        self.user_type_dropdown.click()
        expect(self.page.get_by_role("option", name=user_type, exact=True)).to_be_visible()
        self.page.keyboard.press("Escape")

    def verify_user_type_option_not_visible(self, user_type: str):
        self.user_type_dropdown.click()
        expect(self.page.get_by_role("option", name=user_type, exact=True)).not_to_be_visible()
        self.page.keyboard.press("Escape")

    def verify_organization_options_visible(self, org_names: list):
        self.organization_dropdown.click()
        for org in org_names:
            expect(self.page.get_by_role("option", name=org, exact=True)).to_be_visible()
        self.page.keyboard.press("Escape")

    def cancel_form(self):
        self.page.get_by_role("button", name="Cancel").click()