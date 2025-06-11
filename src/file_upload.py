# 파일 업로드 기능
import glob
import os
import openai
import sys

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def upload_files(pattern, vector_store_id=None, purpose="assistants"):
    matched_files = glob.glob(pattern)
    if not matched_files:
        print(f"No files matched the pattern: {pattern}")
        sys.exit(1)
    for file_path in matched_files:
        if not os.path.isfile(file_path):
            print(f"Not a file: {file_path}")
            continue
        with open(file_path, "rb") as f:
            if vector_store_id:
                file_obj = openai.vector_stores.files.upload(
                    vector_store_id=vector_store_id,
                    file=f
                )
                print(f"Uploaded to Vector Store: {file_obj.id} ({file_path})")
            else:
                file_obj = openai.files.create(
                    file=f,
                    purpose=purpose
                )
                print(f"File uploaded: {file_obj.id} ({file_path})")
