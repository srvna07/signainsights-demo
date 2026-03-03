import pytest
from utils.data_reader import DataReader
from utils.data_factory import DataFactory
from utils.env_loader import get_env
from pages.login_page import LoginPage
from pages.super_admin_page import SuperAdminPage

ENV    = get_env()
config = DataReader.load_yaml(f"configs/{ENV}.yaml")


@pytest.fixture(scope="session")
def super_admin_data():
    data = DataReader.load_yaml("testdata/super_admin.yaml")

    sa = data["super_admin_user"]
    sa["username"] = DataFactory.random_username(sa["usernamePrefix"])
    sa["email"]    = DataFactory.random_email(sa["usernamePrefix"], sa["emailDomain"])

    for key in ["signa_user", "org_admin", "org_user"]:
        u = data["users_to_create"][key]
        u["username"] = DataFactory.random_username(u["usernamePrefix"])
        u["email"]    = DataFactory.random_email(u["usernamePrefix"], u["emailDomain"])

    t = data["target_user_for_modification"]
    t["username"] = DataFactory.random_username(t["usernamePrefix"])
    t["email"]    = DataFactory.random_email(t["usernamePrefix"], t["emailDomain"])

    yield data

    pg = data.get("_page")
    if pg is None:
        return

    sa_page = SuperAdminPage(pg)
    for username in [
        data["super_admin_user"]["username"],
        data["users_to_create"]["signa_user"]["username"],
        data["users_to_create"]["org_admin"]["username"],
        data["users_to_create"]["org_user"]["username"],
        data["target_user_for_modification"]["username"],
    ]:
        try:
            pg.goto(f"{config['base_url'].rstrip('/')}/dashboard")
            sa_page.delete_user_if_exists(username)
        except Exception:
            pass


@pytest.fixture
def super_admin_page(browser, super_admin_data):
    from pathlib import Path
    auth_state = Path("test-results/.auth/state.json")
    context    = browser.new_context(
        no_viewport=True,
        storage_state=str(auth_state) if auth_state.exists() else None,
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    pg = context.new_page()
    pg.set_default_timeout(config["default_timeout"])
    pg.set_default_navigation_timeout(config["navigation_timeout"])
    pg.goto(config["base_url"] + "/dashboard")

    super_admin_data["_page"] = pg
    yield SuperAdminPage(pg)

    output_dir = Path("test-results")
    output_dir.mkdir(parents=True, exist_ok=True)
    context.tracing.stop(path=str(output_dir / "super-admin-trace.zip"))
    context.close()


# Verify super admin has full sidebar access to all pages
@pytest.mark.critical
def test_super_admin_has_full_sidebar_access(super_admin_page):
    super_admin_page.navigate_to_dashboard()
    super_admin_page.verify_full_sidebar_access()


# Verify super admin can see all user type options
@pytest.mark.high
def test_super_admin_can_see_all_user_type_options(super_admin_page):
    super_admin_page.navigate_to_dashboard()
    super_admin_page.verify_all_user_type_options_available()


# Verify super admin can create another super admin user
@pytest.mark.critical
def test_super_admin_can_create_super_admin(super_admin_page, super_admin_data):
    user = super_admin_data["super_admin_user"]
    super_admin_page.navigate_to_dashboard()
    super_admin_page.create_user(user, user["username"], user["email"])
    super_admin_page.verify_user_in_table(user["username"])


# Verify super admin can create signa user
@pytest.mark.high
def test_super_admin_can_create_signa_user(super_admin_page, super_admin_data):
    user = super_admin_data["users_to_create"]["signa_user"]
    super_admin_page.navigate_to_dashboard()
    super_admin_page.create_user(user, user["username"], user["email"])
    super_admin_page.verify_user_in_table(user["username"])


# Verify super admin can create organization admin user
@pytest.mark.high
def test_super_admin_can_create_organization_admin(super_admin_page, super_admin_data):
    user = super_admin_data["users_to_create"]["org_admin"]
    super_admin_page.navigate_to_dashboard()
    super_admin_page.create_user(user, user["username"], user["email"])
    super_admin_page.verify_user_in_table(user["username"])


# Verify super admin can create organization user
@pytest.mark.high
def test_super_admin_can_create_organization_user(super_admin_page, super_admin_data):
    user = super_admin_data["users_to_create"]["org_user"]
    super_admin_page.navigate_to_dashboard()
    super_admin_page.create_user(user, user["username"], user["email"])
    super_admin_page.verify_user_in_table(user["username"])


# Verify super admin can access report registration page
@pytest.mark.high
def test_super_admin_can_access_report_registration(super_admin_page):
    super_admin_page.navigate_to_dashboard()
    super_admin_page.verify_report_registration_page_accessible()


# Verify super admin can access organization registration page
@pytest.mark.high
def test_super_admin_can_access_organization_registration(super_admin_page):
    super_admin_page.navigate_to_dashboard()
    super_admin_page.verify_organizations_page_accessible()


# Verify super admin can modify any user
@pytest.mark.critical
def test_super_admin_can_modify_any_user(super_admin_page, super_admin_data):
    target = super_admin_data["target_user_for_modification"]
    super_admin_page.navigate_to_dashboard()
    super_admin_page.create_user(target, target["username"], target["email"])
    super_admin_page.verify_user_in_table(target["username"])
    super_admin_page.modify_user_name(
        username=target["username"],
        new_first=target["updated_firstName"],
        new_last=target["updated_lastName"],
    )


# Verify super admin can delete any user
@pytest.mark.critical
def test_super_admin_can_delete_any_user(super_admin_page, super_admin_data):
    target = super_admin_data["target_user_for_modification"]
    super_admin_page.navigate_to_dashboard()
    super_admin_page.delete_user(target["username"])
    super_admin_page.verify_user_not_in_table(target["username"])
