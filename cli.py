"""
Interactive command-line interface for the Glossary Transfer project.
Provides easy access to glossary management operations with user-friendly prompts.
"""

import sys
import os
from pathlib import Path
from typing import Optional

from glossary_manager import GlossaryManager
from config import Config


def get_user_choice(options: list, prompt: str, allow_cancel: bool = True) -> Optional[str]:
    """
    Get user choice from a list of options.

    Args:
        options: List of options to choose from
        prompt: Prompt message to display
        allow_cancel: Whether to allow canceling the operation

    Returns:
        Selected option or None if canceled
    """
    while True:
        print(f"\n{prompt}")
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")

        if allow_cancel:
            print(f"  {len(options) + 1}. Cancel")

        try:
            choice = input(f"\nEnter your choice (1-{len(options) + (1 if allow_cancel else 0)}): ").strip()
            choice_num = int(choice)

            if allow_cancel and choice_num == len(options) + 1:
                return None

            if 1 <= choice_num <= len(options):
                return options[choice_num - 1]
            else:
                print("❌ Invalid choice. Please try again.")
        except ValueError:
            print("❌ Please enter a valid number.")
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Goodbye!")
            sys.exit(0)


def get_file_input(prompt: str, folder: str = "glossaries") -> Optional[str]:
    """
    Get file input from user with validation.

    Args:
        prompt: Prompt message to display
        folder: Folder to look for files in

    Returns:
        Selected filename or None if canceled
    """
    folder_path = Path(folder)
    if not folder_path.exists():
        print(f"❌ Folder '{folder}' does not exist.")
        return None

    files = [f.name for f in folder_path.iterdir() if f.is_file() and f.suffix.lower() == '.csv']

    if not files:
        print(f"❌ No CSV files found in '{folder}' folder.")
        return None

    # Separate IWD and regular files
    iwd_files = [f for f in files if f.startswith('iwd_')]
    regular_files = [f for f in files if not f.startswith('iwd_')]

    print(f"\n{prompt}")
    print("Available CSV files:")
    
    file_counter = 1
    file_mapping = {}
    
    # Display regular files first
    if regular_files:
        print("  Regular glossaries:")
        for file in regular_files:
            print(f"    {file_counter}. {file}")
            file_mapping[file_counter] = file
            file_counter += 1
    
    # Display IWD files
    if iwd_files:
        print("  IWD glossaries:")
        for file in iwd_files:
            print(f"    {file_counter}. {file}")
            file_mapping[file_counter] = file
            file_counter += 1
    
    print(f"  {file_counter}. Cancel")

    try:
        choice = input(f"\nEnter your choice (1-{file_counter}): ").strip()
        choice_num = int(choice)

        if choice_num == file_counter:
            return None

        if 1 <= choice_num < file_counter:
            return file_mapping[choice_num]
        else:
            print("❌ Invalid choice.")
            return None
    except ValueError:
        print("❌ Please enter a valid number.")
        return None
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Goodbye!")
        sys.exit(0)


def get_text_input(prompt: str, allow_empty: bool = False) -> Optional[str]:
    """
    Get text input from user.

    Args:
        prompt: Prompt message to display
        allow_empty: Whether to allow empty input

    Returns:
        User input or None if canceled
    """
    try:
        while True:
            user_input = input(f"\n{prompt}: ").strip()
            if allow_empty or user_input:
                return user_input
            print("❌ Input cannot be empty. Please try again.")
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Goodbye!")
        sys.exit(0)


def main():
    """Main interactive CLI function."""
    print("🌍 Glossary Transfer CLI")
    print("=" * 50)

    # Step 1: Select environment
    environments = Config.list_environments()
    environment = get_user_choice(environments, "Select environment:")
    if not environment:
        print("👋 Operation canceled.")
        return

    # Validate environment
    if not Config.validate_environment(environment):
        print(f"❌ Invalid environment: {environment}")
        print(f"Available environments: {', '.join(environments)}")
        sys.exit(1)

    # Step 2: Select operation
    operations = [
        "Upload CSV glossary to Cloud Storage",
        "Download CSV glossary from Cloud Storage",
        "List available glossaries",
        "Validate environment configuration"
    ]

    operation = get_user_choice(operations, "Select operation:")
    if not operation:
        print("👋 Operation canceled.")
        return

    try:
        # Get configuration
        config = Config.get_environment_config(environment)

        # Initialize glossary manager
        manager = GlossaryManager(
            credentials_path=config['credentials_path'],
            project_id=config['project_id'],
            bucket_name=config['bucket_name']
        )

        # Execute selected operation
        if operation == "Upload CSV glossary to Cloud Storage":
            handle_upload(manager, environment)
        elif operation == "Download CSV glossary from Cloud Storage":
            handle_download(manager, environment)
        elif operation == "List available glossaries":
            handle_list(manager)
        elif operation == "Validate environment configuration":
            handle_validate(config, environment)

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


def handle_upload(manager: GlossaryManager, environment: str):
    """Handle upload operation."""
    print(f"\n📤 Upload CSV Glossary to Cloud Storage ({environment})")
    print("-" * 50)

    # Get file to upload
    filename = get_file_input("Select CSV file to upload:")
    if not filename:
        print("👋 Upload canceled.")
        return

    # Determine if this is an IWD glossary based on filename
    is_iwd = filename.startswith('iwd_')
    
    # Get language pair - show appropriate options based on file type
    if is_iwd:
        # For IWD files, show only IWD language pairs
        iwd_pairs = [f"iwd-{pair}" for pair in Config.SUPPORTED_LANGUAGE_PAIRS]
        language_pair = get_user_choice(iwd_pairs, "Select IWD language pair:")
    else:
        # For regular files, show only regular language pairs
        language_pair = get_user_choice(Config.SUPPORTED_LANGUAGE_PAIRS, "Select language pair:")
    
    if not language_pair:
        print("👋 Upload canceled.")
        return

    # Ask about overwrite
    overwrite_choice = get_user_choice(["Yes", "No"], "Overwrite existing file?")
    if not overwrite_choice:
        print("👋 Upload canceled.")
        return

    overwrite = overwrite_choice == "Yes"

    # Perform upload
    file_path = Path('glossaries') / filename
    success = manager.upload_glossary_csv(
        local_file_path=str(file_path),
        language_pair=language_pair,
        overwrite=overwrite
    )

    if success:
        print(f"✅ Successfully uploaded {file_path} for {language_pair}")
    else:
        print(f"❌ Failed to upload {file_path}")


def handle_download(manager: GlossaryManager, environment: str):
    """Handle download operation."""
    print(f"\n📥 Download CSV Glossary from Cloud Storage ({environment})")
    print("-" * 50)

    # Get all available glossaries from Cloud Storage
    available_glossaries = manager.list_available_glossaries()
    
    if not available_glossaries:
        print("❌ No glossaries found in Cloud Storage")
        return

    # Get language pair from available glossaries
    language_pair = get_user_choice(available_glossaries, "Select language pair to download:")
    if not language_pair:
        print("👋 Download canceled.")
        return

    # Ask for custom output filename
    custom_filename = get_text_input("Enter custom output filename (or press Enter for auto-generated):", allow_empty=True)

    # Perform download
    output_path = None
    if custom_filename:
        glossaries_path = Path('glossaries')
        glossaries_path.mkdir(exist_ok=True)
        output_path = str(glossaries_path / custom_filename)

    success = manager.download_glossary_csv(
        language_pair=language_pair,
        local_file_path=output_path
    )

    if success:
        if output_path:
            print(f"✅ Successfully downloaded {language_pair} to {output_path}")
        else:
            auto_path = manager._generate_glossary_filename(language_pair)
            print(f"✅ Successfully downloaded {language_pair} to {auto_path}")
    else:
        print(f"❌ Failed to download {language_pair}")


def handle_list(manager: GlossaryManager):
    """Handle list operation."""
    print(f"\n📋 List Available Glossaries")
    print("-" * 50)

    list_type = get_user_choice(["Cloud Storage", "Translation API"], "Select type to list:")
    if not list_type:
        print("👋 List operation canceled.")
        return

    if list_type == "Cloud Storage":
        glossaries = manager.list_available_glossaries()
        if glossaries:
            print("\n📋 Available glossaries in Cloud Storage:")
            for lang_pair in glossaries:
                print(f"  • {lang_pair}")
        else:
            print("\n📋 No glossaries found in Cloud Storage")
    else:  # Translation API
        glossaries = manager.list_translation_glossaries()
        if glossaries:
            print("\n📋 Available glossaries in Translation API:")
            for glossary in glossaries:
                print(f"  • {glossary['name']} ({glossary['language_pair']}) - {glossary['state']}")
        else:
            print("\n📋 No glossaries found in Translation API")





def handle_validate(config: dict, environment: str):
    """Handle validate operation."""
    print(f"\n🔧 Environment Configuration Validation ({environment})")
    print("-" * 50)

    print(f"🔧 Environment: {environment}")
    print(f"📁 Credentials: {config['credentials_path']}")
    print(f"🔑 Project ID: {config['project_id']}")
    print(f"🪣 Bucket: {config['bucket_name']}")

    if os.path.exists(config['credentials_path']):
        print("✅ Credentials file exists")
    else:
        print("❌ Credentials file not found")

    print(f"🌍 Supported language pairs: {len(Config.SUPPORTED_LANGUAGE_PAIRS)}")
    print("Available language pairs:")
    
    # Display regular language pairs
    print("  Regular glossaries:")
    for lang_pair in Config.SUPPORTED_LANGUAGE_PAIRS:
        print(f"    • {lang_pair}")
    
    # Display IWD language pairs
    print("  IWD glossaries:")
    for lang_pair in Config.SUPPORTED_LANGUAGE_PAIRS:
        print(f"    • iwd-{lang_pair}")
    
    print(f"  Total available pairs: {len(Config.get_all_language_pairs())}")


if __name__ == '__main__':
    main()
