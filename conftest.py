import os
import pytest
from pathlib import Path
from datetime import datetime
from playwright.sync_api import Page, Browser, Playwright

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

ENV    = get_env()
config = DataReader.load_yaml(f"configs/{ENV}.yaml")

AUTH_STATE_FILE       = Path("test-results/.auth/state.json")
SIGNA_AUTH_STATE_FILE = Path("test-results/.auth/signa_state.json")


# ---------------------------------------------------------------------------
# pytest-playwright: browser launch options
# Docs: https://playwright.dev/python/docs/test-runners#fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "args": ["--start-maximized"],
    }


# ---------------------------------------------------------------------------
# pytest-playwright: context options
# Docs: https://playwright.dev/python/docs/test-runners#fixtures
# Docs (videos): https://playwright.dev/python/docs/videos
#
# record_video_size set here — record_video_dir is injected automatically
# by the plugin when --video flag is used.
# storage_state is set here so every function-scoped page starts
# already authenticated (no login needed per test).
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    video_size = config.get("record_video_size", {"width": 1280, "height": 720})
    args = {
        **browser_context_args,
        "no_viewport": True,
        "record_video_size": video_size,
    }
    # Inject saved auth state once it exists (set up by setup_auth below)
    if AUTH_STATE_FILE.exists():
        args["storage_state"] = str(AUTH_STATE_FILE)
    return args


# ---------------------------------------------------------------------------
# Config fixture
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def config_fixture():
    return config


# ---------------------------------------------------------------------------
# Credentials fixtures — single source of truth, fail-fast if missing
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def credentials():
    username = os.getenv("APP_USERNAME")
    password = os.getenv("APP_PASSWORD")
    if not username or not password:
        pytest.exit("APP_USERNAME / APP_PASSWORD not set. Check your .env file.", returncode=1)
    return {"username": username, "password": password}


@pytest.fixture(scope="session")
def signa_credentials():
    username = os.getenv("SIGNA_USERNAME")
    password = os.getenv("SIGNA_PASSWORD")
    if not username or not password:
        pytest.exit("SIGNA_USERNAME / SIGNA_PASSWORD not set. Check your .env file.", returncode=1)
    return {"username": username, "password": password}


@pytest.fixture(scope="session")
def super_admin_credentials():
    username = os.getenv("SUPERADMIN_USERNAME")
    password = os.getenv("SUPERADMIN_PASSWORD")
    if not username or not password:
        pytest.exit("SUPERADMIN_USERNAME / SUPERADMIN_PASSWORD not set. Check your .env file.", returncode=1)
    return {"username": username, "password": password}


@pytest.fixture(scope="session")
def registered_email():
    email = os.getenv("REGISTERED_EMAIL")
    if not email:
        pytest.exit("REGISTERED_EMAIL not set. Check your .env file.", returncode=1)
    return email


# ---------------------------------------------------------------------------
# Auth setup — session-scoped, runs once before all tests.
#
# Docs (auth): https://playwright.dev/python/docs/auth
# The recommended pattern is: log in once, save storage_state to a file,
# then pass that file to every new context via browser_context_args.
# This gives each test a fresh isolated page that is already authenticated.
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def setup_auth(browser: Browser, credentials, signa_credentials):
    """Log in once per session for each user role and save auth state."""
    AUTH_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    # --- Main user ---
    context = browser.new_context(no_viewport=True)
    pg = context.new_page()
    pg.set_default_timeout(config["default_timeout"])
    pg.set_default_navigation_timeout(config["navigation_timeout"])
    login = LoginPage(pg)
    login.navigate(config["base_url"])
    login.login(credentials["username"], credentials["password"])
    pg.wait_for_url("**/dashboard")
    context.storage_state(path=str(AUTH_STATE_FILE))
    context.close()
    logger.info(f"Auth state saved → {AUTH_STATE_FILE}")

    # --- Signa user ---
    signa_context = browser.new_context(no_viewport=True)
    signa_pg = signa_context.new_page()
    signa_pg.set_default_timeout(config["default_timeout"])
    signa_pg.set_default_navigation_timeout(config["navigation_timeout"])
    signa_login = LoginPage(signa_pg)
    signa_login.navigate(config["base_url"])
    signa_login.login(signa_credentials["username"], signa_credentials["password"])
    signa_pg.wait_for_url("**/dashboard")
    signa_context.storage_state(path=str(SIGNA_AUTH_STATE_FILE))
    signa_context.close()
    logger.info(f"Signa auth state saved → {SIGNA_AUTH_STATE_FILE}")


# ---------------------------------------------------------------------------
# authenticated_page — function-scoped, uses saved auth state.
# Each test gets a fresh isolated page that is already logged in.
# Tracing and video are handled automatically by the plugin per-test.
# ---------------------------------------------------------------------------

@pytest.fixture
def authenticated_page(page: Page):
    """Function-scoped page pre-loaded with saved auth state."""
    page.set_default_timeout(config["default_timeout"])
    page.set_default_navigation_timeout(config["navigation_timeout"])
    page.goto(config["base_url"] + "/dashboard")
    return page


# ---------------------------------------------------------------------------
# signa_page — function-scoped, separate context with signa auth state.
# Docs (multiple contexts): https://playwright.dev/python/docs/test-runners
# ---------------------------------------------------------------------------

@pytest.fixture
def signa_page(browser: Browser):
    """Function-scoped page for the Signa user role."""
    context = browser.new_context(
        no_viewport=True,
        storage_state=str(SIGNA_AUTH_STATE_FILE),
        record_video_size=config.get("record_video_size", {"width": 1280, "height": 720}),
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    pg = context.new_page()
    pg.set_default_timeout(config["default_timeout"])
    pg.set_default_navigation_timeout(config["navigation_timeout"])

    yield pg

    # Docs (trace): https://playwright.dev/python/docs/trace-viewer-intro
    # Docs (video): https://playwright.dev/python/docs/videos — saved on close
    output_dir = Path("test-results")
    output_dir.mkdir(parents=True, exist_ok=True)
    context.tracing.stop(path=str(output_dir / "signa-trace.zip"))
    context.close()


# ---------------------------------------------------------------------------
# Page object fixtures — function-scoped to match the plugin's page fixture.
# Docs: https://playwright.dev/python/docs/test-runners#fixtures
# "Function scope: created when requested in a test, destroyed when test ends"
# ---------------------------------------------------------------------------

@pytest.fixture
def login_page(page: Page):
    page.set_default_timeout(config["default_timeout"])
    page.set_default_navigation_timeout(config["navigation_timeout"])
    return LoginPage(page)

@pytest.fixture
def forgot_password_page(page: Page):
    return ForgotPasswordPage(page)

@pytest.fixture
def landing_page(page: Page):
    return LandingPage(page)

@pytest.fixture
def new_user_page(authenticated_page: Page):
    return NewUserPage(authenticated_page)

@pytest.fixture
def new_organization_page(authenticated_page: Page):
    return OrganizationsPage(authenticated_page)

@pytest.fixture
def report_registration_page(authenticated_page: Page):
    return ReportRegistrationPage(authenticated_page)


# ---------------------------------------------------------------------------
# Data fixtures — session-scoped so test data is generated once per run
# ---------------------------------------------------------------------------

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
def update_user_data():
    return DataReader.load_yaml("testdata/update_user.yaml")


@pytest.fixture(scope="session")
def update_organization_data():
    return DataReader.load_yaml("testdata/update_organization.yaml")


# ---------------------------------------------------------------------------
# Failure screenshot hook
# Covers authenticated_page and signa_page which are not the plugin's
# default page fixture and so are not covered by --screenshot flag.
# ---------------------------------------------------------------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep     = outcome.get_result()
    if rep.when == "call" and rep.failed:
        pg = item.funcargs.get("authenticated_page") or item.funcargs.get("signa_page")
        if pg:
            screenshots_dir = Path(__file__).parent / "screenshots"
            screenshots_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename  = f"{item.name.replace('/', '_')}_{timestamp}.png"
            pg.screenshot(path=str(screenshots_dir / filename), full_page=True)
            print(f"\n Screenshot: {filename}")
