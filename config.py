"""
Configuration settings for the Glossary Transfer project.
"""

import os
from typing import Dict, Any


class Config:
    """Configuration class for managing different environments."""

    # Environment settings
    ENVIRONMENTS = {
        'dev': {
            'credentials_file': 'auth_files/dom-dx-translation-dev-da60bb26e907.json',
            'project_id': 'dom-dx-translation-dev',  # Update with your actual project ID
            'bucket_name': 'dom-dx-translation-dev-bucket',  # Update with your actual bucket name
        },
        'prod': {
            'credentials_file': 'auth_files/dom-dx-translation-prod-8ae379a2799e.json',
            'project_id': 'dom-dx-translation-prod',  # Update with your actual project ID
            'bucket_name': 'dom-dx-translation-prod-bucket',  # Update with your actual bucket name
        }
    }

    # Supported language pairs
    SUPPORTED_LANGUAGE_PAIRS = [
        'en-es', 'en-fr', 'en-bs', 'en-sw'
    ]

    # CSV file settings
    CSV_SETTINGS = {
        'encoding': 'utf-8',
        'delimiter': ',',
        'quotechar': '"',
        'index': False
    }

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
