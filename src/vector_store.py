# Vector Store 관리 기능
import openai
import os
import json

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def vector_store_create(name, description=None):
    result = openai.vector_stores.create(
        name=name
    )
    print(f"Created vector store: {result.id} (name: {result.name})")

def vector_store_list():
    result = openai.vector_stores.list()
    for vs in result.data:
        print(f"ID: {vs.id}, Name: {vs.name}, Created: {vs.created_at}")

def vector_store_get(vector_store_id):
    try:
        result = openai.vector_stores.retrieve(vector_store_id)
        # result가 OpenAIObject일 경우 dict로 변환
        if hasattr(result, 'to_dict'):
            result = result.to_dict()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error retrieving vector store: {e}")

def vector_store_delete(vs_id):
    openai.vector_stores.delete(vs_id)
    print(f"Deleted vector store: {vs_id}")

def vector_store_file_list(vector_store_id, filter=None, order="desc", limit=100):
    """
    List all files in a vector store, handling full pagination using 'after' cursor.
    Optional arguments:
      - filter: Filter by file status (in_progress, completed, failed, cancelled)
      - order: asc or desc (default desc)
      - limit: number of files per page (default 100, max 100)
    """
    try:
        after = None
        total = 0
        while True:
            params = {
                "vector_store_id": vector_store_id,
                "order": order,
                "limit": limit
            }
            if after:
                params["after"] = after
            if filter:
                params["filter"] = filter
            result = openai.vector_stores.files.list(**params)
            files = getattr(result, "data", result)
            if not files:
                if total == 0:
                    print("No files found in the vector store.")
                break
            for file in files:
                file_dict = file.to_dict() if hasattr(file, "to_dict") else file
                print(
                    f"ID: {file_dict.get('id')}, "
                    f"Filename: {file_dict.get('filename')}, "
                    f"Created: {file_dict.get('created_at')}, "
                    f"Status: {file_dict.get('status')}"
                )
                total += 1
            # Use the id of the last file as the 'after' cursor for the next page
            if hasattr(files, '__getitem__') and len(files) > 0:
                after = files[-1].id if hasattr(files[-1], 'id') else files[-1].get('id')
            else:
                after = None
            if not after or (hasattr(result, 'has_more') and not result.has_more):
                break
    except Exception as e:
        print(f"Error listing vector store files: {e}")

def vector_store_file_retrieve(vector_store_id, file_id):
    """
    Retrieve a file object from a vector store.
    """
    try:
        file = openai.vector_stores.files.retrieve(
            vector_store_id=vector_store_id,
            file_id=file_id
        )
        print(json.dumps(file.to_dict() if hasattr(file, 'to_dict') else file, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error retrieving vector store file: {e}")

def vector_store_file_retrieve_content(vector_store_id, file_id):
    """
    Retrieve the content of a file from a vector store.
    """
    try:
        content = openai.vector_stores.files.content(
            vector_store_id=vector_store_id,
            file_id=file_id
        )
        # content is a binary stream, print as text if possible
        if hasattr(content, "read"):
            print(content.read().decode("utf-8", errors="replace"))
        else:
            print(content)
    except Exception as e:
        print(f"Error retrieving vector store file content: {e}")

def vector_store_file_update_attribute(vector_store_id, file_id, **kwargs):
    """
    Update file attributes in a vector store.
    kwargs: attributes to update (e.g., metadata)
    """
    try:
        file = openai.vector_stores.files.update(
            vector_store_id=vector_store_id,
            file_id=file_id,
            **kwargs
        )
        print(json.dumps(file.to_dict() if hasattr(file, 'to_dict') else file, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error updating vector store file attribute: {e}")

def vector_store_file_delete(vector_store_id, file_id):
    """
    Delete a file from a vector store.
    """
    try:
        openai.vector_stores.files.delete(
            vector_store_id=vector_store_id,
            file_id=file_id
        )
        print(f"Deleted file {file_id} from vector store {vector_store_id}")
    except Exception as e:
        print(f"Error deleting vector store file: {e}")
