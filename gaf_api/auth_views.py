import urllib.parse as urlparse
import requests

from pyramid.view import view_config
from pyramid.request import Request
from pyramid.response import Response

from gaf_api.services import utils
from gaf_api.auth.oauth import JwtHelper
import gaf_api.database as db


oauth = utils.load_config("oauth.json")

jwt_config = utils.load_config("jwt_config.json")
jwt_interface = JwtHelper(key=jwt_config["secret"])


@view_config(route_name="oauth:authenticate", request_method="GET")
def oauth_start(request: Request):
    """
    Redirects to the Discord OAuth2 login screen
    """
    redirect_url = oauth["redirect_url"]
    query = urlparse.urlencode(query=utils.combine(redirect_uri=redirect_url, **oauth["params"]))
    url = urlparse.urljoin(oauth["auth_url"], "?" + query)

    return Response(status=307, headers={"Location": url})


@view_config(route_name="oauth:authorize", request_method="GET")
def oauth_authorize(request: Request):
    """
    Get's auth token from Discord using oauth code
    """
    code = request.params["code"]
    redirect_url = request.route_url("oauth:authorize")

    data = utils.combine(
        code=code,
        redirect_uri=redirect_url,
        **oauth['token_params']
    )

    r = requests.post(oauth["token_url"], data=data)
    resp = r.json()

    if resp.get("error", False):
        return Response(resp, status=400)

    access_token = resp.get('token_type') + " " + resp.get('access_token')
    refresh_token = resp.get('refresh_token')

    r = requests.get("https://discordapp.com/api/v7/users/@me", headers={"Authorization": access_token})
    r = r.json()

    jwt_token = jwt_interface.encode(id=r["id"])
    db.add_user(r["id"], access_token, refresh_token)

    return Response(status=302, headers={"Location": f"http://www.neverendinggaf.com?token={jwt_token}"})


@view_config(route_name="oauth:@me", request_method="GET")
def get_me(request: Request):
    """
    Returns metadata on the logged in user
    """
    pass
