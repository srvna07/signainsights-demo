import pytest
from playwright.sync_api import expect
import re


@pytest.fixture
def fp_page(forgot_password_page, config_fixture):
    forgot_password_page.navigate(config_fixture["base_url"])
    forgot_password_page.verify_page_loaded()
    return forgot_password_page


# Verify Forgot Password page loads successfully
@pytest.mark.medium
def test_forgot_password_page_loads(forgot_password_page, config_fixture):
    forgot_password_page.navigate(config_fixture["base_url"])
    forgot_password_page.verify_page_loaded()


# Verify page header displays correctly
@pytest.mark.low
def test_header_text_displays_correctly(fp_page):
    fp_page.verify_header_text()


# Verify email input accepts typed text
@pytest.mark.medium
def test_email_input_accepts_text(fp_page):
    test_email = "test.user@example.com"
    fp_page.fill_email(test_email)
    expect(fp_page.email_input).to_have_value(test_email)


# Verify valid email displays success message
@pytest.mark.high
def test_send_reset_link_with_valid_email_shows_success(fp_page, registered_email):
    fp_page.submit_email(registered_email)
    fp_page.verify_success_message_visible()


# Verify invalid email displays error message
@pytest.mark.medium
def test_send_reset_link_with_invalid_email_shows_error(fp_page):
    fp_page.submit_email("notregistered@example.com")
    fp_page.verify_invalid_email_error_visible()


# Verify empty email shows validation error
@pytest.mark.medium
def test_empty_email_validation_shows_error(fp_page, page):
    fp_page.email_input.fill("")
    fp_page.click_send_reset_link()
    fp_page.verify_email_required_error_visible()
    expect(page).to_have_url(re.compile("forgot-password", re.IGNORECASE))


# Verify Contact Us button navigates away from page
@pytest.mark.medium
def test_contact_us_navigation_redirects(fp_page, page):
    fp_page.click_contact_us()
    expect(page).not_to_have_url(re.compile("forgot-password", re.IGNORECASE))


# Verify current URL matches Forgot Password page
@pytest.mark.low
def test_forgot_password_url_verification(forgot_password_page, config_fixture, page):
    forgot_password_page.navigate(config_fixture["base_url"])

    forgot_password_page.verify_url(page)