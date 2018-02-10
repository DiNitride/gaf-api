from datetime import datetime, timedelta, timezone
import json

from pyramid.view import view_config
from pyramid.request import Request
from jwt.exceptions import InvalidTokenError, DecodeError

from gaf_api.services import calendar
from gaf_api.resources import Root
from gaf_api.auth.oauth import JwtHelper
from gaf_api.tools.utils import load_config

jwt_config = load_config("jwt_config.json")
jwt_interface = JwtHelper(key=jwt_config["secret"])




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
    return calendar.get_days_events()


@view_config(route_name="v1:calendar/event", request_method="GET", context=Root)
def get_event(request: Request):
    """
    Get's an event from an event ID
    """
    if isinstance(request, Request):
        event_id = request.matchdict["event"]
    else:
        event_id = request
    return calendar.get_event(event_id)


@view_config(route_name="v1:calendar/event/new", request_method="POST", context=Root)
def new_event(request: Request):
    """
    Creates a new event
    """
    event = request.json_body
    jwt_token = request.headers["authorization"][6:]
    try:
        payload = jwt_interface.decode(jwt_token)
    except InvalidTokenError or DecodeError:
        return {'status': "Error authenticating."}

    if bot_interface.is_user_editor(payload["id"]):
        event["startTime"] = datetime.now(timezone.utc).isoformat()
        event["endTime"] = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        event["metadata"] = json.dumps({"owner": payload["id"]})
        calendar.create_event(event)
        return {'status': "Created event."}

    return {"status": "Unauthorised."}


@view_config(route_name="v1:calendar/event/delete", request_method="DELETE", context=Root)
def delete_event(request: Request):
    """
    Deletes an event with requested ID
    """

    event_id = request.matchdict["event"]
    jwt_token = request.headers["Authorization"][6:]

    try:
        payload = jwt_interface.decode(jwt_token)
    except InvalidTokenError or DecodeError:
        return {'status': "Error authenticating."}

    event = get_event(event_id)

    metadata = json.loads(event["metadata"])

    if metadata["owner"] == payload["id"] or bot_interface.is_user_manager(payload["id"]):
        calendar.delete_event(event_id)
        return {'status': "Deleted event."}

    return {"status": "Unauthorised."}


# @view_config(route_name="v1:calendar/event", request_method="PUT", context=Root, permission="edit")
# def update_event(request: Request):
#     event_id = request.matchdict["event"]
#
#     calendar.update_event(event_id, **request.json_body)
#
#     return {'status': "Updated event."}
