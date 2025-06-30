# google_calendar.py
import datetime
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Only 'calendar.events' scope is needed
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_calendar_service():
    creds = None
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)

def create_event(summary, start_dt, end_dt):
    service = get_calendar_service()

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_dt,
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_dt,
            'timeZone': 'Asia/Kolkata',
        }
    }

    return service.events().insert(calendarId='primary', body=event).execute()
