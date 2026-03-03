import sys
import pytest

test_suite = [
    "tests/test_get_token.py",
    "tests/test_login.py",
    "tests/test_forgot_password.py",
    "tests/test_landing.py",
    "tests/test_newuser.py",
    "tests/test_newOrganization.py",
    "tests/test_report_registration.py",
    "tests/test_reportvisibilityRBAC.py",
    "tests/test_super_admin.py",
    "tests/test_signa_user.py",
    "tests/test_get_data_ids_delete.py",
]

def main():
    # Forward any CLI args passed to this script (e.g. --headed, --browser, -k)
    # then append the test suite paths
    cli_args  = sys.argv[1:]
    args      = ["-v", *cli_args, *test_suite]
    print("\nRunning test suite with args:", args)
    exit_code = pytest.main(args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()