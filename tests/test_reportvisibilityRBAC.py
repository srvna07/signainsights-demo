import uuid
import pytest
from playwright.sync_api import expect

from utils.data_reader import DataReader
from utils.data_factory import DataFactory


@pytest.fixture
def created_orgs(authenticated_page, new_organization_page, new_organization_data):
    base_org = new_organization_data["organization"]
    contact  = new_organization_data["contact"]
    orgs     = []

    for i in range(3):
        unique       = uuid.uuid4().hex[:4]
        org_name     = f"{base_org['namePrefix']}_{i}_{unique}"
        franchise_id = f"{base_org['franchise_id']}_{i}_{unique}"

        new_organization_page.open_form()
        new_organization_page.fill_basic_info(org_name, franchise_id)
        new_organization_page.fill_contact_info(**contact)
        new_organization_page.submit_form()
        new_organization_page.verify_success()

        orgs.append(org_name)

    return orgs


@pytest.fixture
def created_reports(authenticated_page, report_registration_page, report_registration_data, created_orgs):
    base_report = report_registration_data["new_report"]
    report_map  = {}

    report_registration_page.navigate_to()

    for i, org_name in enumerate(created_orgs):
        unique      = uuid.uuid4().hex[:4]
        report_name = f"{base_report['report_name']}_{i}_{unique}"
        menu_name   = f"{base_report['menu_name']}_{i}_{unique}"

        report_registration_page.create_report(
            report_name=report_name,
            menu_name=menu_name,
            workspace_id=f"{base_report['work_space_id']}_{unique}",
            report_id=f"{base_report['report_id']}_{unique}",
            dataset_id=f"{base_report['dataset_id']}_{unique}",
            organization=org_name
        )
        report_map[org_name] = report_name

    return report_map


@pytest.mark.smoke
def test_report_visibility_rbac(authenticated_page, new_user_page, new_user_data,
                                created_orgs, created_reports):
    page    = new_user_page
    user    = new_user_data["user"]
    contact = new_user_data["contact"]

    expect(page.user_management_btn).to_be_visible()
    page.user_management_btn.click()

    org1, org2, org3 = created_orgs
    report1, report2, report3 = created_reports[org1], created_reports[org2], created_reports[org3]

    def create_user(first, last, primary_org, secondary_orgs, visible_reports, hidden_reports, assign_reports):
        uid      = uuid.uuid4().hex[:6]
        username = f"{user['usernamePrefix']}{uid}"
        email    = f"{username}{user['emailDomain']}"

        page.open_form()
        page.fill_basic_info(first, last, username, email)
        page.select_role("Admin")
        page.select_organization(primary_org)
        page.select_user_type("Organization Admin")
        page.select_secondary_orgs(*secondary_orgs)
        page.fill_contact_info(**contact)

        page.open_reports_dropdown()
        for r in visible_reports:
            page.verify_report_visible(r)
        for r in hidden_reports:
            page.verify_report_not_visible(r)
        page.close_reports_dropdown()

        page.select_reports(*assign_reports)
        page.submit_form()
        page.verify_success()

    create_user("Admin", "One", org1, [org2], [report1, report2], [report3], [report1, report2])
    create_user("Admin", "Two", org1, [org3], [report1, report3], [report2], [report1, report3])

    uid_common      = uuid.uuid4().hex[:6]
    username_common = f"{user['usernamePrefix']}{uid_common}"
    email_common    = f"{username_common}{user['emailDomain']}"

    page.open_form()
    page.fill_basic_info("Common", "User", username_common, email_common)
    page.select_role("Admin")
    page.select_organization(org1)
    page.select_user_type("Organization User")
    page.select_secondary_orgs(org2, org3)
    page.fill_contact_info(**contact)

    page.open_reports_dropdown()
    page.verify_report_visible(report1)
    page.verify_report_visible(report2)
    page.verify_report_visible(report3)
    page.close_reports_dropdown()

    page.select_reports(report1, report2, report3)
    page.submit_form()
    page.verify_success()
