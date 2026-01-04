from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

MODEL_NAME = "llama-3.1-8b-instant"

def ai_process(user_input: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "API key not found. Please check your .env file."

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are Maya, a friendly AI voice assistant."},
            {"role": "user", "content": user_input}
        ]
    )

    return response.choices[0].message.content
