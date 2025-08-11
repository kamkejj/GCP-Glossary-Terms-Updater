"""
Command-line interface for the Glossary Transfer project.
Provides easy access to glossary management operations.
"""

import argparse
import sys
import os
from pathlib import Path

from glossary_manager import GlossaryManager
from config import Config


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Glossary Transfer CLI - Manage CSV glossaries for Google Translation V3 API"
    )
    
    # Global arguments
    parser.add_argument(
        '--env', 
        choices=['dev', 'prod'], 
        default='dev',
        help='Environment to use (default: dev)'
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Upload command
    upload_parser = subparsers.add_parser('upload', help='Upload a CSV glossary to Cloud Storage')
    upload_parser.add_argument('file', help='Filename in glossaries/ folder to upload')
    upload_parser.add_argument('language_pair', help='Language pair (e.g., en-es, fr-de)')
    upload_parser.add_argument('--overwrite', action='store_true', help='Overwrite existing file')
    
    # Download command
    download_parser = subparsers.add_parser('download', help='Download a CSV glossary from Cloud Storage')
    download_parser.add_argument('language_pair', help='Language pair (e.g., en-es, fr-de)')
    download_parser.add_argument('output', help='Output filename (will be saved to glossaries/ folder)')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available glossaries')
    list_parser.add_argument('--type', choices=['storage', 'api'], default='storage',
                           help='Type of glossaries to list (default: storage)')
    
    # Create sample command
    sample_parser = subparsers.add_parser('sample', help='Create a sample CSV glossary')
    sample_parser.add_argument('language_pair', help='Language pair (e.g., en-es, fr-de)')
    sample_parser.add_argument('output', help='Output filename (will be saved to glossaries/ folder)')
    
    # Create API glossary command
    api_parser = subparsers.add_parser('create-api', help='Create glossary in Translation API')
    api_parser.add_argument('language_pair', help='Language pair (e.g., en-es, fr-de)')
    api_parser.add_argument('name', help='Name for the glossary in the Translation API')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate environment configuration')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Validate environment
    if not Config.validate_environment(args.env):
        print(f"❌ Invalid environment: {args.env}")
        print(f"Available environments: {', '.join(Config.list_environments())}")
        sys.exit(1)
    
    try:
        # Get configuration
        config = Config.get_environment_config(args.env)
        
        # Initialize glossary manager
        manager = GlossaryManager(
            credentials_path=config['credentials_path'],
            project_id=config['project_id'],
            bucket_name=config['bucket_name']
        )
        
        # Execute command
        if args.command == 'upload':
            # Ensure file is in glossaries folder
            glossaries_path = Path('glossaries')
            glossaries_path.mkdir(exist_ok=True)
            file_path = glossaries_path / args.file
            
            success = manager.upload_glossary_csv(
                local_file_path=str(file_path),
                language_pair=args.language_pair,
                overwrite=args.overwrite
            )
            if success:
                print(f"✅ Successfully uploaded {file_path} for {args.language_pair}")
            else:
                print(f"❌ Failed to upload {file_path}")
                sys.exit(1)
        
        elif args.command == 'download':
            # Ensure glossaries folder exists
            glossaries_path = Path('glossaries')
            glossaries_path.mkdir(exist_ok=True)
            output_path = glossaries_path / args.output
            
            success = manager.download_glossary_csv(
                language_pair=args.language_pair,
                local_file_path=str(output_path)
            )
            if success:
                print(f"✅ Successfully downloaded {args.language_pair} to {output_path}")
            else:
                print(f"❌ Failed to download {args.language_pair}")
                sys.exit(1)
        
        elif args.command == 'list':
            if args.type == 'storage':
                glossaries = manager.list_available_glossaries()
                if glossaries:
                    print("📋 Available glossaries in Cloud Storage:")
                    for lang_pair in glossaries:
                        print(f"  • {lang_pair}")
                else:
                    print("📋 No glossaries found in Cloud Storage")
            else:  # api
                glossaries = manager.list_translation_glossaries()
                if glossaries:
                    print("📋 Available glossaries in Translation API:")
                    for glossary in glossaries:
                        print(f"  • {glossary['name']} ({glossary['language_pair']}) - {glossary['state']}")
                else:
                    print("📋 No glossaries found in Translation API")
        
        elif args.command == 'sample':
            # Ensure glossaries folder exists
            glossaries_path = Path('glossaries')
            glossaries_path.mkdir(exist_ok=True)
            output_path = glossaries_path / args.output
            
            success = manager.create_sample_glossary_csv(
                language_pair=args.language_pair,
                output_path=str(output_path)
            )
            if success:
                print(f"✅ Created sample glossary: {output_path}")
            else:
                print(f"❌ Failed to create sample glossary")
                sys.exit(1)
        
        elif args.command == 'create-api':
            success = manager.create_glossary_in_translation_api(
                language_pair=args.language_pair,
                glossary_name=args.name
            )
            if success:
                print(f"✅ Successfully created glossary '{args.name}' in Translation API")
            else:
                print(f"❌ Failed to create glossary in Translation API")
                sys.exit(1)
        
        elif args.command == 'validate':
            print(f"🔧 Environment: {args.env}")
            print(f"📁 Credentials: {config['credentials_path']}")
            print(f"🔑 Project ID: {config['project_id']}")
            print(f"🪣 Bucket: {config['bucket_name']}")
            
            if os.path.exists(config['credentials_path']):
                print("✅ Credentials file exists")
            else:
                print("❌ Credentials file not found")
            
            print(f"🌍 Supported language pairs: {len(Config.SUPPORTED_LANGUAGE_PAIRS)}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
