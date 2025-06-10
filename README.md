# oai.py: OpenAI CLI Tool

A command-line interface (CLI) for interacting with OpenAI's API, inspired by Azure CLI. This tool allows you to upload files, manage vector stores, perform text-to-speech (TTS), ask questions using vector search, and use Chat Completion (GPT) models—all from your terminal.

## Features
- **File Upload**: Upload files to OpenAI (supports wildcards and vector store upload)
- **Text-to-Speech (TTS)**: Convert text or files to speech (mp3)
- **Ask**: Ask questions using OpenAI's file_search tool and vector store
- **Chat Completion**: Interact with GPT models (gpt-4o, gpt-3.5-turbo, etc.)
- **Vector Store Management**: Create, list, get, and delete vector stores

## Requirements
- Python 3.8+
- `openai` Python package
- (Optional) `python-dotenv` if you want to use a `.env` file for your API key

## Setup
1. **Install dependencies:**
   ```sh
   pip install openai
   ```
   (Optional for .env support)
   ```sh
   pip install python-dotenv
   ```
2. **Set your OpenAI API key as an environment variable:**
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
python oai.py chat --user "Tell me a joke."
python oai.py chat --system "You are a helpful assistant." --user "Summarize this document."
python oai.py chat --user "Stream this answer." --stream
```

### Vector Store Management
Create, list, get, and delete vector stores:
```sh
python oai.py vector-store create --name "MyStore" --description "Test vector store"
python oai.py vector-store list
python oai.py vector-store get --id <VECTOR_STORE_ID>
python oai.py vector-store delete --id <VECTOR_STORE_ID>
```

## Help
For help on any command, use:
```sh
python oai.py --help
python oai.py <command> --help
```

## License
MIT License
