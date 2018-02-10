import requests

from ..tools.utils import load_config

bot_config = load_config("bot_config.json")

BOT_TOKEN = bot_config["token"]


def is_user_editor(self, user_id):
    guild_id = 172425299559055381
    editor_role = "262334316611239937"

    r = requests.get(f"https://discordapp.com/api/v7/guilds/{guild_id}/members/{user_id}",
                     headers={"Authorization": f"Bot {BOT_TOKEN}"})

    if r.status_code == 200:
        member = r.json()
        roles = member.get("roles", [])
        for r in roles:
            if r == editor_role:
                return True
            else:
                continue
        return False


def is_user_manager(self, user_id):
    guild_id = 172425299559055381
    manager_role = "172426922947641344"

    r = requests.get(f"https://discordapp.com/api/v7/guilds/{guild_id}/members/{user_id}",
                     headers={"Authorization": f"Bot {BOT_TOKEN}"})

    if r.status_code == 200:
        member = r.json()
        roles = member.get("roles", [])
        for r in roles:
            if r == manager_role:
                return True
            else:
                continue
        return False
