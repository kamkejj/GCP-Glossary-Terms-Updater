#!/usr/bin/env python3
"""
Test script for GlossaryEntryManager

This script tests the basic functionality of the GlossaryEntryManager class
without making actual API calls to Google Cloud.
"""

import json
import os
import sys
from unittest.mock import Mock, patch
from glossary_manager import GlossaryEntryManager


def test_initialization():
    """Test GlossaryEntryManager initialization."""
    print("Testing GlossaryEntryManager initialization...")
    
    # Mock the service account credentials
    with patch('glossary_manager.service_account.Credentials.from_service_account_file') as mock_creds:
        mock_creds.return_value = Mock()
        
        # Test initialization
        manager = GlossaryEntryManager(
            project_id="test-project",
            auth_file="auth_files/test-auth.json",
            location="us-central1"
        )
        
        assert manager.project_id == "test-project"
        assert manager.location == "us-central1"
        assert manager.auth_file == "auth_files/test-auth.json"
        assert manager.parent == "projects/test-project/locations/us-central1"
        assert manager.base_url == "https://translation.googleapis.com/v3"
        
        print("✓ Initialization test passed")


def test_get_headers():
    """Test _get_headers method."""
    print("Testing _get_headers method...")
    
    with patch('glossary_manager.service_account.Credentials.from_service_account_file') as mock_creds:
        mock_creds.return_value = Mock()
        
        manager = GlossaryEntryManager(
            project_id="test-project",
            auth_file="auth_files/test-auth.json"
        )
        
        # Mock the credentials
        manager.credentials.token = "test-token"
        manager.credentials.valid = True
        
        headers = manager._get_headers()
        
        assert headers["Authorization"] == "Bearer test-token"
        assert headers["Content-Type"] == "application/json; charset=utf-8"
        assert headers["x-goog-user-project"] == "test-project"
        
        print("✓ Get headers test passed")


def test_list_glossary_entries():
    """Test list_glossary_entries method."""
    print("Testing list_glossary_entries method...")
    
    with patch('glossary_manager.service_account.Credentials.from_service_account_file') as mock_creds:
        mock_creds.return_value = Mock()
        
        with patch('glossary_manager.requests.get') as mock_get:
            # Create a mock response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "glossaryEntries": [
                    {
                        "name": "projects/test-project/locations/us-central1/glossaries/test-glossary/glossaryEntries/entry-123",
                        "description": "Test entry",
                        "termsSet": {
                            "terms": [
                                {
                                    "languageCode": "en",
                                    "text": "hello"
                                }
                            ]
                        }
                    }
                ]
            }
            mock_get.return_value = mock_response
            
            # Initialize manager
            manager = GlossaryEntryManager(
                project_id="test-project",
                auth_file="auth_files/test-auth.json"
            )
            
            # Mock the credentials
            manager.credentials.token = "test-token"
            manager.credentials.valid = True
            
            # Test listing entries
            entries = manager.list_glossary_entries("test-glossary")
            
            assert len(entries) == 1
            assert entries[0]["name"] == "projects/test-project/locations/us-central1/glossaries/test-glossary/glossaryEntries/entry-123"
            assert entries[0]["description"] == "Test entry"
            assert len(entries[0]["termsSet"]["terms"]) == 1
            assert entries[0]["termsSet"]["terms"][0]["languageCode"] == "en"
            assert entries[0]["termsSet"]["terms"][0]["text"] == "hello"
            
            # Verify the API call
            mock_get.assert_called_once()
            call_args = mock_get.call_args
            assert "test-glossary/glossaryEntries" in call_args[0][0]
            assert call_args[1]["params"]["pageSize"] == 100
            
            print("✓ List glossary entries test passed")


def test_get_glossary_entry():
    """Test get_glossary_entry method."""
    print("Testing get_glossary_entry method...")
    
    with patch('glossary_manager.service_account.Credentials.from_service_account_file') as mock_creds:
        mock_creds.return_value = Mock()
        
        with patch('glossary_manager.requests.get') as mock_get:
            # Create a mock response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "name": "projects/test-project/locations/us-central1/glossaries/test-glossary/glossaryEntries/entry-123",
                "description": "Test entry",
                "termsSet": {
                    "terms": [
                        {
                            "languageCode": "en",
                            "text": "hello"
                        }
                    ]
                }
            }
            mock_get.return_value = mock_response
            
            # Initialize manager
            manager = GlossaryEntryManager(
                project_id="test-project",
                auth_file="auth_files/test-auth.json"
            )
            
            # Mock the credentials
            manager.credentials.token = "test-token"
            manager.credentials.valid = True
            
            # Test getting an entry
            entry = manager.get_glossary_entry("test-glossary", "entry-123")
            
            assert entry is not None
            assert entry["name"] == "projects/test-project/locations/us-central1/glossaries/test-glossary/glossaryEntries/entry-123"
            assert entry["description"] == "Test entry"
            assert len(entry["termsSet"]["terms"]) == 1
            assert entry["termsSet"]["terms"][0]["languageCode"] == "en"
            assert entry["termsSet"]["terms"][0]["text"] == "hello"
            
            # Verify the API call
            mock_get.assert_called_once()
            call_args = mock_get.call_args
            assert "test-glossary/glossaryEntries/entry-123" in call_args[0][0]
            
            print("✓ Get glossary entry test passed")


def test_create_glossary_entry():
    """Test create_glossary_entry method."""
    print("Testing create_glossary_entry method...")
    
    with patch('glossary_manager.service_account.Credentials.from_service_account_file') as mock_creds:
        mock_creds.return_value = Mock()
        
        with patch('glossary_manager.requests.post') as mock_post:
            # Create a mock response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "name": "projects/test-project/locations/us-central1/glossaries/test-glossary/glossaryEntries/new-entry-456"
            }
            mock_post.return_value = mock_response
            
            # Initialize manager
            manager = GlossaryEntryManager(
                project_id="test-project",
                auth_file="auth_files/test-auth.json"
            )
            
            # Mock the credentials
            manager.credentials.token = "test-token"
            manager.credentials.valid = True
            
            # Test creating an entry
            terms = [
                {"language_code": "en", "text": "hello"},
                {"language_code": "es", "text": "hola"}
            ]
            
            entry_id = manager.create_glossary_entry("test-glossary", terms, "Test entry")
            
            assert entry_id == "new-entry-456"
            
            # Verify the API call
            mock_post.assert_called_once()
            call_args = mock_post.call_args
            assert "test-glossary/glossaryEntries" in call_args[0][0]
            
            # Verify the request body
            request_body = call_args[1]["json"]
            assert request_body["termsSet"]["terms"] == terms
            assert request_body["description"] == "Test entry"
            
            print("✓ Create glossary entry test passed")


def test_error_handling():
    """Test error handling."""
    print("Testing error handling...")
    
    with patch('glossary_manager.service_account.Credentials.from_service_account_file') as mock_creds:
        mock_creds.return_value = Mock()
        
        with patch('glossary_manager.requests.get') as mock_get:
            # Create a mock response for 404 error
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.text = "Glossary not found"
            mock_get.return_value = mock_response
            
            # Initialize manager
            manager = GlossaryEntryManager(
                project_id="test-project",
                auth_file="auth_files/test-auth.json"
            )
            
            # Mock the credentials
            manager.credentials.token = "test-token"
            manager.credentials.valid = True
            
            # Test error handling
            entries = manager.list_glossary_entries("non-existent-glossary")
            
            assert entries == []
            
            print("✓ Error handling test passed")


def test_command_line_parsing():
    """Test command line argument parsing."""
    print("Testing command line argument parsing...")
    
    # Test with valid arguments
    test_args = [
        "list",
        "--project-id", "test-project",
        "--glossary-id", "test-glossary",
        "--auth-file", "auth_files/test-auth.json"
    ]
    
    with patch.object(sys, 'argv', ['glossary_manager.py'] + test_args):
        with patch('glossary_manager.GlossaryEntryManager') as mock_manager_class:
            mock_manager = Mock()
            mock_manager_class.return_value = mock_manager
            mock_manager.list_glossary_entries.return_value = []
            
            # Import and run main (this will test argument parsing)
            from glossary_manager import main
            main()
            
            # Verify the manager was called correctly
            mock_manager_class.assert_called_once_with(
                project_id="test-project",
                auth_file="auth_files/test-auth.json",
                location="us-central1"
            )
            mock_manager.list_glossary_entries.assert_called_once_with("test-glossary", 100)
            
            print("✓ Command line parsing test passed")


def main():
    """Run all tests."""
    print("Running GlossaryEntryManager tests...")
    print("=" * 50)
    
    try:
        test_initialization()
        test_get_headers()
        test_list_glossary_entries()
        test_get_glossary_entry()
        test_create_glossary_entry()
        test_error_handling()
        test_command_line_parsing()
        
        print("\n" + "=" * 50)
        print("✓ All tests passed!")
        print("\nThe GlossaryEntryManager is ready to use.")
        print("\nTo use with real data:")
        print("1. Update the configuration in example_usage.py")
        print("2. Run: python example_usage.py")
        print("3. Or use the command line interface:")
        print("   python glossary_manager.py list --project-id YOUR_PROJECT --glossary-id YOUR_GLOSSARY --auth-file auth_files/your-auth.json")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
