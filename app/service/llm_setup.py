import os
from dotenv import load_dotenv

load_dotenv()
from langchain_xai import ChatXAI


x_api_key = os.getenv("GROK_API_KEY")

chat = ChatXAI(
    xai_api_key=x_api_key,
    model="grok-4-0709",
)

