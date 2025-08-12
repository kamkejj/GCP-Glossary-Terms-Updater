"""
Configuration settings for the Glossary Transfer project.
"""

import os
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for managing different environments."""

    # Environment settings - now using environment variables
    ENVIRONMENTS = {
        'dev': {
            'credentials_file': os.getenv('DEV_CREDENTIALS_FILE', 'auth_files/dom-dx-translation-dev-da60bb26e907.json'),
            'project_id': os.getenv('DEV_PROJECT_ID', 'dom-dx-translation-dev'),
            'bucket_name': os.getenv('DEV_BUCKET_NAME', 'dom-dx-translation-dev-bucket'),
        },
        'prod': {
            'credentials_file': os.getenv('PROD_CREDENTIALS_FILE', 'auth_files/dom-dx-translation-prod-8ae379a2799e.json'),
            'project_id': os.getenv('PROD_PROJECT_ID', 'dom-dx-translation-prod'),
            'bucket_name': os.getenv('PROD_BUCKET_NAME', 'dom-dx-translation-prod-bucket'),
        }
    }

    # Supported language pairs - now configurable via environment variable
    SUPPORTED_LANGUAGE_PAIRS = os.getenv('SUPPORTED_LANGUAGE_PAIRS', 'en-es,en-fr,en-bs,en-sw').split(',')

    # CSV file settings
    CSV_SETTINGS = {
        'encoding': os.getenv('CSV_ENCODING', 'utf-8'),
        'delimiter': os.getenv('CSV_DELIMITER', ','),
        'quotechar': os.getenv('CSV_QUOTECHAR', '"'),
        'index': os.getenv('CSV_INDEX', 'False').lower() == 'true'
    }

    @classmethod
    def get_all_language_pairs(cls) -> List[str]:
        """
        Get all available language pairs including both regular and IWD variants.
        
        Returns:
            List of all language pairs (regular and IWD)
        """
        all_pairs = []
        
        # Add regular language pairs
        all_pairs.extend(cls.SUPPORTED_LANGUAGE_PAIRS)
        
        # Add IWD variants
        for pair in cls.SUPPORTED_LANGUAGE_PAIRS:
            all_pairs.append(f"iwd-{pair}")
            
        return all_pairs

    @classmethod
    def get_environment_config(cls, environment: str = 'dev') -> Dict[str, Any]:
        """
        Get configuration for a specific environment.

        Args:
            environment: Environment name ('dev' or 'prod')

        Returns:
            Dictionary with environment configuration
        """
        if environment not in cls.ENVIRONMENTS:
            raise ValueError(f"Unknown environment: {environment}")

        config = cls.ENVIRONMENTS[environment].copy()

        # Get the absolute path to the credentials file
        config['credentials_path'] = os.path.join(
            os.getcwd(),
            config['credentials_file']
        )

        return config

    @classmethod
    def validate_environment(cls, environment: str) -> bool:
        """
        Validate that an environment exists and has required files.

        Args:
            environment: Environment name to validate

        Returns:
            bool: True if valid, False otherwise
        """
        if environment not in cls.ENVIRONMENTS:
            return False

        config = cls.get_environment_config(environment)
        credentials_path = config['credentials_path']

        return os.path.exists(credentials_path)

    @classmethod
    def list_environments(cls) -> list:
        """
        List all available environments.

        Returns:
            List of environment names
        """
        return list(cls.ENVIRONMENTS.keys())

    @classmethod
    def get_current_environment(cls) -> str:
        """
        Get the current environment from environment variable.

        Returns:
            Current environment name (defaults to 'dev')
        """
        return os.getenv('ENVIRONMENT', 'dev')
