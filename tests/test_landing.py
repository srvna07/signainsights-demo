import pytest
from playwright.sync_api import expect


@pytest.fixture
def landing(landing_page, authenticated_page):
    return landing_page


# Verify Landing Page loads successfully with all components
@pytest.mark.medium
def test_landing_page_loads(landing):
    landing.verify_page_loaded()


# Verify sidebar menu navigation loads correct URL
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
def test_sidebar_navigation_loads_correct_url(landing, menu_name, expected_slug):
    landing.click_sidebar_item(menu_name)
    landing.verify_url_contains(expected_slug)