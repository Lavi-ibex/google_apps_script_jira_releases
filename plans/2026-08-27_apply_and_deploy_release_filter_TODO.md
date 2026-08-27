# TODO — Apply and Deploy Release Filter

## Context
Apply the verified local `Code.gs` release filter to the existing Apps Script project and deploy a new web-app version so the live Google Sites widget shows only versions released in 2026.

## Tasks

- [x] 1. Replace the Apps Script project’s `Code.gs` content with the verified local implementation.
       Files: Apps Script project `Code.gs`
       Done when: the editor contains the `releasedVersionsIn2026` server-side filter and the project is saved.

- [x] 2. Create a new version of the existing web-app deployment.
       Files: Apps Script web-app deployment
       Done when: the existing deployment URL serves the saved project version.

- [x] 3. Refresh the live widget and verify its cards and totals exclude unreleased and non-2026 versions.
       Files: deployed web-app URL
       Done when: the dashboard no longer shows the previous 88 total / 56 released result.

## Out of Scope

- Changing Jira versions or release data.
- Changing Script Properties, credentials, or sharing permissions.
- Changing the HTML dashboard design.
