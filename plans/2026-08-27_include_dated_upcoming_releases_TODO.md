# TODO — Include Dated Upcoming Releases

## Context
Correct the dashboard filter so it displays all active or overdue Jira versions that have a nonblank planned release date, alongside versions released in 2026. This makes the “Upcoming / Active” count meaningful while preserving the 2026 scope for the released count.

## Tasks

- [x] 1. Update the server-side filter to include non-archived unreleased versions with a nonblank release date, plus released versions dated in 2026.
       Files: `Code.gs`
       Done when: dated upcoming and overdue versions are returned, undated versions and released versions outside 2026 are excluded.

- [x] 2. Update regression fixtures and assertions for the combined upcoming and released-2026 result set.
       Files: `test_payload_structure.py`
       Done when: the test proves dated upcoming and overdue versions are included while undated and released-2025 versions remain excluded.

- [x] 3. Run the regression test.
       Files: `test_payload_structure.py`
       Done when: the test command exits successfully.

- [x] 4. Deploy the saved HTML label and corrected server-side filter to the active second web-app URL, then refresh its cached data.
       Files: Apps Script `Code.gs`, `Index.html`, active web-app deployment
       Done when: the live dashboard shows a nonzero Upcoming / Active count for dated unreleased versions and the “Released in 2026” label.

## Out of Scope

- Including archived versions or undated versions.
- Including releases completed outside calendar year 2026.
- Changing the first web-app URL.
