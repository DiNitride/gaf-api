import pprint

from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build

# Scope for accessing Google Calendar stuff, should be the only one we need
scopes = ['https://www.googleapis.com/auth/calendar']

# We're using a service account to automate auth
# The service account logs in with an id and secret
# It can access any calendar it is shared with
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'credentials.json',
    scopes)

http = credentials.authorize(Http())

# 'Service' is the magic object that you can use to interact with the API
service = build(
    "calendar",
    "v3",
    http=http
)

# Example event body
event = {
  'summary': 'Event Name',
  'location': 'Our house, in the middle of our street',
  'description': 'This will be our bootleg JSON storage',
  'start': {
    'date': '2017-10-19'    # This creates an all day event, we'll want to use
                            # dateTime instead.
  },
  'end': {
    'date': '2017-10-19'
  },
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}

# This performs the request to the API. These can be separate or
# Chained like so.
# Note: No request is made until the .execute() method is called
event = service.events().insert(calendarId="#####", body=event).execute()

# This for some reason gives you a link to a creation confirmation page
# with all the information filled in, but the event is created
# regardless
print(event.get("htmlLink"))
