import pytest
import uuid
from playwright.sync_api import expect
from pages.dashboard_page import DashboardPage




# ── Create new organization ────────────────────────────────────────────────────
@pytest.fixture
def create_new_organization(authenticated_page, new_organization_page, new_organization_data):
    page = new_organization_page

    org    = new_organization_data["organization"]
    contact = new_organization_data["contact"]

    page.open_form()

    page.fill_basic_info(
        org_name=org["namePrefix"],
        franchise_id=org["franchise_id"]
    )

    
    page.fill_contact_info(**contact)
    

    page.submit_form()
    page.verify_success()

    return org["namePrefix"]

@pytest.fixture
def create_new_report(authenticated_page, report_registration_page, report_registration_data, new_organization_data):
    # Use 'report_registration_data' for everything to stay consistent
    new_report = report_registration_data["new_report"]
    org    = new_organization_data["organization"]
    
    # FIX: Get organization name from the global org_data since it's loaded at the top
    # or from the merged fixture if you updated it as shown above
    org_name_prefix = org["namePrefix"] 
    
    report_registration_page.create_report(
        report_name=new_report["report_name"],
        menu_name=new_report["menu_name"],
        workspace_id=new_report["work_space_id"],
        report_id=new_report["report_id"],
        dataset_id=new_report["dataset_id"],
        organization=org_name_prefix
    )
    expect(authenticated_page.get_by_text(new_report["report_name"])).to_be_visible()
    return new_report["report_name"]

# =========================================================
# TEST — Dashboard Checkbox Visibility
# =========================================================
@pytest.mark.smoke
def test_dashboard_report_visibility(
    authenticated_page,
    existing_user_page,
    new_user_data,
    new_user_page,
    report_registration_page,
    create_new_organization,
    create_new_report,
    new_organization_data,
    new_organization_page,
    report_registration_data,
    env,
    config_fixture
):

    user = new_user_data["user"]
    contact = new_user_data["contact"]

    # =====================================================
    # STEP 1 — Create User With Org + Report
    # =====================================================
    username ="pravin"
    org_name   = new_organization_data["organization"]["namePrefix"]

    new_user_page.navigate_to_dashboard(config_fixture["base_url"])
    new_user_page.user_management_btn.click()
    new_user_page.edit_user(username)
    new_user_page.select_organization(org_name)
    
    


    new_user_page.open_reports_dropdown()
    org_report = report_registration_data["new_report"]["report_name"]  # Get the report name created in the fixture
    new_user_page.verify_report_visible(org_report)
    new_user_page.close_reports_dropdown()
    new_user_page.select_reports(org_report)
    

    new_user_page.verify_update_success()


    # =====================================================
    # STEP 2 — Enable Dashboard Checkbox
    # =====================================================
    report_registration_page.navigate_to()
    report_registration_page.search(org_report)
    report_registration_page.click_edit(org_report)

    # Click Dashboard Checkbox
    report_registration_page.dashboard_checkbox_is_checked()

    report_registration_page.confirm_update()
    report_registration_page.verify_update_success()

    # =====================================================
    # STEP 3 — Navigate To Dashboard & Verify
    # =====================================================


    new_user_page.navigate_to_dashboard(config_fixture["base_url"])
    if env.lower() == "dev":
        pytest.skip(
            "Skipping dashboard verification on dev environment due to known issue with test data isolation."
        )

    # This will execute ONLY if env is NOT dev
    dashboard = DashboardPage(existing_user_page)
    dashboard.verify_dashboard_cards_visible()

