import os
import pytest
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

from utils.env_loader import get_env
from utils.data_reader import DataReader
from utils.data_factory import DataFactory
from utils.logger import get_logger
from pages.login_page import LoginPage
from pages.forgot_password_page import ForgotPasswordPage
from pages.newuser_page import NewUserPage
from pages.organizations_page import OrganizationsPage
from pages.report_registration_page import ReportRegistrationPage
from pages.landing_page import LandingPage

logger = get_logger(__name__)

ENV = get_env()
config = DataReader.load_yaml(f"configs/{ENV}.yaml")


@pytest.fixture(scope="session")
def config_fixture():
    return config


@pytest.fixture(scope="session")
def browser():
    """Launch browser once per test session."""
    with sync_playwright() as p:
        browser = getattr(p, config["browser"]).launch(
            headless=config["headless"],
            args=["--start-maximized"]
        )

        logger.info(f"ENV: {ENV} | Base URL: {config['base_url']}")
        logger.info(f"Browser: {config['browser']} | Headless: {config['headless']}")

        yield browser
        browser.close()
@pytest.fixture(scope="session")
def page(browser):
    """Single shared page for normal tests."""
    context = browser.new_context(no_viewport=True)
    page = context.new_page()

    page.set_default_timeout(config["default_timeout"])
    page.set_default_navigation_timeout(config["navigation_timeout"])

    yield page
    context.close()

@pytest.fixture
def fresh_context(browser):
    """Fresh context for multi-user tests."""
    context = browser.new_context(no_viewport=True)
    page = context.new_page()

    page.set_default_timeout(config["default_timeout"])
    page.set_default_navigation_timeout(config["navigation_timeout"])

    yield page
    context.close()
@pytest.fixture(scope="session")
def authenticated_page(page):
    """Logs in once and reuses the session for all 50 tests."""
    
    login = LoginPage(page)
    login.navigate(config["base_url"])
    # Uses Environment Variables for security
    login.login(os.getenv("USERNAME"), os.getenv("PASSWORD"))
    logger.info("✓ Session authenticated. Reusing for all tests.")
    return page

@pytest.fixture
def existing_user_page(fresh_context):
    """Logs in as existing normal user in separate session."""
    page = fresh_context
    login = LoginPage(page)
    login.navigate(config["base_url"])
    login.login(os.getenv("SECOND_USER"), os.getenv("SECOND_PASSWORD"))
    return page


@pytest.fixture
def login_page(page):
    return LoginPage(page)

@pytest.fixture
def forgot_password_page(page):
    return ForgotPasswordPage(page)

@pytest.fixture
def landing_page(page):
    return LandingPage(page)

@pytest.fixture
def new_user_page(page):
    return NewUserPage(page)

@pytest.fixture
def new_organization_page(page):
    return OrganizationsPage(page)

@pytest.fixture
def report_registration_page(page):
    return ReportRegistrationPage(page)

@pytest.fixture
def dashboard_page(page): 
    return DashboardPage(page)



@pytest.fixture(scope="session")
def new_user_data():
    data   = DataReader.load_yaml("testdata/new_user.yaml")
    prefix = data["user"]["usernamePrefix"] + "_"
    data["user"]["username"] = DataFactory.random_username(prefix)
    data["user"]["email"]    = DataFactory.random_email(prefix, data["user"]["emailDomain"])
    return data


@pytest.fixture(scope="session")
def new_organization_data():
    data = DataReader.load_yaml("testdata/new_organization.yaml")
    data["organization"]["namePrefix"]   = DataFactory.random_org_name(data["organization"]["namePrefix"] + "_")
    data["organization"]["franchise_id"] = data["organization"]["franchise_id"] + "_" + DataFactory.random_string()
    return data


@pytest.fixture(scope="session")
def report_registration_data():
    report_data = DataReader.load_yaml("testdata/report_registration.yaml")
    org_data    = DataReader.load_yaml("testdata/new_organization.yaml")
    report_data["new_report"]["report_name"]  = DataFactory.generate_report_name()
    report_data["new_report"]["menu_name"]    = DataFactory.generate_menu_name()
    report_data["edit_report"]["report_name"] = DataFactory.generate_report_name("test_edited_report")
    report_data["organization"]               = org_data["organization"]
    return report_data


@pytest.fixture(scope="session")
def signa_page(page):
    context = page.context.browser.new_context(no_viewport=True)
    pg = context.new_page()
    pg.set_default_timeout(config["default_timeout"])
    pg.set_default_navigation_timeout(config["navigation_timeout"])
    login = LoginPage(pg)
    login.navigate(config["base_url"])
    login.login(os.getenv("SIGNA_USERNAME"), os.getenv("SIGNA_PASSWORD"))
    pg.wait_for_url("**/dashboard")
    logger.info("Signa User session authenticated.")
    yield pg
    context.close()


@pytest.fixture(scope="session")
def update_user_data():
    return DataReader.load_yaml("testdata/update_user.yaml")


@pytest.fixture(scope="session")
def update_organization_data():
    return DataReader.load_yaml("testdata/update_organization.yaml")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        pg = item.funcargs.get("authenticated_page") or item.funcargs.get("page")
        if pg:
            screenshots_dir = Path(__file__).parent / "screenshots"
            screenshots_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename  = f"{item.name.replace('/', '_')}_{timestamp}.png"
            pg.screenshot(path=str(screenshots_dir / filename), full_page=True)
            print(f"\n Screenshot: {filename}")

@pytest.fixture(scope="session")
def env():
    return ENV
