from pyramid.view import view_config
from pyramid.request import Request
from pyramid.response import Response

from ..resources import Root
from ..services import db_interface as db


def valid_acronym(acronym: str):
    acronym = acronym.lower()
    try:
        g, a, f = acronym.split()
        if g[0] == "g" and a[0] == "a" and f[0] == "f":
            return True
    except ValueError:
        return False


@view_config(route_name="v3:acronym", request_method="GET", context=Root)
def get_acronym(request: Request):
    id = request.matchdict["id"]
    acronym = db.get_acronym_by_id(id)
    return {"id": acronym[0], "acronym": acronym[1]}


@view_config(route_name="v3:acronyms", request_method="GET", context=Root)
def get_acronyms(request: Request):
    return db.get_all_acronyms()


@view_config(route_name="v3:acronyms/new", request_method="POST", context=Root)
def add_acronym(request: Request):
    acronym = request.json_body["acronym"]
    if valid_acronym(acronym):
        if db.add_acronym(acronym):
            return {"status": "Added acronym"}
        return {"status": "Error adding acronym (Either invalid or already in database)"}
