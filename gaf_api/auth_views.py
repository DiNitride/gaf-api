import urllib.parse as urlparse
import requests

from pyramid.view import view_config
from pyramid.request import Request
from pyramid.response import Response

from gaf_api.services import utils

oauth = utils.load_config("oauth.json")


@view_config(route_name="oauth:authenticate", request_method="GET")
def oauth_start(request: Request):
    """
    Redirects to the Discord OAuth2 login screen
    """
    redirect_url = request.route_url("oauth:authorize")
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

    print(urlparse.urlencode(data))

    r = requests.post(oauth["token_url"], data=data)
    resp = r.json()

    if resp.get("error", False):
        return Response(resp, status=400)

    access_token = resp.get('token_type') + " " + resp.get('access_token')
    print(access_token)


@view_config(route_name="oauth:@me", request_method="GET")
def get_me(request: Request):
    """
    Returns metadata on the logged in user
    """
    pass
