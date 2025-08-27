#!/usr/bin/env python3
"""
Google Cloud Translation v3 Glossary Entry Manager

This module provides functionality to work with Google Cloud Translation v3
glossary entries using the REST API directly, since the glossary entry methods
are not yet available in the current Google Cloud Translation v3 library.
"""

import argparse
import json
import os
import sys
from typing import Dict, List, Optional, Any
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request


class GlossaryEntryManager:
    """Manages Google Cloud Translation v3 glossary entries using REST API."""

    def __init__(self, project_id: str, auth_file: str, location: str = "us-central1"):
        """
        Initialize the GlossaryEntryManager.

        Args:
            project_id: Google Cloud project ID
            auth_file: Path to the service account JSON file
            location: Google Cloud location (default: us-central1)
        """
        self.project_id = project_id
        self.location = location
        self.auth_file = auth_file

        # Set up authentication
        self.credentials = service_account.Credentials.from_service_account_file(
            auth_file,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )

        # Base URL for the Translation API
        self.base_url = "https://translation.googleapis.com/v3"

        # Construct the parent path
        self.parent = f"projects/{project_id}/locations/{location}"

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        # Refresh the token if needed
        if not self.credentials.valid:
            self.credentials.refresh(Request())

        return {
            "Authorization": f"Bearer {self.credentials.token}",
            "Content-Type": "application/json; charset=utf-8",
            "x-goog-user-project": self.project_id
        }

    def list_glossary_entries(self, glossary_id: str, page_size: int = 100) -> List[Dict[str, Any]]:
        """
        List all entries in a glossary.

        Args:
            glossary_id: The ID of the glossary
            page_size: Number of entries to return per page (default: 100)

        Returns:
            List of glossary entries as dictionaries
        """
        try:
            # Construct the URL
            url = f"{self.base_url}/{self.parent}/glossaries/{glossary_id}/glossaryEntries"

            # Add query parameters
            params = {"pageSize": page_size}

            print(f"Listing glossary entries for glossary: {glossary_id}")
            print(f"URL: {url}")

            # Make the API call
            response = requests.get(url, headers=self._get_headers(), params=params)

            if response.status_code == 200:
                data = response.json()
                entries = data.get("glossaryEntries", [])
                print(f"Found {len(entries)} glossary entries")
                return entries
            elif response.status_code == 404:
                print(f"Error: Glossary '{glossary_id}' not found")
                return []
            elif response.status_code == 403:
                print(f"Error: Permission denied. Check your service account permissions.")
                return []
            else:
                print(f"Error: HTTP {response.status_code} - {response.text}")
                return []

        except Exception as e:
            print(f"Error listing glossary entries: {e}")
            return []

    def get_glossary_entry(self, glossary_id: str, entry_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific glossary entry by ID.

        Args:
            glossary_id: The ID of the glossary
            entry_id: The ID of the glossary entry

        Returns:
            Glossary entry as dictionary or None if not found
        """
        try:
            # Construct the URL
            url = f"{self.base_url}/{self.parent}/glossaries/{glossary_id}/glossaryEntries/{entry_id}"

            print(f"Getting glossary entry: {entry_id}")
            print(f"URL: {url}")

            # Make the API call
            response = requests.get(url, headers=self._get_headers())

            if response.status_code == 200:
                entry = response.json()
                print(f"Retrieved entry: {entry_id}")
                return entry
            elif response.status_code == 404:
                print(f"Error: Glossary entry '{entry_id}' not found")
                return None
            else:
                print(f"Error: HTTP {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"Error getting glossary entry: {e}")
            return None

    def create_glossary_entry(self, glossary_id: str, terms: List[Dict[str, str]],
                            description: str = "") -> Optional[str]:
        """
        Create a new glossary entry.

        Args:
            glossary_id: The ID of the glossary
            terms: List of terms with language_code and text
            description: Description of the glossary entry

        Returns:
            The ID of the created entry or None if failed
        """
        try:
            # Construct the URL
            url = f"{self.base_url}/{self.parent}/glossaries/{glossary_id}/glossaryEntries"

            # Prepare the request body
            request_body = {
                "termsSet": {
                    "terms": terms
                }
            }

            if description:
                request_body["description"] = description

            print(f"Creating glossary entry in glossary: {glossary_id}")
            print(f"URL: {url}")
            print(f"Request body: {json.dumps(request_body, indent=2)}")

            # Make the API call
            response = requests.post(url, headers=self._get_headers(), json=request_body)

            if response.status_code == 200:
                entry = response.json()
                entry_id = entry["name"].split("/")[-1]
                print(f"Created glossary entry: {entry_id}")
                return entry_id
            else:
                print(f"Error: HTTP {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"Error creating glossary entry: {e}")
            return None

    def update_glossary_entry(self, glossary_id: str, entry_id: str,
                            terms: List[Dict[str, str]], description: str = "") -> bool:
        """
        Update an existing glossary entry.

        Args:
            glossary_id: The ID of the glossary
            entry_id: The ID of the glossary entry
            terms: List of terms with language_code and text
            description: Description of the glossary entry

        Returns:
            True if successful, False otherwise
        """
        try:
            # Construct the URL
            url = f"{self.base_url}/{self.parent}/glossaries/{glossary_id}/glossaryEntries/{entry_id}"

            # Prepare the request body
            request_body = {
                "termsSet": {
                    "terms": terms
                }
            }

            if description:
                request_body["description"] = description

            print(f"Updating glossary entry: {entry_id}")
            print(f"URL: {url}")
            print(f"Request body: {json.dumps(request_body, indent=2)}")

            # Make the API call
            response = requests.patch(url, headers=self._get_headers(), json=request_body)

            if response.status_code == 200:
                entry = response.json()
                print(f"Updated glossary entry: {entry_id}")
                return True
            else:
                print(f"Error: HTTP {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"Error updating glossary entry: {e}")
            return False

    def delete_glossary_entry(self, glossary_id: str, entry_id: str) -> bool:
        """
        Delete a glossary entry.

        Args:
            glossary_id: The ID of the glossary
            entry_id: The ID of the glossary entry

        Returns:
            True if successful, False otherwise
        """
        try:
            # Construct the URL
            url = f"{self.base_url}/{self.parent}/glossaries/{glossary_id}/glossaryEntries/{entry_id}"

            print(f"Deleting glossary entry: {entry_id}")
            print(f"URL: {url}")

            # Make the API call
            response = requests.delete(url, headers=self._get_headers())

            if response.status_code == 200:
                print(f"Deleted glossary entry: {entry_id}")
                return True
            else:
                print(f"Error: HTTP {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"Error deleting glossary entry: {e}")
            return False


def main():
    """Main function to handle command line arguments and execute operations."""
    parser = argparse.ArgumentParser(
        description="Google Cloud Translation v3 Glossary Entry Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all entries in a glossary
  python glossary_manager.py list --project-id my-project --glossary-id my-glossary --auth-file auth_files/service-account.json

  # Get a specific entry
  python glossary_manager.py get --project-id my-project --glossary-id my-glossary --entry-id entry-123 --auth-file auth_files/service-account.json

  # Create a new entry
  python glossary_manager.py create --project-id my-project --glossary-id my-glossary --terms '[{"language_code": "en", "text": "hello"}, {"language_code": "es", "text": "hola"}]' --auth-file auth_files/service-account.json
        """
    )

    parser.add_argument("action", choices=["list", "get", "create", "update", "delete"],
                       help="Action to perform")
    parser.add_argument("--project-id", required=True,
                       help="Google Cloud project ID")
    parser.add_argument("--glossary-id", required=True,
                       help="Glossary ID")
    parser.add_argument("--auth-file", required=True,
                       help="Path to service account JSON file")
    parser.add_argument("--location", default="us-central1",
                       help="Google Cloud location (default: us-central1)")
    parser.add_argument("--entry-id",
                       help="Glossary entry ID (required for get, update, delete actions)")
    parser.add_argument("--terms",
                       help="JSON string of terms for create/update actions")
    parser.add_argument("--description", default="",
                       help="Description for the glossary entry")
    parser.add_argument("--page-size", type=int, default=100,
                       help="Number of entries to return per page (default: 100)")
    parser.add_argument("--output", choices=["json", "table"],
                       default="table", help="Output format (default: table)")

    args = parser.parse_args()

    # Validate arguments
    if args.action in ["get", "update", "delete"] and not args.entry_id:
        parser.error(f"Action '{args.action}' requires --entry-id")

    if args.action in ["create", "update"] and not args.terms:
        parser.error(f"Action '{args.action}' requires --terms")

    # Check if auth file exists
    if not os.path.exists(args.auth_file):
        print(f"Error: Auth file '{args.auth_file}' not found")
        sys.exit(1)

    # Initialize the manager
    try:
        manager = GlossaryEntryManager(
            project_id=args.project_id,
            auth_file=args.auth_file,
            location=args.location
        )
    except Exception as e:
        print(f"Error initializing GlossaryEntryManager: {e}")
        sys.exit(1)

    # Execute the requested action
    if args.action == "list":
        entries = manager.list_glossary_entries(args.glossary_id, args.page_size)

        if args.output == "json":
            print(json.dumps(entries, indent=2))
        else:
            if entries:
                print(f"\nGlossary Entries for '{args.glossary_id}':")
                print("-" * 80)
                for i, entry in enumerate(entries, 1):
                    entry_id = entry.get("name", "").split("/")[-1] if entry.get("name") else f"entry-{i}"
                    print(f"\n{i}. Entry ID: {entry_id}")
                    if entry.get("description"):
                        print(f"   Description: {entry['description']}")
                    if entry.get("termsSet", {}).get("terms"):
                        print("   Terms:")
                        for term in entry["termsSet"]["terms"]:
                            print(f"     {term.get('languageCode', 'unknown')}: {term.get('text', 'unknown')}")
            else:
                print("No entries found.")

    elif args.action == "get":
        entry = manager.get_glossary_entry(args.glossary_id, args.entry_id)

        if args.output == "json":
            print(json.dumps(entry, indent=2) if entry else "null")
        else:
            if entry:
                print(f"\nGlossary Entry: {args.entry_id}")
                print("-" * 40)
                if entry.get("description"):
                    print(f"Description: {entry['description']}")
                if entry.get("termsSet", {}).get("terms"):
                    print("Terms:")
                    for term in entry["termsSet"]["terms"]:
                        print(f"  {term.get('languageCode', 'unknown')}: {term.get('text', 'unknown')}")
            else:
                print("Entry not found.")

    elif args.action == "create":
        try:
            terms = json.loads(args.terms)
            entry_id = manager.create_glossary_entry(
                args.glossary_id, terms, args.description
            )
            if entry_id:
                print(f"Successfully created entry with ID: {entry_id}")
            else:
                print("Failed to create entry.")
        except json.JSONDecodeError:
            print("Error: Invalid JSON format for --terms")
            sys.exit(1)

    elif args.action == "update":
        try:
            terms = json.loads(args.terms)
            success = manager.update_glossary_entry(
                args.glossary_id, args.entry_id, terms, args.description
            )
            if success:
                print("Successfully updated entry.")
            else:
                print("Failed to update entry.")
        except json.JSONDecodeError:
            print("Error: Invalid JSON format for --terms")
            sys.exit(1)

    elif args.action == "delete":
        success = manager.delete_glossary_entry(args.glossary_id, args.entry_id)
        if success:
            print("Successfully deleted entry.")
        else:
            print("Failed to delete entry.")


if __name__ == "__main__":
    main()
