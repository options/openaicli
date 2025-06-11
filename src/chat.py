# Chat 기능
import openai
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def chat(model="gpt-4o", system=None, user=None, stream=False):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    if user:
        messages.append({"role": "user", "content": user})
    else:
        user_input = input("User: ")
        messages.append({"role": "user", "content": user_input})
    if stream:
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )
        for chunk in response:
            if hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print()
    else:
        response = openai.chat.completions.create(
            model=model,
            messages=messages
        )
        print(response.choices[0].message.content)
