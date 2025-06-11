import argparse
import sys
import openai
import glob
import os
from src.file_upload import upload_files
from src.tts import tts
from src.chat import chat
from src.vector_store import (
    vector_store_create, vector_store_list, vector_store_get, vector_store_delete,
    vector_store_file_list, vector_store_file_retrieve, vector_store_file_retrieve_content,
    vector_store_file_update_attribute, vector_store_file_delete
)

# Get API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Error: Please set the OPENAI_API_KEY environment variable.")
    sys.exit(1)
openai.api_key = OPENAI_API_KEY

def main():
    parser = argparse.ArgumentParser(
        prog="openai-cli",
        description="OpenAI CLI Tool\n\nA command-line interface for OpenAI API: upload files, manage vector stores, TTS, Q&A, and chat.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command")

    # 파일 업로드
    upload_parser = subparsers.add_parser(
        "file-upload",
        help="Upload files (wildcard supported)",
        description="Upload files to OpenAI. Supports wildcards and vector store upload.\n\nExamples:\n  python oai.py file-upload --file '*.md'\n  python oai.py file-upload --file 'data.txt' --vector-store-id <ID>\n"
    )
    upload_parser.add_argument(
        "--file", required=True,
        help="File name or wildcard pattern to upload. Example: *.md, data.txt"
    )
    upload_parser.add_argument(
        "--vector-store-id",
        help="(Optional) Vector Store ID to upload files into. If omitted, uploads as a general file."
    )
    upload_parser.add_argument(
        "--purpose", default="assistants",
        help="Purpose of the file. Default: assistants. Options: assistants, fine-tune, etc."
    )

    # TTS
    tts_parser = subparsers.add_parser(
        "tts",
        help="Convert text to speech (TTS)",
        description="Convert text or a file to speech (mp3).\n\nExamples:\n  python oai.py tts --text 'Hello'\n  python oai.py tts --input-file input.txt --output output.mp3\n"
    )
    tts_parser.add_argument(
        "--text",
        help="Text to convert to speech. If omitted, --input-file must be provided."
    )
    tts_parser.add_argument(
        "--input-file",
        help="Path to a text file to convert to speech."
    )
    tts_parser.add_argument(
        "--output", default="speech_output.mp3",
        help="Output mp3 file name. Default: speech_output.mp3"
    )
    tts_parser.add_argument(
        "--model", default="tts-1-hd",
        help="TTS model name. Default: tts-1-hd"
    )
    tts_parser.add_argument(
        "--voice", default="echo",
        help="TTS voice name. Default: echo"
    )

    # Chat Completion
    chat_parser = subparsers.add_parser(
        "chat",
        help="Chat Completion (GPT model conversation)",
        description="Chat with GPT models.\n\nExamples:\n  python oai.py chat --user 'Tell me a joke.'\n  python oai.py chat --system 'You are a helpful assistant.' --user 'Summarize this.'\n  python oai.py chat --user 'Stream this answer.' --stream\n"
    )
    chat_parser.add_argument(
        "--model", default="gpt-4o",
        help="Model name. Default: gpt-4o. Options: gpt-4o, gpt-3.5-turbo, etc."
    )
    chat_parser.add_argument(
        "--system",
        help="System prompt (optional). Sets the assistant's behavior."
    )
    chat_parser.add_argument(
        "--user",
        help="User prompt (optional). If omitted, will prompt for input."
    )
    chat_parser.add_argument(
        "--stream", action="store_true",
        help="Use streaming output. Prints tokens as they are generated."
    )
    chat_parser.add_argument(
        "--vector-store-id",
        help="(Optional) Vector Store ID to use file_search tool in chat."
    )

    # Vector Store management
    vs_parser = subparsers.add_parser(
        "vector-store",
        help="Manage vector stores",
        description="Manage vector stores: create, list, get, delete.\n\nExamples:\n  python oai.py vector-store create --name 'MyStore' --description 'Test'\n  python oai.py vector-store list\n  python oai.py vector-store get --id <ID>\n  python oai.py vector-store delete --id <ID>\n"
    )
    vs_subparsers = vs_parser.add_subparsers(dest="vs_command")

    # Create vector store
    vs_create = vs_subparsers.add_parser(
        "create",
        help="Create a new vector store",
        description="Create a new vector store. Requires a name. Optionally add a description."
    )
    vs_create.add_argument(
        "--name", required=True,
        help="Name for the vector store."
    )
    vs_create.add_argument(
        "--description",
        help="Description for the vector store (optional)."
    )

    # List vector stores
    vs_list = vs_subparsers.add_parser(
        "list",
        help="List all vector stores",
        description="List all vector stores in your account."
    )

    # Retrieve vector store
    vs_get = vs_subparsers.add_parser(
        "get",
        help="Get details of a vector store",
        description="Get details of a vector store by ID."
    )
    vs_get.add_argument(
        "--id", required=True,
        help="Vector Store ID to retrieve."
    )

    # Delete vector store
    vs_delete = vs_subparsers.add_parser(
        "delete",
        help="Delete a vector store",
        description="Delete a vector store by ID. This action is irreversible."
    )
    vs_delete.add_argument(
        "--id", required=True,
        help="Vector Store ID to delete."
    )

    # Vector Store File management
    vsf_parser = subparsers.add_parser(
        "vector-store-file",
        help="Manage files in a vector store",
        description="Manage files in a vector store: list, retrieve-file, retrieve-file-content, update-file-attribute, delete-file."
    )
    vsf_subparsers = vsf_parser.add_subparsers(dest="vsf_command")

    # List files
    vsf_list = vsf_subparsers.add_parser(
        "list",
        help="List files in a vector store"
    )
    vsf_list.add_argument(
        "--vector-store-id", required=True,
        help="Vector Store ID"
    )

    # Retrieve file object
    vsf_retrieve = vsf_subparsers.add_parser(
        "retrieve-file",
        help="Retrieve a file object from a vector store"
    )
    vsf_retrieve.add_argument(
        "--vector-store-id", required=True,
        help="Vector Store ID"
    )
    vsf_retrieve.add_argument(
        "--file-id", required=True,
        help="File ID"
    )

    # Retrieve file content
    vsf_content = vsf_subparsers.add_parser(
        "retrieve-file-content",
        help="Retrieve the content of a file from a vector store"
    )
    vsf_content.add_argument(
        "--vector-store-id", required=True,
        help="Vector Store ID"
    )
    vsf_content.add_argument(
        "--file-id", required=True,
        help="File ID"
    )

    # Update file attribute
    vsf_update = vsf_subparsers.add_parser(
        "update-file-attribute",
        help="Update file attributes in a vector store"
    )
    vsf_update.add_argument(
        "--vector-store-id", required=True,
        help="Vector Store ID"
    )
    vsf_update.add_argument(
        "--file-id", required=True,
        help="File ID"
    )
    vsf_update.add_argument(
        "--attribute", required=True,
        help="Attribute name to update (e.g. 'metadata')"
    )
    vsf_update.add_argument(
        "--value", required=True,
        help="New value for the attribute (JSON string if complex type)"
    )

    # Delete file
    vsf_delete = vsf_subparsers.add_parser(
        "delete-file",
        help="Delete a file from a vector store"
    )
    vsf_delete.add_argument(
        "--vector-store-id", required=True,
        help="Vector Store ID"
    )
    vsf_delete.add_argument(
        "--file-id", required=True,
        help="File ID"
    )

    args = parser.parse_args()

    if args.command == "file-upload":
        upload_files(args.file, args.vector_store_id, args.purpose)
    elif args.command == "tts":
        tts(text=args.text, input_file=args.input_file, output=args.output, model=args.model, voice=args.voice)
    elif args.command == "ask":
        print("The 'ask' command has been removed.")
    elif args.command == "chat":
        chat(
            model=args.model,
            system=args.system,
            user=args.user,
            stream=args.stream,
            vector_store_id=args.vector_store_id
        )
    elif args.command == "vector-store":
        if args.vs_command == "create":
            vector_store_create(args.name, args.description)
        elif args.vs_command == "list":
            vector_store_list()
        elif args.vs_command == "get":
            vector_store_get(args.id)
        elif args.vs_command == "delete":
            vector_store_delete(args.id)
        else:
            print("No vector store subcommand specified. Use create, list, get, or delete.")
    elif args.command == "vector-store-file":
        if args.vsf_command == "list":
            vector_store_file_list(args.vector_store_id)
        elif args.vsf_command == "retrieve-file":
            vector_store_file_retrieve(args.vector_store_id, args.file_id)
        elif args.vsf_command == "retrieve-file-content":
            vector_store_file_retrieve_content(args.vector_store_id, args.file_id)
        elif args.vsf_command == "update-file-attribute":
            import json
            try:
                value = json.loads(args.value)
            except Exception:
                value = args.value
            vector_store_file_update_attribute(
                args.vector_store_id,
                args.file_id,
                **{args.attribute: value}
            )
        elif args.vsf_command == "delete-file":
            vector_store_file_delete(args.vector_store_id, args.file_id)
        else:
            print("No vector store file subcommand specified. Use list, retrieve-file, retrieve-file-content, update-file-attribute, or delete-file.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
