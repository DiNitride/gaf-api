from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient import discovery
from gaf_api.services import utils
from datetime import datetime, timedelta

creds = ServiceAccountCredentials.from_json_keyfile_dict(utils.load_config("google_keys.json"),
                                                         scopes=['https://www.googleapis.com/auth/calendar'])
service = discovery.build(
    "calendar", "v3",
    http=creds.authorize(Http())
)
calendar_id = ""

def get_week_events():
    """Returns the next 7 days' events"""
    start_time = datetime.now()
    end_time = start_time + timedelta(days=7)

    res = service.event().list(calendarId=calendar_id, timeMin=start_time.isoformat(), timeMax=end_time.isoformat())\
        .execute()
    return res.get("items")

def add_event(**event):
    service.event().insert(calendarId=calendar_id, body=event).execute()
