import json
import pytest
from pathlib import Path
from playwright.sync_api import Page
from pages.login_page import LoginPage
from utils.data_reader import DataReader
from utils.env_loader import get_env

ROOT   = Path(__file__).parent.parent
ENV    = get_env()
config = DataReader.load_yaml(f"configs/{ENV}.yaml")


def test_get_token(page: Page, credentials):
    """Log in and save the AccessToken from localStorage to config.json.
    This token is consumed by test_get_data_ids_delete.py for API cleanup.
    """
    login = LoginPage(page)
    login.navigate(config["base_url"])
    login.login(credentials["username"], credentials["password"])
    page.wait_for_url("**/dashboard", timeout=config["navigation_timeout"])
    page.wait_for_timeout(2000)

    token = page.evaluate("() => localStorage.getItem('AccessToken')")

    assert token, "AccessToken not found in localStorage — login may have failed."

    config_file   = ROOT / "config.json"
    data          = json.loads(config_file.read_text()) if config_file.exists() else {}
    data["token"] = token
    config_file.write_text(json.dumps(data, indent=2))
    print("✓ Token saved to config.json")
