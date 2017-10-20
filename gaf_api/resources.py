from pyramid.security import Allow, Everyone


class Root(object):
    __acl__ = [
        (Allow, Everyone, "view"),
        (Allow, "role:262334316611239937", ("add", "edit"))
    ]

