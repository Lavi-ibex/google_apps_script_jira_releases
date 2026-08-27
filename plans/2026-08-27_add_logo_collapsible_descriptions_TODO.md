# TODO - Add Logo and Collapsible Descriptions

## Context

Improve the Jira releases dashboard header and release cards by adding the supplied Ibex logo, replacing the subtitle with the corrected Google Apps Script wording, and making each non-empty release description expandable on demand. The implementation will remain self-contained in the existing Google Apps Script HTML asset and will preserve escaped Jira-supplied content.

## Tasks

- [x] 1. Add the supplied Ibex logo as a project asset and display it centered above the dashboard title, subtitle, and action buttons.
       Files: assets/ibex-logo.png, Index.html
       Done when: the logo is centered above the title, subtitle, and action buttons without distorting the responsive layout in light or dark mode.

- [x] 2. Replace the subtitle text with “Live releases tracked from Jira Cloud - powered by Google Apps Script”.
       Files: Index.html
       Done when: the exact corrected subtitle is displayed.

- [x] 3. Make each non-empty release description collapsible and accessible.
       Files: Index.html
       Done when: descriptions are collapsed initially, each control expands or collapses only its own escaped description, and the control exposes its expanded state to assistive technology.

- [x] 4. Verify the UI locally and run the existing release transformation regression test.
       Files: Index.html, test_payload_structure.py
       Done when: the local page shows the logo, corrected subtitle, and working description controls, and `python3 test_payload_structure.py` passes.

## Out of Scope

- Changing Jira data retrieval, filtering, cache behavior, or release counts.
- Changing the existing public deployment before a separate deployment approval.
- Redesigning other dashboard elements or altering the supplied logo artwork.
