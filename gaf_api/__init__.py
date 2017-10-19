from pyramid.config import Configurator
from pyramid.renderers import json_renderer_factory
from gaf_api.services.oauth import BearerAuthenticationPolicy, JwtHelper
from gaf_api.resources import Root
from os import getenv
import logging

LOGGER = logging.getLogger("gaf_api")

def get_root(request):
    return Root()

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    config = Configurator(settings=settings)
    config.set_root_factory(get_root)
    config.add_renderer(None, json_renderer_factory)

    helper = JwtHelper(key=getenv("JWT_KEY"))
    # config.set_authentication_policy(BearerAuthenticationPolicy(jwt_helper=helper))

    # API v1
    config.add_route('v1:calendar/events', '/api/v1/calendar/events')
    config.add_route('v1:calendar/event/new', '/api/v1/calendar/event/new')
    config.add_route('v1:calendar/event', '/api/v1/calendar/event/{event}')
    config.scan(".api_v1")

    # OAuth
    # config.add_route("oauth:authenticate", '/oauth2/authenticate')

    return config.make_wsgi_app()
