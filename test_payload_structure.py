#!/usr/bin/env python3
"""
Unit test and payload verification for Google Sites Jira Releases Apps Script backend.
Validates sorting, status categorization, null-handling, and schema compatibility.
"""

import json
import sys
from pathlib import Path

# Simulated sample payload matching Jira Cloud /rest/api/3/project/{key}/versions
SAMPLE_JIRA_VERSIONS = [
    {
        "self": "https://ibex-ai.atlassian.net/rest/api/3/version/10001",
        "id": "10001",
        "name": "Ibex v4.1.0",
        "archived": False,
        "released": True,
        "releaseDate": "2026-03-15",
        "userReleaseDate": "15/Mar/2026",
        "projectId": 10000,
        "description": "General release with performance enhancements and bug fixes."
    },
    {
        "self": "https://ibex-ai.atlassian.net/rest/api/3/version/10002",
        "id": "10002",
        "name": "Ibex v4.2.0",
        "archived": False,
        "released": False,
        "releaseDate": "2026-09-30",
        "userReleaseDate": "30/Sep/2026",
        "overdue": False,
        "projectId": 10000,
        "description": "Next major release including new AI model integrations."
    },
    {
        "self": "https://ibex-ai.atlassian.net/rest/api/3/version/10003",
        "id": "10003",
        "name": "Ibex v3.9 (Legacy)",
        "archived": True,
        "released": True,
        "releaseDate": "2025-11-01",
        "userReleaseDate": "01/Nov/2025",
        "projectId": 10000
    },
    {
        "self": "https://ibex-ai.atlassian.net/rest/api/3/version/10004",
        "id": "10004",
        "name": "Ibex v4.1.5 (Hotfix)",
        "archived": False,
        "released": False,
        "overdue": True,
        "releaseDate": "2026-08-01",
        "userReleaseDate": "01/Aug/2026",
        "projectId": 10000,
        "description": "Critical security and stability patches."
    },
    {
        "self": "https://ibex-ai.atlassian.net/rest/api/3/version/10005",
        "id": "10005",
        "name": "Undated Draft Version",
        "archived": False,
        "released": False,
        "releaseDate": "   ",
        "projectId": 10000
    }
]

def process_raw_versions(raw_versions):
    """Python port of the Apps Script transformation logic for testing"""
    formatted = []
    for v in raw_versions:
        release_date = v.get("releaseDate")
        if (
            v.get("archived")
            or not isinstance(release_date, str)
            or not release_date.strip()
            or (v.get("released") and not release_date.startswith("2026-"))
        ):
            continue

        status = "Unreleased"
        status_category = "unreleased"

        if v.get("archived"):
            status = "Archived"
            status_category = "archived"
        elif v.get("released"):
            status = "Released"
            status_category = "released"
        elif v.get("overdue"):
            status = "Overdue"
            status_category = "overdue"

        formatted.append({
            "id": v.get("id"),
            "name": v.get("name", "Unnamed Version"),
            "status": status,
            "statusCategory": status_category,
            "released": bool(v.get("released")),
            "archived": bool(v.get("archived")),
            "overdue": bool(v.get("overdue")),
            "releaseDate": release_date,
            "userReleaseDate": v.get("userReleaseDate") or v.get("releaseDate") or "No date set",
            "description": v.get("description") or "No description provided."
        })

    cat_rank = {"overdue": 1, "unreleased": 2, "released": 3, "archived": 4}

    def sort_key(item):
        rank = cat_rank.get(item["statusCategory"], 99)
        date = item["releaseDate"]
        # For released, reverse date sorting
        if item["statusCategory"] == "released":
            return (rank, "" if not date else "".join(chr(255 - ord(c)) for c in date))
        return (rank, date if date else "9999-99-99")

    formatted.sort(key=sort_key)
    return formatted

def test_transformation():
    print("Testing transformation logic...")
    processed = process_raw_versions(SAMPLE_JIRA_VERSIONS)
    
    assert len(processed) == 3, f"Expected 3 visible items, got {len(processed)}"
    assert all(item["releaseDate"].strip() for item in processed)
    assert all(not item["archived"] for item in processed)
    assert all(
        not item["released"] or item["releaseDate"].startswith("2026-")
        for item in processed
    )
    assert all(item["name"] not in {"Ibex v3.9 (Legacy)", "Undated Draft Version"} for item in processed)
    
    assert processed[0]["name"] == "Ibex v4.1.5 (Hotfix)"
    assert processed[0]["status"] == "Overdue"
    assert processed[1]["name"] == "Ibex v4.2.0"
    assert processed[1]["status"] == "Unreleased"
    assert processed[2]["name"] == "Ibex v4.1.0"
    assert processed[2]["status"] == "Released"

    print("✅ All transformation and sorting tests PASSED successfully!")
    print(json.dumps(processed, indent=2))


def test_description_update_endpoint_contract():
    """Verify that the Apps Script update endpoint retains its security contract."""
    code = Path(__file__).with_name("Code.gs").read_text(encoding="utf-8")

    assert "function apiUpdateReleaseDescription(versionId, description)" in code
    assert "assertAuthorizedIbexUser();" in code
    assert "AUTHORIZED_EMAIL_DOMAIN = 'ibex-ai.com'" in code
    assert "/^\\d{1,20}$/.test(versionId)" in code
    assert "description.length > MAX_DESCRIPTION_LENGTH" in code
    assert "method: 'put'" in code
    assert "'/rest/api/2/version/' + encodeURIComponent(versionId)" in code
    assert "payload: JSON.stringify({ description: description })" in code
    assert "CacheService.getScriptCache().remove(CACHE_KEY);" in code
    assert "function getSafeJiraValidationMessage(response)" in code
    assert "message.slice(0, 240)" in code

    print("✅ Description update endpoint contract test passed.")

if __name__ == "__main__":
    test_transformation()
    test_description_update_endpoint_contract()
