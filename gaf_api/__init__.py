from pyramid.config import Configurator
from pyramid.renderers import json_renderer_factory
from pyramid.authorization import ACLAuthorizationPolicy
from .auth.oauth import BearerAuthenticationPolicy, JwtHelper, groups
from .resources import APIRoot
from .tools import utils
import logging

LOGGER = logging.getLogger("gaf_api")
jwt_cfg = utils.load_config("jwt_config.json")

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

    helper = JwtHelper(key=jwt_cfg["secret"])
    config.set_authentication_policy(BearerAuthenticationPolicy(groups, jwt_helper=helper))
    config.set_authorization_policy(ACLAuthorizationPolicy())

    # API v1
    config.scan(".views.api_views")
    config.scan(".views.calendar_views")
    config.scan(".views.acronym_views")
    config.scan(".views.auth_views")

    return config.make_wsgi_app()
