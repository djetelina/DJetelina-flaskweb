from discord.ext import commands
import aiohttp
import json
import datetime
import asyncio
import requests
from functools import partial
from bs4 import BeautifulSoup

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
        msg = await self.bot.say("Fetching statistics for {} (0/3)".format(tag))

        user = tag.replace("#", "-")

        with aiohttp.ClientSession() as session:
            async with session.get("https://owapi.net/api/v2/u/{}/stats/competitive".format(user)) as resp:
                try:
                    comp_data = await resp.json()

                except json.decoder.JSONDecodeError:
                    await self.bot.edit_message(msg, "Error contacting Overwatch API")
                    return

        await self.bot.edit_message(msg, "Fetching information about heroes for {} (1/3)".format(tag))

        with aiohttp.ClientSession() as session:
            async with session.get("https://owapi.net/api/v2/u/{}/heroes/competitive".format(user)) as resp:
                try:
                    heroes_data = await resp.json()

                except json.decoder.JSONDecodeError:
                    await self.bot.edit_message(msg, "Error contacting Overwatch API")
                    return

        await self.bot.edit_message(msg, "Processing stats {},(2/3)".format(tag))

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
                                         "Most played: {3} ({4})".format(
            tag, rank, win_rate, hero, convert_to_time(most_played), convert_to_time(total_played), level))

    @commands.command(description="Diablo Greater Rift", brief="Diablo GR")
    async def diablo(self, tag: str, character_id: str):
        battletag = tag.replace("#", "-")
        player_name = battletag.split("-")[0]
        url = "http://www.diabloprogress.com/hero/{}/{}/{}".format(battletag, player_name, character_id)
        loop = asyncio.get_event_loop()
        post_data = json.dumps({"update": 1})
        headers = {"X-Requested-With": "XMLHttpRequest"}
        msg = await self.bot.say("Updating diabloprogress (0/4)")
        future_post = loop.run_in_executor(None, partial(requests.post, url, data=post_data, headers=headers))
        await future_post
        self.bot.edit_message(msg, "Waiting 5 seconds for diabloprogress to update (1/4)")
        await asyncio.sleep(5)
        await self.bot.edit_message(msg, "Fetching updated stats (2/4)")
        future = loop.run_in_executor(None, requests.get, url)
        res = await future
        try:
            res.raise_for_status()
        except Exception as e:
            await self.bot.edit_message(msg, "Error fetching diabloprogress: *{}*".format(e))
            return
        await self.bot.edit_message(msg, "Got stats, processing (3/4)")
        soup = BeautifulSoup(res.text, "html.parser")
        stats = soup.findAll("h2", text="Stats")[0]
        stats_table = stats.findNext("div")
        stats_attrs = stats_table.findAll('div')
        paragon = "unknown"
        gr = "unknown"
        for attribute in stats_attrs:
            title = attribute.findAll("span", {"class": "char_attr_name"})[0]
            if title.getText().startswith("Paragon"):
                paragon = title.findNext("span").getText()
            if title.getText() == "Solo GRift:":
                gr = title.findNext("span").getText()

        await self.bot.edit_message(msg, "**Seasonal Diablo stats for {0}**\n"
                                         "Paragon: {1}\n"
                                         "Solo GR: {2}\n".format(
            tag, paragon, gr))


def convert_to_time(hours: float):
    delta = datetime.timedelta(hours=hours)
    string = str(delta).split(':')[0]
    affix = 'hours'
    if string.endswith("1"):
        affix = 'hour'
    return "{} {}".format(string, affix)


def setup(bot):
    bot.add_cog(Gaming(bot))
