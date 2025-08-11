"""
Glossary Manager for Google Translation V3 API with Cloud Storage integration.
Handles downloading and uploading CSV glossary files to/from Google Cloud Storage.
"""

import os
import json
import logging
from typing import List, Dict, Optional, Tuple
from pathlib import Path

import pandas as pd
from google.cloud import storage, translate_v3
from google.oauth2 import service_account
from google.api_core import exceptions


class GlossaryManager:
    """
    Manages glossary CSV files for Google Translation V3 API using Cloud Storage.
    """
    
    def __init__(self, credentials_path: str, project_id: str, bucket_name: str):
        """
        Initialize the GlossaryManager.
        
        Args:
            credentials_path: Path to the Google Cloud service account JSON file
            project_id: Google Cloud project ID
            bucket_name: Name of the Cloud Storage bucket for glossaries
        """
        self.credentials_path = credentials_path
        self.project_id = project_id
        self.bucket_name = bucket_name
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize clients
        self._setup_clients()
        
        # Supported languages (can be extended)
        self.supported_languages = [
            'en', 'es', 'fr', 'de', 'it', 'pt', 'nl', 'ja', 'ko', 'zh', 
            'ar', 'hi', 'ru', 'sv', 'da', 'no', 'fi', 'pl', 'tr', 'th'
        ]
    
    def _setup_clients(self):
        """Setup Google Cloud clients with authentication."""
        try:
            # Load credentials
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path
            )
            
            # Initialize clients
            self.storage_client = storage.Client(
                credentials=credentials, 
                project=self.project_id
            )
            self.translate_client = translate_v3.TranslationServiceClient(
                credentials=credentials
            )
            
            self.logger.info(f"Successfully initialized clients for project: {self.project_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to setup clients: {str(e)}")
            raise
    
    def upload_glossary_csv(self, local_file_path: str, language_pair: str, 
                           overwrite: bool = False) -> bool:
        """
        Upload a CSV glossary file to Cloud Storage.
        
        Args:
            local_file_path: Path to the local CSV file
            language_pair: Language pair (e.g., 'en-es', 'fr-de')
            overwrite: Whether to overwrite existing file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate file exists
            if not os.path.exists(local_file_path):
                self.logger.error(f"File not found: {local_file_path}")
                return False
            
            # Validate CSV format
            if not self._validate_csv_format(local_file_path):
                self.logger.error(f"Invalid CSV format: {local_file_path}")
                return False
            
            # Create blob name - handle both regular and IWD glossaries
            if language_pair.startswith('iwd-'):
                # IWD glossary: iwd-en-es -> iwd_en_es_glossary.csv
                clean_pair = language_pair[4:]  # Remove 'iwd-' prefix
                blob_name = f"iwd_{clean_pair.replace('-', '_')}_glossary.csv"
            else:
                # Regular glossary: en-es -> en_es_glossary.csv
                blob_name = f"{language_pair.replace('-', '_')}_glossary.csv"
            
            # Get bucket and blob
            bucket = self.storage_client.bucket(self.bucket_name)
            blob = bucket.blob(blob_name)
            
            # Check if file exists and overwrite flag
            if blob.exists() and not overwrite:
                self.logger.warning(f"File already exists: {blob_name}. Use overwrite=True to replace.")
                return False
            
            # Upload file
            blob.upload_from_filename(local_file_path)
            
            self.logger.info(f"Successfully uploaded {local_file_path} to {blob_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to upload glossary: {str(e)}")
            return False
    
    def download_glossary_csv(self, language_pair: str, local_file_path: str) -> bool:
        """
        Download a CSV glossary file from Cloud Storage.
        
        Args:
            language_pair: Language pair (e.g., 'en-es', 'fr-de')
            local_file_path: Path where to save the local CSV file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create blob name - handle both regular and IWD glossaries
            if language_pair.startswith('iwd-'):
                # IWD glossary: iwd-en-es -> iwd_en_es_glossary.csv
                clean_pair = language_pair[4:]  # Remove 'iwd-' prefix
                blob_name = f"iwd_{clean_pair.replace('-', '_')}_glossary.csv"
            else:
                # Regular glossary: en-es -> en_es_glossary.csv
                blob_name = f"{language_pair.replace('-', '_')}_glossary.csv"
            
            # Get bucket and blob
            bucket = self.storage_client.bucket(self.bucket_name)
            blob = bucket.blob(blob_name)
            
            # Check if file exists
            if not blob.exists():
                self.logger.error(f"File not found in Cloud Storage: {blob_name}")
                return False
            
            # Create directory if it doesn't exist (only if there's a directory path)
            if os.path.dirname(local_file_path):
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            
            # Download file
            blob.download_to_filename(local_file_path)
            
            self.logger.info(f"Successfully downloaded {blob_name} to {local_file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to download glossary: {str(e)}")
            return False
    
    def list_available_glossaries(self) -> List[str]:
        """
        List all available glossaries in Cloud Storage.
        
        Returns:
            List of language pairs that have glossaries
        """
        try:
            bucket = self.storage_client.bucket(self.bucket_name)
            blobs = bucket.list_blobs()
            
            glossaries = []
            for blob in blobs:
                if blob.name.endswith('glossary.csv'):
                    # Handle both path structures:
                    # 1. glossaries/{language_pair}/glossary.csv (new structure)
                    # 2. {language_pair}_glossary.csv (current structure)
                    
                    if blob.name.startswith('glossaries/'):
                        # New structure: glossaries/en-es/glossary.csv
                        parts = blob.name.split('/')
                        if len(parts) >= 3:
                            language_pair = parts[1]
                            glossaries.append(language_pair)
                    else:
                        # Current structure: en_es_glossary.csv or iwd_en_es_glossary.csv
                        filename = blob.name.replace('_glossary.csv', '')
                        
                        # Handle iwd_ prefix
                        if filename.startswith('iwd_'):
                            filename = filename[4:]  # Remove 'iwd_' prefix
                            # Convert underscores to hyphens for language pairs
                            language_pair = filename.replace('_', '-')
                            glossaries.append(f"iwd-{language_pair}")
                        else:
                            # Convert underscores to hyphens for language pairs
                            language_pair = filename.replace('_', '-')
                            glossaries.append(language_pair)
            
            return list(set(glossaries))  # Remove duplicates
            
        except Exception as e:
            self.logger.error(f"Failed to list glossaries: {str(e)}")
            return []
    
    def create_glossary_in_translation_api(self, language_pair: str, 
                                         glossary_name: str) -> bool:
        """
        Create a glossary in the Google Translation API using the CSV from Cloud Storage.
        
        Args:
            language_pair: Language pair (e.g., 'en-es', 'fr-de')
            glossary_name: Name for the glossary in the Translation API
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get the source and target languages
            source_lang, target_lang = language_pair.split('-')
            
            # Create the parent resource name
            parent = f"projects/{self.project_id}/locations/global"
            
            # Create the glossary resource
            glossary = {
                "name": f"{parent}/glossaries/{glossary_name}",
                "language_pair": {
                    "source_language_code": source_lang,
                    "target_language_code": target_lang
                },
                "input_config": {
                    "gcs_source": {
                        "input_uri": f"gs://{self.bucket_name}/{language_pair.replace('-', '_')}_glossary.csv" if not language_pair.startswith('iwd-') else f"gs://{self.bucket_name}/iwd_{language_pair[4:].replace('-', '_')}_glossary.csv"
                    }
                }
            }
            
            # Create the glossary
            operation = self.translate_client.create_glossary(
                parent=parent,
                glossary=glossary
            )
            
            # Wait for the operation to complete
            result = operation.result()
            
            self.logger.info(f"Successfully created glossary: {glossary_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create glossary in Translation API: {str(e)}")
            return False
    
    def list_translation_glossaries(self) -> List[Dict]:
        """
        List all glossaries in the Google Translation API.
        
        Returns:
            List of glossary information dictionaries
        """
        try:
            parent = f"projects/{self.project_id}/locations/global"
            
            glossaries = []
            for glossary in self.translate_client.list_glossaries(parent=parent):
                glossaries.append({
                    'name': glossary.name,
                    'language_pair': f"{glossary.language_pair.source_language_code}-{glossary.language_pair.target_language_code}",
                    'entry_count': glossary.entry_count,
                    'state': glossary.state.name
                })
            
            return glossaries
            
        except Exception as e:
            self.logger.error(f"Failed to list Translation API glossaries: {str(e)}")
            return []
    
    def _validate_csv_format(self, file_path: str) -> bool:
        """
        Validate that the CSV file has the correct format for glossaries.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            df = pd.read_csv(file_path)
            
            # Check if it has at least 2 columns (source and target)
            if len(df.columns) < 2:
                self.logger.error("CSV must have at least 2 columns (source and target)")
                return False
            
            # Check if it has data
            if len(df) == 0:
                self.logger.error("CSV file is empty")
                return False
            
            self.logger.info(f"CSV validation passed: {len(df)} entries, {len(df.columns)} columns")
            return True
            
        except Exception as e:
            self.logger.error(f"CSV validation failed: {str(e)}")
            return False
    
    def create_sample_glossary_csv(self, language_pair: str, output_path: str) -> bool:
        """
        Create a sample CSV file for a language pair.
        
        Args:
            language_pair: Language pair (e.g., 'en-es', 'fr-de')
            output_path: Path where to save the sample CSV
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            source_lang, target_lang = language_pair.split('-')
            
            # Sample data (you can customize this)
            sample_data = {
                source_lang: ['hello', 'world', 'computer', 'software', 'database'],
                target_lang: ['hola', 'mundo', 'computadora', 'software', 'base de datos']
            }
            
            df = pd.DataFrame(sample_data)
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save to CSV
            df.to_csv(output_path, index=False)
            
            self.logger.info(f"Created sample glossary CSV: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create sample CSV: {str(e)}")
            return False
