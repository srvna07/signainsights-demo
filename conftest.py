import os
import pytest
from pathlib import Path
from datetime import datetime
from playwright.sync_api import Page, Browser

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

AUTH_STATE_FILE           = Path("test-results/.auth/state.json")
SIGNA_AUTH_STATE_FILE     = Path("test-results/.auth/signa_state.json")
ORG_USER_AUTH_STATE_FILE  = Path("test-results/.auth/org_user_state.json")
ORG_ADMIN_AUTH_STATE_FILE = Path("test-results/.auth/org_admin_state.json")

_failed_key = pytest.StashKey()


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {**browser_type_launch_args, "args": ["--start-maximized"]}


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    args = {
        **browser_context_args,
        "no_viewport": True,
        "record_video_size": config.get("record_video_size", {"width": 1280, "height": 720}),
    }
    if AUTH_STATE_FILE.exists():
        args["storage_state"] = str(AUTH_STATE_FILE)
    return args


@pytest.fixture(scope="session")
def config_fixture():
    return config


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
def org_user_credentials():
    username = os.getenv("ORG_USER_USERNAME")
    password = os.getenv("ORG_USER_PASSWORD")
    if not username or not password:
        pytest.exit("ORG_USER_USERNAME / ORG_USER_PASSWORD not set. Check your .env file.", returncode=1)
    return {"username": username, "password": password}


@pytest.fixture(scope="session")
def org_admin_credentials():
    username = os.getenv("ORG_ADMIN_USERNAME")
    password = os.getenv("ORG_ADMIN_PASSWORD")
    if not username or not password:
        pytest.exit("ORG_ADMIN_USERNAME / ORG_ADMIN_PASSWORD not set. Check your .env file.", returncode=1)
    return {"username": username, "password": password}


@pytest.fixture(scope="session")
def registered_email():
    email = os.getenv("REGISTERED_EMAIL")
    if not email:
        pytest.exit("REGISTERED_EMAIL not set. Check your .env file.", returncode=1)
    return email


@pytest.fixture(scope="session", autouse=True)
def setup_auth(browser: Browser, credentials, signa_credentials, org_user_credentials, org_admin_credentials):
    AUTH_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

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

    org_user_context = browser.new_context(no_viewport=True)
    org_user_pg = org_user_context.new_page()
    org_user_pg.set_default_timeout(config["default_timeout"])
    org_user_pg.set_default_navigation_timeout(config["navigation_timeout"])
    org_user_login = LoginPage(org_user_pg)
    org_user_login.navigate(config["base_url"])
    org_user_login.login(org_user_credentials["username"], org_user_credentials["password"])
    org_user_pg.wait_for_url("**/dashboard")
    org_user_context.storage_state(path=str(ORG_USER_AUTH_STATE_FILE))
    org_user_context.close()
    logger.info(f"Org user auth state saved → {ORG_USER_AUTH_STATE_FILE}")

    org_admin_context = browser.new_context(no_viewport=True)
    org_admin_pg = org_admin_context.new_page()
    org_admin_pg.set_default_timeout(config["default_timeout"])
    org_admin_pg.set_default_navigation_timeout(config["navigation_timeout"])
    org_admin_login = LoginPage(org_admin_pg)
    org_admin_login.navigate(config["base_url"])
    org_admin_login.login(org_admin_credentials["username"], org_admin_credentials["password"])
    org_admin_pg.wait_for_url("**/dashboard")
    org_admin_context.storage_state(path=str(ORG_ADMIN_AUTH_STATE_FILE))
    org_admin_context.close()
    logger.info(f"Org admin auth state saved → {ORG_ADMIN_AUTH_STATE_FILE}")


def _safe_name(request) -> str:
    return (
        request.node.name
        .replace("/", "_").replace("\\", "_")
        .replace("[", "_").replace("]", "_")
        .replace(" ", "_")
    )


def _teardown(context, pg, request, prefix: str):
    failed    = request.node.stash.get(_failed_key, False)
    test_name = _safe_name(request)
    if failed:
        failure_dir = Path(f"test-results/failures/{prefix}-{test_name}")
        failure_dir.mkdir(parents=True, exist_ok=True)
        # Save trace
        context.tracing.stop(path=str(failure_dir / "trace.zip"))
        # Save screenshot
        pg.screenshot(path=str(failure_dir / "screenshot.png"), full_page=True)
        # Save video — must close context first, then move
        context.close()
        if pg.video:
            pg.video.save_as(str(failure_dir / "video.webm"))
        print(f"\n Failure artifacts → {failure_dir}")
    else:
        context.tracing.stop()
        context.close()
        if pg.video:
            pg.video.delete()


@pytest.fixture
def authenticated_page(page: Page):
    page.set_default_timeout(config["default_timeout"])
    page.set_default_navigation_timeout(config["navigation_timeout"])
    page.goto(config["base_url"] + "/user-management")
    return page


@pytest.fixture
def signa_page(browser: Browser, request):
    context = browser.new_context(
        no_viewport=True,
        storage_state=str(SIGNA_AUTH_STATE_FILE),
        record_video_dir="test-results/.tmp-video/signa",
        record_video_size=config.get("record_video_size", {"width": 1280, "height": 720}),
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    pg = context.new_page()
    pg.set_default_timeout(config["default_timeout"])
    pg.set_default_navigation_timeout(config["navigation_timeout"])
    pg.goto(config["base_url"] + "/user-management")
    yield pg
    _teardown(context, pg, request, "signa")


@pytest.fixture
def org_user_page(browser: Browser, request):
    context = browser.new_context(
        no_viewport=True,
        storage_state=str(ORG_USER_AUTH_STATE_FILE),
        record_video_dir="test-results/.tmp-video/org-user",
        record_video_size=config.get("record_video_size", {"width": 1280, "height": 720}),
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    pg = context.new_page()
    pg.set_default_timeout(config["default_timeout"])
    pg.set_default_navigation_timeout(config["navigation_timeout"])
    pg.goto(config["base_url"] + "/dashboard")
    yield pg
    _teardown(context, pg, request, "org-user")


@pytest.fixture
def org_admin_page(browser: Browser, request):
    context = browser.new_context(
        no_viewport=True,
        storage_state=str(ORG_ADMIN_AUTH_STATE_FILE),
        record_video_dir="test-results/.tmp-video/org-admin",
        record_video_size=config.get("record_video_size", {"width": 1280, "height": 720}),
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    pg = context.new_page()
    pg.set_default_timeout(config["default_timeout"])
    pg.set_default_navigation_timeout(config["navigation_timeout"])
    pg.goto(config["base_url"] + "/dashboard")
    yield pg
    _teardown(context, pg, request, "org-admin")


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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep     = outcome.get_result()
    if rep.when == "call":
        item.stash[_failed_key] = rep.failed