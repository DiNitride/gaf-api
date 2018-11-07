from pyramid.security import Allow, Everyone
from gaf_api.services.calendar import get_event


class Param:
    def __init__(self, cls):
        self.cls = cls

    def __getitem__(self, item):
        return self.cls(item)


class APIRoot(object):
    def __init__(self, request):
        self.request = request
        self.tree = {
            "calendar": {
                "event": Param(Event),
                "events": Events()
            },
            "acronym": Param(Acronym),
            "acronyms": Acronyms(),
            "oauth2": Oauth2()
        }

    def __acl__(self):
        return [
            (Allow, Everyone, "view")
        ]

    def __getitem__(self, item):
        return self.tree[item]


class Oauth2(object):
    pass


class Events(object):
    __acl__ = [
        (Allow, Everyone, "view"),
        (Allow, "role:107591876533592064", "add"),  # TODO: remove this debug role
        (Allow, "role:262334316611239937", "add")
    ]


class Event(object):
    def __init__(self, event_id):
        self.event_id = event_id
        self.ev_data = get_event(event_id)
        self.owner_id = self.ev_data.get("metadata", {}).get("owner", None)

    def __acl__(self):
        return [
            (Allow, Everyone, "view"),
            (Allow, self.owner_id, "edit")
        ]


class Acronyms(object):
    pass


class Acronym(object):
    def __init__(self, acronym_id):
        self.acronym_id = acronym_id
