import pytest
from utils.data_reader import DataReader
from utils.data_factory import DataFactory
from pages.super_admin_page import SuperAdminPage


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

    page = data.get("_page")
    if page is None:
        return

    cfg = DataReader.load_yaml(f"configs/{__import__('utils.env_loader', fromlist=['get_env']).get_env()}.yaml")
    sa_page = SuperAdminPage(page)

    for username in [
        data["super_admin_user"]["username"],
        data["users_to_create"]["signa_user"]["username"],
        data["users_to_create"]["org_admin"]["username"],
        data["users_to_create"]["org_user"]["username"],
        data["target_user_for_modification"]["username"],
    ]:
        try:
            page.goto(f"{cfg['base_url'].rstrip('/')}/dashboard")
            page.wait_for_load_state("networkidle")
            sa_page.delete_user_if_exists(username)
        except Exception:
            pass


@pytest.fixture(scope="session")
def super_admin_page(page, super_admin_data):
    context = page.context.browser.new_context(no_viewport=True)
    pg = context.new_page()
    from utils.data_reader import DataReader as DR
    from utils.env_loader import get_env
    from pages.login_page import LoginPage
    import os
    cfg = DR.load_yaml(f"configs/{get_env()}.yaml")
    login = LoginPage(pg)
    login.navigate(cfg["base_url"])
    login.login(os.getenv("USERNAME"), os.getenv("PASSWORD"))
    pg.wait_for_url("**/dashboard")
    super_admin_data["_page"] = pg
    yield SuperAdminPage(pg)
    context.close()


@pytest.mark.smoke
@pytest.mark.critical
def test_super_admin_has_full_sidebar_access(super_admin_page):
    super_admin_page.navigate_to_dashboard()
    super_admin_page.verify_full_sidebar_access()


@pytest.mark.smoke
@pytest.mark.high
def test_super_admin_can_see_all_user_type_options(super_admin_page):
    super_admin_page.navigate_to_dashboard()
    super_admin_page.verify_all_user_type_options_available()


@pytest.mark.smoke
@pytest.mark.critical
def test_super_admin_can_create_super_admin(super_admin_page, super_admin_data):
    user = super_admin_data["super_admin_user"]
    super_admin_page.navigate_to_dashboard()
    super_admin_page.create_user(user, user["username"], user["email"])
    super_admin_page.verify_user_in_table(user["username"])


@pytest.mark.smoke
@pytest.mark.high
def test_super_admin_can_create_signa_user(super_admin_page, super_admin_data):
    user = super_admin_data["users_to_create"]["signa_user"]
    super_admin_page.navigate_to_dashboard()
    super_admin_page.create_user(user, user["username"], user["email"])
    super_admin_page.verify_user_in_table(user["username"])


@pytest.mark.smoke
@pytest.mark.high
def test_super_admin_can_create_organization_admin(super_admin_page, super_admin_data):
    user = super_admin_data["users_to_create"]["org_admin"]
    super_admin_page.navigate_to_dashboard()
    super_admin_page.create_user(user, user["username"], user["email"])
    super_admin_page.verify_user_in_table(user["username"])


@pytest.mark.smoke
@pytest.mark.high
def test_super_admin_can_create_organization_user(super_admin_page, super_admin_data):
    user = super_admin_data["users_to_create"]["org_user"]
    super_admin_page.navigate_to_dashboard()
    super_admin_page.create_user(user, user["username"], user["email"])
    super_admin_page.verify_user_in_table(user["username"])


@pytest.mark.smoke
@pytest.mark.high
def test_super_admin_can_access_report_registration(super_admin_page):
    super_admin_page.navigate_to_dashboard()
    super_admin_page.verify_report_registration_page_accessible()


@pytest.mark.smoke
@pytest.mark.high
def test_super_admin_can_access_organization_registration(super_admin_page):
    super_admin_page.navigate_to_dashboard()
    super_admin_page.verify_organizations_page_accessible()


@pytest.mark.smoke
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


@pytest.mark.smoke
@pytest.mark.critical
def test_super_admin_can_delete_any_user(super_admin_page, super_admin_data):
    target = super_admin_data["target_user_for_modification"]
    super_admin_page.navigate_to_dashboard()
    super_admin_page.delete_user(target["username"])
    super_admin_page.verify_user_not_in_table(target["username"])