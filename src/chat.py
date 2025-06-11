# Chat 기능
import openai
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def chat(model="gpt-4o", system=None, user=None, stream=False, vector_store_id=None):
    import openai

    if not user:
        user = input("User: ")

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})

    # vector_store_id가 있으면 file_search tool 사용
    if vector_store_id:
        client = openai.OpenAI()
        response = client.responses.create(
            model=model,
            input=user,
            tools=[{
                "type": "file_search",
                "vector_store_ids": [vector_store_id]
            }],
            stream=stream
        )
        if stream:
            for chunk in response:
                if hasattr(chunk, "delta") and chunk.delta:
                    print(chunk.delta, end="", flush=True)
            print()
        else:
            # 비스트림 응답
            print(response)
    else:
        # 기존 방식 (tools 없이 일반 chat)
        completion = openai.chat.completions.create(
            model=model,
            messages=messages,
            stream=stream
        )
        if stream:
            for chunk in completion:
                if hasattr(chunk, "choices") and chunk.choices:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, "content") and delta.content:
                        print(delta.content, end="", flush=True)
            print()
        else:
            print(completion.choices[0].message.content)
