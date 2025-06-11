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
python src/oai.py file-upload --file '*.md'
python src/oai.py file-upload --file 'data.txt' --vector-store-id <ID>
```

**Options:**
- `--file` (required): File name or wildcard pattern to upload. Example: `*.md`, `data.txt`
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
- `--vector-store-id`: (Optional) Vector Store ID to use file_search tool in chat.

---

#### vector-store

Manage vector stores: create, list, get, delete.

**Examples:**
```bash
python src/oai.py vector-store create --name 'MyStore'
python src/oai.py vector-store list
python src/oai.py vector-store get --id <ID>
python src/oai.py vector-store delete --id <ID>
```

**Subcommands:**
- `create`: Create a new vector store (`--name`)
- `list`: List all vector stores
- `get`: Get details of a vector store (`--id`)
- `delete`: Delete a vector store (`--id`)

---

#### vector-store-file

Manage files in a vector store: list, retrieve-file, retrieve-file-content, update-file-attribute, delete-file.

**Examples:**
```bash
python src/oai.py vector-store-file list --vector-store-id <ID>
python src/oai.py vector-store-file retrieve-file --vector-store-id <ID> --file-id <FILE_ID>
python src/oai.py vector-store-file retrieve-file-content --vector-store-id <ID> --file-id <FILE_ID>
python src/oai.py vector-store-file update-file-attribute --vector-store-id <ID> --file-id <FILE_ID> --attribute metadata --value '{"key":"value"}'
python src/oai.py vector-store-file delete-file --vector-store-id <ID> --file-id <FILE_ID>
```

**Subcommands:**
- `list`: List files in a vector store (`--vector-store-id`, optional: `--filter`, `--order`, `--limit`)
- `retrieve-file`: Retrieve a file object (`--vector-store-id`, `--file-id`)
- `retrieve-file-content`: Retrieve file content (`--vector-store-id`, `--file-id`)
- `update-file-attribute`: Update file attribute (`--vector-store-id`, `--file-id`, `--attribute`, `--value`)
- `delete-file`: Delete a file (`--vector-store-id`, `--file-id`)

**Options for `list`:**
- `--filter`: Filter by file status (`in_progress`, `completed`, `failed`, `cancelled`)
- `--order`: Sort order by created_at (`asc` or `desc`, default: `desc`)
- `--limit`: Number of files per page (1-100, default: 100)

---

## Development

Standard Python project layout. Main CLI entrypoint: `src/oai.py`.

## License

MIT
