from discord.ext import commands
import aiohttp
import json


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

        most_played = 0
        hero = ""
        for key, value in heroes_data['heroes'].items():
            if value > most_played:
                hero = key
                most_played = value

        await self.bot.edit_message(msg, "**Competitive Overwatch stats for {0}**\n"
                                         "Rank: {1}\n"
                                         "Winrate: {2}%\n"
                                         "Most played: {3} ({4} hours)".format(tag, rank, win_rate, hero, most_played))


def setup(bot):
    bot.add_cog(Gaming(bot))
