import pytest
from playwright.sync_api import expect


# Verify organization can be created for report registration
@pytest.mark.medium
def test_create_organization_for_report_registration(new_organization_page, new_organization_data):
    org     = new_organization_data["organization"]
    contact = new_organization_data["contact"]

    new_organization_page.open_form()
    new_organization_page.fill_basic_info(org["namePrefix"], org["franchise_id"])
    new_organization_page.fill_contact_info(**contact)
    new_organization_page.submit_form()

    new_organization_page.verify_success()


# Verify report can be created successfully
@pytest.mark.medium
def test_create_report_success(report_registration_page, report_registration_data, new_organization_data):
    new_report = report_registration_data["new_report"]
    org_name   = new_organization_data["organization"]["namePrefix"]

    report_registration_page.create_report(
        report_name=new_report["report_name"],
        menu_name=new_report["menu_name"],
        workspace_id=new_report["work_space_id"],
        report_id=new_report["report_id"],
        dataset_id=new_report["dataset_id"],
        organization=org_name
    )

    report_registration_page.verify_report_visible(new_report["report_name"])


# Verify report can be edited successfully
@pytest.mark.medium
def test_edit_report_success(report_registration_page, report_registration_data):
    new_report  = report_registration_data["new_report"]
    edit_report = report_registration_data["edit_report"]

    report_registration_page.navigate_to()
    report_registration_page.edit_report(
        report_name=new_report["report_name"],
        new_name=edit_report["report_name"],
        additional_roles=["Sales & Marketing"]
    )

    report_registration_page.verify_report_visible(edit_report["report_name"])


# Verify report search functionality works
@pytest.mark.medium
def test_search_report_returns_expected_result(report_registration_page, report_registration_data):
    report_name = report_registration_data["edit_report"]["report_name"]

    report_registration_page.navigate_to()
    report_registration_page.search(report_name)
    report_registration_page.verify_search_result(report_name)
    report_registration_page.clear_search()


# Verify table displays maximum 5 rows per page
@pytest.mark.low
def test_rows_per_page_5(authenticated_page, report_registration_page):
    report_registration_page.navigate_to()
    report_registration_page.set_rows_per_page(5)
    rows = authenticated_page.locator("table tbody tr")
    expect(rows.first).to_be_visible()
    assert rows.count() <= 5


# Verify table displays maximum 25 rows per page
@pytest.mark.low
def test_rows_per_page_25(authenticated_page, report_registration_page):
    report_registration_page.navigate_to()
    report_registration_page.set_rows_per_page(25)
    rows = authenticated_page.locator("table tbody tr")
    assert rows.count() <= 25


# Verify report can be deleted successfully
@pytest.mark.medium
def test_delete_report_success(report_registration_page, report_registration_data):
    report_name = report_registration_data["edit_report"]["report_name"]

    report_registration_page.navigate_to()
    report_registration_page.delete_report(report_name)
    report_registration_page.verify_report_not_visible(report_name)


# Verify organization can be deleted successfully
@pytest.mark.medium
def test_delete_organization_success(new_organization_page, new_organization_data):
    org_name = new_organization_data["organization"]["namePrefix"]

    new_organization_page.navigate_to_organizations()
    new_organization_page.delete_organization(org_name)
    new_organization_page.verify_delete_success()