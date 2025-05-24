from dotenv import load_dotenv
import os

load_dotenv()  # .env 파일 로드

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-3.5-turbo")