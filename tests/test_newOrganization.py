import pytest


# Verify organization can be created successfully
@pytest.mark.smoke
def test_create_organization_success(new_organization_page, new_organization_data):
    org     = new_organization_data["organization"]
    contact = new_organization_data["contact"]

    new_organization_page.open_form()
    new_organization_page.fill_basic_info(org["namePrefix"], org["franchise_id"])
    new_organization_page.fill_contact_info(**contact)
    new_organization_page.submit_form()

    new_organization_page.verify_success()


# Verify duplicate organization shows error
@pytest.mark.smoke
def test_create_duplicate_organization_shows_error(new_organization_page, new_organization_data):
    org     = new_organization_data["organization"]
    contact = new_organization_data["contact"]

    new_organization_page.open_form()
    new_organization_page.fill_basic_info(org["namePrefix"], "FRAN123")
    new_organization_page.fill_contact_info(**contact)
    new_organization_page.submit_form()

    new_organization_page.verify_duplicate_error()
    new_organization_page.cancel_btn.click()


# Verify organization can be edited successfully
@pytest.mark.smoke
def test_edit_organization_updates(new_organization_page, new_organization_data,
                                   update_organization_data, config_fixture):
    org_name = new_organization_data["organization"]["namePrefix"]

    new_organization_page.navigate_to(config_fixture["base_url"] + "/dashboard")
    new_organization_page.navigate_to_organizations()
    new_organization_page.edit_organization(org_name)
    new_organization_page.update_organization(update_organization_data)
    new_organization_page.update_btn.click()

    new_organization_page.verify_update_success()
    new_organization_page.verify_organization_in_table(update_organization_data["updated_basic"]["name"])


# Verify organization can be deleted successfully
@pytest.mark.smoke
def test_delete_organization_success(new_organization_page, update_organization_data, config_fixture):
    org_name = update_organization_data["updated_basic"]["name"]

    new_organization_page.navigate_to(config_fixture["base_url"] + "/dashboard")
    new_organization_page.navigate_to_organizations()
    new_organization_page.delete_organization(org_name)

    new_organization_page.verify_delete_success()
    new_organization_page.verify_organization_not_in_table(org_name)