# 📅 Google Calendar Booking Agent

A conversational AI agent that helps users book appointments on their Google Calendar through a modern chat interface. The agent understands natural language, checks calendar availability, suggests time slots, and confirms bookings—all via chat.

---

## 🚀 Features
- Natural, back-and-forth conversation for booking appointments
- Checks Google Calendar availability and suggests free slots
- Books and confirms events directly in your calendar
- Modern, professional Streamlit chat UI with login
- FastAPI backend with Langchain/LangGraph agent logic
- Secure API key management with `.env`

---

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI
- **Agent Framework:** Langchain or LangGraph
- **Frontend:** Streamlit
- **LLM/Chat Model:** Any LLM API (OpenAI, Gemini, Grok, etc.)
- **Calendar Integration:** Google Calendar API (Service Account)

---

## ⚡ Quickstart (Local)

1. **Clone the repo:**
   ```
   git clone <your-repo-url>
   cd Assignment4
   ```
2. **Create and activate a virtual environment:**
   ```
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   pip install python-dotenv
   ```
4. **Set up environment variables:**
   - Copy `.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=sk-xxxxxxx
     ```
5. **Google Calendar setup:**
   - Create a Google Cloud project and enable the Calendar API
   - Create a Service Account, download `service_account.json`, and place it in the project root
   - Share your Google Calendar with the service account email ("Make changes to events" permission)
6. **Run the backend:**
   ```
   uvicorn main:app --reload
   ```
7. **Run the frontend:**
   ```
   streamlit run app.py
   ```

---

## 🌐 Deployment
- Deploy both backend (FastAPI) and frontend (Streamlit) to Railway, Render, Fly.io, etc.
- Update `API_URL` in `app.py` to point to your deployed backend.
- Add your secrets (`.env`, `service_account.json`) securely on the platform.

---

## 📝 Usage Examples
- "Book a meeting tomorrow at 3pm."
- "Am I free this Thursday afternoon?"
- "Suggest some free slots for a 30-minute meeting this week."
- "Cancel my meeting on Friday at 2pm."

---

## 🙏 Credits
- Built by Priyanshu Singh
- Powered by Streamlit, FastAPI, Langchain, and Google Cloud
