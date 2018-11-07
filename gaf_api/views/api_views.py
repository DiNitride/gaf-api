from pyramid.request import Request
from pyramid.view import view_config

from ..resources import APIRoot


@view_config(context=APIRoot, name="live", request_method="GET")
def live_check(request: Request):
    """
    Checks if things are working fine
    :param request: Some stuff idk
    :return: dfjhioesbfgyuhrbsj
    """
    return {"API Live": True, "principals": request.effective_principals}
