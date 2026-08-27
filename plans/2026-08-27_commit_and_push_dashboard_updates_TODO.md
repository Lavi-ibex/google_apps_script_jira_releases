# TODO - Commit and Push Dashboard Updates

## Context

Record all currently pending changes in the Google Apps Script Jira releases repository, including the verified release-filter corrections, dashboard logo and description controls, supplied logo asset, and dated plan records. Push the resulting commit to the existing `origin/main` remote.

## Tasks

- [x] 1. Review the final staged file list and run the existing regression test.
       Files: Code.gs, Index.html, test_payload_structure.py, assets/ibex-logo.png, plans/
       Done when: the staged set contains all current project changes and `python3 test_payload_structure.py` passes.

- [x] 2. Create one commit containing all current project changes.
       Files: all files listed by `git status --short`
       Done when: a new local commit records the complete pending change set.

- [x] 3. Push the new commit to `origin/main` and verify the remote tracking state.
       Files: Git repository history
       Done when: `origin/main` contains the new commit and the worktree is clean.

## Out of Scope

- Altering source behavior beyond the currently pending changes.
- Rewriting, squashing, force-pushing, or changing repository access settings.
