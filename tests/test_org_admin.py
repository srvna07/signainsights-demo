from time import sleep

import pytest
from utils.data_factory import DataFactory
from utils.data_reader import DataReader
from pages.landing_page import LandingPage
from pages.newuser_page import NewUserPage
from pages.organizations_page import OrganizationsPage
from pages.report_registration_page import ReportRegistrationPage


# ---------------------------------------------------------------------------
# Session-scoped fixture — load org admin test data once
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def org_admin_data():
    data = DataReader.load_yaml("testdata/org_admin.json")
    u    = data["org_user_to_create"]
    u["username"] = DataFactory.random_username(u["usernamePrefix"])
    u["email"]    = DataFactory.random_email(u["usernamePrefix"], u["emailDomain"])
    return data


# ---------------------------------------------------------------------------
# Per-test fixtures — org admin session using existing page objects
# ---------------------------------------------------------------------------

@pytest.fixture
def org_admin_landing_page(org_admin_page):
    return LandingPage(org_admin_page)


@pytest.fixture
def org_admin_user_page(org_admin_page):
    return NewUserPage(org_admin_page)


@pytest.fixture
def org_admin_orgs_page(org_admin_page):
    return OrganizationsPage(org_admin_page)


@pytest.fixture
def org_admin_report_page(org_admin_page):
    return ReportRegistrationPage(org_admin_page)

# Verify org admin can access User Management and heading is visible
@pytest.mark.high
def test_org_admin_can_access_user_management(org_admin_user_page):
    org_admin_user_page.user_management_btn.click()
    org_admin_user_page.verify_heading_visible()


# Verify org admin user type dropdown only shows org-level types
@pytest.mark.critical
def test_org_admin_user_type_only_shows_org_types(org_admin_user_page):
    org_admin_user_page.open_form()
    org_admin_user_page.verify_user_type_option_visible("Organization Admin")
    org_admin_user_page.verify_user_type_option_visible("Organization User")
    org_admin_user_page.verify_user_type_option_not_visible("Super Admin")
    org_admin_user_page.verify_user_type_option_not_visible("Signa User")
    org_admin_user_page.cancel_form()


# # Verify org admin organization dropdown only shows their own organizations
# @pytest.mark.high
# def test_org_admin_organization_dropdown_shows_own_orgs(org_admin_user_page, org_admin_data):
#     all_orgs = [org_admin_data["primary_organization"]] + org_admin_data["secondary_organizations"]
#     org_admin_user_page.open_form()
#     org_admin_user_page.verify_organization_options_visible(all_orgs)
#     org_admin_user_page.cancel_form()


# Verify org admin can create an Organization User under their primary organization
@pytest.mark.critical
def test_org_admin_can_create_org_user_in_primary_org(org_admin_user_page, org_admin_data):
    u = org_admin_data["org_user_to_create"]
    org_admin_user_page.open_form()
    org_admin_user_page.fill_basic_info(u["firstName"], u["lastName"], u["username"], u["email"])
    org_admin_user_page.select_role(u["role"])
    org_admin_user_page.select_organization(org_admin_data["primary_organization"])
    org_admin_user_page.select_user_type(u["userType"])
    org_admin_user_page.fill_contact_info(**u["contact"])
    org_admin_user_page.submit_form()
    org_admin_user_page.verify_success()
    org_admin_user_page.verify_user_in_table(u["username"])


# Verify org admin can delete an org user they created
@pytest.mark.high
def test_org_admin_can_delete_org_user(org_admin_user_page, org_admin_data, config_fixture):
    username = org_admin_data["org_user_to_create"]["username"]
    org_admin_user_page.navigate_to_dashboard(config_fixture["base_url"])
    org_admin_user_page.user_management_btn.click()
    org_admin_user_page.delete_user(username)
    org_admin_user_page.verify_delete_success()
    org_admin_user_page.verify_user_not_in_table(username)


# Verify org admin cannot find a Signa user in the user management table
@pytest.mark.critical
def test_org_admin_cannot_see_signa_user_in_table(org_admin_user_page, signa_credentials):
    org_admin_user_page.user_management_btn.click()
    org_admin_user_page.search_user(signa_credentials["username"])
    org_admin_user_page.verify_user_not_in_table(signa_credentials["username"])


# Verify org admin cannot find a Super Admin in the user management table
@pytest.mark.critical
def test_org_admin_cannot_see_super_admin_in_table(org_admin_user_page, super_admin_credentials):
    org_admin_user_page.user_management_btn.click()
    org_admin_user_page.search_user(super_admin_credentials["username"])
    org_admin_user_page.verify_user_not_in_table(super_admin_credentials["username"])



# Verify Report Registrations nav is not visible in org admin sidebar
@pytest.mark.critical
def test_org_admin_cannot_see_report_registrations_in_sidebar(org_admin_report_page):
    org_admin_report_page.verify_nav_not_visible()


# Verify Organizations nav is not visible in org admin sidebar
@pytest.mark.critical
def test_org_admin_cannot_see_organizations_in_sidebar(org_admin_orgs_page):
    org_admin_orgs_page.verify_nav_not_visible()


# Verify org admin can navigate to Insights
@pytest.mark.high
def test_org_admin_can_access_insights(org_admin_landing_page, config_fixture):
    org_admin_landing_page.navigate(config_fixture["base_url"])
    org_admin_landing_page.insights_accessible()


