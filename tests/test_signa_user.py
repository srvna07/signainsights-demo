import pytest
from utils.data_factory import DataFactory
from utils.data_reader import DataReader
from pages.organizations_page import OrganizationsPage
from pages.report_registration_page import ReportRegistrationPage
from pages.newuser_page import NewUserPage


@pytest.fixture(scope="session")
def signa_org_name():
    return DataFactory.random_org_name("test_signa_org_")


@pytest.fixture(scope="session")
def signa_user_names():
    domain = DataReader.load_yaml("testdata/new_user.yaml")["user"]["emailDomain"]
    return {
        "signa":     {"username": DataFactory.random_username("test_signa_"),    "email": DataFactory.random_email("test_signa_",    domain)},
        "org_admin": {"username": DataFactory.random_username("test_orgadmin_"), "email": DataFactory.random_email("test_orgadmin_", domain)},
        "org_user":  {"username": DataFactory.random_username("test_orguser_"),  "email": DataFactory.random_email("test_orguser_",  domain)},
    }


@pytest.fixture(scope="session")
def signa_report_data():
    return {
        "report_name": DataFactory.generate_report_name("test_signa_report"),
        "menu_name":   DataFactory.generate_menu_name("test_signa_menu"),
        "edit_name":   DataFactory.generate_report_name("test_signa_edited_report"),
    }


@pytest.fixture
def signa_orgs_page(signa_page):
    return OrganizationsPage(signa_page)


@pytest.fixture
def signa_reports_page(signa_page):
    return ReportRegistrationPage(signa_page)


@pytest.fixture
def signa_users_page(signa_page):
    return NewUserPage(signa_page)


def create_user(users_page, first, last, username, email, role, org, user_type, contact):
    users_page.open_form()
    users_page.fill_basic_info(first, last, username, email)
    users_page.select_role(role)
    users_page.select_organization(org)
    users_page.select_user_type(user_type)
    users_page.fill_contact_info(**contact)
    users_page.submit_form()
    users_page.verify_success()
    users_page.verify_user_in_table(username)


# Verify organization can be created by signa user
@pytest.mark.medium
def test_signa_user_create_organization(signa_orgs_page, new_organization_data, signa_org_name):
    contact = new_organization_data["contact"]

    signa_orgs_page.open_form()
    signa_orgs_page.fill_basic_info(signa_org_name, DataFactory.random_string())
    signa_orgs_page.fill_contact_info(**contact)
    signa_orgs_page.submit_form()

    signa_orgs_page.verify_success()
    signa_orgs_page.verify_organization_in_table(signa_org_name)


# Verify report can be created by signa user
@pytest.mark.medium
def test_signa_user_create_report(signa_reports_page, signa_report_data, signa_org_name, report_registration_data):
    signa_reports_page.create_report(
        report_name=signa_report_data["report_name"],
        menu_name=signa_report_data["menu_name"],
        workspace_id=report_registration_data["new_report"]["work_space_id"],
        report_id=report_registration_data["new_report"]["report_id"],
        dataset_id=report_registration_data["new_report"]["dataset_id"],
        organization=signa_org_name,
    )

    signa_reports_page.search(signa_report_data["report_name"])
    signa_reports_page.verify_report_visible(signa_report_data["report_name"])


# Verify signa user can be created
@pytest.mark.medium
def test_signa_user_create_signa_user(signa_users_page, new_user_data, signa_user_names):
    names = signa_user_names["signa"]
    create_user(
        signa_users_page,
        first="Signa", last="User",
        username=names["username"], email=names["email"],
        role=new_user_data["role"],
        org=new_user_data["organization"],
        user_type="Signa User",
        contact=new_user_data["contact"],
    )


# Verify organization admin user can be created
@pytest.mark.medium
def test_signa_user_create_org_admin(signa_users_page, new_user_data, signa_user_names, signa_org_name):
    names = signa_user_names["org_admin"]
    create_user(
        signa_users_page,
        first="Org", last="Admin",
        username=names["username"], email=names["email"],
        role=new_user_data["role"],
        org=signa_org_name,
        user_type="Organization Admin",
        contact=new_user_data["contact"],
    )


# Verify organization user can be created
@pytest.mark.medium
def test_signa_user_create_org_user(signa_users_page, new_user_data, signa_user_names, signa_org_name):
    names = signa_user_names["org_user"]
    create_user(
        signa_users_page,
        first="Org", last="User",
        username=names["username"], email=names["email"],
        role=new_user_data["role"],
        org=signa_org_name,
        user_type="Organization User",
        contact=new_user_data["contact"],
    )


# Verify organization can be edited by signa user
@pytest.mark.medium
def test_signa_user_edit_organization(signa_orgs_page, signa_org_name, update_organization_data):
    signa_orgs_page.navigate_to_organizations()
    signa_orgs_page.edit_organization(signa_org_name)
    signa_orgs_page.update_organization(update_organization_data)
    signa_orgs_page.update_btn.click()

    signa_orgs_page.verify_update_success()
    signa_orgs_page.verify_organization_in_table(update_organization_data["updated_basic"]["name"])


# Verify report can be edited by signa user
@pytest.mark.medium
def test_signa_user_edit_report(signa_reports_page, signa_report_data):
    signa_reports_page.navigate_to()
    signa_reports_page.edit_report(
        report_name=signa_report_data["report_name"],
        new_name=signa_report_data["edit_name"],
        additional_roles=["Sales & Marketing"],
    )

    signa_reports_page.verify_report_visible(signa_report_data["edit_name"])


# Verify user can be edited by signa user
@pytest.mark.medium
def test_signa_user_edit_user(signa_users_page, signa_user_names, update_user_data, config_fixture):
    username = signa_user_names["org_admin"]["username"]

    signa_users_page.navigate_to_dashboard(config_fixture["base_url"])
    signa_users_page.user_management_btn.click()
    signa_users_page.edit_user(username)
    signa_users_page.update_user(update_user_data)
    signa_users_page.update_btn.click()

    signa_users_page.verify_update_success()


# Verify report can be deleted by signa user
@pytest.mark.medium
def test_signa_user_delete_report(signa_reports_page, signa_report_data):
    signa_reports_page.navigate_to()
    signa_reports_page.delete_report(signa_report_data["edit_name"])
    signa_reports_page.verify_report_not_visible(signa_report_data["edit_name"])


# Verify user can be deleted by signa user
@pytest.mark.medium
def test_signa_user_delete_user(signa_users_page, signa_user_names, config_fixture):
    username = signa_user_names["org_user"]["username"]

    signa_users_page.navigate_to_dashboard(config_fixture["base_url"])
    signa_users_page.user_management_btn.click()
    signa_users_page.delete_user(username)

    signa_users_page.verify_delete_success()
    signa_users_page.verify_user_not_in_table(username)


# Verify organization can be deleted by signa user
@pytest.mark.medium
def test_signa_user_delete_organization(signa_orgs_page, update_organization_data):
    org_name = update_organization_data["updated_basic"]["name"]

    signa_orgs_page.navigate_to_organizations()
    signa_orgs_page.delete_organization(org_name)

    signa_orgs_page.verify_delete_success()
    signa_orgs_page.verify_organization_not_in_table(org_name)


# Verify signa user cannot access super admin users in search
@pytest.mark.medium
def test_signa_user_cannot_access_super_admin(signa_users_page, super_admin_credentials):
    sa_username = super_admin_credentials["username"]
    signa_users_page.user_management_btn.click()
    signa_users_page.search_user(sa_username)
    signa_users_page.verify_user_not_in_table(sa_username)