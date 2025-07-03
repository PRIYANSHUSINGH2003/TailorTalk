import datetime
from typing import List, Dict, Any
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to your service account key file (update this path)
SERVICE_ACCOUNT_FILE = 'elite-nuance-464806-e1-94722a41ac98.json'
# The calendar ID to use (can be 'primary' or a specific calendar ID)
CALENDAR_ID = 'primary'  # Replace with your calendar ID if needed

# Scopes required for Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """
    Authenticate and return a Google Calendar service using a service account.
    """
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build('calendar', 'v3', credentials=credentials)
    return service

def list_events(service, time_min: str, time_max: str) -> List[Dict[str, Any]]:
    """
    List events on the calendar between time_min and time_max (RFC3339 format).
    """
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return events_result.get('items', [])

def create_event(service, summary: str, start_time: str, end_time: str, description: str = "") -> Dict[str, Any]:
    """
    Create a new event on the calendar.
    """
    event = {
        'summary': summary,
        'description': description,
        'start': {'dateTime': start_time, 'timeZone': 'UTC'},
        'end': {'dateTime': end_time, 'timeZone': 'UTC'},
    }
    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return created_event

# INSTRUCTIONS:
# 1. Download your Google Service Account JSON key and place it in the project directory as 'service_account.json'.
# 2. Share your Google Calendar with the service account email (found in the JSON key file).
# 3. Update CALENDAR_ID if you want to use a non-primary calendar.
