import argparse
import sys
import openai
import glob
import os

# Get API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Error: Please set the OPENAI_API_KEY environment variable.")
    sys.exit(1)
openai.api_key = OPENAI_API_KEY

def main():
    parser = argparse.ArgumentParser(prog="openai-cli", description="OpenAI CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    # 파일 업로드
    upload_parser = subparsers.add_parser("file upload", help="Upload files (wildcard supported)")
    upload_parser.add_argument("--pattern", required=True, help="File name or wildcard pattern to upload (e.g. *.md)")
    upload_parser.add_argument("--vector-store-id", help="Vector Store ID (optional)")
    upload_parser.add_argument("--purpose", default="assistants", help="File purpose (assistants, fine-tune, etc)")

    # TTS
    tts_parser = subparsers.add_parser("tts", help="Convert text to speech (TTS)")
    tts_parser.add_argument("--text", help="Text to convert to speech")
    tts_parser.add_argument("--input-file", help="Text file path")
    tts_parser.add_argument("--output", default="speech_output.mp3", help="Output mp3 file name")
    tts_parser.add_argument("--model", default="tts-1-hd", help="TTS model name")
    tts_parser.add_argument("--voice", default="echo", help="TTS voice name")

    # 질문/응답
    ask_parser = subparsers.add_parser("ask", help="Ask a question (with vector store search)")
    ask_parser.add_argument("--vector-store-id", help="Vector Store ID")
    ask_parser.add_argument("--question", help="Question text")

    # Chat Completion
    chat_parser = subparsers.add_parser("chat", help="Chat Completion (GPT model conversation)")
    chat_parser.add_argument("--model", default="gpt-4o", help="Model name (e.g. gpt-4o, gpt-3.5-turbo)")
    chat_parser.add_argument("--system", help="System prompt (optional)")
    chat_parser.add_argument("--user", help="User prompt (optional)")
    chat_parser.add_argument("--stream", action="store_true", help="Use streaming output")

    # Vector Store management
    vs_parser = subparsers.add_parser("vector-store", help="Manage vector stores")
    vs_subparsers = vs_parser.add_subparsers(dest="vs_command")

    # Create vector store
    vs_create = vs_subparsers.add_parser("create", help="Create a new vector store")
    vs_create.add_argument("--name", required=True, help="Name for the vector store")
    vs_create.add_argument("--description", help="Description for the vector store")

    # List vector stores
    vs_list = vs_subparsers.add_parser("list", help="List all vector stores")

    # Retrieve vector store
    vs_get = vs_subparsers.add_parser("get", help="Get details of a vector store")
    vs_get.add_argument("--id", required=True, help="Vector Store ID")

    # Delete vector store
    vs_delete = vs_subparsers.add_parser("delete", help="Delete a vector store")
    vs_delete.add_argument("--id", required=True, help="Vector Store ID")

    args = parser.parse_args()

    if args.command == "file upload":
        pattern = args.pattern
        matched_files = glob.glob(pattern)
        if not matched_files:
            print(f"No files matched the pattern: {pattern}")
            sys.exit(1)
        for file_path in matched_files:
            if not os.path.isfile(file_path):
                print(f"Not a file: {file_path}")
                continue
            with open(file_path, "rb") as f:
                if args.vector_store_id:
                    file_obj = openai.vector_stores.files.upload(
                        vector_store_id=args.vector_store_id,
                        file=f
                    )
                    print(f"Uploaded to Vector Store: {file_obj.id} ({file_path})")
                else:
                    file_obj = openai.files.create(
                        file=f,
                        purpose=args.purpose
                    )
                    print(f"File uploaded: {file_obj.id} ({file_path})")

    elif args.command == "tts":
        if args.input_file:
            with open(args.input_file, "r", encoding="utf-8") as f:
                text = f.read().strip()
        else:
            text = args.text
        if not text:
            print("Text is required.")
            sys.exit(1)
        response = openai.audio.speech.create(
            model=args.model,
            voice=args.voice,
            input=text
        )
        with open(args.output, "wb") as f:
            f.write(response.content)
        print(f"Audio file saved: {args.output}")

    elif args.command == "ask":
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        vector_store_id = args.vector_store_id
        question = args.question or input("Enter your question: ")
        response = client.responses.create(
            model="gpt-4o",
            input=question,
            tools=[{
                "type": "file_search",
                "vector_store_ids": [vector_store_id] if vector_store_id else []
            }],
            stream=True
        )
        for chunk in response:
            if hasattr(chunk, "delta") and chunk.delta:
                print(chunk.delta, end="", flush=True)
        print()
    elif args.command == "chat":
        messages = []
        if args.system:
            messages.append({"role": "system", "content": args.system})
        if args.user:
            messages.append({"role": "user", "content": args.user})
        else:
            user_input = input("User: ")
            messages.append({"role": "user", "content": user_input})
        if args.stream:
            response = openai.chat.completions.create(
                model=args.model,
                messages=messages,
                stream=True
            )
            for chunk in response:
                if hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end="", flush=True)
            print()
        else:
            response = openai.chat.completions.create(
                model=args.model,
                messages=messages
            )
            print(response.choices[0].message.content)
    elif args.command == "vector-store":
        if args.vs_command == "create":
            result = openai.vector_stores.create(
                name=args.name,
                description=args.description if args.description else None
            )
            print(f"Created vector store: {result.id} (name: {result.name})")
        elif args.vs_command == "list":
            result = openai.vector_stores.list()
            for vs in result.data:
                print(f"ID: {vs.id}, Name: {vs.name}, Created: {vs.created_at}")
        elif args.vs_command == "get":
            vs = openai.vector_stores.retrieve(args.id)
            print(f"ID: {vs.id}\nName: {vs.name}\nDescription: {vs.description}\nCreated: {vs.created_at}")
        elif args.vs_command == "delete":
            openai.vector_stores.delete(args.id)
            print(f"Deleted vector store: {args.id}")
        else:
            print("No vector store subcommand specified. Use create, list, get, or delete.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
