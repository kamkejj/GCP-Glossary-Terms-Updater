#!/usr/bin/env python3
"""
Demo script for GlossaryEntryManager

This script demonstrates how to use the GlossaryEntryManager with the actual
auth files in the project. Update the configuration variables below with your
actual project and glossary details.
"""

import json
import os
from glossary_manager import GlossaryEntryManager


def main():
    """Demo the GlossaryEntryManager functionality."""
    
    # Configuration - UPDATE THESE VALUES with your actual details
    PROJECT_ID = "your-project-id"  # Replace with your actual project ID
    GLOSSARY_ID = "your-glossary-id"  # Replace with your actual glossary ID
    LOCATION = "us-central1"  # Update if your glossary is in a different location
    
    # Choose which auth file to use (dev or prod)
    AUTH_FILE = "auth_files/dom-dx-translation-dev-da60bb26e907.json"
    # AUTH_FILE = "auth_files/dom-dx-translation-prod-8ae379a2799e.json"
    
    print("Google Cloud Translation v3 Glossary Entry Manager Demo")
    print("=" * 60)
    
    # Check if auth file exists
    if not os.path.exists(AUTH_FILE):
        print(f"Error: Auth file '{AUTH_FILE}' not found")
        print("Available auth files:")
        for file in os.listdir("auth_files"):
            if file.endswith(".json"):
                print(f"  - auth_files/{file}")
        return
    
    # Check if configuration is set
    if PROJECT_ID == "your-project-id" or GLOSSARY_ID == "your-glossary-id":
        print("Please update the configuration variables in this script:")
        print(f"  PROJECT_ID: {PROJECT_ID}")
        print(f"  GLOSSARY_ID: {GLOSSARY_ID}")
        print(f"  LOCATION: {LOCATION}")
        print(f"  AUTH_FILE: {AUTH_FILE}")
        print("\nExample:")
        print("  PROJECT_ID = 'my-translation-project'")
        print("  GLOSSARY_ID = 'my-glossary'")
        return
    
    try:
        # Initialize the glossary manager
        print(f"Initializing GlossaryEntryManager...")
        print(f"Project ID: {PROJECT_ID}")
        print(f"Glossary ID: {GLOSSARY_ID}")
        print(f"Location: {LOCATION}")
        print(f"Auth file: {AUTH_FILE}")
        print("-" * 60)
        
        manager = GlossaryEntryManager(
            project_id=PROJECT_ID,
            auth_file=AUTH_FILE,
            location=LOCATION
        )
        
        # Demo 1: List all glossary entries
        print("\n1. Listing all glossary entries:")
        print("=" * 40)
        entries = manager.list_glossary_entries(GLOSSARY_ID)
        
        if entries:
            print(f"\nFound {len(entries)} entries:")
            for i, entry in enumerate(entries[:3], 1):  # Show first 3 entries
                entry_id = entry.get("name", "").split("/")[-1] if entry.get("name") else f"entry-{i}"
                print(f"\n{i}. Entry ID: {entry_id}")
                if entry.get("description"):
                    print(f"   Description: {entry['description']}")
                if entry.get("termsSet", {}).get("terms"):
                    print("   Terms:")
                    for term in entry["termsSet"]["terms"]:
                        print(f"     {term.get('languageCode', 'unknown')}: {term.get('text', 'unknown')}")
            
            if len(entries) > 3:
                print(f"\n... and {len(entries) - 3} more entries")
        else:
            print("No entries found in the glossary")
        
        # Demo 2: Get a specific entry (if entries exist)
        if entries:
            first_entry_id = entries[0].get("name", "").split("/")[-1] if entries[0].get("name") else "entry-1"
            print(f"\n\n2. Getting specific entry '{first_entry_id}':")
            print("=" * 50)
            
            entry = manager.get_glossary_entry(GLOSSARY_ID, first_entry_id)
            if entry:
                print(f"Entry ID: {first_entry_id}")
                if entry.get("description"):
                    print(f"Description: {entry['description']}")
                if entry.get("termsSet", {}).get("terms"):
                    print("Terms:")
                    for term in entry["termsSet"]["terms"]:
                        print(f"  {term.get('languageCode', 'unknown')}: {term.get('text', 'unknown')}")
            else:
                print(f"Entry '{first_entry_id}' not found")
        
        # Demo 3: Show how to create a new entry (without actually creating it)
        print(f"\n\n3. Example of creating a new entry:")
        print("=" * 45)
        
        example_terms = [
            {"language_code": "en", "text": "demo"},
            {"language_code": "es", "text": "demostración"},
            {"language_code": "fr", "text": "démonstration"}
        ]
        
        print("To create a new entry, use:")
        print("```python")
        print("entry_id = manager.create_glossary_entry(")
        print(f"    glossary_id='{GLOSSARY_ID}',")
        print(f"    terms={json.dumps(example_terms, indent=4)},")
        print("    description='Demo entry for testing'")
        print(")")
        print("```")
        
        # Demo 4: Show command line usage
        print(f"\n\n4. Command line usage examples:")
        print("=" * 40)
        
        print("List all entries:")
        print(f"python glossary_manager.py list --project-id {PROJECT_ID} --glossary-id {GLOSSARY_ID} --auth-file {AUTH_FILE}")
        
        if entries:
            first_entry_id = entries[0].get("name", "").split("/")[-1] if entries[0].get("name") else "entry-1"
            print(f"\nGet specific entry:")
            print(f"python glossary_manager.py get --project-id {PROJECT_ID} --glossary-id {GLOSSARY_ID} --entry-id {first_entry_id} --auth-file {AUTH_FILE}")
        
        print(f"\nCreate new entry:")
        print(f"python glossary_manager.py create --project-id {PROJECT_ID} --glossary-id {GLOSSARY_ID} --terms '[{{\"language_code\": \"en\", \"text\": \"hello\"}}, {{\"language_code\": \"es\", \"text\": \"hola\"}}]' --auth-file {AUTH_FILE}")
        
        print(f"\n\nConfiguration Summary:")
        print("=" * 25)
        print(f"Project ID: {PROJECT_ID}")
        print(f"Glossary ID: {GLOSSARY_ID}")
        print(f"Location: {LOCATION}")
        print(f"Auth file: {AUTH_FILE}")
        print(f"Total entries found: {len(entries) if entries else 0}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you have updated PROJECT_ID and GLOSSARY_ID with your actual values")
        print("2. Verify that the auth file exists and has the correct permissions")
        print("3. Check that your service account has the necessary permissions for Cloud Translation API")
        print("4. Ensure the glossary exists in the specified location")
        print("5. Make sure the Cloud Translation API is enabled in your project")


if __name__ == "__main__":
    main()
