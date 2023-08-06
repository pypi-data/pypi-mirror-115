
import requests


class Bedwars_Stats:
    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

    def bedwars_wins(self, name):
        data = requests.get(
            url="https://api.hypixel.net/player",
            params={
                "key": str(self.API_KEY),
                "name": str(name)
            }
        ).json()

        try:
            bedwars_wins = data['player']['achievements']['bedwars_wins']
            return bedwars_wins

        except TypeError:
            return "Username Not Found"

        except KeyError:
            return "name on cooldown , refer https://api.hypixel.net/ for more information"

    def bedwars_coins(self, name):
        data = requests.get(
            url="https://api.hypixel.net/player",
            params={
                "key": str(self.API_KEY),
                "name": str(name)
            }
        ).json()

        try:
            bedwars_coins = data['player']['stats']['Bedwars']['coins']
            return bedwars_coins

        except TypeError:
            return "Username Not Found"

        except KeyError:
            return "name on cooldown , refer https://api.hypixel.net/ for more information"

    def bedwars_level(self, name):
        data = requests.get(
            url="https://api.hypixel.net/player",
            params={
                "key": str(self.API_KEY),
                "name": str(name)
            }
        ).json()

        try:
            bedwars_level = data['player']['achievements']['bedwars_level']
            return bedwars_level

        except TypeError:
            return "Username Not Found"

        except KeyError:
            return "name on cooldown , refer https://api.hypixel.net/ for more information"

    def bedwars_winstreak(self, name):
        data = requests.get(
            url="https://api.hypixel.net/player",
            params={
                "key": str(self.API_KEY),
                "name": str(name)
            }
        ).json()

        try:
            bedwars_streak = data['player']['stats']['Bedwars']['winstreak']
            return bedwars_streak

        except TypeError:
            return "Username Not Found"

        except KeyError:
            return "name on cooldown , refer https://api.hypixel.net/ for more information"

    def bedwars_beds_destroyed(self, name):
        data = requests.get(
            url="https://api.hypixel.net/player",
            params={
                "key": str(self.API_KEY),
                "name": str(name)
            }
        ).json()

        try:
            bedwars_beds_destroyed = data['player']['stats']['Bedwars']['beds_broken_bedwars']
            return bedwars_beds_destroyed

        except TypeError:
            return "Username Not Found"

        except KeyError:
            return "name on cooldown , refer https://api.hypixel.net/ for more information"

    def bedwars_losses(self, name):
        data = requests.get(
            url="https://api.hypixel.net/player",
            params={
                "key": str(self.API_KEY),
                "name": str(name)
            }
        ).json()

        try:
            bedwars_loses = data['player']['stats']['Bedwars']['losses_bedwars']
            return bedwars_loses

        except TypeError:
            return "Username Not Found"

        except KeyError:
            return "name on cooldown , refer https://api.hypixel.net/ for more information"

    def bedwars_final_kills(self, name):
        data = requests.get(
            url="https://api.hypixel.net/player",
            params={
                "key": str(self.API_KEY),
                "name": str(name)
            }
        ).json()
        try:

            bedwars_finals = data['player']['stats']['Bedwars']['final_kills_bedwars']
            return bedwars_finals

        except TypeError:
            return "Username Not Found"

        except KeyError:
            return "name on cooldown , refer https://api.hypixel.net/ for more information"

    def bedwars_kills(self, name):
        data = requests.get(
            url="https://api.hypixel.net/player",
            params={
                "key": str(self.API_KEY),
                "name": str(name)
            }
        ).json()
        try:

            bedwars_kills = data['player']['stats']['Bedwars']['kills_bedwars']
            return bedwars_kills

        except TypeError:
            return "Username Not Found"

        except KeyError:
            return "name on cooldown , refer https://api.hypixel.net/ for more information"


class Skywars_Stats:
    def __init__(self, API_KEY):
        self.key = API_KEY

    def skywars_wins(self, name):
        data = requests.get(
            url="https://api.hypixel.net/player",
            params={
                "key": str(self.key),
                "name": str(name)
            }
        ).json()

        try:
            skywars_wins = data['player']['stats']['SkyWars']['wins']
            return skywars_wins
        except TypeError:
            return "Username Not Found"

        except KeyError:
            return "name on cooldown , refer https://api.hypixel.net/ for more information"

    def skywars_coins(self, name):
        data = requests.get(
            url="https://api.hypixel.net/player",
            params={
                "key": str(self.key),
                "name": str(name)
            }

        ).json()

        try:
            skywars_coins = data['player']['stats']['SkyWars']['coins']
            return skywars_coins

        except TypeError:
            return "Username Not Found"

        except KeyError:
            return "name on cooldown , refer https://api.hypixel.net/ for more information"

    def skywars_kills(self, name):
        data = requests.get(
            url="https://api.hypixel.net/player",
            params={
                "key": str(self.key),
                "name": str(name)
            }

        ).json()

        try:
            skywars_kills = data['player']['stats']['SkyWars']['kills']
            return skywars_kills

        except TypeError:
            return "Username Not Found"

        except KeyError:
            return "name on cooldown , refer https://api.hypixel.net/ for more information"

    def skywars_winstreak(self, name):
        data = requests.get(
            url="https://api.hypixel.net/player",
            params={
                "key": str(self.key),
                "name": str(name)
            }

        ).json()

        try:
            skywars_winstreak = data['player']['stats']['SkyWars']['win_streak']
            return skywars_winstreak

        except TypeError:
            return "Username Not Found"

        except KeyError:
            return "name on cooldown , refer https://api.hypixel.net/ for more information"

    def skywars_matches(self, name):
        data = requests.get(
            url="https://api.hypixel.net/player",
            params={
                "key": str(self.key),
                "name": str(name)
            }

        ).json()

        try:
            skywars_matches = data['player']['stats']['SkyWars']['games']
            return skywars_matches

        except TypeError:
            return "Username Not Found"

        except KeyError:
            return "name on cooldown , refer https://api.hypixel.net/ for more information"

    def skywars_losses(self, name):
        data = requests.get(
            url="https://api.hypixel.net/player",
            params={
                "key": str(self.key),
                "name": str(name)
            }

        ).json()

        try:
            skywars_losses = data['player']['stats']['SkyWars']['losses']
            return skywars_losses

        except TypeError:
            return "Username Not Found"

        except KeyError:
            return "name on cooldown , refer https://api.hypixel.net/ for more information"


