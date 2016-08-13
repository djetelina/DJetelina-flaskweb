from discord.ext import commands
import aiohttp
import json
import datetime

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
        msg = await self.bot.say("Fetching stats for {} (0/2 statistics)".format(tag))

        user = tag.replace("#", "-")

        with aiohttp.ClientSession() as session:
            async with session.get("https://owapi.net/api/v2/u/{}/stats/competitive".format(user)) as resp:
                try:
                    comp_data = await resp.json()

                except json.decoder.JSONDecodeError:
                    await self.bot.edit_message(msg, "Error contacting Overwatch API")
                    return

        await self.bot.edit_message(msg, "Fetching stats for {} (1/2 hero information)".format(tag))

        with aiohttp.ClientSession() as session:
            async with session.get("https://owapi.net/api/v2/u/{}/heroes/competitive".format(user)) as resp:
                try:
                    heroes_data = await resp.json()

                except json.decoder.JSONDecodeError:
                    await self.bot.edit_message(msg, "Error contacting Overwatch API")
                    return

        await self.bot.edit_message(msg, "Got stats for {}, processing!".format(tag))

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
                                         "Most played: {3} ({4} hour(s)".format(
            tag, rank, win_rate, hero, convert_to_time(most_played), convert_to_time(total_played), level))


def convert_to_time(hours:float):
    delta = datetime.timedelta(hours=hours)
    string = str(delta).split(':')[0]
    affix = 'hours'
    if string.endswith("1"):
        affix = "hour"
    return "{} {}".format(string, affix)


def setup(bot):
    bot.add_cog(Gaming(bot))
