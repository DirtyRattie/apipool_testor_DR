

# API Testing Tool
apipool_testor_DirtyRattie


## Introduction

This tool allows you to test multiple APIs and models in parallel for connectivity and accessibility. It helps identify which API endpoints and models are functional.


## Features

- Test multiple APIs with different models.
- Configurable prompts and settings.
- Results are displayed in a clear and organized format.
- Secure API key storage.

## Quick Use
1. Fill in your `api_key` and `api_url` in api_config.json
2. **Just run the script**
  ```bash
  cd apipool_testor_DirtyRattie
  python apipool_testor.py
  ```

## Installation

1. Clone the repository

```bash
git clone https://github.com/your-repo/api-testing-tool.git
cd api-testing-tool
```

2. Install the required dependencies
   
```bash
pip install -r requirements.txt
```

## Configuration

### 1. API Configuration (`api_config.json`)

Add your API URLs and API keys to the `api_config.json` file. Example:

```json
[
    {
        "api_url": "https://your-api-url.com/v1/chat/completions",
        "api_key": "your-api-key"
    }
]
```

### 2. Test Configuration (`test_config.json`)

Define the models, system prompt, and user prompt to test. Example:

```json
{
    "models": ["gpt-4", "gpt-3.5-turbo"],
    "system_prompt": "Answer briefly",
    "user_prompt": "Who are you?"
}
```

### 3. Ensure Security

You can save your private api in `api_config.json`. Make sure `api_config.json`is written in`.gitignore` to prevent uploading your keys

```
# Prevent sensitive data from being uploaded
api_config.json
```

## Usage

1. Run the tool:
   
```bash
python test_apis.py
```

2. View the results in the terminal.

## Output Example

The tool will display results like this:

```
--- Testing Results ---

API URL: https://your-api-url.com/v1/chat/completions
  - Model: gpt-4
    Status: accessible
    Reply: Hello! How can I assist you today?
  - Model: gpt-3.5-turbo
    Status: failed (status code: 401)
    Error: Unauthorized access

...
```

## Contributing

Feel free to open an issue or submit a pull request for improvements!

## License

This project is licensed under the MIT License.
