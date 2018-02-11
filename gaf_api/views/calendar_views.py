from datetime import datetime, timedelta, timezone
import json

from pyramid.view import view_config
from pyramid.request import Request

from ..services import calendar
from ..resources import APIRoot, Event, Events


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
    return request.context.ev_data


# Managing Events

@view_config(context=Events, name="new", request_method="POST")
def new_event(request: Request):
    """
    Creates a new event
    """
    event = {}
    payload = request.json_body

    event["name"] = payload["name"]
    event["channel"] = payload["channel"]
    event["startTime"] = datetime.now(timezone.utc).isoformat()
    event["endTime"] = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    event["metadata"] = {"owner": payload["id"]}
    calendar.create_event(event)
    return {'status': "Created event."}


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
