import requests

from pyramid.authentication import CallbackAuthenticationPolicy
from pyramid.request import Request
import jwt


class JwtHelper:

    def __init__(self, key: str):
        self.algorithm = "HS512"
        self.key = key

    def decode(self, token: str):
        return jwt.decode(token, self.key, self.algorithm)

    def encode(self, **claims):
        return jwt.encode(claims, self.key, self.algorithm)


class BearerAuthenticationPolicy(CallbackAuthenticationPolicy):
    """
    Implements pyramid's CallbackAuthenticationPolicy
    """
    def __init__(self, callback, jwt_helper=None):
        self.callback = callback
        self.jwt_helper = jwt_helper

    def unauthenticated_userid(self, request: Request):
        """
        Returns the userid stored in a request's token, or None if the token is missing or invalid.
        """
        token = request.headers['authorization']

        if token is None or token == "":
            return None

        try:
            store = self.jwt_helper.decode(token)
            return store.get("user_id")
        except jwt.JWTError:
            return None

    def remember(self, request: Request, userid, **kw):
        """
        Not used for Bearer policy (since the client application chooses when to provide the token)
        """
        pass

    def forget(self, request: Request):
        pass


class DiscordBearerClient:
    def __init__(self, token_type: str, access_token: str, refresh_token: str):
        """

        :param token_type: Token type from token request response
        :param access_token: Access token from token request response
        :param refresh_token: Refresh token from token request response
        """
        self.token_type = token_type
        self.access_token = access_token
        self.refresh_token = refresh_token

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


# really?
def groups(client_userid, request: Request):
    """
    Returns a user's groups for the authentication policy callback
    """
    guild_id = 0  # This should be gaf's guild ID: configurable?

    # Here we use the bot's token to get hold of the user's roles
    # Bot's token isn't in yet - replace the string with a variable or whatever
    r = requests.get(f"https://discordapp.com/api/v7/guilds/{guild_id}/members/{client_userid}",
                     headers={"Authorization": "GAF_TOKEN_IN_CONFIG"})

    if r.status_code == 200:
        member = r.json()
        roles = member.get("roles", [])

        return list(map(lambda roleid: f"role:{roleid}", roles))
