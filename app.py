import streamlit as st
import requests
import uuid
from streamlit.components.v1 import html

st.set_page_config(page_title="Google Calendar Booking Agent", page_icon="📅", layout="wide")

# --- Simple Login Credentials (for demo; use env vars or a secure method in production) ---
VALID_USERNAME = "user"
VALID_PASSWORD = "pass123"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("""
        <style>
        body {
            background: linear-gradient(120deg, #e0eafc 0%, #cfdef3 100%) !important;
        }
        .login-card {
            background: #fff;
            border-radius: 18px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.08);
            padding: 2.5em 2em 2em 2em;
            max-width: 370px;
            margin: 5em auto 2em auto;
        }
        .login-title {
            font-size: 2.1em;
            font-weight: 700;
            text-align: center;
            margin-bottom: 0.5em;
            color: #1976d2;
        }
        .login-subtitle {
            text-align: center;
            color: #555;
            margin-bottom: 1.5em;
        }
        .login-icon {
            display: flex;
            justify-content: center;
            margin-bottom: 1em;
        }
        .stTextInput>div>div>input {
            font-size: 1.1em;
            padding: 0.7em;
        }
        .stButton>button {
            background: linear-gradient(90deg, #1976d2 0%, #42a5f5 100%);
            color: #fff;
            font-weight: 600;
            border-radius: 8px;
            padding: 0.7em 0;
            font-size: 1.1em;
            box-shadow: 0 2px 8px rgba(25,118,210,0.08);
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-icon"><img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Google_Calendar_icon_%282020%29.svg" width="60"></div>', unsafe_allow_html=True)
    st.markdown('<div class="login-title">Sign in to Calendar Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-subtitle">Book appointments with AI</div>', unsafe_allow_html=True)
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                st.session_state["authenticated"] = True
                st.success("Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("Invalid username or password.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# Sidebar with branding and instructions
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/a/a5/Google_Calendar_icon_%282020%29.svg", width=60)
    st.markdown("""
    # Google Calendar Booking Agent
    
    **Your Mission:**
    > Build a conversational AI agent that can assist users in booking appointments on your Google Calendar. The agent should be capable of engaging in a natural, back-and-forth conversation with the user, understanding their intent, checking calendar availability, suggesting suitable time slots, and confirming bookings — all seamlessly through chat.
    
    **Technical Stack Requirements:**
    - **Backend:** Python with FastAPI
    - **Agent Framework:** LangGraph or Langchain
    - **Frontend:** Streamlit chat interface
    - **LLM/Chat Model:** Any LLM API (Gemini, Grok, etc.)
    
    **Google Calendar Integration:**
    - Use a Service Account for integrating with Google Calendar (no OAuth needed)
    - Connect your Google Calendar or a test calendar; bookings will be made in this connected calendar
    
    ---
    **Instructions:**
    - Type your request (e.g., "Book a meeting tomorrow at 3pm")
    - The agent will check your calendar and suggest/book slots
    - All bookings are made in your connected Google Calendar
    """)
    st.markdown("---")
    st.caption("Made with Streamlit · Powered by FastAPI & Langchain")

# Backend API URL (adjust if running elsewhere)
API_URL = "http://localhost:8000/chat"

# Session state for chat history and session ID
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

st.markdown("""
    <style>
    body {
        background: linear-gradient(120deg, #f8fafc 0%, #e0eafc 100%) !important;
        font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
    }
    .main .block-container {
        background: rgba(255,255,255,0.95);
        border-radius: 18px;
        box-shadow: 0 4px 32px rgba(25,118,210,0.07);
        padding: 2.5em 2em 2em 2em;
        margin-top: 2em;
        margin-bottom: 2em;
    }
    .stChatMessage.user {
        background: linear-gradient(90deg, #e3f2fd 60%, #bbdefb 100%);
        border-radius: 16px 16px 4px 16px;
        padding: 14px 18px;
        margin-bottom: 10px;
        font-size: 1.08em;
        box-shadow: 0 2px 8px rgba(33,150,243,0.07);
    }
    .stChatMessage.agent {
        background: linear-gradient(90deg, #f1f8e9 60%, #c8e6c9 100%);
        border-radius: 16px 16px 16px 4px;
        padding: 14px 18px;
        margin-bottom: 10px;
        font-size: 1.08em;
        box-shadow: 0 2px 8px rgba(76,175,80,0.07);
        display: flex;
        align-items: flex-start;
    }
    .stChatMessage.agent img {
        margin-right: 12px;
        border-radius: 50%;
        box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    }
    .stChatInput {margin-top: 2em;}
    .footer {
        text-align: center;
        color: #888;
        font-size: 0.98em;
        margin-top: 2em;
        margin-bottom: 0.5em;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📅 Google Calendar Booking Agent")

# Chat message display using st.chat_message (Streamlit 1.25+)
for msg in st.session_state["messages"]:
    if msg["role"] == "agent":
        with st.chat_message("agent"):
            st.markdown(f'<img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Google_Calendar_icon_%282020%29.svg" width="32" style="vertical-align:middle; margin-right:10px;"> {msg["content"]}', unsafe_allow_html=True)
    else:
        with st.chat_message("user"):
            st.markdown(msg["content"])

# Footer
st.markdown('<div class="footer">&copy; 2024 Google Calendar Booking Agent &mdash; Built by Ankit VERMA</div>', unsafe_allow_html=True)

# User input (modern chat input)
user_input = st.chat_input("Type your message and press Enter...")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.spinner("Agent is typing..."):
        try:
            response = requests.post(
                API_URL,
                json={
                    "message": user_input,
                    "session_id": st.session_state["session_id"],
                    "context": {},
                },
                timeout=30,
            )
            if response.status_code == 200:
                agent_reply = response.json()["response"]
            else:
                agent_reply = f"[Error] Backend returned status {response.status_code}"
        except Exception as e:
            agent_reply = f"[Error] {str(e)}"
    st.session_state["messages"].append({"role": "agent", "content": agent_reply})
    st.rerun()
