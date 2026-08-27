#!/usr/bin/env python3
"""
Unit test and payload verification for Google Sites Jira Releases Apps Script backend.
Validates sorting, status categorization, null-handling, and schema compatibility.
"""

import json
import sys

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
    }
]

def process_raw_versions(raw_versions):
    """Python port of the Apps Script transformation logic for testing"""
    formatted = []
    for v in raw_versions:
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
            "releaseDate": v.get("releaseDate", ""),
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
    
    assert len(processed) == 4, f"Expected 4 items, got {len(processed)}"
    
    # Check ordering: Overdue (4.1.5) -> Unreleased (4.2.0) -> Released (4.1.0) -> Archived (3.9)
    assert processed[0]["name"] == "Ibex v4.1.5 (Hotfix)", f"Unexpected 1st item: {processed[0]['name']}"
    assert processed[0]["status"] == "Overdue"
    
    assert processed[1]["name"] == "Ibex v4.2.0", f"Unexpected 2nd item: {processed[1]['name']}"
    assert processed[1]["status"] == "Unreleased"
    
    assert processed[2]["name"] == "Ibex v4.1.0", f"Unexpected 3rd item: {processed[2]['name']}"
    assert processed[2]["status"] == "Released"
    
    assert processed[3]["name"] == "Ibex v3.9 (Legacy)", f"Unexpected 4th item: {processed[3]['name']}"
    assert processed[3]["status"] == "Archived"
    assert processed[3]["description"] == "No description provided."

    print("✅ All transformation and sorting tests PASSED successfully!")
    print(json.dumps(processed, indent=2))

if __name__ == "__main__":
    test_transformation()
