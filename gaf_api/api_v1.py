from datetime import datetime, timedelta, timezone

from pyramid.view import view_config
from pyramid.request import Request

from gaf_api.services import calendar
from gaf_api.resources import Root


@view_config(route_name="v1:live", request_method="GET", context=Root)
def live_check(request: Request):
    """
    Checks if things are working fine
    """
    return {"API Live": True}


@view_config(route_name="v1:calendar/events", request_method="GET", context=Root)
def get_events(request: Request):
    """
    Returns the day's events
    """
    calendar.create_event(event = {
        "name": "Test event",
        "id": "",
        "channel": "Channel 1",
        "description": "Bootleg JSON",
        "startTime": datetime.now(timezone.utc).isoformat(),
        "endTime": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    })
    return calendar.get_days_events()


@view_config(route_name="v1:calendar/event", request_method="GET", context=Root)
def get_event(request: Request):
    """
    Get's an event from an event ID
    """
    event_id = request.matchdict["event"]
    return calendar.get_event(event_id)


@view_config(route_name="v1:calendar/event/new", request_method="POST", context=Root, permission="add")
def new_event(request: Request):
    """
    Creates a new event
    """
    event = request.json_body
    calendar.create_event(**event)
    return {'status': "OK"}


# @view_config(route_name="v1:calendar/event", request_method="PUT", context=Root, permission="edit")
# def update_event(request: Request):
#     event_id = request.matchdict["event"]
#
#     calendar.update_event(event_id, **request.json_body)
#
#     return {'status': "Updated event."}


@view_config(route_name="v1:calendar/event", request_method="DELETE", context=Root, permission="edit")
def delete_event(request: Request):
    event_id = request.matchdict["event"]

    calendar.delete_event(event_id)

    return {'status': "Deleted event."}
