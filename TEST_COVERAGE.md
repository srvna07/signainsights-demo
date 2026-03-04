# Test Coverage

> Last Updated: March 04, 2026  
> Total Tests: 51

---

## Markers
- `critical` — critical severity tests
- `high` — high severity tests
- `medium` — medium severity tests
- `low` — low severity tests
- `smoke` — smoke tests

---

## Test Suites

**Login Page Tests** (6 tests)
1. Page loads with all elements visible — `test_login_page_loads`
2. Password field is masked — `test_password_input_is_masked`
3. Empty form submission shows username and password required errors — `test_empty_login_shows_validation_errors`
4. Wrong password shows incorrect password error — `test_wrong_password_shows_error`
5. Valid credentials redirect to dashboard — `test_valid_login_redirects_to_dashboard`
6. Forgot Password link navigates to forgot password page — `test_forgot_password_navigation_opens_page`

**Forgot Password Page Tests** (8 tests)
1. Page loads with all elements visible — `test_forgot_password_page_loads`
2. Header displays "Forgot Password" correctly — `test_header_text_displays_correctly`
3. Email input accepts typed text — `test_email_input_accepts_text`
4. Valid registered email shows success message — `test_send_reset_link_with_valid_email_shows_success`
5. Unregistered email shows user not found error — `test_send_reset_link_with_invalid_email_shows_error`
6. Empty email submission shows required error and stays on page — `test_empty_email_validation_shows_error`
7. Contact Us button navigates away from the page — `test_contact_us_navigation_redirects`
8. URL correctly contains "forgot-password" — `test_forgot_password_url_verification`

**Landing Page Tests** (2 tests)
1. Landing page loads with all navigation and UI components visible — `test_landing_page_loads`
2. Each sidebar menu item navigates to its correct URL — `test_sidebar_navigation_loads_correct_url`

**New User Page Tests** (3 tests)
1. New user can be created successfully and appears in the table — `test_create_new_user`
2. Existing user details can be edited and updated successfully — `test_edit_user_updates_user`
3. Existing user can be deleted and is removed from the table — `test_delete_user_removes_from_table`

**Organization Page Tests** (4 tests)
1. New organization can be created successfully — `test_create_organization_success`
2. Duplicate organization submission shows an error — `test_create_duplicate_organization_shows_error`
3. Existing organization details can be edited and updated successfully — `test_edit_organization_updates`
4. Existing organization can be deleted and is removed from the table — `test_delete_organization_success`

**Report Registration Page Tests** (8 tests)
1. Organization can be created for report registration — `test_create_organization_for_report_registration`
2. New report can be created successfully and appears in the table — `test_create_report_success`
3. Existing report can be edited and updated successfully — `test_edit_report_success`
4. Report search returns the expected result — `test_search_report_returns_expected_result`
5. Table paginates correctly with 5 rows per page — `test_rows_per_page_5`
6. Table paginates correctly with 25 rows per page — `test_rows_per_page_25`
7. Existing report can be deleted and is no longer visible — `test_delete_report_success`
8. Organization can be deleted successfully after report tests — `test_delete_organization_success`

**Report RBAC Tests** (1 test)
1. Users can only see reports belonging to their assigned primary and secondary organizations — `test_report_visibility_based_on_rbac`

**Super Admin Tests** (10 tests)
1. Super admin has full sidebar access to all navigation items — `test_super_admin_has_full_sidebar_access`
2. All four user type options are available in the dropdown — `test_super_admin_can_see_all_user_type_options`
3. Super admin can create another super admin user — `test_super_admin_can_create_super_admin`
4. Super admin can create a signa user — `test_super_admin_can_create_signa_user`
5. Super admin can create an organization admin user — `test_super_admin_can_create_organization_admin`
6. Super admin can create an organization user — `test_super_admin_can_create_organization_user`
7. Super admin can access the report registration page — `test_super_admin_can_access_report_registration`
8. Super admin can access the organization registration page — `test_super_admin_can_access_organization_registration`
9. Super admin can modify any user details — `test_super_admin_can_modify_any_user`
10. Super admin can delete any user — `test_super_admin_can_delete_any_user`

**Signa User Tests** (12 tests)
1. Signa user can create an organization — `test_signa_user_create_organization`
2. Signa user can create a report — `test_signa_user_create_report`
3. Signa user can create a signa user — `test_signa_user_create_signa_user`
4. Signa user can create an organization admin user — `test_signa_user_create_org_admin`
5. Signa user can create an organization user — `test_signa_user_create_org_user`
6. Signa user can edit an organization — `test_signa_user_edit_organization`
7. Signa user can edit a report — `test_signa_user_edit_report`
8. Signa user can edit a user — `test_signa_user_edit_user`
9. Signa user can delete a report — `test_signa_user_delete_report`
10. Signa user can delete a user — `test_signa_user_delete_user`
11. Signa user can delete an organization — `test_signa_user_delete_organization`
12. Signa user cannot see or access super admin users — `test_signa_user_cannot_access_super_admin`
