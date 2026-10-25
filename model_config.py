import os 
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel, set_tracing_disabled

load_dotenv(override=True)

set_tracing_disabled(True)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "llama3.2")
HOW_MANY_SEARCHES = int(os.getenv("HOW_MANY_SEARCHES", 3))
REPORT_LANGUAGE = os.getenv("REPORT_LANGUAGE", "Spanish")
USE_EMAIL = os.getenv("USE_EMAIL", "false").lower() == "true"

_client = AsyncOpenAI(base_url=OLLAMA_BASE_URL,api_key="ollama")

MODEL= OpenAIChatCompletionsModel(OLLAMA_MODEL_NAME,openai_client=_client)