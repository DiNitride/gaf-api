from datetime import datetime, timedelta, timezone

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.request import Request

from ..services import calendar
from ..resources import Event, Events


# Getting Events

@view_config(context=Events, request_method="GET")
def get_events(request: Request):
    """
    Returns the day's events
    """
    return calendar.get_days_events()


@view_config(context=Event, request_method="GET")
def get_event(request: Request):
    """
    Get's an event from an event ID
    """
    print("########################")
    print(request.context.event_id)
    print(request.context.ev_data)
    print("##########################")
    return request.context.ev_data


# Managing Events

@view_config(context=Events, name="new", request_method="POST", permission="add")
def new_event(request: Request):
    """
    Creates a new event
    """
    event = {}
    payload = request.json_body

    if request.unauthenticated_userid is None:
        return Response("Unauthorized!", status=403)

    event["name"] = payload["name"]
    event["channel"] = payload["channel"]
    event["metadata"] = {"owner": request.unauthenticated_userid}

    start = datetime.fromtimestamp(payload["start"], tz=timezone.utc)
    event["startTime"] = start.isoformat()

    if payload.get("end", False):
        event["endTime"] = datetime.fromtimestamp(payload["end"], tz=timezone.utc)
    else:
        event["endTime"] = (start + timedelta(hours=1)).isoformat()

    ev_id = calendar.create_event(event)
    return {'status': "Created event.", "event_id": ev_id}


@view_config(context=Event, name="delete", request_method="DELETE", permission="edit")
def delete_event(request: Request):
    """
    Deletes an event with requested ID
    """
    event_id = request.context.event_id
    calendar.delete_event(event_id)
    return {'status': "Deleted event."}


# @view_config(route_name="v1:calendar/event", request_method="PUT", context=Root, permission="edit")
# def update_event(request: Request):
#     event_id = request.matchdict["event"]
#
#     calendar.update_event(event_id, **request.json_body)
#
#     return {'status': "Updated event."}
