import json
import pytest
import requests
from pathlib import Path
from utils.data_reader import DataReader
from utils.env_loader import get_env

ROOT   = Path(__file__).parent.parent
ENV    = get_env()
config = DataReader.load_yaml(f"configs/{ENV}.yaml")

API_BASE = config.get("apiUrl")
if not API_BASE:
    raise EnvironmentError(f"'apiUrl' is not set in configs/{ENV}.yaml")

USER_PREFIX   = "test_"
REPORT_PREFIX = "test_"
ORG_PREFIX    = "test_"


def get_token():
    config_file = ROOT / "config.json"
    return json.loads(config_file.read_text()).get("token") if config_file.exists() else None


def delete_all(session, fetch_url, delete_url, id_field, name_field, prefix, label):
    print(f"\n--- {label} ---")
    response = session.get(f"{API_BASE}{fetch_url}")
    assert response.ok, f"Failed to fetch {label}: {response.status_code}"

    data    = response.json()
    records = data if isinstance(data, list) else data.get("Data", [])

    items = [i for i in records if i[name_field].startswith(prefix)]
    print(f"Found {len(items)} test {label}.")

    if not items:
        print(f"No test {label} to delete.")
        return

    deleted, failed = 0, 0
    for item in items:
        item_id = item[id_field]
        res     = session.delete(f"{API_BASE}{delete_url}/{item_id}")
        if res.ok:
            print(f"[OK] Deleted {item[name_field]} (ID: {item_id})")
            deleted += 1
        else:
            print(f"[ERROR] Failed {item[name_field]} (ID: {item_id}): {res.status_code}")
            failed += 1

    print(f"[SUMMARY] {label} — Deleted: {deleted}, Failed: {failed}")


# Verify test data is deleted from API
def test_cleanup_api_test_data():
    token = get_token()
    if not token:
        pytest.skip("Token not found. Run test_get_token.py first.")

    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}"})

    delete_all(session, "/api/User/findallusers", "/api/User/delete",
               "UserId", "UserName", USER_PREFIX, "Users")

    delete_all(session, "/api/Report/findall?pageNumber=1&pageSize=1000", "/api/Report/delete",
               "ReportId", "ReportName", REPORT_PREFIX, "Reports")

    delete_all(session, "/api/Organization/findall?pageNumber=1&pageSize=1000", "/api/Organization/delete",
               "OrganizaionId", "OrganizationName", ORG_PREFIX, "Organizations")


if __name__ == "__main__":
    token   = get_token()
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}"})
    delete_all(session, "/api/User/findallusers", "/api/User/delete",
               "UserId", "UserName", USER_PREFIX, "Users")
    delete_all(session, "/api/Report/findall?pageNumber=1&pageSize=1000", "/api/Report/delete",
               "ReportId", "ReportName", REPORT_PREFIX, "Reports")
    delete_all(session, "/api/Organization/findall?pageNumber=1&pageSize=1000", "/api/Organization/delete",
               "OrganizaionId", "OrganizationName", ORG_PREFIX, "Organizations")
