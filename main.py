from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict

# Load environment variables
from dotenv import load_dotenv
import os
load_dotenv()

# Langchain imports
from langchain.llms import OpenAI  # Example: Replace with your LLM provider
from langchain.prompts import PromptTemplate

# Google Calendar integration
from calendar_utils import get_calendar_service, list_events
import datetime

app = FastAPI()

# Allow CORS for local development and Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str = None
    context: Dict[str, Any] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str = None
    context: Dict[str, Any] = None

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    user_message = chat_request.message

    # --- Langchain LLM Pipeline (replace with your LLM and API key) ---
    # Example using OpenAI, but you can use Gemini, Grok, etc.
    # Set your API key as an environment variable or config
    try:
        llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
        prompt = PromptTemplate(input_variables=["message"], template="User: {message}\nAI:")
        chain = prompt | llm
        response_text = chain.invoke({"message": user_message})
    except Exception as e:
        response_text = f"[LLM Error] {str(e)}"

    # --- Google Calendar Integration Example ---
    # List events for the next 24 hours as a demonstration
    try:
        service = get_calendar_service()
        now = datetime.datetime.utcnow()
        time_min = now.isoformat() + 'Z'
        time_max = (now + datetime.timedelta(days=1)).isoformat() + 'Z'
        events = list_events(service, time_min, time_max)
        if events:
            event_summaries = [e['summary'] for e in events if 'summary' in e]
            response_text += f"\n\nUpcoming events in next 24h: {event_summaries}"
        else:
            response_text += "\n\nNo events in the next 24 hours."
    except Exception as e:
        response_text += f"\n[Calendar Error] {str(e)}"

    return ChatResponse(response=response_text, session_id=chat_request.session_id, context=chat_request.context)

@app.get("/")
def root():
    return {"message": "FastAPI backend for Google Calendar Booking Agent is running."}
