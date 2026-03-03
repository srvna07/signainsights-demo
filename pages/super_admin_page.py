"""
pages/super_admin_page.py

Super Admin page object - handles super admin specific functionality and user management.
"""

from playwright.sync_api import Page, Locator, expect
from .base_page import BasePage


class SuperAdminPage(BasePage):
    """
    Super Admin page object.

    Manages:
    - Super admin dashboard access
    - User creation and management
    - User type and role selection
    - User table search and filtering
    - Super admin specific requirements
    """

    def __init__(self, page: Page):
        """Initialize SuperAdminPage with all locators."""
        super().__init__(page)

        # ── Sidebar Navigation ─────────────────────────────────────────────
        self.nav_dashboard: Locator = page.get_by_role(
            "button", name="Dashboard", exact=False
        )
        self.nav_user_management: Locator = page.get_by_role(
            "button", name="User Management", exact=False
        )
        self.nav_insights: Locator = page.get_by_role(
            "button", name="Insights", exact=False
        )
        self.nav_organizations: Locator = page.get_by_role(
            "button", name="Organizations", exact=False
        )
        self.nav_report_registrations: Locator = page.get_by_role(
            "button", name="Report Registrations", exact=False
        )

        # ── User Management Table ──────────────────────────────────────────
        self.new_user_btn: Locator = page.get_by_role("button", name="New User")
        self.create_btn: Locator = page.get_by_role("button", name="Create")
        self.update_btn: Locator = page.get_by_role("button", name="Update")
        self.delete_btn: Locator = page.get_by_role("button", name="Delete")
        self.search_input: Locator = page.get_by_role("textbox", name="Search")

        # ── User Form Fields ───────────────────────────────────────────────
        self.first_name: Locator = page.get_by_role("textbox", name="First Name")
        self.last_name: Locator = page.get_by_role("textbox", name="Last Name")
        self.username: Locator = page.get_by_role("textbox", name="User Name")
        self.email: Locator = page.get_by_role("textbox", name="Email")
        self.dob: Locator = page.get_by_role("textbox", name="Date of Birth")
        self.phone: Locator = page.get_by_role("textbox", name="1 (702) 123-")
        self.address1: Locator = page.get_by_role("textbox", name="Address1")
        self.address2: Locator = page.get_by_role("textbox", name="Address2")
        self.country: Locator = page.get_by_role("textbox", name="Country")
        self.city: Locator = page.get_by_role("textbox", name="City")
        self.state: Locator = page.get_by_role("textbox", name="State")
        self.zip_code: Locator = page.get_by_role("textbox", name="Zip Code")

        # ── Dropdown Fields ───────────────────────────────────────────────
        self.role_dropdown: Locator = page.get_by_role("combobox", name="Role")
        self.organization_dropdown: Locator = page.get_by_role(
            "combobox", name="Organization", exact=True
        )
        self.user_type_dropdown: Locator = page.get_by_role(
            "combobox", name="User Type"
        )

        # ── Success/Error Messages ────────────────────────────────────────
        self.success_message: Locator = page.get_by_text("User created successfully")
        self.update_success_message: Locator = page.get_by_text(
            "User updated successfully"
        )
        self.delete_success_message: Locator = page.get_by_text(
            "User deleted successfully"
        )

    # ─────────────────────────────────────────────────────────────────────────
    # Navigation
    # ─────────────────────────────────────────────────────────────────────────

    def navigate_to_dashboard(self) -> None:
        """Navigate to dashboard."""
        from utils.data_reader import DataReader
        from utils.env_loader import get_env

        cfg = DataReader.load_yaml(f"configs/{get_env()}.yaml")
        self.navigate_to_and_wait_network(f"{cfg['base_url'].rstrip('/')}/user-management")

    # ─────────────────────────────────────────────────────────────────────────
    # Actions - Form Management
    # ─────────────────────────────────────────────────────────────────────────

    def open_form(self) -> None:
        """Open new user creation form."""
        self.nav_user_management.click()
        self.new_user_btn.click()

    def fill_basic_info(
        self, first: str, last: str, username: str, email: str
    ) -> None:
        """
        Fill basic user information.

        Args:
            first: First name
            last: Last name
            username: Username
            email: Email address
        """
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.username.fill(username)
        self.email.fill(email)

    def fill_contact_info(self, contact: dict) -> None:
        """
        Fill contact information.

        Args:
            contact: Dictionary with contact fields
        """
        self.dob.fill(contact["dob"])
        self.phone.fill(contact["phone"])
        self.address1.fill(contact["address1"])
        self.address2.fill(contact["address2"])
        self.country.fill(contact["country"])
        self.city.fill(contact["city"])
        self.state.fill(contact["state"])
        self.zip_code.fill(contact["zipCode"])

    # ─────────────────────────────────────────────────────────────────────────
    # Actions - Dropdowns
    # ─────────────────────────────────────────────────────────────────────────

    def select_role(self, role: str) -> None:
        """
        Select role from dropdown.

        Args:
            role: Role name
        """
        self.select_dropdown_by_label(self.role_dropdown, role)

    def select_organization(self, org: str) -> None:
        """
        Select organization from dropdown.

        Args:
            org: Organization name
        """
        self.select_dropdown_by_label(self.organization_dropdown, org)

    def select_user_type(self, user_type: str) -> None:
        """
        Select user type from dropdown.

        Args:
            user_type: User type (e.g., Super Admin, Signa User)
        """
        self.select_dropdown_by_label(self.user_type_dropdown, user_type)

    # ─────────────────────────────────────────────────────────────────────────
    # Actions - User Management
    # ─────────────────────────────────────────────────────────────────────────

    def create_user(self, user_data: dict, username: str, email_addr: str) -> None:
        """
        Create a new user with complete information.

        Args:
            user_data: User data dictionary with firstName, lastName, role, etc.
            username: Username to create
            email_addr: Email address
        """
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
        """
        Search for user in table by username.

        Args:
            username: Username to search for
        """
        self.search_input.click()
        self.search_input.fill(username)
        # Wait for search results to appear
        self.page.wait_for_load_state("networkidle")

    def edit_user(self, username: str) -> None:
        """
        Navigate to edit form for specified user.

        Args:
            username: Username to edit
        """
        self.search_user(username)
        # Wait for edit button to appear for the searched user
        self.page.get_by_role("button", name="Edit").first.wait_for()
        self.page.get_by_role("button", name="Edit").first.click()

    def modify_user_name(
        self, username: str, new_first: str, new_last: str
    ) -> None:
        """
        Modify user's first and last name.

        Args:
            username: User to modify
            new_first: New first name
            new_last: New last name
        """
        self.nav_user_management.click()
        self.edit_user(username)
        self.first_name.clear()
        self.first_name.fill(new_first)
        self.last_name.clear()
        self.last_name.fill(new_last)
        self.update_btn.click()
        self.assert_visible(self.update_success_message)

    def delete_user(self, username: str) -> None:
        """
        Delete user from system.

        Args:
            username: Username to delete
        """
        self.nav_user_management.click()
        self.page.wait_for_load_state("networkidle")
        self.search_user(username)
        self.page.wait_for_load_state("networkidle")

        # Wait for the specific user row and get delete button from that row
        user_row = self.page.get_by_role("row", name=username)
        user_row.wait_for(state="visible")

        # Get the delete button within the specific user row
        delete_btn_in_row = user_row.get_by_label("Delete")
        delete_btn_in_row.wait_for(state="visible")
        delete_btn_in_row.click()  # Click delete/trash icon

        # Wait for confirmation dialog to appear and click confirm
        self.page.wait_for_load_state("networkidle")
        confirm_delete_btn = self.page.get_by_role("button", name="Delete").last
        confirm_delete_btn.wait_for(state="visible")
        confirm_delete_btn.click()  # Confirm deletion in dialog

        # Wait for success message
        self.assert_visible(self.delete_success_message)

        # Wait for dashboard to stabilize
        self.page.wait_for_load_state("networkidle")

    def delete_user_if_exists(self, username: str) -> None:
        """
        Best-effort delete user.

        Used in teardown - gracefully skips if user not found.

        Args:
            username: Username to delete
        """
        try:
            self.nav_user_management.click()
            self.search_user(username)
            # Get the specific user row
            user_row = self.page.get_by_role("row", name=username)
            # Only proceed if user row is visible
            if user_row.is_visible(timeout=2000):
                delete_btn_in_row = user_row.get_by_label("Delete")
                delete_btn_in_row.click()  # trash icon
                delete_btn_in_row.click()  # confirm dialog
                self.delete_success_message.wait_for(timeout=5000)
        except Exception:
            pass  # User may not exist, that's ok

    # ─────────────────────────────────────────────────────────────────────────
    # Assertions / Verifications
    # ─────────────────────────────────────────────────────────────────────────

    def verify_user_in_table(self, username: str) -> None:
        """
        Verify user exists in user management table.

        Args:
            username: Username to verify
        """
        self.search_user(username)
        self.assert_visible(self.page.get_by_text(username, exact=False))

    def verify_user_not_in_table(self, username: str) -> None:
        """
        Verify user does not exist in table.

        Args:
            username: Username to verify is absent
        """
        self.search_user(username)
        self.page.wait_for_load_state("networkidle")
        expect(self.page.get_by_text(username, exact=False)).not_to_be_visible()

    # ─────────────────────────────────────────────────────────────────────────
    # Assertions - Super Admin Requirements
    # ─────────────────────────────────────────────────────────────────────────

    def verify_full_sidebar_access(self) -> None:
        """
        TC-SA-01: Verify Super Admin has full sidebar access.

        All sidebar items must be visible.
        """
        self.assert_visible(self.nav_dashboard)
        self.assert_visible(self.nav_user_management)
        self.assert_visible(self.nav_insights)
        self.assert_visible(self.nav_organizations)
        self.assert_visible(self.nav_report_registrations)

    def verify_all_user_type_options_available(self) -> None:
        """
        TC-SA-06: Verify all four user types are available in dropdown.

        Required user types: Super Admin, Signa User, Organization Admin, Organization User
        """
        self.open_form()
        self.user_type_dropdown.click()

        # Verify all four user types
        self.assert_visible(
            self.page.get_by_role("option", name="Super Admin", exact=True)
        )
        self.assert_visible(
            self.page.get_by_role("option", name="Signa User", exact=True)
        )
        self.assert_visible(
            self.page.get_by_role("option", name="Organization Admin", exact=True)
        )
        self.assert_visible(
            self.page.get_by_role("option", name="Organization User", exact=True)
        )

        # Close dialog cleanly
        self.page.keyboard.press("Escape")
        self.page.get_by_role("button", name="Cancel").click()

    def verify_report_registration_page_accessible(self) -> None:
        """
        TC-SA-07: Verify Super Admin can access Report Registrations page.
        """
        self.nav_report_registrations.click()
        self.assert_url_contains("report-registration")

    def verify_organizations_page_accessible(self) -> None:
        """
        TC-SA-08: Verify Super Admin can access Organization Registration page.
        """
        self.nav_organizations.click()
        self.assert_url_contains("organization-registration")


