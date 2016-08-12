from discord.ext import commands
import aiohttp
import json

heroes = {
    "junkrat": "Junkrat",
    "mccree": "McCree",
    "reinhardt": "Reinhardt",
    "lucio": "Lucio",
    "genji": "Genji",
    "torbjorn": "Torbjörn",
    "bastion": "Bastion",
    "reaper": "Reaper",
    "soldier76": "Soldier 76",
    "mercy": "Mercy",
    "winston": "Winston",
    "hanzo": "Hanzo",
    "tracer": "Tracer",
    "mei": "Mei",
    "zarya": "Zarya",
    "symmetra": "Symmetra",
    "ana": "Ana",
    "zenyatta": "Zenyatta",
    "pharah": "Pharah",
    "widowmaker": "Widowmaker",
    "roadhog": "Roadhog",
    "dva": "D.Va"
}

class Gaming:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Overwatch profile", brief="Overwatch profile")
    async def overwatch(self, tag: str):
        msg = await self.bot.say("Fetching stats for {}".format(tag))

        user = tag.replace("#", "-")

        with aiohttp.ClientSession() as session:
            async with session.get("https://owapi.net/api/v2/u/{}/stats/competitive".format(user)) as resp:
                try:
                    comp_data = await resp.json()

                except json.decoder.JSONDecodeError:
                    await self.bot.edit_message(msg, "Error contacting Overwatch API")
                    return

        with aiohttp.ClientSession() as session:
            async with session.get("https://owapi.net/api/v2/u/{}/heroes/competitive".format(user)) as resp:
                try:
                    heroes_data = await resp.json()

                except json.decoder.JSONDecodeError:
                    await self.bot.edit_message(msg, "Error contacting Overwatch API")
                    return

        rank = comp_data["overall_stats"]["comprank"]
        win_rate = comp_data["overall_stats"]["win_rate"]
        prestige = comp_data["overall_stats"]["prestige"]
        if prestige > 0:
            level = "{}{}".format(prestige, comp_data["overall_stats"]["level"])
        else:
            level = comp_data["overall_stats"]["level"]
        total_played = comp_data["game_stats"]["time_played"]

        most_played = 0
        hero = ""
        for key, value in heroes_data['heroes'].items():
            if value > most_played:
                hero = heroes[key]
                most_played = value

        await self.bot.edit_message(msg, "**Competitive Overwatch stats for {0}**\n"
                                         "Level: {6}\n"
                                         "Rank: {1}\n"
                                         "Winrate: {2}%\n"
                                         "Most played: {3} ({4} out of {5} hours)".format(
            tag, rank, win_rate, hero, most_played, total_played, level))


def setup(bot):
    bot.add_cog(Gaming(bot))
