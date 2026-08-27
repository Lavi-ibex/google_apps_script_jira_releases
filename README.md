# Google Sites Jira Releases Dashboard Guide

A lightweight, secure, responsive, and themeable alternative to Jira's default releases page, designed to be embedded directly into Google Sites.

---

## 1. Features & Architecture

- **Direct Jira Hyperlinks:** Each release name is a clickable direct link (`https://ibex-ai.atlassian.net/projects/IBX/versions/{id}`) with an external link indicator that opens the release page in Jira in a new tab for instant viewing and editing.
- **Dark / Light Mode Support:** Includes a dedicated theme toggle button in the header with high-contrast color palettes for both modes. User preference is saved in `localStorage` and defaults automatically to the user's OS preference.
- **Pure Client-Side Rendering:** Uses `HtmlService.createHtmlOutputFromFile('Index')` with asynchronous `google.script.run` data fetching. This completely prevents template compilation syntax errors.
- **Secure Backend Proxy:** Jira authentication credentials (`JIRA_USER_EMAIL` and `JIRA_API_TOKEN`) reside exclusively inside Google Apps Script `Script Properties`. They are **never** exposed in client-side HTML/JavaScript or to site visitors.
- **Hourly Caching:** Google Apps Script `CacheService` caches Jira releases data for 1 hour (3600 seconds) to ensure near-instant site loading times.
- **On-Demand Refresh:** A clean "Refresh" button on the UI allows users to invalidate the cache and fetch live data immediately.
- **Google Sites Embedding:** Configured with `XFrameOptionsMode.ALLOWALL` for responsive iframe embedding.

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

### Step 4: Deploy the New Version (Crucial for Google Sites to see updates)
When you update code in Apps Script, you **must update the active deployment**:
1. At the top right of the Apps Script editor, click **Deploy > Manage deployments**.
2. Select your active Web app deployment from the list on the left.
3. Click the **Pencil (Edit)** icon at the top right of the modal.
4. Under **Version**, select **New version**.
5. Click **Deploy**.

*(Note: Because the deployment URL remains the exact same, Google Sites will immediately start serving the updated version with Dark Mode and Jira Links upon page refresh!)*

---

## 3. Customization & Maintenance

- **Changing the Jira Project:** Update `JIRA_PROJECT_KEY` in Script Properties (e.g. to another project key).
- **Default Theme:** To change the default fallback theme from Light to Dark, change `<html lang="en" data-theme="light">` to `data-theme="dark"` in `Index.html`.
