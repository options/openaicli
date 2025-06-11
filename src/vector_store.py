# Vector Store 관리 기능
import openai
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def vector_store_create(name, description=None):
    result = openai.vector_stores.create(
        name=name,
        description=description if description else None
    )
    print(f"Created vector store: {result.id} (name: {result.name})")

def vector_store_list():
    result = openai.vector_stores.list()
    for vs in result.data:
        print(f"ID: {vs.id}, Name: {vs.name}, Created: {vs.created_at}")

def vector_store_get(vs_id):
    vs = openai.vector_stores.retrieve(vs_id)
    print(f"ID: {vs.id}\nName: {vs.name}\nDescription: {vs.description}\nCreated: {vs.created_at}")

def vector_store_delete(vs_id):
    openai.vector_stores.delete(vs_id)
    print(f"Deleted vector store: {vs_id}")
