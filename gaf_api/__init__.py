from pyramid.config import Configurator
from pyramid.renderers import json_renderer_factory

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    config = Configurator(settings=settings)
    config.add_renderer(None, json_renderer_factory)

    # API v1
    config.add_route('v1:calendar/events', '/api/v1/calendar/events')
    config.add_route('v1:calendar/event/new', '/api/v1/calendar/event/new')
    config.add_route('v1:calendar/event', '/api/v1/calendar/event/{event}')
    config.scan(".api_v1")

    return config.make_wsgi_app()
