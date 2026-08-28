# Ibex Jira Releases Web App Guide

A lightweight, secure, responsive, and themeable Google Apps Script web app for viewing and updating Ibex Jira release versions.

---

## 1. Features & Architecture

- **Direct Jira Hyperlinks:** Each release name is a clickable direct link (`https://ibex-ai.atlassian.net/projects/IBX/versions/{id}`) with an external link indicator that opens the release page in Jira in a new tab for instant viewing and editing.
- **Dark / Light Mode Support:** Includes a dedicated theme toggle button in the header with high-contrast color palettes for both modes. User preference is saved in `localStorage` and defaults automatically to the user's OS preference.
- **Pure Client-Side Rendering:** Uses `HtmlService.createHtmlOutputFromFile('Index')` with asynchronous `google.script.run` data fetching. This completely prevents template compilation syntax errors.
- **Secure Backend Proxy:** Jira authentication credentials (`JIRA_USER_EMAIL` and `JIRA_API_TOKEN`) reside exclusively inside Google Apps Script `Script Properties`. They are **never** exposed in client-side HTML/JavaScript or to site visitors.
- **Hourly Caching:** Google Apps Script `CacheService` caches Jira releases data for 1 hour (3600 seconds) to ensure near-instant site loading times. Reloading the browser reloads the dashboard but uses this normal cached-data path whenever a valid cache entry exists.
- **On-Demand Refresh:** The dashboard **Refresh** button bypasses the cache and fetches current release data from Jira immediately.
- **Optional Google Sites Embedding:** Configured with `XFrameOptionsMode.ALLOWALL` so the web app can also be embedded in a Google Site when needed.
- **Release Selection:** Shows non-archived, unreleased versions with a planned release date, plus non-archived versions released during calendar year 2026. Released versions are newest first; active versions are ordered by their planned date.
- **Collapsible Descriptions:** Use the header **Show all descriptions** control to expand every available description at once, or hide them all again. Each release card also retains its own **Show description** control and a compact **Edit** action when expanded.
- **Domain-Restricted Description Editing:** Signed-in `ibex-ai.com` users can edit a release description. The update is sent from Apps Script to Jira with the server-side service account, then the one-hour release cache is cleared so refreshed results show the saved value.
- **Domain-Restricted Release-Date Editing:** Signed-in `ibex-ai.com` users can select the small **Edit** action beside a release date, choose a valid replacement date, and save it. A date is required and cannot be cleared. Apps Script updates Jira through the server-side service account, clears the cache, and refreshes the dashboard so the release is shown in its newly sorted position.

---

## 2. Setup & Update Instructions

### Step 1: Open Your Existing Apps Script Project
1. Open [Google Apps Script](https://script.google.com/).
2. Open your `Ibex Jira Releases Widget` project.

### Step 2: Update Script and Template Files
1. In `Code.gs`, replace its contents with the code from `Code.gs`.
2. In `Index.html`, replace its contents with the code from `Index.html`.

### Step 3: Configure Jira Credentials (if not already set)
1. In the Apps Script left navigation sidebar, click **Project Settings** (gear icon ⚙️).
2. Under **Script Properties**, ensure you have:
   - `JIRA_BASE_URL`: `https://ibex-ai.atlassian.net`
   - `JIRA_PROJECT_KEY`: `IBX`
   - `JIRA_USER_EMAIL`: `your.email@ibex-ai.com`
   - `JIRA_API_TOKEN`: Your Atlassian API token

The Jira account identified by `JIRA_USER_EMAIL` must have permission to manage versions in the configured Jira project. Keep this account and its API token in Script Properties only.

### Step 4: Open the Live Dashboard

Use the existing web app URL:

https://script.google.com/a/macros/ibex-ai.com/s/AKfycbzmoYfAQQEVFAvfXqv1ASx7DWo3__scTuBPh5k3FLMrRuRiQr8RQWOY6MVGto-fjvgj/exec

To view every description, select **Show all descriptions** to the left of the theme control. Select **Hide all descriptions** to collapse them again. To edit one description, select its **Show description**, select **Edit**, make the change, and select **Save description**. To change a release date, select the small **Edit** action in its date badge, choose a valid date, and select **Save date**. A release date cannot be cleared. Editing is available only to signed-in users in the `ibex-ai.com` domain.

### Step 5: Deploy the New Web App Version
When you update code in Apps Script, you **must update the active deployment**:
1. At the top right of the Apps Script editor, click **Deploy > Manage deployments**.
2. Select your active Web app deployment from the list on the left.
3. Click the **Pencil (Edit)** icon at the top right of the modal.
4. Under **Version**, select **New version**.
5. Click **Deploy**.

*(Note: The deployment URL remains the same. The direct web app serves the new version after the deployment is updated. If the app is embedded elsewhere, refresh that host page after deploying.)*

---

## 3. Customization & Maintenance

- **Changing the Jira Project:** Update `JIRA_PROJECT_KEY` in Script Properties (e.g. to another project key).
- **Default Theme:** To change the default fallback theme from Light to Dark, change `<html lang="en" data-theme="light">` to `data-theme="dark"` in `Index.html`.
- **Release Filtering:** The visibility rules are implemented in `processRawVersions` in `Code.gs`; update `test_payload_structure.py` alongside an intentional change to these rules.
- **Description Updates:** `apiUpdateReleaseDescription(versionId, description)` validates the signed-in domain, validates input size, updates Jira through the server-side proxy, and clears the cached release payload.
