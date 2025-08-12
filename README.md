# Glossary Transfer for Google Translation V3 API

A Python solution for managing CSV glossary files with Google Cloud Storage and the Google Translation V3 API. This project provides tools to upload, download, and manage translation glossaries across different environments, with support for both regular and IWD (Iowa Workforce Development) glossaries.

## Features

- 📤 **Upload CSV glossaries** to Google Cloud Storage
- 📥 **Download CSV glossaries** from Cloud Storage
- 🔧 **Create glossaries** in Google Translation V3 API
- 📋 **List available glossaries** in both Cloud Storage and Translation API
- 🌍 **Support for multiple language pairs**
- 🏢 **IWD glossary support** - Special handling for Iowa Workforce Development glossaries
- 🔄 **Environment management** (dev/prod)
- 🛠️ **Command-line interface** for easy operations
- ✅ **CSV validation** and error handling
- 📁 **Smart file organization** - Separates regular and IWD glossaries

## Prerequisites

- Python 3.8 or higher
- Google Cloud project with Translation API enabled
- Google Cloud Storage bucket for glossaries
- Service account credentials JSON file

## Installation

1. **Clone or download the project files**

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your environment:**
   - Copy `.env.example` to `.env` and update with your actual values
   - Ensure your service account JSON files are in the project directory

## Configuration

The project uses environment variables for configuration, making it easy to manage different environments and sensitive data.

### Environment Variables Setup

1. **Copy the example environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file** with your actual values:

   ```bash
   # Current environment (dev or prod)
   ENVIRONMENT=dev

   # Development environment settings
   DEV_CREDENTIALS_FILE=auth_files/dom-dx-translation-dev-da60bb26e907.json
   DEV_PROJECT_ID=your-dev-project-id
   DEV_BUCKET_NAME=your-dev-bucket-name

   # Production environment settings
   PROD_CREDENTIALS_FILE=auth_files/dom-dx-translation-prod-8ae379a2799e.json
   PROD_PROJECT_ID=your-prod-project-id
   PROD_BUCKET_NAME=your-prod-bucket-name

   # Supported language pairs (comma-separated)
   SUPPORTED_LANGUAGE_PAIRS=en-es,en-fr,en-bs,en-sw

   # CSV file settings
   CSV_ENCODING=utf-8
   CSV_DELIMITER=,
   CSV_QUOTECHAR="
   CSV_INDEX=False
   ```

### Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Current environment (dev/prod) | `dev` |
| `DEV_CREDENTIALS_FILE` | Path to dev credentials JSON file | `auth_files/dom-dx-translation-dev-da60bb26e907.json` |
| `DEV_PROJECT_ID` | Google Cloud dev project ID | `dom-dx-translation-dev` |
| `DEV_BUCKET_NAME` | Google Cloud Storage dev bucket name | `dom-dx-translation-dev-bucket` |
| `PROD_CREDENTIALS_FILE` | Path to prod credentials JSON file | `auth_files/dom-dx-translation-prod-8ae379a2799e.json` |
| `PROD_PROJECT_ID` | Google Cloud prod project ID | `dom-dx-translation-prod` |
| `PROD_BUCKET_NAME` | Google Cloud Storage prod bucket name | `dom-dx-translation-prod-bucket` |
| `SUPPORTED_LANGUAGE_PAIRS` | Comma-separated list of language pairs | `en-es,en-fr,en-bs,en-sw` |
| `CSV_ENCODING` | CSV file encoding | `utf-8` |
| `CSV_DELIMITER` | CSV delimiter character | `,` |
| `CSV_QUOTECHAR` | CSV quote character | `"` |
| `CSV_INDEX` | Whether to include index in CSV | `False` |

### Legacy Configuration (Optional)

If you prefer to edit `config.py` directly, you can still do so. The environment variables will override the hardcoded values.

## Glossary Types

The system supports two types of glossaries:

### Regular Glossaries
- Standard translation glossaries
- Filename format: `{source}_{target}_glossary.csv` (e.g., `en_es_glossary.csv`)
- Language pair format: `{source}-{target}` (e.g., `en-es`)

### IWD Glossaries
- Special glossaries for Iowa Workforce Development
- Filename format: `iwd_{source}_{target}_glossary.csv` (e.g., `iwd_en_bs_glossary.csv`)
- Language pair format: `iwd-{source}-{target}` (e.g., `iwd-en-bs`)

The system automatically detects the glossary type based on the filename and provides appropriate language pair options during upload and download operations.

## Usage

### Interactive Command Line Interface

The project includes a user-friendly interactive CLI that guides you through each operation with prompts and selections:

**Note:** All glossary files are automatically managed in the `glossaries/` folder. The interactive CLI will show you available files and let you select from lists instead of typing commands.

#### Running the Interactive CLI

```bash
python cli.py
```

The CLI will guide you through:

1. **Environment Selection**: Choose between `dev` or `prod`
2. **Operation Selection**: Choose from available operations:
   - Upload CSV glossary to Cloud Storage
   - Download CSV glossary from Cloud Storage
   - List available glossaries
   - Validate environment configuration
3. **File Selection**: Browse and select CSV files from the `glossaries/` folder
   - Files are organized by type (Regular vs IWD glossaries)
4. **Language Pair Selection**: Choose from appropriate language pairs based on file type
5. **Additional Options**: Configure overwrite settings, custom filenames, etc.

#### Example Interactive Session

```
🌍 Glossary Transfer CLI
==================================================

Select environment:
  1. dev
  2. prod
  3. Cancel

Enter your choice (1-3): 1

Select operation:
  1. Upload CSV glossary to Cloud Storage
  2. Download CSV glossary from Cloud Storage
  3. List available glossaries
  4. Validate environment configuration
  5. Cancel

Enter your choice (1-5): 1

📤 Upload CSV Glossary to Cloud Storage (dev)
--------------------------------------------------

Select CSV file to upload:
Available CSV files:
  Regular glossaries:
    1. en_es_glossary.csv
    2. en_fr_glossary.csv
  IWD glossaries:
    3. iwd_en_bs_glossary.csv
    4. Cancel

Enter your choice (1-4): 3

Select IWD language pair:
  1. iwd-en-es
  2. iwd-en-fr
  3. iwd-en-bs
  4. iwd-en-sw
  5. Cancel

Enter your choice (1-5): 3

Overwrite existing file?
  1. Yes
  2. No
  3. Cancel

Enter your choice (1-3): 2

✅ Successfully uploaded glossaries/iwd_en_bs_glossary.csv for iwd-en-bs
```

### Programmatic Usage

```python
from glossary_manager import GlossaryManager
from config import Config

# Get configuration
config = Config.get_environment_config('dev')

# Initialize manager
manager = GlossaryManager(
    credentials_path=config['credentials_path'],
    project_id=config['project_id'],
    bucket_name=config['bucket_name']
)

# Upload a regular glossary
success = manager.upload_glossary_csv(
    local_file_path='glossaries/en_es_glossary.csv',
    language_pair='en-es',
    overwrite=True
)

# Upload an IWD glossary
success = manager.upload_glossary_csv(
    local_file_path='glossaries/iwd_en_bs_glossary.csv',
    language_pair='iwd-en-bs',
    overwrite=True
)

# Download a regular glossary (with auto-generated filename)
success = manager.download_glossary_csv(
    language_pair='en-es'
    # local_file_path is optional - will auto-generate filename
)

# Download an IWD glossary with custom filename
success = manager.download_glossary_csv(
    language_pair='iwd-en-bs',
    local_file_path='glossaries/custom_iwd_glossary.csv'
)

# List available glossaries (includes both regular and IWD)
glossaries = manager.list_available_glossaries()
print(f"Available glossaries: {glossaries}")
# Output: ['en-es', 'en-fr', 'iwd-en-bs', 'iwd-en-sw']
```

## Auto-Generated Filenames

When downloading glossaries, the system automatically generates filenames based on the language pair:

- **Regular glossaries**: `en-es` → `glossaries/en_es_glossary.csv`
- **IWD glossaries**: `iwd-en-bs` → `glossaries/iwd_en_bs_glossary.csv`

This ensures consistent naming conventions and eliminates the need to remember specific filenames. You can still specify a custom filename if needed.

## CSV Format

Glossary CSV files should have the following format:

```csv
en,es
hello,hola
world,mundo
computer,computadora
software,software
database,base de datos
```

- First column: Source language terms
- Second column: Target language terms
- No headers required (though they can be included)
- UTF-8 encoding recommended

## Supported Language Pairs

The system supports various language pairs including:

### Regular Language Pairs
- `en-es` (English to Spanish)
- `en-fr` (English to French)
- `en-bs` (English to Bosnian)
- `en-sw` (English to Swahili)

### IWD Language Pairs
- `iwd-en-es` (IWD English to Spanish)
- `iwd-en-fr` (IWD English to French)
- `iwd-en-bs` (IWD English to Bosnian)
- `iwd-en-sw` (IWD English to Swahili)

The system automatically generates IWD variants for all regular language pairs. See `config.py` for the complete list of supported language pairs.

## File Structure

```
glossary_transfer/
├── glossary_manager.py      # Main glossary management class
├── config.py               # Configuration settings
├── cli.py                  # Command-line interface
├── example_usage.py        # Example usage scripts
├── test_glossary_types.py  # Test script for IWD functionality
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── glossaries/            # Folder for all glossary CSV files
│   ├── en_es_glossary.csv      # Regular glossary
│   ├── en_fr_glossary.csv      # Regular glossary
│   └── iwd_en_bs_glossary.csv  # IWD glossary
└── auth_files/            # Folder for authentication files
    ├── dom-dx-translation-dev-da60bb26e907.json    # Dev credentials
    └── dom-dx-translation-prod-8ae379a2799e.json   # Prod credentials
```

## Testing

Run the test script to verify IWD functionality:

```bash
python test_glossary_types.py
```

This will test:
- IWD vs regular glossary detection
- Language pair validation
- Filename generation
- Configuration methods
- File organization

## Error Handling

The system includes comprehensive error handling for:

- Invalid credentials
- Missing files
- Network connectivity issues
- Invalid CSV formats
- Cloud Storage permissions
- Translation API quotas
- Filename/language pair mismatches
- IWD vs regular glossary validation

## Examples

Run the example script to see the system in action:

```bash
python example_usage.py
```

This will demonstrate:

- Creating sample glossaries
- Uploading to Cloud Storage
- Downloading from Cloud Storage
- Creating glossaries in Translation API
- Listing available glossaries

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Ensure your service account JSON file is valid
   - Check that the service account has the necessary permissions

2. **Bucket Not Found**
   - Verify the bucket name in `config.py`
   - Ensure the bucket exists in your Google Cloud project

3. **Translation API Errors**
   - Enable the Translation API in your Google Cloud project
   - Check your API quotas and billing

4. **CSV Format Issues**
   - Ensure the CSV has at least 2 columns
   - Check for proper UTF-8 encoding
   - Verify the file is not empty

5. **Filename/Language Pair Mismatch**
   - Ensure IWD files use `iwd-` prefixed language pairs
   - Regular files should use standard language pairs
   - Check that filenames match the expected naming convention

### Debug Mode

Enable debug logging by modifying the logging level in `glossary_manager.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review the example usage
3. Run the test script to verify functionality
4. Open an issue in the repository
