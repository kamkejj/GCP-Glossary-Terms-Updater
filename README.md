# Google Cloud Translation v3 Glossary Entry Manager

A Python application for managing Google Cloud Translation v3 glossary entries. This tool provides functionality to list, create, update, and delete glossary entries using the Google Cloud Translation API.

## Features

- **List Glossary Entries**: Retrieve all entries from a glossary
- **Get Specific Entry**: Retrieve a single glossary entry by ID
- **Create New Entry**: Add new entries to a glossary
- **Update Entry**: Modify existing glossary entries
- **Delete Entry**: Remove entries from a glossary
- **Multiple Output Formats**: JSON and table output formats
- **Error Handling**: Comprehensive error handling and user feedback

## Prerequisites

- Python 3.8 or higher
- Google Cloud project with Cloud Translation API enabled
- Service account with appropriate permissions
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your Google Cloud credentials:
   - Place your service account JSON file in the `auth_files/` directory
   - Ensure the service account has the necessary permissions for Cloud Translation API

   Example contents of this file:

```bash
  {
    "type": "service_account",
    "project_id": "",
    "private_key_id": "",
    "private_key": "",
    "client_email": "",
    "client_id": "",
    "auth_uri": "",
    "token_uri": "",
    "auth_provider_x509_cert_url": "",
    "client_x509_cert_url": "",
    "universe_domain": ""
  }
```

4. Configure environment variables (optional):
   - Copy `.env.example` to `.env`
   - Update the values in `.env` with your actual project configuration:
   - Get the Project id in the service auth file

```bash
cp .env.example .env
```

Then edit `.env` and set your values:

```env
PROJECT_ID=your-actual-project-id
LOCATION=us-central1
```

## Required Permissions

Your service account needs the following permissions:

- `cloudtranslate.glossaries.list`
- `cloudtranslate.glossaryEntries.list`
- `cloudtranslate.glossaryEntries.get`
- `cloudtranslate.glossaryEntries.create`
- `cloudtranslate.glossaryEntries.update`
- `cloudtranslate.glossaryEntries.delete`

You can grant these permissions by assigning the `Cloud Translation API Editor` role (`roles/cloudtranslate.editor`) to your service account.

## Usage

### Iowa DX Glossaries

en_bs_glossary - Bosnian glossary
en_es_glossary - Spanish glossary
en_fr_glossary - French glossary
en_sw_glossary - Swahili glossary

#### IWD Specfic Glossaries

iwd_en_bs_glossary - IWD Bosnian glossary
iwd_en_es_glossary - IWD Spanish glossary
iwd_en_fr_glossary - IWD French glossary
iwd_en_sw_glossary - IWD Swahili glossary

### Command Line Interface

The application provides a command-line interface for all operations:

#### List Glossary Entries

Using default values from `.env` file:

```bash
python glossary_manager.py list \
  --glossary-id YOUR_GLOSSARY_ID \
  --auth-file auth_files/your-service-account.json
```

Or override with custom project ID:

```bash
python glossary_manager.py list \
  --project-id YOUR_PROJECT_ID \
  --glossary-id YOUR_GLOSSARY_ID \
  --auth-file auth_files/your-service-account.json
```

#### Get a Specific Entry

Using default values from `.env` file:

```bash
python glossary_manager.py get \
  --glossary-id YOUR_GLOSSARY_ID \
  --entry-id ENTRY_ID \
  --auth-file auth_files/your-service-account.json
```

#### Create a New Entry

Using default values from `.env` file:

```bash
python glossary_manager.py create \
  --glossary-id YOUR_GLOSSARY_ID \
  --terms '[{"language_code": "en", "text": "hello"}, {"language_code": "es", "text": "hola"}]' \
  --description "Greeting terms" \
  --auth-file auth_files/your-service-account.json
```

#### Update an Entry

Using default values from `.env` file:

```bash
python glossary_manager.py update \
  --glossary-id YOUR_GLOSSARY_ID \
  --entry-id ENTRY_ID \
  --terms '[{"language_code": "en", "text": "hello"}, {"language_code": "es", "text": "hola"}]' \
  --description "Updated terms" \
  --auth-file auth_files/your-service-account.json
```

#### Delete an Entry

Using default values from `.env` file:

```bash
python glossary_manager.py delete \
  --glossary-id YOUR_GLOSSARY_ID \
  --entry-id ENTRY_ID \
  --auth-file auth_files/your-service-account.json
```

### Additional Options

- `--project-id`: Google Cloud project ID (default: from `.env` file or `PROJECT_ID` environment variable)
- `--location`: Google Cloud location (default: from `.env` file or `us-central1`)
- `--page-size`: Number of entries to return per page (default: `100`)
- `--output`: Output format (`json` or `table`, default: `table`)

## Error Handling

The application provides comprehensive error handling for common issues:

- **Authentication errors**: Invalid service account credentials
- **Permission errors**: Insufficient permissions for the requested operation
- **Not found errors**: Glossary or entry doesn't exist
- **Invalid input**: Malformed JSON or missing required parameters

## Troubleshooting

### Common Issues

1. **Authentication Error**: Ensure your service account JSON file is valid and has the correct permissions
2. **Permission Denied**: Verify your service account has the necessary Cloud Translation API permissions
3. **Glossary Not Found**: Check that the glossary ID and location are correct
4. **Invalid JSON**: Ensure terms are provided in valid JSON format

### Getting Help

- Check the Google Cloud Translation API documentation: <https://cloud.google.com/translate/docs>
- Verify your service account permissions in the Google Cloud Console
- Ensure your project has the Cloud Translation API enabled

## API Reference

The application uses the Google Cloud Translation v3 API. For detailed API documentation, see:

- [Cloud Translation API Documentation](https://cloud.google.com/translate/docs)
- [Glossary Management Guide](https://cloud.google.com/translate/docs/advanced/glossary)

## License

This project is provided as-is for educational and development purposes. Please ensure compliance with Google Cloud Platform terms of service when using this application.
