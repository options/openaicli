# 질문/응답 기능
import os
import sys
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def ask(vector_store_id=None, question=None):
    client = OpenAI(api_key=OPENAI_API_KEY)
    if not question:
        question = input("Enter your question: ")
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
