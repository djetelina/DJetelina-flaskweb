import discord
from discord.ext import commands
# noinspection PyPackageRequirements
from plugins.discord.utils import checks


class Admin:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @checks.is_owner()
    async def play(self, *, playing: str):
        await self.bot.change_status(game=discord.Game(name=playing))
        await self.bot.say("I'm now playing {}".format(playing))

    @commands.command(hidden=True, pass_context=True)
    @checks.is_owner()
    async def nick(self, ctx, *, nick: str):
        await self.bot.change_nickname(ctx.message.server.me, nick)
        await self.bot.say("I might being having an identity crisis. New name accepted")

    @commands.command(hidden=True)
    @checks.is_owner()
    async def reload(self, *, module: str):
        """
        Reloads a module.
        :param module: Module to be reloaded, cogs.general -> from cogs folder general module
        """
        module = module.strip()

        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)

        except Exception as e:
            await self.bot.say('\U0001f52b')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))

        else:
            await self.bot.say('\U0001f44c')

    @commands.command(hidden=True)
    @checks.is_owner()
    async def load(self, *, module: str):
        """
        Loads a module.
        :param module: Module to be loaded, cogs.general -> from cogs folder general module
        """
        module = module.strip()

        try:
            self.bot.load_extension(module)

        except Exception as e:
            await self.bot.say('\U0001f52b')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))

        else:
            await self.bot.say('\U0001f44c')

    @commands.command(hidden=True)
    @checks.is_owner()
    async def unload(self, *, module: str):
        """Unloads a module."""
        module = module.strip()

        try:
            self.bot.unload_extension(module)

        except Exception as e:
            await self.bot.say('\U0001f52b')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))

        else:
            await self.bot.say('\U0001f44c')


def setup(bot):
    bot.add_cog(Admin(bot))
