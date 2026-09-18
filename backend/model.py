from langchain_google_genai import ChatGoogleGenerativeAI

from backend.config import GOOGLE_API_KEY, MODEL_NAME


primary_model = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
)

fallback_model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
)

model = primary_model