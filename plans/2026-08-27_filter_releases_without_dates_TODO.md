# TODO — Filter Releases Without Planned Dates

## Context
Update the Google Apps Script release transformation so the Google Sites dashboard displays only Jira versions whose planned release date (`releaseDate`) is present and nonblank. Filtering on the server keeps dashboard counts and displayed cards consistent.

## Tasks

- [x] 1. Filter version records without a nonblank planned release date before formatting and sorting.
       Files: `Code.gs`
       Done when: `processRawVersions` returns no object for Jira versions whose `releaseDate` is missing, empty, or whitespace-only.

- [x] 2. Extend the local transformation test with a version that has no planned release date.
       Files: `test_payload_structure.py`
       Done when: the test proves that the undated version is omitted and all dated versions retain their intended ordering.

- [x] 3. Run the regression test.
       Files: `test_payload_structure.py`
       Done when: the test command exits successfully.

## Out of Scope

- Filtering by release status, start date, or description.
- Changing the dashboard layout, card labels, or theme.
- Deploying a new Apps Script web-app version.
