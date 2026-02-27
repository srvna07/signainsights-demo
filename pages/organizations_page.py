from playwright.sync_api import Page, expect
from .base_page import BasePage


class OrganizationsPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.organization_btn         = page.get_by_role("button", name=" Organizations")
        self.new_organization_btn     = page.get_by_role("button", name="New Organization")
        self.create_btn               = page.get_by_role("button", name="Create")
        self.update_btn               = page.get_by_role("button", name="Update")
        self.cancel_btn               = page.get_by_role("button", name="Cancel")
        self.delete_btn               = page.get_by_role("button", name="Delete")
        self.edit_btn                 = page.get_by_role("button", name="Edit")
        self.search_input             = page.get_by_role("textbox", name="Search")

        self.organization_name        = page.get_by_role("textbox", name="Organization Name")
        self.franchise_id             = page.get_by_role("textbox", name="Franchise ID")
        self.address_1                = page.get_by_role("textbox", name="Address 1")
        self.address_2                = page.get_by_role("textbox", name="Address 2")
        self.city                     = page.get_by_role("textbox", name="City")
        self.state                    = page.get_by_role("textbox", name="State")
        self.country                  = page.get_by_role("textbox", name="Country")
        self.zip_code                 = page.get_by_role("textbox", name="Zip Code")
        self.phone                    = page.locator("text=Phone Number").locator("..").locator("input[type='tel']")
        self.mobile                   = page.locator("text=Mobile Number").locator("..").locator("input[type='tel']")
        self.web_address              = page.get_by_role("textbox", name="Web Address")

        self.success_message          = page.get_by_text("Organization created successfully")
        self.update_success_message   = page.get_by_text("Organization updated successfully")
        self.delete_success_message   = page.get_by_text("Organization deleted successfully")
        self.duplicate_error_message  = page.get_by_text("Organization already exists.")

    def open_form(self):
        self.organization_btn.click()
        self.new_organization_btn.click()

    def navigate_to_organizations(self):
        self.organization_btn.click()

    def fill_basic_info(self, org_name: str, franchise_id: str):
        self.organization_name.fill(org_name)
        self.franchise_id.fill(franchise_id)

    def fill_contact_info(self, phone: str, mobile: str, address1: str, address2: str,
                          city: str, state: str, country: str, zip_code: str, web_address: str):
        self.phone.fill(phone)
        self.mobile.fill(mobile)
        self.address_1.fill(address1)
        self.address_2.fill(address2)
        self.city.fill(city)
        self.state.fill(state)
        self.country.fill(country)
        self.zip_code.fill(zip_code)
        self.web_address.fill(web_address)

    def submit_form(self):
        self.create_btn.click()

    def search_organization(self, org_name: str):
        self.search_input.click()
        self.search_input.fill(org_name)

    def edit_organization(self, org_name: str):
        self.search_organization(org_name)
        row = self.page.get_by_role("row", name=org_name).first
        row.wait_for(state="visible")
        row.get_by_role("button", name="Edit").click()

    def delete_organization(self, org_name: str):
        self.search_organization(org_name)
        row = self.page.get_by_role("row", name=org_name).first
        row.wait_for(state="visible")
        row.get_by_role("button", name="Delete").click()
        self.page.get_by_role("button", name="Delete").click()

    def _clear_field(self, field):
        if field.input_value():
            field.clear()

    def update_organization(self, update_data: dict):
        basic   = update_data["updated_basic"]
        contact = update_data["contact"]

        self._clear_field(self.organization_name)
        self.organization_name.fill(basic["name"])
        self._clear_field(self.franchise_id)
        self.franchise_id.fill(basic["franchise_id"])
        self._clear_field(self.phone)
        self.phone.fill(contact["phone"])
        self._clear_field(self.mobile)
        self.mobile.fill(contact["mobile"])
        self._clear_field(self.address_1)
        self.address_1.fill(contact["address1"])
        self._clear_field(self.address_2)
        self.address_2.fill(contact["address2"])
        self._clear_field(self.city)
        self.city.fill(contact["city"])
        self._clear_field(self.state)
        self.state.fill(contact["state"])
        self._clear_field(self.country)
        self.country.fill(contact["country"])
        self._clear_field(self.web_address)
        self.web_address.fill(contact["web_address"])
        self._clear_field(self.zip_code)
        self.zip_code.fill(contact["zip_code"])

    def verify_success(self):
        expect(self.success_message).to_be_visible(timeout=10000)

    def verify_update_success(self):
        expect(self.update_success_message).to_be_visible(timeout=10000)

    def verify_delete_success(self):
        expect(self.delete_success_message).to_be_visible(timeout=10000)

    def verify_duplicate_error(self):
        expect(self.duplicate_error_message).to_be_visible()

    def verify_organization_in_table(self, org_name: str):
        self.search_organization(org_name)
        expect(self.page.get_by_text(org_name).first).to_be_visible()

    def verify_organization_not_in_table(self, org_name: str):
        self.search_organization(org_name)
        expect(self.page.get_by_role("cell", name=org_name).first).not_to_be_visible()


