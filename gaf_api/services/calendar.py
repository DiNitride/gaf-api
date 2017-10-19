from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient import discovery
from gaf_api.services import utils
from datetime import datetime, timedelta, timezone

creds = ServiceAccountCredentials.from_json_keyfile_dict(utils.load_config("google_keys.json"),
                                                         scopes=['https://www.googleapis.com/auth/calendar'])
service = discovery.build(
    "calendar", "v3",
    http=creds.authorize(Http()),
    cache_discovery=False
)
calendar_id = "primary"

def get_week_events():
    """
    Returns the next 7 days' events.
    """
    start_time = datetime.now(tz=timezone.utc)
    end_time = start_time + timedelta(days=7)

    res = service.events().list(calendarId=calendar_id, timeMin=start_time.isoformat(), timeMax=end_time.isoformat())\
        .execute()
    return res.get("items")

def get_event(event_id: str):
    return service.events().get(calendarId=calendar_id, eventId=event_id).execute()

def add_event(**kwargs):
    event = transform_event_keys(kwargs)

    service.events().insert(calendarId=calendar_id, body=event).execute()

def update_event(event_id: str, **kwargs):
    event = transform_event_keys(kwargs)

    service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()

def delete_event(event_id: str):
    service.events().delete(calendarId=calendar_id, eventId=event_id).execute()

def transform_event_keys(items: dict):
    """
    Transforms an event from our internal format to the google format.
    """
    return {
        "summary": items.get("name"),
        "description": items.get("description", None),
        "start": {
            "dateTime": items.get("start_time", datetime.now(timezone.utc).isoformat())
        },
        "end": {
            "dateTime": items.get("end_time", None)
        }
    }


# Example event body
# event = {
#   'summary': 'Event Name',
#   'location': 'Our house, in the middle of our street',
#   'description': 'This will be our bootleg JSON storage',
#   'start': {
#     'date': '2017-10-19'    # This creates an all day event, we'll want to use
#                             # dateTime instead.
#   },
#   'end': {
#     'date': '2017-10-19'
#   },
#   'reminders': {
#     'useDefault': False,
#     'overrides': [
#       {'method': 'email', 'minutes': 24 * 60},
#       {'method': 'popup', 'minutes': 10},
#     ],
#   },
# }
