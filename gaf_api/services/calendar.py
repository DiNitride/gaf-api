from datetime import datetime, timedelta, timezone
from httplib2 import Http

from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery

from ..tools import utils

creds = ServiceAccountCredentials.from_json_keyfile_dict(utils.load_config("google_keys.json"),
                                                         scopes=['https://www.googleapis.com/auth/calendar'])
service = discovery.build(
    "calendar", "v3",
    http=creds.authorize(Http()),
    cache_discovery=False
)

calendar_id = utils.load_config("calendar_id.json").get("id")


def get_days_events():
    """
    Returns the next 24 hours of events
    """
    start_time = datetime.now(tz=timezone.utc)
    end_time = start_time + timedelta(days=1)

    res = service.events().list(calendarId=calendar_id, timeMin=start_time.isoformat(), timeMax=end_time.isoformat())\
        .execute()

    events = []
    for e in res.get("items"):
        events.append(google_to_api(e))

    return {"events": events}


def get_event(event_id: str):
    """
    Get's an event's data from a specific ID
    """
    res = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
    event = google_to_api(res)
    return event


def create_event(event: dict):
    """
    Takes a dictionary in internal event format and creates it on the calendar.
    """
    event = api_to_google(event)

    del event["id"]  # Deletes any ID passed so Google generates us a unique ID

    service.events().insert(calendarId=calendar_id, body=event).execute()


# def update_event(event_id: str, **kwargs):
#     event = transform_event_keys(kwargs)
#
#     service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()


def delete_event(event_id: str):
    """
    Delete's an event based on a specific ID
    """
    service.events().delete(calendarId=calendar_id, eventId=event_id).execute()


def google_to_api(g: dict):
    """
    Converts from the Google Resource format to our internal JSON Format
    """
    event = {
        "name": g.get("summary"),
        "id": g.get("id"),
        "channel": g.get("location"),
        "metadata": g.get("description"),
        "startTime": g.get("start").get("dateTime"),
        "endTime": g.get("end").get("dateTime")
    }
    return event


def api_to_google(items: dict):
    """
    Transforms our interal JSON Object to the Google Resource
    """
    g = {
        "summary": items.get("name"),
        "id": items.get("id"),
        "location": items.get("channel"),
        "description": items.get("metadata"),
        "start": {"dateTime": items.get("startTime")},
        "end": {"dateTime": items.get("endTime")}
    }
    return g
