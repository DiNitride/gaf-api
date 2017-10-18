from pyramid.security import Allow, Everyone

class Calendar(object):
    __acl__ = [
        (Allow, Everyone, "view"),
        (Allow, "group:editors", "edit")
    ]

