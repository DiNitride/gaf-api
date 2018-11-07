from pyramid.view import view_config
from pyramid.request import Request

from ..resources import Acronym, Acronyms
from ..services import db_interface as db


def valid_acronym(acronym: str):
    acronym = acronym.lower()
    try:
        g, a, f = acronym.split()
        if g[0] == "g" and a[0] == "a" and f[0] == "f":
            return True
    except ValueError:
        return False


@view_config(context=Acronym, request_method="GET")
def get_acronym(request: Request):
    id = request.context.acronym_id
    acronym = db.get_acronym_by_id(id)
    return {"id": acronym[0], "acronym": acronym[1]}


@view_config(context=Acronyms, request_method="GET")
def get_acronyms(request: Request):
    return db.get_all_acronyms()


@view_config(context=Acronyms, name="new", request_method="POST")
def add_acronym(request: Request):
    acronym = request.json_body["acronym"]
    if valid_acronym(acronym):
        if db.add_acronym(acronym):
            return {"status": "Added acronym"}
        return {"status": "Error adding acronym (Already in database)"}
    return {"status": "Error adding acronym (Invalid Acronym)"}
