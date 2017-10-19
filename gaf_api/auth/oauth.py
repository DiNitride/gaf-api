# from pyramid.authentication import CallbackAuthenticationPolicy
# from pyramid.request import Request
# from jose import jwt

# class JwtHelper:
#     algorithm = "HS512"
#
#     def __init__(self, key: str):
#         self.key = key
#
#     def decode(self, token: str):
#         return jwt.decode(token, self.key, self.algorithm)
#
#     def encode(self, **claims):
#         return jwt.encode(claims, self.key, self.algorithm)
#
# class BearerAuthenticationPolicy(CallbackAuthenticationPolicy):
#     def __init__(self, callback, jwt_helper=None):
#         self.callback = callback
#         self.jwt_helper = jwt_helper
#
#     def unauthenticated_userid(self, request: Request):
#         token = request.headers['authorization']
#
#         if token is None or token == "":
#             return None
#
#         try:
#             store = self.jwt_helper.decode(token)
#             return store.get("user_id")
#         except jwt.JWTError:
#             return None
#
#     def remember(self, request: Request, userid, **kw):
#         pass
#
#     def forget(self, request: Request):
#         pass
