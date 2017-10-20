from pyramid.authentication import CallbackAuthenticationPolicy
from pyramid.request import Request
from jose import jwt
import requests

class JwtHelper:
    algorithm = "HS512"

    def __init__(self, key: str):
        self.key = key

    def decode(self, token: str):
        return jwt.decode(token, self.key, self.algorithm)

    def encode(self, **claims):
        return jwt.encode(claims, self.key, self.algorithm)

class BearerAuthenticationPolicy(CallbackAuthenticationPolicy):
    def __init__(self, callback, jwt_helper=None):
        self.callback = callback
        self.jwt_helper = jwt_helper

    def unauthenticated_userid(self, request: Request):
        token = request.headers['authorization']

        if token is None or token == "":
            return None

        try:
            store = self.jwt_helper.decode(token)
            return store.get("user_id")
        except jwt.JWTError:
            return None

    def remember(self, request: Request, userid, **kw):
        pass

    def forget(self, request: Request):
        pass

class DiscordBearerClient:
    def __init__(self, token_type: str, access_token: str, refresh_token: str, guild_id: int=0):
        """

        :param token_type: Token type from token request response
        :param access_token: Access token from token request response
        :param refresh_token: Refresh token from token request response
        :param guild_id: Guild ID to use for :meth groups: call.
        """
        self.token_type = token_type
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.guild_id = guild_id  # This should be gaf's guild ID: configurable?

    def get_token(self):
        """
        Returns the formatted access token of this client
        """
        return " ".join([self.token_type, self.access_token])

    def get_user_info(self):
        """
        Gets the authenticated user's info
        """
        r = requests.get("https://discordapp.com/api/v7/users/@me", headers={"Authorization": self.get_token()})

        if r.status_code == 401:
            pass  # Refresh token here

        return r.json()

    def groups(self, client_userid, request: Request):
        """
        Returns a user's groups for the authentication policy callback
        """
        guild_id = self.guild_id
        userid = self.get_user_info().get("id")

        if userid != client_userid:
            return None  # oauth user and client user mismatch - not sure how but good to check.

        # Here we use the bot's token to get hold of the user's roles
        # Bot's token isn't in yet - replace the string with a variable or whatever
        r = requests.get(f"https://discordapp.com/api/v7/guilds/{guild_id}/members/{userid}",
                         headers={"Authorization": "GAF_TOKEN_IN_CONFIG"})

        if r.status_code == 200:
            member = r.json()
            roles = member.get("roles", [])

            return list(map(lambda roleid: f"role:{roleid}", roles))
