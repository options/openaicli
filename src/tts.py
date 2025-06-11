# TTS(Text-to-Speech) 기능
import openai
import sys
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def tts(text=None, input_file=None, output="speech_output.mp3", model="tts-1-hd", voice="echo"):
    if input_file:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read().strip()
    if not text:
        print("Text is required.")
        sys.exit(1)
    response = openai.audio.speech.create(
        model=model,
        voice=voice,
        input=text
    )
    with open(output, "wb") as f:
        f.write(response.content)
    print(f"Audio file saved: {output}")
