from datetime import datetime, timedelta, timezone
import json

from pyramid.view import view_config
from pyramid.request import Request
from jwt.exceptions import InvalidTokenError, DecodeError

from gaf_api.services import calendar
from gaf_api.resources import Root
from gaf_api.auth.oauth import JwtHelper
from gaf_api.tools.utils import load_config


@view_config(route_name="v1:live", request_method="GET", context=Root)
def live_check(request: Request):
    """
    Checks if things are working fine
    """
    return {"API Live": True}
