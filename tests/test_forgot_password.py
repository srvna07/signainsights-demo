import os
import pytest
from playwright.sync_api import expect
import re


# ---------------------------------------------------------------
# Fixture: navigate to Forgot Password page before each test
# ---------------------------------------------------------------
@pytest.fixture
def fp_page(forgot_password_page, config_fixture):
    """Navigate to Forgot Password page and verify it has loaded."""
    forgot_password_page.navigate(config_fixture["base_url"])
    forgot_password_page.verify_page_loaded()
    return forgot_password_page


# ---------------------------------------------------------------
# Forgot Password - TC 01: Page loads successfully
# ---------------------------------------------------------------
@pytest.mark.smoke
@pytest.mark.medium
def test_page_loads(forgot_password_page, config_fixture):
    """Verify Forgot Password page loads with header, email input, and Send Reset Link button."""
    forgot_password_page.navigate(config_fixture["base_url"])
    forgot_password_page.verify_page_loaded()


# ---------------------------------------------------------------
# Forgot Password - TC 02: Verify header text
# ---------------------------------------------------------------
@pytest.mark.smoke
@pytest.mark.low
def test_header_text(fp_page):
    """Verify page header displays 'Forgot Password'."""
    fp_page.verify_header_text()


# ---------------------------------------------------------------
# Forgot Password - TC 03: Email input accepts text
# ---------------------------------------------------------------
@pytest.mark.medium
def test_email_input_accepts_text(fp_page):
    """Verify email input accepts typed characters correctly."""
    test_email = "test.user@example.com"

    fp_page.fill_email(test_email)

    expect(fp_page.email_input).to_have_value(test_email)


# ---------------------------------------------------------------
# Forgot Password - TC 04: Send reset link with valid email
# ---------------------------------------------------------------
@pytest.mark.high
def test_send_reset_link_valid_email(fp_page):
    """Valid registered email should display a confirmation message."""
    registered_email = os.getenv("REGISTERED_EMAIL")

    fp_page.submit_email(registered_email)

    fp_page.verify_success_message_visible()


# ---------------------------------------------------------------
# Forgot Password - TC 05: Send reset link with invalid email
# ---------------------------------------------------------------
@pytest.mark.medium
def test_send_reset_link_invalid_email(fp_page):
    """Invalid / unregistered email should display an error message."""
    fp_page.submit_email("notregistered@example.com")

    fp_page.verify_invalid_email_error_visible()


# ---------------------------------------------------------------
# Forgot Password - TC 06: Empty email validation
# ---------------------------------------------------------------
@pytest.mark.medium
def test_empty_email_validation(fp_page, page):
    """Clicking Send Reset Link with empty email should show 'Email is required'."""
    fp_page.email_input.fill("")
    fp_page.click_send_reset_link()

    fp_page.verify_email_required_error_visible()

    expect(page).to_have_url(re.compile("forgot-password", re.IGNORECASE))


# ---------------------------------------------------------------
# Forgot Password - TC 07: Contact Us button navigation
# ---------------------------------------------------------------
@pytest.mark.medium
def test_contact_us_navigation(fp_page, page):
    """Clicking Contact Us should navigate away from Forgot Password page."""
    fp_page.click_contact_us()

    expect(page).not_to_have_url(re.compile("forgot-password", re.IGNORECASE))


# ---------------------------------------------------------------
# Forgot Password - TC 08: URL verification
# ---------------------------------------------------------------
@pytest.mark.smoke
@pytest.mark.low
def test_url_verification(forgot_password_page, config_fixture, page):
    """Current URL should match the Forgot Password page URL exactly."""
    forgot_password_page.navigate(config_fixture["base_url"])

    forgot_password_page.verify_url(page)