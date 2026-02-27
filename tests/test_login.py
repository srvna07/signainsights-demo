import pytest
import os
from playwright.sync_api import expect
import re


# -------------------------
# Fixture to ensure login page is loaded
# -------------------------
@pytest.fixture
def login_page_ready(login_page, config_fixture):
    """Ensure the login page is loaded before running any dependent test."""
    login_page.navigate(config_fixture["base_url"])
    login_page.verify_page_loaded()
    return login_page


# -------------------------
# Login - TC 01: Verify login page loads
# -------------------------
@pytest.mark.smoke
@pytest.mark.medium
def test_login_page_loads(login_page, config_fixture):
    """Smoke test: Verify login page loads correctly."""
    login_page.navigate(config_fixture["base_url"])
    login_page.verify_page_loaded()


# -------------------------
# Login - TC 02: Password input is masked
# -------------------------
@pytest.mark.low
def test_password_masked(login_page_ready):
    """Password input should always be masked."""
    login_page = login_page_ready
    expect(login_page.password_input).to_have_attribute("type", "password")


# -------------------------
# Login - TC 03: Empty login should fail
# -------------------------
@pytest.mark.critical
def test_empty_login(login_page_ready):
    """Empty login should fail with validation messages."""
    login_page = login_page_ready
    login_page.username_input.fill("")
    login_page.password_input.fill("")
    login_page.click_login()

    # Verify validation messages appear
    expect(login_page.username_required_error).to_be_visible()
    expect(login_page.password_required_error).to_be_visible()


# -------------------------
# Login - TC 04: Invalid password login should fail
# -------------------------
@pytest.mark.critical
def test_wrong_password(login_page_ready):
    """Invalid password should not allow login."""
    login_page = login_page_ready
    username = os.getenv("USERNAME")

    login_page.login(username, "WrongPassword123!")

    # Verify password incorrect error is visible (auto-waits)
    expect(login_page.password_incorrect_error).to_be_visible()

    # Optional: ensure user is still on login page
    expect(login_page.welcome_text).to_be_visible()


# -------------------------
# Login - TC 05: Valid login should succeed
# -------------------------
@pytest.mark.high
def test_valid_login(login_page_ready, page):
    """Valid login should succeed - user redirected to dashboard."""
    login_page = login_page_ready
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    login_page.login(username, password)

    # Verify user is redirected away from login page
    expect(page).not_to_have_url(re.compile("/login"))
    expect(page).to_have_url(re.compile("dashboard", re.IGNORECASE))


# -------------------------
# Login - TC 06: Forgot Password navigation
# -------------------------
@pytest.mark.medium
def test_forgot_password_navigation(login_page_ready, page):
    """Verify clicking Forgot Password link navigates to Forgot Password page."""
    login_page = login_page_ready
    login_page.click_forgot_password()

    expect(login_page.forgot_password_header).to_be_visible()
    expect(page).to_have_url(re.compile("forgot-password", re.IGNORECASE))