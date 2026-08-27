# TODO — Publish GitHub Repository

## Context
Publish the existing Google Apps Script Jira Releases dashboard as the public GitHub repository `Lavi-ibex/google_apps_script_jira_releases`, preserving its current source files and avoiding credentials.

## Tasks

- [x] 1. Review the publishable project files and add Git exclusions for local or credential-bearing configuration.
       Files: `.gitignore`
       Done when: source files are included while local Apps Script configuration and common secret files are excluded.

- [ ] 2. Initialize this directory as a Git repository and create its first local commit.
       Files: `.git/`, all tracked project files
       Done when: Git reports an initial commit containing only the intended project files.

- [ ] 3. Create the public GitHub repository and push the initial commit.
       Files: GitHub repository `Lavi-ibex/google_apps_script_jira_releases`
       Done when: the remote repository exists publicly and its default branch contains the initial commit.

## Out of Scope

- Deploying or modifying the Google Apps Script web app.
- Adding Jira credentials, tokens, or Script Properties to Git.
- Changing dashboard functionality.
