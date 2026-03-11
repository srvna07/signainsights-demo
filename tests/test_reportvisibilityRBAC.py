import uuid
import pytest


@pytest.fixture
def created_orgs(new_organization_page, new_organization_data):
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
def created_reports(report_registration_page, report_registration_data, created_orgs):
    base_report = report_registration_data["new_report"]
    report_map  = {}

    report_registration_page.navigate_to_report_registration()

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


# Verify report visibility based on user role and organization RBAC
@pytest.mark.medium
def test_report_visibility_based_on_rbac(new_user_page, new_user_data, created_orgs, created_reports):
    user    = new_user_data["user"]
    contact = new_user_data["contact"]

    new_user_page.user_management_btn.click()

    org1, org2, org3       = created_orgs
    report1, report2, report3 = created_reports[org1], created_reports[org2], created_reports[org3]

    def create_user(first, last, primary_org, secondary_orgs, visible_reports, hidden_reports, assign_reports):
        uid      = uuid.uuid4().hex[:6]
        username = f"{user['usernamePrefix']}{uid}"
        email    = f"{username}{user['emailDomain']}"

        new_user_page.open_form()
        new_user_page.fill_basic_info(first, last, username, email)
        new_user_page.select_role("Admin")
        new_user_page.select_organization(primary_org)
        new_user_page.select_user_type("Organization Admin")
        new_user_page.select_secondary_orgs(*secondary_orgs)
        new_user_page.fill_contact_info(**contact)

        new_user_page.open_reports_dropdown()
        for r in visible_reports:
            new_user_page.verify_report_visible(r)
        for r in hidden_reports:
            new_user_page.verify_report_not_visible(r)
        new_user_page.close_reports_dropdown()

        new_user_page.select_reports(*assign_reports)
        new_user_page.submit_form()
        new_user_page.verify_success()

    create_user("Admin", "One", org1, [org2], [report1, report2], [report3], [report1, report2])
    create_user("Admin", "Two", org1, [org3], [report1, report3], [report2], [report1, report3])

    uid_common      = uuid.uuid4().hex[:6]
    username_common = f"{user['usernamePrefix']}{uid_common}"
    email_common    = f"{username_common}{user['emailDomain']}"

    new_user_page.open_form()
    new_user_page.fill_basic_info("Common", "User", username_common, email_common)
    new_user_page.select_role("Admin")
    new_user_page.select_organization(org1)
    new_user_page.select_user_type("Organization User")
    new_user_page.select_secondary_orgs(org2, org3)
    new_user_page.fill_contact_info(**contact)

    new_user_page.open_reports_dropdown()
    new_user_page.verify_report_visible(report1)
    new_user_page.verify_report_visible(report2)
    new_user_page.verify_report_visible(report3)
    new_user_page.close_reports_dropdown()

    new_user_page.select_reports(report1, report2, report3)
    new_user_page.submit_form()
    new_user_page.verify_success()