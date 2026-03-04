import pytest
from playwright.sync_api import expect


@pytest.fixture
def login_page_ready(login_page, config_fixture):
    login_page.navigate(config_fixture["base_url"])
    login_page.verify_page_loaded()
    return login_page


# Verify login page loads successfully
@pytest.mark.medium
def test_login_page_loads(login_page_ready):
    pass


# Verify password input is masked
@pytest.mark.low
def test_password_input_is_masked(login_page_ready):
    expect(login_page_ready.password_input).to_have_attribute("type", "password")


# Verify empty login fails with validation messages
@pytest.mark.critical
def test_empty_login_shows_validation_errors(login_page_ready):
    login_page_ready.username_input.fill("")
    login_page_ready.password_input.fill("")
    login_page_ready.click_login()
    expect(login_page_ready.username_required_error).to_be_visible()
    expect(login_page_ready.password_required_error).to_be_visible()


# Verify invalid password fails login
@pytest.mark.critical
def test_wrong_password_shows_error(login_page_ready, credentials):
    login_page_ready.login(credentials["username"], "WrongPassword123!")
    expect(login_page_ready.password_incorrect_error).to_be_visible()


# Verify valid login succeeds and redirects to dashboard
@pytest.mark.high
def test_valid_login_redirects_to_dashboard(login_page_ready, credentials):
    login_page_ready.login(credentials["username"], credentials["password"])
    login_page_ready.verify_redirected_to_dashboard()


# Verify Forgot Password link navigates to correct page
@pytest.mark.medium
def test_forgot_password_navigation_opens_page(login_page_ready):
    login_page_ready.click_forgot_password()
    login_page_ready.verify_forgot_password_navigation()