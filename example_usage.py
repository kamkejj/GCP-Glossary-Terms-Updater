"""
Example usage of the Glossary Manager for Google Translation V3 API.
This script demonstrates how to use the GlossaryManager class programmatically.
"""

import os
from glossary_manager import GlossaryManager
from config import Config


def main():
    """Example usage of the GlossaryManager."""
    
    # Configuration
    environment = 'dev'  # or 'prod'
    config = Config.get_environment_config(environment)
    
    print(f"🚀 Starting Glossary Manager example for {environment} environment")
    print(f"📁 Project: {config['project_id']}")
    print(f"🪣 Bucket: {config['bucket_name']}")
    print("-" * 50)
    
    # Initialize the glossary manager
    manager = GlossaryManager(
        credentials_path=config['credentials_path'],
        project_id=config['project_id'],
        bucket_name=config['bucket_name']
    )
    
    # Example 1: Create a sample glossary CSV
    print("\n📝 Example 1: Creating a sample glossary CSV")
    sample_file = "glossaries/en-es_sample.csv"
    success = manager.create_sample_glossary_csv(
        language_pair='en-es',
        output_path=sample_file
    )
    
    if success:
        print(f"✅ Created sample glossary: {sample_file}")
    else:
        print("❌ Failed to create sample glossary")
        return
    
    # Example 2: Upload the sample glossary to Cloud Storage
    print("\n📤 Example 2: Uploading glossary to Cloud Storage")
    success = manager.upload_glossary_csv(
        local_file_path=sample_file,
        language_pair='en-es',
        overwrite=True
    )
    
    if success:
        print("✅ Successfully uploaded glossary to Cloud Storage")
    else:
        print("❌ Failed to upload glossary")
        return
    
    # Example 3: List available glossaries in Cloud Storage
    print("\n📋 Example 3: Listing available glossaries in Cloud Storage")
    glossaries = manager.list_available_glossaries()
    
    if glossaries:
        print("Available glossaries:")
        for lang_pair in glossaries:
            print(f"  • {lang_pair}")
    else:
        print("No glossaries found in Cloud Storage")
    
    # Example 4: Download a glossary from Cloud Storage
    print("\n📥 Example 4: Downloading glossary from Cloud Storage")
    download_path = "glossaries/en-es_downloaded.csv"
    success = manager.download_glossary_csv(
        language_pair='en-es',
        local_file_path=download_path
    )
    
    if success:
        print(f"✅ Successfully downloaded glossary to {download_path}")
    else:
        print("❌ Failed to download glossary")
    
    # Example 5: Create a glossary in the Translation API
    print("\n🔧 Example 5: Creating glossary in Translation API")
    success = manager.create_glossary_in_translation_api(
        language_pair='en-es',
        glossary_name='example-glossary-en-es'
    )
    
    if success:
        print("✅ Successfully created glossary in Translation API")
    else:
        print("❌ Failed to create glossary in Translation API")
    
    # Example 6: List glossaries in Translation API
    print("\n📋 Example 6: Listing glossaries in Translation API")
    api_glossaries = manager.list_translation_glossaries()
    
    if api_glossaries:
        print("Translation API glossaries:")
        for glossary in api_glossaries:
            print(f"  • {glossary['name']} ({glossary['language_pair']}) - {glossary['state']}")
    else:
        print("No glossaries found in Translation API")
    
    print("\n🎉 Example completed successfully!")


def batch_upload_example():
    """Example of batch uploading multiple glossaries."""
    
    print("\n🔄 Batch Upload Example")
    print("-" * 30)
    
    # Configuration
    environment = 'dev'
    config = Config.get_environment_config(environment)
    
    # Initialize manager
    manager = GlossaryManager(
        credentials_path=config['credentials_path'],
        project_id=config['project_id'],
        bucket_name=config['bucket_name']
    )
    
    # Language pairs to process
    language_pairs = ['en-es', 'en-fr', 'en-de', 'fr-es', 'de-fr']
    
    for lang_pair in language_pairs:
        print(f"\nProcessing {lang_pair}...")
        
        # Create sample file
        sample_file = f"glossaries/{lang_pair}_sample.csv"
        success = manager.create_sample_glossary_csv(
            language_pair=lang_pair,
            output_path=sample_file
        )
        
        if success:
            # Upload to Cloud Storage
            upload_success = manager.upload_glossary_csv(
                local_file_path=sample_file,
                language_pair=lang_pair,
                overwrite=True
            )
            
            if upload_success:
                print(f"✅ Successfully processed {lang_pair}")
            else:
                print(f"❌ Failed to upload {lang_pair}")
        else:
            print(f"❌ Failed to create sample for {lang_pair}")
    
    print("\n🎯 Batch upload example completed!")


if __name__ == '__main__':
    # Run the main example
    main()
    
    # Run the batch upload example
    batch_upload_example()
