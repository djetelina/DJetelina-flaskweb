from discord.ext import commands
import os

bot = commands.Bot(command_prefix='!', description="I'm the best bot!")
extensions = ['plugins.discord.cogs.admin',
              'plugins.discord.cogs.gaming']


@bot.event
async def on_ready():
    print('Discord bot ready')


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
