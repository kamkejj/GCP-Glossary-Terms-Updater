#!/usr/bin/env python3
"""
Example usage of the GlossaryEntryManager

This script demonstrates how to use the GlossaryEntryManager class
to work with Google Cloud Translation v3 glossary entries.
"""

import json
import os
from glossary_manager import GlossaryEntryManager


def main():
    """Example usage of the GlossaryEntryManager."""
    
    # Configuration - update these values with your actual project and glossary details
    PROJECT_ID = "your-project-id"  # Replace with your actual project ID
    GLOSSARY_ID = "your-glossary-id"  # Replace with your actual glossary ID
    LOCATION = "us-central1"  # Update if your glossary is in a different location
    
    # Choose which auth file to use (dev or prod)
    AUTH_FILE = "auth_files/dom-dx-translation-dev-da60bb26e907.json"
    # AUTH_FILE = "auth_files/dom-dx-translation-prod-8ae379a2799e.json"
    
    # Check if auth file exists
    if not os.path.exists(AUTH_FILE):
        print(f"Error: Auth file '{AUTH_FILE}' not found")
        print("Please update the AUTH_FILE variable with the correct path")
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
        
        # Example 1: List all glossary entries
        print("\n1. Listing all glossary entries:")
        print("=" * 40)
        entries = manager.list_glossary_entries(GLOSSARY_ID)
        
        if entries:
            print(f"\nFound {len(entries)} entries:")
            for i, entry in enumerate(entries[:5], 1):  # Show first 5 entries
                entry_id = entry['name'].split('/')[-1]
                print(f"\n{i}. Entry ID: {entry_id}")
                if entry['description']:
                    print(f"   Description: {entry['description']}")
                print("   Terms:")
                for term in entry['terms']:
                    print(f"     {term['language_code']}: {term['text']}")
            
            if len(entries) > 5:
                print(f"\n... and {len(entries) - 5} more entries")
        else:
            print("No entries found in the glossary")
        
        # Example 2: Get a specific entry (if entries exist)
        if entries:
            first_entry_id = entries[0]['name'].split('/')[-1]
            print(f"\n\n2. Getting specific entry '{first_entry_id}':")
            print("=" * 50)
            
            entry = manager.get_glossary_entry(GLOSSARY_ID, first_entry_id)
            if entry:
                print(f"Entry ID: {first_entry_id}")
                if entry['description']:
                    print(f"Description: {entry['description']}")
                print("Terms:")
                for term in entry['terms']:
                    print(f"  {term['language_code']}: {term['text']}")
            else:
                print(f"Entry '{first_entry_id}' not found")
        
        # Example 3: Create a new entry (commented out to avoid accidental creation)
        print(f"\n\n3. Example of creating a new entry (commented out):")
        print("=" * 55)
        
        # Example terms for a new entry
        example_terms = [
            {"language_code": "en", "text": "example"},
            {"language_code": "es", "text": "ejemplo"},
            {"language_code": "fr", "text": "exemple"}
        ]
        
        print("To create a new entry, uncomment the following code:")
        print("```python")
        print("entry_id = manager.create_glossary_entry(")
        print(f"    glossary_id='{GLOSSARY_ID}',")
        print(f"    terms={json.dumps(example_terms, indent=4)},")
        print("    description='Example entry for demonstration'")
        print(")")
        print("if entry_id:")
        print(f"    print(f'Created entry with ID: {{entry_id}}')")
        print("```")
        
        # Example 4: Update an entry (commented out to avoid accidental modification)
        print(f"\n\n4. Example of updating an entry (commented out):")
        print("=" * 50)
        
        if entries:
            first_entry_id = entries[0]['name'].split('/')[-1]
            print(f"To update entry '{first_entry_id}', uncomment the following code:")
            print("```python")
            print("updated_terms = [")
            print('    {"language_code": "en", "text": "updated example"},')
            print('    {"language_code": "es", "text": "ejemplo actualizado"}')
            print("]")
            print("success = manager.update_glossary_entry(")
            print(f"    glossary_id='{GLOSSARY_ID}',")
            print(f"    entry_id='{first_entry_id}',")
            print("    terms=updated_terms,")
            print("    description='Updated description'")
            print(")")
            print("if success:")
            print("    print('Entry updated successfully')")
            print("```")
        
        # Example 5: Delete an entry (commented out to avoid accidental deletion)
        print(f"\n\n5. Example of deleting an entry (commented out):")
        print("=" * 50)
        
        if entries:
            first_entry_id = entries[0]['name'].split('/')[-1]
            print(f"To delete entry '{first_entry_id}', uncomment the following code:")
            print("```python")
            print("success = manager.delete_glossary_entry(")
            print(f"    glossary_id='{GLOSSARY_ID}',")
            print(f"    entry_id='{first_entry_id}'")
            print(")")
            print("if success:")
            print("    print('Entry deleted successfully')")
            print("```")
        
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


if __name__ == "__main__":
    main()
