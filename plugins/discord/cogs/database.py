from discord.ext import commands


class Database:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(description="Register with the bot", brief="Register with the bot", pass_context=True)
    async def register(self, ctx):
        if ctx.invoked_subcommand is None:
            reply = self.bot.db.register_user(ctx.message.author)
            await self.bot.say(reply)

    @register.command(name="battletag",
                      description="Register battletag with the bot",
                      brief="Register battletag with the bot",
                      pass_context=True)
    async def _battletag(self, ctx, battletag: str):
        reply = self.bot.db.edit_battletag(ctx.message.author, battletag)
        await self.bot.say(reply)

    @register.command(name="diablo",
                      description="Register diablo character with the bot",
                      brief="Register diablo character with the bot",
                      pass_context=True)
    async def _diablo(self, ctx, char: str):
        reply = self.bot.db.edit_diablo_char(ctx.message.author, char)
        await self.bot.say(reply)

    @register.command(name="nickname",
                      description="Register nickname with the bot",
                      brief="Register nickname with the bot",
                      pass_context=True)
    async def _nickname(self, ctx, nickname: str):
        reply = self.bot.db.edit_nickname(ctx.message.author, nickname)
        await self.bot.say(reply)

    @commands.command(description="What does the bot know about you?", pass_context=True)
    async def about(self, ctx):
        nickname = self.bot.db.get_nickname(ctx.message.author) if not False else "unknown"
        battletag = self.bot.db.get_battletag(ctx.message.author) if not False else "unknown"
        diablo_char = self.bot.db.get_diablo_char(ctx.message.author) if not False else "unknown"
        await self.bot.say("Nickname: {}\n"
                           "Battletag: {}\n"
                           "Diablo char: {}\n".format(nickname, battletag, diablo_char))


def setup(bot):
    bot.add_cog(Database(bot))
