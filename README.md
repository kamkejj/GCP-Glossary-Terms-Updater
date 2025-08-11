# Glossary Transfer for Google Translation V3 API

A Python solution for managing CSV glossary files with Google Cloud Storage and the Google Translation V3 API. This project provides tools to upload, download, and manage translation glossaries across different environments.

## Features

- 📤 **Upload CSV glossaries** to Google Cloud Storage
- 📥 **Download CSV glossaries** from Google Cloud Storage
- 🔧 **Create glossaries** in Google Translation V3 API
- 📋 **List available glossaries** in both Cloud Storage and Translation API
- 🌍 **Support for multiple language pairs**
- 🔄 **Environment management** (dev/prod)
- 🛠️ **Command-line interface** for easy operations
- ✅ **CSV validation** and error handling

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

## Usage

### Command Line Interface

The project includes a comprehensive CLI for easy operations:

**Note:** All glossary files are automatically managed in the `glossaries/` folder. When uploading, specify only the filename (e.g., `glossary.csv`) and it will be looked for in the `glossaries/` folder. When downloading, the filename is automatically generated based on the language pair (e.g., `en-es` becomes `en_es_glossary.csv`), but you can also specify a custom filename.

#### Validate Environment

```bash
python cli.py --env dev validate
```

#### Upload a Glossary

```bash
python cli.py --env dev upload glossary.csv en-es --overwrite
```

#### Download a Glossary

```bash
# Download with auto-generated filename (recommended)
python cli.py --env dev download en-es

# Download with custom filename
python cli.py --env dev download en-es --output custom_glossary.csv
```

#### List Available Glossaries

```bash
# List glossaries in Cloud Storage
python cli.py --env dev list --type storage

# List glossaries in Translation API
python cli.py --env dev list --type api
```

#### Create Sample Glossary

```bash
python cli.py --env dev sample en-es sample_glossary.csv
```

#### Create Glossary in Translation API

```bash
python cli.py --env dev create-api en-es my-glossary-name
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

# Upload a glossary
success = manager.upload_glossary_csv(
    local_file_path='glossaries/my_glossary.csv',
    language_pair='en-es',
    overwrite=True
)

# Download a glossary (with auto-generated filename)
success = manager.download_glossary_csv(
    language_pair='en-es'
    # local_file_path is optional - will auto-generate filename
)

# Download a glossary with custom filename
success = manager.download_glossary_csv(
    language_pair='en-es',
    local_file_path='glossaries/custom_glossary.csv'
)

# List available glossaries
glossaries = manager.list_available_glossaries()
print(f"Available glossaries: {glossaries}")
```

## Auto-Generated Filenames

When downloading glossaries, the system automatically generates filenames based on the language pair:

- **Regular glossaries**: `en-es` → `glossaries/en_es_glossary.csv`
- **IWD glossaries**: `iwd-en-es` → `glossaries/iwd_en_es_glossary.csv`

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

- `en-es` (English to Spanish)
- `en-fr` (English to French)
- `en-de` (English to German)
- `fr-es` (French to Spanish)
- `de-fr` (German to French)
- And many more...

See `config.py` for the complete list of supported language pairs.

## File Structure

```
glossary_transfer/
├── glossary_manager.py      # Main glossary management class
├── config.py               # Configuration settings
├── cli.py                  # Command-line interface
├── example_usage.py        # Example usage scripts
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── glossaries/            # Folder for all glossary CSV files
└── auth_files/            # Folder for authentication files
    ├── dom-dx-translation-dev-da60bb26e907.json    # Dev credentials
    └── dom-dx-translation-prod-8ae379a2799e.json   # Prod credentials
```

## Error Handling

The system includes comprehensive error handling for:

- Invalid credentials
- Missing files
- Network connectivity issues
- Invalid CSV formats
- Cloud Storage permissions
- Translation API quotas

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
3. Open an issue in the repository
