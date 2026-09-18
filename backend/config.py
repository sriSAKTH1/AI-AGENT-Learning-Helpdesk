import os
from dotenv import load_dotenv

load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "false")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv(
    "LANGSMITH_PROJECT",
    "ai-learning-agent",
)

MAX_MODEL_CALLS = 5
MAX_TOOL_CALLS = 3

CONFIDENCE_THRESHOLD = 0.70


if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY is missing. "
        "Add it to your .env file."
    )

if not TAVILY_API_KEY:
    raise ValueError(
        "TAVILY_API_KEY is missing. "
        "Add it to your .env file."
    )