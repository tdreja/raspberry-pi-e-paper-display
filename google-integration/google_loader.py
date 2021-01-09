# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START calendar_quickstart]
from __future__ import print_function

import datetime
import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    for value in daily_events():
        print(value[0].isoformat() + ' ' + value[1])


def daily_events(today=datetime.date.today()):
    start_date = today
    start_time = datetime.datetime.combine(start_date, datetime.time(0, 0, 0))
    end_date = start_date + datetime.timedelta(1)
    end_time = datetime.datetime.combine(end_date, datetime.time(0, 0, 0))

    utc_start = datetime.datetime.utcfromtimestamp(start_time.timestamp())
    utc_end = datetime.datetime.utcfromtimestamp(end_time.timestamp())
    return load_events(load_calendars(), min_time=utc_start, max_time=utc_end)


def service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def load_calendars():
    names = find_calendar_names()
    calendar = []

    events_result = service().calendarList().list().execute()
    items = events_result.get('items', [])

    if not items:
        print('No calendars found.')
        return calendar

    for cal in items:
        if not names or cal['summary'] in names:
            calendar.append(cal)
    return calendar


def find_calendar_names():
    names = []
    if not os.path.exists('../calendars.csv'):
        return names

    f = open('../calendars.csv', encoding="utf-8")
    for line in f.readlines():
        names.append(line.strip())
    f.close()
    return names


def load_events(calendars, min_time=datetime.datetime.utcnow(), max_time=datetime.datetime.utcnow()):
    results = []
    events = []
    if not calendars:
        events.extend(events_for_calendar(calendar_id='primary', min_time=min_time, max_time=max_time))
    else:
        for cal in calendars:
            events.extend(events_for_calendar(calendar_id=cal['id'], min_time=min_time, max_time=max_time))

    if not events:
        return results
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_time = datetime.datetime.fromisoformat(start)
        results.append((start_time, event['summary']))

    return results


def events_for_calendar(calendar_id, min_time=datetime.datetime.utcnow(), max_time=datetime.datetime.utcnow()):
    events_result = service().events().list(calendarId=calendar_id,
                                            timeMin=min_time.isoformat() + 'Z',
                                            timeMax=max_time.isoformat() + 'Z',
                                            maxResults=5, singleEvents=True,
                                            orderBy='startTime').execute()
    return events_result.get('items', [])


if __name__ == '__main__':
    main()
# [END calendar_quickstart]
