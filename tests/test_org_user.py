import pytest
from playwright.sync_api import expect
from utils.data_reader import DataReader
from pages.landing_page import LandingPage
from pages.newuser_page import NewUserPage
from pages.organizations_page import OrganizationsPage
from pages.report_registration_page import ReportRegistrationPage


# ---------------------------------------------------------------------------
# Session-scoped fixture — load org user test data once
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def org_user_data():
    return DataReader.load_yaml("testdata/org_user.json")


# ---------------------------------------------------------------------------
# Per-test fixtures — org user session using existing page objects
# ---------------------------------------------------------------------------

@pytest.fixture
def org_user_landing_page(org_user_page):
    return LandingPage(org_user_page)


@pytest.fixture
def org_user_new_user_page(org_user_page):
    return NewUserPage(org_user_page)


@pytest.fixture
def org_user_orgs_page(org_user_page):
    return OrganizationsPage(org_user_page)


@pytest.fixture
def org_user_report_page(org_user_page):
    return ReportRegistrationPage(org_user_page)


# ===========================================================================
# REQUIREMENT 1 — Org User has access ONLY to their own account
# ===========================================================================

# Verify org user can access the dashboard and Dashboard heading is visible
@pytest.mark.high
def test_org_user_can_access_dashboard(org_user_landing_page, config_fixture):
    org_user_landing_page.navigate(config_fixture["base_url"])
    org_user_landing_page.assert_url_contains("/dashboard")


# Verify User Management is not visible in the org user sidebar
@pytest.mark.critical
def test_org_user_cannot_see_user_management_in_sidebar(org_user_new_user_page):
    expect(org_user_new_user_page.user_management_btn).not_to_be_visible()


# Verify Organizations menu is not visible in the org user sidebar
@pytest.mark.critical
def test_org_user_cannot_see_organizations_in_sidebar(org_user_orgs_page):
    expect(org_user_orgs_page.organization_btn).not_to_be_visible()


# Verify org user is blocked from /user-management — heading not shown
@pytest.mark.high
def test_org_user_blocked_from_user_management_route(org_user_new_user_page, config_fixture):
    org_user_new_user_page.navigate_to(config_fixture["base_url"] + "/user-management")
    org_user_new_user_page.page.wait_for_load_state("domcontentloaded")
    org_user_new_user_page.verify_heading_not_visible()


# Verify org user is blocked from /organization-registration — heading not shown
@pytest.mark.high
def test_org_user_blocked_from_organization_registration_route(org_user_orgs_page, config_fixture):
    org_user_orgs_page.navigate_to(config_fixture["base_url"] + "/organization-registration")
    org_user_orgs_page.page.wait_for_load_state("domcontentloaded")
    org_user_orgs_page.verify_heading_not_visible()


# Verify org user is blocked from /report-registration — heading not shown
@pytest.mark.high
def test_org_user_blocked_from_report_registration_route(org_user_report_page, config_fixture):
    org_user_report_page.navigate_to(config_fixture["base_url"] + "/report-registration")
    org_user_report_page.page.wait_for_load_state("domcontentloaded")
    org_user_report_page.verify_heading_not_visible()


# ===========================================================================
# REQUIREMENT 2 — Org User can be assigned to multiple organizations
# ===========================================================================

# Verify primary organization appears in org user's org switcher
@pytest.mark.high
def test_org_user_primary_org_visible_in_switcher(org_user_landing_page, org_user_data):
    primary = org_user_data["org_user_multi"]["organization"]
    org_user_landing_page.verify_orgs_visible_in_switcher([primary])


# Verify all secondary organizations appear in org user's org switcher
@pytest.mark.high
def test_org_user_secondary_orgs_visible_in_switcher(org_user_landing_page, org_user_data):
    secondary_orgs = org_user_data["org_user_multi"]["secondaryOrganizations"]
    org_user_landing_page.verify_orgs_visible_in_switcher(secondary_orgs)


# Verify org user can switch between all assigned organizations
@pytest.mark.medium
def test_org_user_can_switch_between_organizations(org_user_landing_page, org_user_data):
    u = org_user_data["org_user_multi"]

    for org in u["secondaryOrganizations"]:
        org_user_landing_page.switch_organization(org)

    # Switch back to primary org
    org_user_landing_page.switch_organization(u["organization"])