# TODO — Rename Released Summary Label

## Context
Update the dashboard summary label to clarify that the displayed count is limited to Jira versions released during 2026, matching the server-side filter already deployed.

## Tasks

- [ ] 1. Rename the released summary label to “Released in 2026”.
       Files: `Index.html`
       Done when: the KPI label clearly states the 2026 scope without changing count logic.

- [ ] 2. Apply the updated HTML to the Apps Script project and deploy a new version of the active web app.
       Files: Apps Script `Index.html`, active web-app deployment
       Done when: the second web-app URL shows the updated label.

## Out of Scope

- Changing release filters, counts, or card content.
- Changing the first web-app URL.
- Changing theme, layout, or credential settings.
