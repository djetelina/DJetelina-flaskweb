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
                    await self.bot.say("Error contacting overwatch API")
                    return

        rank = comp_data["overall_stats"]["comprank"]
        win_rate = comp_data["overall_stats"]["win_rate"]

        await self.bot.edit_message(msg, "*Overwatch stats for {0}*\n"
                                         "Rank: {1}\n"
                                         "Winrate: {2}%".format(tag, rank, win_rate))


def find_value(stats, to_find):
    for item in stats:
        if item.getText() == to_find:
            return item.next_sibling.getText()


def setup(bot):
    bot.add_cog(Gaming(bot))
