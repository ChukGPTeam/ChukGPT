import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # .env에서 환경변수 로드

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_gpt(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes Python code to control a PC."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
