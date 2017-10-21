import requests


class BotInterface:

    def __init__(self, token):
        self.token = token

    def is_user_editor(self, user_id):
        guild_id = 172425299559055381
        editor_role = "262334316611239937"

        r = requests.get(f"https://discordapp.com/api/v7/guilds/{guild_id}/members/{user_id}",
                         headers={"Authorization": f"{self.token}"})

        if r.status_code == 200:
            member = r.json()
            roles = member.get("roles", [])
            for r in roles:
                if r["id"] == editor_role:
                    return True
                else:
                    return False

    def is_user_manager(self, user_id):
        guild_id = 172425299559055381
        manager_role = "172426922947641344"

        r = requests.get(f"https://discordapp.com/api/v7/guilds/{guild_id}/members/{user_id}",
                         headers={"Authorization": f"{self.token}"})

        if r.status_code == 200:
            member = r.json()
            roles = member.get("roles", [])
            for r in roles:
                if r["id"] == manager_role:
                    return True
                else:
                    return False
