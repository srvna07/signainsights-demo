import pytest


# Verify organization can be created successfully
@pytest.mark.smoke
def test_create_organization_success(authenticated_page, new_organization_page, new_organization_data):
    page    = new_organization_page
    org     = new_organization_data["organization"]
    contact = new_organization_data["contact"]

    page.open_form()
    page.fill_basic_info(org["namePrefix"], org["franchise_id"])
    page.fill_contact_info(**contact)
    page.submit_form()

    page.verify_success()


# Verify duplicate organization shows error
@pytest.mark.smoke
def test_create_duplicate_organization_shows_error(authenticated_page, new_organization_page, new_organization_data):
    page    = new_organization_page
    org     = new_organization_data["organization"]
    contact = new_organization_data["contact"]

    page.open_form()
    page.fill_basic_info(org["namePrefix"], "FRAN123")
    page.fill_contact_info(**contact)
    page.submit_form()

    page.verify_duplicate_error()
    page.cancel_btn.click()


# Verify organization can be edited successfully
def test_edit_organization_updates(authenticated_page, new_organization_page, new_organization_data,
                                   update_organization_data, config_fixture):
    page     = new_organization_page
    org_name = new_organization_data["organization"]["namePrefix"]

    page.navigate_to(config_fixture["base_url"] + "/dashboard")
    page.navigate_to_organizations()
    page.edit_organization(org_name)
    page.update_organization(update_organization_data)
    page.update_btn.click()

    page.verify_update_success()
    page.verify_organization_in_table(update_organization_data["updated_basic"]["name"])


# Verify organization can be deleted successfully
@pytest.mark.smoke
def test_delete_organization_success(authenticated_page, new_organization_page, update_organization_data,
                                     config_fixture):
    page     = new_organization_page
    org_name = update_organization_data["updated_basic"]["name"]

    page.navigate_to(config_fixture["base_url"] + "/dashboard")
    page.navigate_to_organizations()
    page.delete_organization(org_name)

    page.verify_delete_success()
    page.verify_organization_not_in_table(org_name)
