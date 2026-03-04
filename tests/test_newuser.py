import pytest


# Verify user can be created successfully and appears in table
@pytest.mark.smoke
def test_create_new_user(new_user_page, new_user_data):
    user    = new_user_data["user"]
    contact = new_user_data["contact"]

    new_user_page.open_form()
    new_user_page.fill_basic_info(user["firstName"], user["lastName"], user["username"], user["email"])
    new_user_page.select_role(new_user_data["role"])
    new_user_page.select_organization(new_user_data["organization"])
    new_user_page.select_user_type(new_user_data["userType"])
    new_user_page.select_secondary_orgs(*new_user_data["secondaryOrganizations"])
    new_user_page.fill_contact_info(**contact)
    new_user_page.select_reports(*new_user_data["reports"])
    new_user_page.submit_form()

    new_user_page.verify_success()
    new_user_page.verify_user_in_table(user["username"])


# Verify user can be edited successfully
@pytest.mark.smoke
def test_edit_user_updates_user(new_user_page, new_user_data, update_user_data):
    username = new_user_data["user"]["username"]

    new_user_page.user_management_btn.click()
    new_user_page.edit_user(username)
    new_user_page.update_user(update_user_data)
    new_user_page.update_btn.click()

    new_user_page.verify_update_success()


# Verify user can be deleted successfully and is removed from table
@pytest.mark.smoke
def test_delete_user_removes_from_table(new_user_page, new_user_data, config_fixture):
    username = new_user_data["user"]["username"]

    new_user_page.navigate_to_dashboard(config_fixture["base_url"])
    new_user_page.user_management_btn.click()
    new_user_page.delete_user(username)

    new_user_page.verify_delete_success()
    new_user_page.verify_user_not_in_table(username)