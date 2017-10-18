from pyramid.view import view_config
from pyramid.request import Request
from pyramid.response import Response
from gaf_api.services import calendar

@view_config(route_name="v1:calendar/events", request_method="GET")
def get_events(request: Request):
    return {"events": calendar.get_week_events()}

@view_config(route_name="v1:calendar/event/new", request_method="POST")
def new_event(request: Request):
    event = request.json_body
    calendar.add_event(**event)

    return {'status': "OK"}

@view_config(route_name="v1:calendar/event", request_method="GET")
def get_event(request: Request):
    event_id = request.matchdict["event"]
    return calendar.get_event(event_id)

@view_config(route_name="v1:calendar/event", request_method="PUT")
def update_event(request: Request):
    event_id = request.matchdict["event"]

    # idk yet man

    return Response({'status': "Not Yet Implemented"}, status=202)

@view_config(route_name="v1:calendar/event", request_method="DELETE")
def delete_event(request: Request):
    event_id = request.matchdict["event"]

    calendar.delete_event(event_id)

    return {'status': "Deleted event."}
