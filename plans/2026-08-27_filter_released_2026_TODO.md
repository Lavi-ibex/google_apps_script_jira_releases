# TODO — Show Released 2026 Versions Only

## Context
Change the server-side Jira release filter so the dashboard displays only versions that Jira marks as released and whose release date falls in calendar year 2026. This replaces the previous rule that displayed all versions with any planned release date.

## Tasks

- [x] 1. Filter Jira versions to released records with an ISO release date in 2026.
       Files: `Code.gs`
       Done when: `processRawVersions` returns only records where `released` is true and `releaseDate` begins with `2026-`.

- [x] 2. Update the regression fixture and assertions for the released-2026-only contract.
       Files: `test_payload_structure.py`
       Done when: 2026 unreleased, 2025 released, and undated versions are all excluded, while the 2026 released version remains.

- [x] 3. Run the regression test.
       Files: `test_payload_structure.py`
       Done when: the test command exits successfully.

## Out of Scope

- Showing upcoming or unreleased 2026 versions.
- Showing releases from years other than 2026.
- Changing dashboard layout, card labels, or deployment settings.
