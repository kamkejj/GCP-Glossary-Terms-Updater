"""
Test script to verify the basic setup and configuration.
Run this script to check if everything is properly configured.
"""

import os
import json
from config import Config


def test_configuration():
    """Test the configuration setup."""
    print("🔧 Testing Configuration...")
    print("-" * 40)
    
    # Test environment listing
    environments = Config.list_environments()
    print(f"Available environments: {environments}")
    
    # Test each environment
    for env in environments:
        print(f"\nTesting {env} environment:")
        
        # Check if environment is valid
        if Config.validate_environment(env):
            print(f"  ✅ {env} environment is valid")
            
            # Get configuration
            config = Config.get_environment_config(env)
            
            # Check credentials file
            if os.path.exists(config['credentials_path']):
                print(f"  ✅ Credentials file exists: {config['credentials_path']}")
                
                # Try to read and parse JSON
                try:
                    with open(config['credentials_path'], 'r') as f:
                        creds = json.load(f)
                    
                    # Check for required fields
                    required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email']
                    missing_fields = [field for field in required_fields if field not in creds]
                    
                    if not missing_fields:
                        print(f"  ✅ Credentials file is valid JSON with required fields")
                        print(f"  📁 Project ID in credentials: {creds.get('project_id', 'Not found')}")
                    else:
                        print(f"  ❌ Missing required fields: {missing_fields}")
                        
                except json.JSONDecodeError:
                    print(f"  ❌ Credentials file is not valid JSON")
                except Exception as e:
                    print(f"  ❌ Error reading credentials: {str(e)}")
            else:
                print(f"  ❌ Credentials file not found: {config['credentials_path']}")
            
            # Display configuration
            print(f"  🔑 Project ID: {config['project_id']}")
            print(f"  🪣 Bucket: {config['bucket_name']}")
        else:
            print(f"  ❌ {env} environment is invalid")
    
    print(f"\n🌍 Supported language pairs: {len(Config.SUPPORTED_LANGUAGE_PAIRS)}")
    print(f"📋 Sample pairs: {Config.SUPPORTED_LANGUAGE_PAIRS[:5]}")


def test_dependencies():
    """Test if required dependencies are available."""
    print("\n📦 Testing Dependencies...")
    print("-" * 40)
    
    required_packages = [
        'google.cloud.storage',
        'google.cloud.translate_v3',
        'google.oauth2',
        'pandas',
        'pathlib'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - Not installed")
    
    print("\n💡 If any packages are missing, run: pip install -r requirements.txt")


def test_file_structure():
    """Test if all required files are present."""
    print("\n📁 Testing File Structure...")
    print("-" * 40)
    
    required_files = [
        'glossary_manager.py',
        'config.py',
        'cli.py',
        'example_usage.py',
        'requirements.txt',
        'README.md'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - Missing")
    
    # Check for credential files
    print("\n🔐 Credential Files:")
    for env in Config.list_environments():
        config = Config.get_environment_config(env)
        cred_file = config['credentials_file']
        if os.path.exists(cred_file):
            print(f"  ✅ {cred_file}")
        else:
            print(f"  ❌ {cred_file} - Missing")


def main():
    """Run all tests."""
    print("🚀 Glossary Transfer Setup Test")
    print("=" * 50)
    
    test_file_structure()
    test_dependencies()
    test_configuration()
    
    print("\n" + "=" * 50)
    print("🎯 Setup Test Complete!")
    print("\nNext steps:")
    print("1. Update project IDs and bucket names in config.py")
    print("2. Install missing dependencies: pip install -r requirements.txt")
    print("3. Test with: python cli.py validate --env dev")
    print("4. Run example: python example_usage.py")


if __name__ == '__main__':
    main()
