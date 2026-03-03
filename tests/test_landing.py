import pytest
from playwright.sync_api import expect


# ---------------------------------------------------------------
# Fixture: authenticated landing page
# ---------------------------------------------------------------
@pytest.fixture
def landing(landing_page, authenticated_page):
    """Provide a LandingPage instance backed by an authenticated session."""
    return landing_page


# ---------------------------------------------------------------
# Landing Page - TC 01: Verify Landing Page loads successfully
# ---------------------------------------------------------------
@pytest.mark.smoke
@pytest.mark.medium
def test_landing_page_loads(landing):
    """Verify Landing Page loads with sidebar, top bar user menu, and footer."""
    landing.verify_page_loaded()

@pytest.mark.medium
@pytest.mark.parametrize(
    "menu_name, expected_slug",
    [
        ("Dashboard", "dashboard"),
        ("User Management", "user-management"),
        ("Insights", "insights"),
        ("Organizations", "organization-registration"),
        ("Report Registrations", "report-registration"),
    ],
)
def test_sidebar_navigation(landing, menu_name, expected_slug):
    """Verify sidebar menu navigation loads correct URL."""
    landing.click_sidebar_item(menu_name)
    landing.verify_url_contains(expected_slug)