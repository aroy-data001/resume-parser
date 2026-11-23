import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("groq_api_key")

if not my_api_key:
    raise ValueError("Invalid API key!")

client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"
