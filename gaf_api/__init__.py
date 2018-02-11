from pyramid.config import Configurator
from pyramid.renderers import json_renderer_factory
from pyramid.authorization import ACLAuthorizationPolicy
from gaf_api.auth.oauth import BearerAuthenticationPolicy, JwtHelper, groups
from gaf_api.resources import APIRoot
from os import getenv
import logging

# from .services import db_interface as db

LOGGER = logging.getLogger("gaf_api")


def get_root(request):
    return {
        "api": {
            "v1": APIRoot(request)
        }
    }

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """

    config = Configurator(settings=settings)
    config.set_root_factory(get_root)
    config.add_renderer(None, json_renderer_factory)

    helper = JwtHelper(key=getenv("JWT_KEY"))
    config.set_authentication_policy(BearerAuthenticationPolicy(groups, jwt_helper=helper))
    config.set_authorization_policy(ACLAuthorizationPolicy())

    # API v1
    # config.add_route("v1:acronyms", "/api/v1/acronyms")
    # config.add_route("v1:acronyms/new", "/api/v1/acronyms/new")
    config.scan(".views.api_views")
    config.scan(".views.calendar_views")
    config.scan(".views.acronym_views")

    # OAuth
    # config.add_route('oauth:authenticate', '/oauth2/authenticate')
    # config.add_route('oauth:authorize', '/oauth2/authorize')
    # config.add_route("oauth:@me", "/oauth2/@me")
    # config.scan(".auth_views")
    
    

    return config.make_wsgi_app()
