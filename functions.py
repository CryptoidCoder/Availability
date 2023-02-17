from __future__ import print_function

from datetime import datetime, date, time
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

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

def parsemessage(colour):
    if colour == 'red':
            current_message = 'CryptoidCoder Is Unable To Talk / Message / Call.'
    elif colour == 'amber':
            current_message = 'CryptoidCoder Is Free To Message However Can Only Be Called If An Emergency.'
    elif colour == 'green':
            current_message = 'CryptoidCoder Is Free To Talk / Message / Call.'

    return current_message

def eventsnow(calendar_id):
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        current_date = date.today()
        today_begin_utc = f"{current_date}T00:00:00Z" #begining second of today
        today_end_utc = f"{current_date}T23:59:59Z" #ending second of today

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

def events_now_all_calendars():
    red_cal_id = os.getenv('red_calendar_id')
    red_cal_now = eventsnow(red_cal_id)
    amber_cal_id = os.getenv('amber_calendar_id')
    amber_cal_now = eventsnow(amber_cal_id)
    green_cal_id = os.getenv('green_calendar_id')
    green_cal_now = eventsnow(green_cal_id)
            
    if green_cal_now != None or amber_cal_now != None or red_cal_now != None: #if events today
        if red_cal_now != None: #if at least 1 of the events is a red calendar event
            traffic_light_colour = 'red'
        elif amber_cal_now != None: #if at least 1 of the events is an amber calendar event
            traffic_light_colour = 'amber'
        elif green_cal_now != None: #if at least 1 of the events is a green calendar event
            traffic_light_colour = 'green'
    else:
        traffic_light_colour = 'green'

    return traffic_light_colour

def eventscheck(calendar_id, lookupdate, lookuptimestart, lookuptimeend):
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        current_date = date.today()
        lookup_date_list = lookupdate.split('-') #create list, Year,Month,Day
        lookup_timestart_list = lookuptimestart.split(':') #create list; Hour, Minute
        lookup_timeend_list = lookuptimeend.split(':') #create list; Hour, Minute


        #calculate start time UTC
        #datetime(YEAR,MONTH,DAY,HOUR,MINUTE,SECOND)
        target_start = datetime(int(lookup_date_list[0]), int(lookup_date_list[1]), int(lookup_date_list[2]), int(lookup_timestart_list[0]), int(lookup_timestart_list[1]), 0)
        target_start_utc = target_start.isoformat() + 'Z'

        #calculate end time UTC
        target_end = datetime(int(lookup_date_list[0]), int(lookup_date_list[1]), int(lookup_date_list[2]), int(lookup_timeend_list[0]), int(lookup_timeend_list[1]), 0)
        target_end_utc = target_end.isoformat() + 'Z'

        events_result = service.events().list(calendarId=calendar_id, timeMin=target_start_utc, timeMax = target_end_utc,
                                              maxResults=5, singleEvents=True,
                                              orderBy='startTime').execute()
        daysevents = events_result.get('items', [])

        if not daysevents:
            #print('No upcoming events found.')
            return
        
        parsed_daysevents = []
        for event in daysevents: #events today
            event_name = event['summary'] # get event name
            event_start_time = event['start'].get('dateTime', event['start'].get('date')) #get event start time
            event_end_time = event['end'].get('dateTime', event['end'].get('date')) #get event end time

            if target_start_utc <= event_start_time: #has event not started?
                if target_end_utc >= event_end_time: #has event ended?
                    parsed_daysevents.append(event_name) #add event as it is within the times


        if parsed_daysevents != []: #if events happening now
            return parsed_daysevents
        else:
            return None

    except HttpError as error:
        #print('An error occurred: %s' % error)
        return None
    
def eventscheck_all_calendars(lookupdate, lookuptimestart, lookuptimeend):
    red_cal_id = os.getenv('red_calendar_id')
    red_cal_now = eventscheck(red_cal_id, lookupdate, lookuptimestart, lookuptimeend)
    amber_cal_id = os.getenv('amber_calendar_id')
    amber_cal_now = eventscheck(amber_cal_id, lookupdate, lookuptimestart, lookuptimeend)
    green_cal_id = os.getenv('green_calendar_id')
    green_cal_now = eventscheck(green_cal_id, lookupdate, lookuptimestart, lookuptimeend)

    if green_cal_now != None or amber_cal_now != None or red_cal_now != None: #if events today
        if red_cal_now != None: #if at least 1 of the events is a red calendar event
            traffic_light_colour = 'red'
        elif amber_cal_now != None: #if at least 1 of the events is an amber calendar event
            traffic_light_colour = 'amber'
        elif green_cal_now != None: #if at least 1 of the events is a green calendar event
            traffic_light_colour = 'green'
    else:
        traffic_light_colour = 'green'

    return traffic_light_colour


# Main
tokeninit()