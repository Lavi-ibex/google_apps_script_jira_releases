# Project Instructions

## Purpose

This project is a Google Apps Script web app that displays Jira release versions in a Google Sites embed.

## Project Structure

- `Code.gs` is the server-side Apps Script entry point and Jira API proxy.
- `Index.html` is the client-side dashboard UI served by `HtmlService`.
- `test_payload_structure.py` is a local Python verification of the release transformation, status assignment, and sorting behavior.

## Security Requirements

- Keep Jira credentials only in Apps Script Script Properties: `JIRA_USER_EMAIL` and `JIRA_API_TOKEN`.
- Never put tokens, passwords, or user credentials in source files, HTML, logs, tests, or error messages.
- Preserve server-side Jira fetching through `UrlFetchApp`; do not expose Jira authentication to the browser.
- Treat Jira release names and descriptions as untrusted input. Escape values before inserting them into HTML.

## Development Rules

- Keep `doGet` compatible with Google Sites embedding by retaining `XFrameOptionsMode.ALLOWALL` unless the embedding approach changes deliberately.
- Preserve the public client-callable function `apiGetReleases(forceRefresh)` when updating the UI or backend.
- Keep cache behavior explicit when changing data-fetching logic. The current cache TTL is one hour.
- Use ES5-compatible JavaScript syntax in `Code.gs` and `Index.html` unless the target Apps Script runtime compatibility is confirmed.

## Validation

After changing release transformation or ordering behavior, run:

```bash
python3 test_payload_structure.py
```

Update the Python test alongside intentional changes to the transformation contract.

## Deployment

Source edits do not update the live Google Sites widget automatically. Deploy a new version of the existing Apps Script web app after validating changes.

## Local Planning Files

- Store task plans in `plans/` using the dated `YYYY-MM-DD_plan_name_TODO.md` naming convention.
- `plans/` is local-only documentation. It must remain ignored by Git and must not be committed.
