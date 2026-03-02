import subprocess
import sys
import pytest

test_suite = [
    "get_token.py",
    "tests/test_login.py",
    "tests/test_forgot_password.py",
    "tests/test_landing.py",
    "tests/test_newuser.py",
    "tests/test_newOrganization.py",
    "tests/test_report_registration.py",
    "tests/test_reportvisibilityRBAC.py",
    "tests/test_super_admin.py",
    "tests/test_signa_user.py",
]

def main():
    # Run get_token.py first
    subprocess.run([sys.executable, "get_token.py"])

    # Run pytest tests
    args = ["-v", *test_suite[1:]]
    print("\nRunning test suite with:", test_suite[1:])
    exit_code = pytest.main(args)
    exit(exit_code)


if __name__ == "__main__":
    main()


