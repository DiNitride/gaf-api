from pyramid.view import view_config
from pyramid.request import Request
from gaf_api.services import calendar
from gaf_api.resources import Root


@view_config(route_name="v1:calendar/events", request_method="GET", context=Root)
def get_events(request: Request):
    """
    Returns the days events
    """
    # TODO: Change this to day not week events
    return {"events": calendar.get_week_events()}


# @view_config(route_name="v1:calendar/event/new", request_method="POST", context=Root, permission="edit")
# def new_event(request: Request):
#     event = request.json_body
#     calendar.add_event(**event)
#     return {'status': "OK"}


@view_config(route_name="v1:calendar/event", request_method="GET", context=Root)
def get_event(request: Request):
    """
    Get's an event from an event ID
    """
    event_id = request.matchdict["event"]
    return calendar.get_event(event_id)


# @view_config(route_name="v1:calendar/event", request_method="PUT", context=Root, permission="edit")
# def update_event(request: Request):
#     event_id = request.matchdict["event"]
#
#     calendar.update_event(event_id, **request.json_body)
#
#     return {'status': "Updated event."}


# @view_config(route_name="v1:calendar/event", request_method="DELETE", context=Root, permission="edit")
# def delete_event(request: Request):
#     event_id = request.matchdict["event"]
#
#     calendar.delete_event(event_id)
#
#     return {'status': "Deleted event."}
