import pytest


# Verify user can be created successfully and appears in table
@pytest.mark.smoke
def test_create_new_user(authenticated_page, new_user_page, new_user_data, config_fixture):
    page    = new_user_page
    user    = new_user_data["user"]
    contact = new_user_data["contact"]

    page.open_form()
    page.fill_basic_info(user["firstName"], user["lastName"], user["username"], user["email"])
    page.select_role(new_user_data["role"])
    page.select_organization(new_user_data["organization"])
    page.select_user_type(new_user_data["userType"])
    page.select_secondary_orgs(*new_user_data["secondaryOrganizations"])
    page.fill_contact_info(**contact)
    page.select_reports(*new_user_data["reports"])
    page.submit_form()

    page.verify_success()
    page.verify_user_in_table(user["username"])


# Verify user can be edited successfully
@pytest.mark.smoke
def test_edit_user_updates_user(authenticated_page, new_user_page, new_user_data, update_user_data):
    page     = new_user_page
    username = new_user_data["user"]["username"]

    page.user_management_btn.click()
    page.edit_user(username)
    page.update_user(update_user_data)
    page.update_btn.click()

    page.verify_update_success()


# Verify user can be deleted successfully and is removed from table
@pytest.mark.smoke
def test_delete_user_removes_from_table(authenticated_page, new_user_page, new_user_data, config_fixture):
    page     = new_user_page
    username = new_user_data["user"]["username"]

    page.navigate_to_dashboard(config_fixture["base_url"])
    page.user_management_btn.click()
    page.delete_user(username)

    page.verify_delete_success()
    page.verify_user_not_in_table(username)
