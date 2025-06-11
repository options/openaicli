# OpenAI CLI Tool

A command-line interface for OpenAI API: upload files, manage vector stores, TTS, Q&A, and chat.

## Requirements

- Python 3.8+
- `openai` Python package
- Set the `OPENAI_API_KEY` environment variable

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python src/oai.py <command> [options]
```

### Commands

#### file-upload

Upload files to OpenAI. Supports wildcards and vector store upload.

**Examples:**
```bash
python src/oai.py file-upload --pattern '*.md'
python src/oai.py file-upload --pattern 'data.txt' --vector-store-id <ID>
```

**Options:**
- `--pattern` (required): File name or wildcard pattern to upload. Example: `*.md`, `data.txt`
- `--vector-store-id`: (Optional) Vector Store ID to upload files into.
- `--purpose`: Purpose of the file. Default: `assistants`.

---

#### tts

Convert text or a file to speech (mp3).

**Examples:**
```bash
python src/oai.py tts --text 'Hello'
python src/oai.py tts --input-file input.txt --output output.mp3
```

**Options:**
- `--text`: Text to convert to speech.
- `--input-file`: Path to a text file to convert to speech.
- `--output`: Output mp3 file name. Default: `speech_output.mp3`
- `--model`: TTS model name. Default: `tts-1-hd`
- `--voice`: TTS voice name. Default: `echo`

---

#### ask

Ask a question using OpenAI's file_search tool and vector store.

**Example:**
```bash
python src/oai.py ask --vector-store-id <ID> --question 'What is cloud computing?'
```

**Options:**
- `--vector-store-id`: Vector Store ID to use for context-aware search.
- `--question`: Question text.

---

#### chat

Chat with GPT models.

**Examples:**
```bash
python src/oai.py chat --user 'Tell me a joke.'
python src/oai.py chat --system 'You are a helpful assistant.' --user 'Summarize this.'
python src/oai.py chat --user 'Stream this answer.' --stream
```

**Options:**
- `--model`: Model name. Default: `gpt-4o`
- `--system`: System prompt (optional).
- `--user`: User prompt (optional).
- `--stream`: Use streaming output.

---

#### vector-store

Manage vector stores: create, list, get, delete.

**Examples:**
```bash
python src/oai.py vector-store create --name 'MyStore' --description 'Test'
python src/oai.py vector-store list
python src/oai.py vector-store get --id <ID>
python src/oai.py vector-store delete --id <ID>
```

**Subcommands:**
- `create`: Create a new vector store (`--name`, `--description`)
- `list`: List all vector stores
- `get`: Get details of a vector store (`--id`)
- `delete`: Delete a vector store (`--id`)

---

## Development

Standard Python project layout. Main CLI entrypoint: `src/oai.py`.

## License

MIT
