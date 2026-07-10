import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
LOG_FILE = "logs/audit.jsonl"
VALID_TIERS = {"safe", "caution", "refuse"}
