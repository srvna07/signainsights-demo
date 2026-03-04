from playwright.sync_api import Page, Locator, expect
from .base_page import BasePage


class SuperAdminPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.nav_dashboard             = page.get_by_role("button", name="Dashboard",            exact=False)
        self.nav_user_management       = page.get_by_role("button", name="User Management",      exact=False)
        self.nav_insights              = page.get_by_role("button", name="Insights",             exact=False)
        self.nav_organizations         = page.get_by_role("button", name="Organizations",        exact=False)
        self.nav_report_registrations  = page.get_by_role("button", name="Report Registrations", exact=False)

        self.new_user_btn              = page.get_by_role("button", name="New User")
        self.create_btn                = page.get_by_role("button", name="Create")
        self.update_btn                = page.get_by_role("button", name="Update")
        self.delete_btn                = page.get_by_role("button", name="Delete")
        self.search_input              = page.get_by_role("textbox", name="Search")

        self.first_name                = page.get_by_role("textbox", name="First Name")
        self.last_name                 = page.get_by_role("textbox", name="Last Name")
        self.username                  = page.get_by_role("textbox", name="User Name")
        self.email                     = page.get_by_role("textbox", name="Email")
        self.dob                       = page.get_by_role("textbox", name="Date of Birth")
        self.phone                     = page.get_by_role("textbox", name="1 (702) 123-")
        self.address1                  = page.get_by_role("textbox", name="Address1")
        self.address2                  = page.get_by_role("textbox", name="Address2")
        self.country                   = page.get_by_role("textbox", name="Country")
        self.city                      = page.get_by_role("textbox", name="City")
        self.state                     = page.get_by_role("textbox", name="State")
        self.zip_code                  = page.get_by_role("textbox", name="Zip Code")

        self.role_dropdown             = page.get_by_role("combobox", name="Role")
        self.organization_dropdown     = page.get_by_role("combobox", name="Organization", exact=True)
        self.user_type_dropdown        = page.get_by_role("combobox", name="User Type")

        self.success_message           = page.get_by_text("User created successfully")
        self.update_success_message    = page.get_by_text("User updated successfully")
        self.delete_success_message    = page.get_by_text("User deleted successfully")

    def navigate_to_dashboard(self) -> None:
        from utils.data_reader import DataReader
        from utils.env_loader import get_env
        cfg = DataReader.load_yaml(f"configs/{get_env()}.yaml")
        self.navigate_to_and_wait_network(f"{cfg['base_url'].rstrip('/')}/user-management")

    def open_form(self) -> None:
        self.nav_user_management.click()
        self.new_user_btn.click()

    def fill_basic_info(self, first: str, last: str, username: str, email: str) -> None:
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.username.fill(username)
        self.email.fill(email)

    def fill_contact_info(self, contact: dict) -> None:
        self.dob.fill(contact["dob"])
        self.phone.fill(contact["phone"])
        self.address1.fill(contact["address1"])
        self.address2.fill(contact["address2"])
        self.country.fill(contact["country"])
        self.city.fill(contact["city"])
        self.state.fill(contact["state"])
        self.zip_code.fill(contact["zipCode"])

    def select_role(self, role: str) -> None:
        self.select_dropdown_by_label(self.role_dropdown, role)

    def select_organization(self, org: str) -> None:
        self.select_dropdown_by_label(self.organization_dropdown, org)

    def select_user_type(self, user_type: str) -> None:
        self.select_dropdown_by_label(self.user_type_dropdown, user_type)

    def create_user(self, user_data: dict, username: str, email_addr: str) -> None:
        self.open_form()
        self.fill_basic_info(
            first=user_data["firstName"],
            last=user_data["lastName"],
            username=username,
            email=email_addr,
        )
        self.select_role(user_data["role"])
        self.select_organization(user_data["organization"])
        self.select_user_type(user_data["userType"])
        self.fill_contact_info(user_data["contact"])
        self.create_btn.click()
        self.assert_visible(self.success_message)

    def search_user(self, username: str) -> None:
        self.search_input.click()
        self.search_input.fill(username)
        self.page.wait_for_load_state("networkidle")

    def edit_user(self, username: str) -> None:
        self.search_user(username)
        self.page.get_by_role("button", name="Edit").first.wait_for()
        self.page.get_by_role("button", name="Edit").first.click()

    def modify_user_name(self, username: str, new_first: str, new_last: str) -> None:
        self.nav_user_management.click()
        self.edit_user(username)
        self.first_name.clear()
        self.first_name.fill(new_first)
        self.last_name.clear()
        self.last_name.fill(new_last)
        self.update_btn.click()
        self.assert_visible(self.update_success_message)

    def delete_user(self, username: str) -> None:
        self.nav_user_management.click()
        self.page.wait_for_load_state("networkidle")
        self.search_user(username)
        self.page.wait_for_load_state("networkidle")

        user_row = self.page.get_by_role("row", name=username)
        user_row.wait_for(state="visible")

        delete_btn_in_row = user_row.get_by_label("Delete")
        delete_btn_in_row.wait_for(state="visible")
        delete_btn_in_row.click()

        self.page.wait_for_load_state("networkidle")
        confirm_delete_btn = self.page.get_by_role("button", name="Delete").last
        confirm_delete_btn.wait_for(state="visible")
        confirm_delete_btn.click()

        self.assert_visible(self.delete_success_message)
        self.page.wait_for_load_state("networkidle")

    def delete_user_if_exists(self, username: str) -> None:
        try:
            self.nav_user_management.click()
            self.search_user(username)
            user_row = self.page.get_by_role("row", name=username)
            if user_row.is_visible(timeout=2000):
                delete_btn_in_row = user_row.get_by_label("Delete")
                delete_btn_in_row.click()
                delete_btn_in_row.click()
                self.delete_success_message.wait_for(timeout=5000)
        except Exception:
            pass

    def verify_user_in_table(self, username: str) -> None:
        self.search_user(username)
        self.assert_visible(self.page.get_by_text(username, exact=False))

    def verify_user_not_in_table(self, username: str) -> None:
        self.search_user(username)
        self.page.wait_for_load_state("networkidle")
        expect(self.page.get_by_text(username, exact=False)).not_to_be_visible()

    def verify_full_sidebar_access(self) -> None:
        self.assert_visible(self.nav_dashboard)
        self.assert_visible(self.nav_user_management)
        self.assert_visible(self.nav_insights)
        self.assert_visible(self.nav_organizations)
        self.assert_visible(self.nav_report_registrations)

    def verify_all_user_type_options_available(self) -> None:
        self.open_form()
        self.user_type_dropdown.click()
        self.assert_visible(self.page.get_by_role("option", name="Super Admin",        exact=True))
        self.assert_visible(self.page.get_by_role("option", name="Signa User",         exact=True))
        self.assert_visible(self.page.get_by_role("option", name="Organization Admin", exact=True))
        self.assert_visible(self.page.get_by_role("option", name="Organization User",  exact=True))
        self.page.keyboard.press("Escape")
        self.page.get_by_role("button", name="Cancel").click()

    def verify_report_registration_page_accessible(self) -> None:
        self.nav_report_registrations.click()
        self.assert_url_contains("report-registration")

    def verify_organizations_page_accessible(self) -> None:
        self.nav_organizations.click()
        self.assert_url_contains("organization-registration")