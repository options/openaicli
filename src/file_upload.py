# 파일 업로드 기능 (OpenAI file search tool 가이드에 맞춰 재구현)
import glob
import os
import openai
import sys

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def upload_files(file, vector_store_id=None, purpose="assistants"):
    """
    파일 또는 와일드카드 패턴을 받아 OpenAI 파일 업로드 또는 벡터스토어 파일 업로드를 수행합니다.
    vector_store_id가 있으면 vector store에 업로드, 없으면 일반 파일 업로드.
    """
    # 와일드카드 및 폴더 지원
    matched_files = glob.glob(file, recursive=True)
    files_to_upload = []
    for path in matched_files:
        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for fname in files:
                    files_to_upload.append(os.path.join(root, fname))
        elif os.path.isfile(path):
            files_to_upload.append(path)
    if not files_to_upload:
        print(f"No files matched the pattern: {file}")
        sys.exit(1)

    for file_path in files_to_upload:
        if not os.path.isfile(file_path):
            print(f"Not a file: {file_path}")
            continue
        with open(file_path, "rb") as f:
            if vector_store_id:
                # 벡터스토어에 파일 업로드 (file_search 용)
                file_obj = openai.vector_stores.files.upload(
                    vector_store_id=vector_store_id,
                    file=f
                )
                print(f"Uploaded to Vector Store: {file_obj.id} ({file_path})")
            else:
                # 일반 파일 업로드 (purpose: assistants 등)
                file_obj = openai.files.create(
                    file=f,
                    purpose=purpose
                )
                print(f"File uploaded: {file_obj.id} ({file_path})")
