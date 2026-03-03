import pytest
from playwright.sync_api import Page

from pages.smoke_page import SmokePage
from utils.data_reader import DataReader
from utils.env_loader import get_env

ENV      = get_env()
config   = DataReader.load_yaml(f"configs/{ENV}.yaml")
BASE_URL = config["base_url"]


@pytest.fixture
def smoke_page(authenticated_page: Page) -> SmokePage:
    return SmokePage(authenticated_page)


# Verify all left sidebar navigation buttons are visible after login
@pytest.mark.smoke
def test_sidebar_items_present(smoke_page: SmokePage):
    smoke_page.navigate_to_dashboard(BASE_URL)
    smoke_page.verify_all_sidebar_items_present()


# Verify user menu (top bar) and footer links are visible on dashboard
@pytest.mark.smoke
def test_top_bar_and_footer_present(smoke_page: SmokePage):
    smoke_page.navigate_to_dashboard(BASE_URL)
    smoke_page.verify_user_menu_present()
    smoke_page.verify_footer_links_present()


# Verify report iframe is rendered and visible on the Insights page
@pytest.mark.smoke
def test_report_iframe_displayed(smoke_page: SmokePage):
    smoke_page.navigate_to_dashboard(BASE_URL)
    smoke_page.verify_report_iframe_displayed()