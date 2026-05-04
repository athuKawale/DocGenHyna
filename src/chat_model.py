from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

load_dotenv()


def chat_model(model_name: str = os.getenv("LLM_MODEL"), temperature: float = os.getenv("LLM_TEMPERATURE")):
    return init_chat_model(model_name, temperature=temperature) 