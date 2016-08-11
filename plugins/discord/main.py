from discord.ext import commands
import os

bot = commands.Bot(command_prefix='!', description="I'm the best bot!")
extensions = ['plugins.discord.cogs.admin',
              'plugins.discord.cogs.gaming']


@bot.event
async def on_ready():
    print('Discord bot ready')


@bot.event
async def on_member_update(old, new):
    general = bot.get_channel("206507394187001856")
    if old.game != new.game:
        if old.game == None:
            await bot.send_message(general, "**GAME UPDATE** | **{0.name}** | Started playing **{1.game}**".format(old, new))
        elif new.game == None:
            await bot.send_message(general, "**GAME UPDATE** | **{0.name}** |  Stopped playing **{0.game}**".format(old))
        else:
            await bot.send_message(general, "**GAME UPDATE** | **{0.name}** | **{0.game}** to **{1.game}**".format(old, new))


async def run_discord():
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print('Discord {} extension loaded'.format(extension))

        except Exception as e:
            print('Discord failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

    await bot.start(os.environ.get('DISCORD_TOKEN'))


if __name__ == '__main__':
    run_discord()
