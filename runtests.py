import sys
import pytest

# Step 1: runs sequentially before parallel — token + smoke must pass to continue
pre_suite = [
    "tests/test_get_token.py",
    "tests/test_smoke.py",
]

# Step 2: runs in parallel
parallel_suite = [
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

# Step 3: runs alone after parallel
post_suite = [
    "tests/test_get_data_ids_delete.py",
]


def main():
    cli_args = sys.argv[1:]

    # --- Phase 1: sequential pre-run (token + smoke) ---
    print("\n[Phase 1] Running pre-suite sequentially (token + smoke)...")
    exit_code = pytest.main(["-v", *cli_args, *pre_suite])
    if exit_code != 0:
        print("\n[Aborted] Pre-suite failed. Skipping parallel and cleanup phases.")
        sys.exit(exit_code)

    # --- Phase 2: parallel run ---
    print("\n[Phase 2] Running parallel suite...")
    exit_code = pytest.main(["-v", "--numprocesses=auto", "--dist=loadfile", *cli_args, *parallel_suite])
    if exit_code != 0:
        print("\n[Aborted] Parallel suite failed. Skipping cleanup phase.")
        sys.exit(exit_code)

    # --- Phase 3: sequential post-run (cleanup) ---
    print("\n[Phase 3] Running post-suite sequentially (cleanup)...")
    exit_code = pytest.main(["-v", *cli_args, *post_suite])
    sys.exit(exit_code)


if __name__ == "__main__":
    main()