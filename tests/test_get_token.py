import json
from pathlib import Path
from dotenv import dotenv_values
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from utils.data_reader import DataReader

ROOT = Path(__file__).parent.parent
env_vars = dotenv_values(ROOT / ".env")
ENV = env_vars.get("ENV", "dev")
config = DataReader.load_yaml(f"configs/{ENV}.yaml")


def get_access_token():
    username = env_vars.get("USERNAME")
    password = env_vars.get("PASSWORD")

    if not username or not password:
        print("✗ USERNAME or PASSWORD not found in .env")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            login = LoginPage(page)
            login.navigate(config["base_url"])
            login.login(username, password)
            page.wait_for_url("**/dashboard", timeout=config["navigation_timeout"])
            page.wait_for_timeout(2000)

            token = page.evaluate("() => localStorage.getItem('AccessToken')")

            if token:
                config_file = ROOT / "config.json"
                data = json.loads(config_file.read_text()) if config_file.exists() else {}
                data["token"] = token
                config_file.write_text(json.dumps(data, indent=2))
                print(f"✓ Token saved to config.json")
            else:
                print("✗ Token not found in localStorage")
        finally:
            browser.close()


def test_get_token():
    get_access_token()


if __name__ == "__main__":
    get_access_token()