from __future__ import print_function

from datetime import datetime, date, time
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from dotenv import load_dotenv
load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
calendar_id = os.getenv('calendar_id')


def tokeninit():
    global creds
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

def eventsnow():
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        current_date = date.today()
        today_begin_utc = f'{current_date}T00:00:00Z' #begining second of today
        today_end_utc = f'{current_date}T23:59:59Z' #ending second of today

        events_result = service.events().list(calendarId=calendar_id, timeMin=today_begin_utc, timeMax = today_end_utc,
                                              maxResults=5, singleEvents=True,
                                              orderBy='startTime').execute()
        todaysevents = events_result.get('items', [])

        if not todaysevents:
            #print('No upcoming events found.')
            return
        
        parsed_todaysevents = []
        for event in todaysevents: #events today
            event_name = event['summary'] # get event name
            event_start_time = event['start'].get('dateTime', event['start'].get('date')) #get event start time
            event_end_time = event['end'].get('dateTime', event['end'].get('date')) #get event end time
            if now > event_start_time: #has event started?
                if now < event_end_time: #has event not ended?
                    parsed_todaysevents.append(event_name)

        if parsed_todaysevents != []: #if events happening now
            return parsed_todaysevents
        else:
            return None

    except HttpError as error:
        #print('An error occurred: %s' % error)
        return None

tokeninit()
#current_events = eventsnow()
