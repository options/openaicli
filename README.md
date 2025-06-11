# oai.py: OpenAI CLI Tool

A command-line interface (CLI) for interacting with OpenAI's API, inspired by Azure CLI. This tool allows you to upload files, manage vector stores, perform text-to-speech (TTS), ask questions using vector search, and use Chat Completion (GPT) models—all from your terminal.

## Features
- **File Upload**: Upload files to OpenAI (supports wildcards and vector store upload)
- **Text-to-Speech (TTS)**: Convert text or files to speech (mp3)
- **Ask**: Ask questions using OpenAI's file_search tool and vector store
- **Chat Completion**: Interact with GPT models (gpt-4o, gpt-3.5-turbo, etc.)
- **Vector Store Management**: Create, list, get, and delete vector stores
- **Built-in Help**: Use the `--help` option with any command or subcommand to see detailed usage instructions and available options. For example, `python oai.py --help` or `python oai.py chat --help`.

## Requirements
- Python 3.8+
- `openai` Python package
- (Optional) `python-dotenv` if you want to use a `.env` file for your API key

## Setup
1. **Create and activate a virtual environment:**
   ```sh
   python -m venv .venv
   # Windows
   .\.venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```
2. **Install dependencies:**
   ```sh
   pip install openai python-dotenv
   ```
3. **Set your OpenAI API key as an environment variable:**
   ```sh
   $env:OPENAI_API_KEY="sk-..."   # PowerShell
   # or
   export OPENAI_API_KEY="sk-..." # Bash
   ```
   Or create a `.env` file with:
   ```
   OPENAI_API_KEY=sk-...
   ```

## Usage
Run the CLI with Python:
```sh
python oai.py <command> [options]
```

### File Upload
Upload files to OpenAI (supports wildcards):
```sh
python oai.py file upload --pattern "*.md"
python oai.py file upload --pattern "data.txt" --vector-store-id <VECTOR_STORE_ID>
```

### Text-to-Speech (TTS)
Convert text or a file to speech (mp3):
```sh
python oai.py tts --text "Hello, world!"
python oai.py tts --input-file input.txt --output output.mp3
```

### Ask (Vector Store Q&A)
Ask a question using a vector store:
```sh
python oai.py ask --vector-store-id <VECTOR_STORE_ID> --question "What is cloud computing?"
```

### Chat Completion
Chat with GPT models:
```sh
python oai.py chat --model gpt-4o --system "You are a helpful assistant." --message "Hello!"
```

## Help
For any command or subcommand, you can view detailed help and usage instructions by adding `--help`. For example:
```sh
python oai.py --help
python oai.py chat --help
python oai.py vector-store --help
```

## Version Control
The `.venv/` folder is used for the Python virtual environment and is excluded from the Git repository (see `.gitignore`).
