from pyramid.view import view_config
from pyramid.request import Request
from gaf_api.services import calendar

@view_config(route_name="v1:calendar/events")
def get_events(request: Request):
    return {"events": calendar.get_week_events()}
