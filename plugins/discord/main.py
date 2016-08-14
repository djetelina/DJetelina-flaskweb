from discord.ext import commands
from datetime import datetime
from plugins.discord.helpers.database import Database
import os

bot = commands.Bot(command_prefix='!', description="I'm the best bot!")
extensions = ['plugins.discord.cogs.admin',
              'plugins.discord.cogs.gaming',
              'plugins.discord.cogs.database']


@bot.event
async def on_ready():
    print('Discord bot ready')


@bot.event
async def on_member_update(old, new):
    general = bot.get_channel("206507394187001856")
    if old.game != new.game:
        if old.game is None:
            await bot.send_message(general,
                                   "**GAME UPDATE** | **{0.name}** | Started playing **{1.game}** ({2:%H:%M})".format(
                                       old, new, datetime.now()))
        elif new.game is None:
            await bot.send_message(general,
                                   "**GAME UPDATE** | **{0.name}** | No longer playing **{0.game}** ({1:%H:%M})".format(
                                       old, datetime.now()))
        else:
            await bot.send_message(general,
                                   "**GAME UPDATE** | **{0.name}** | **{0.game}** to **{1.game}** ({2:%H:%M})".format(
                                       old, new, datetime.now()))


async def run_discord():
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print('Discord {} extension loaded'.format(extension))

        except Exception as e:
            print('Discord failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

    bot.db = Database()

    await bot.start(os.environ.get('DISCORD_TOKEN'))


if __name__ == '__main__':
    run_discord()
