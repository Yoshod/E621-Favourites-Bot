import nextcord
import sys
import os
from nextcord.ext import commands

from configutils import get_config

intents = nextcord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=get_config("BOT", "command prefix", "e621!"), intents=intents)


@bot.command()
async def load(ctx, extension):
    """Load cog."""
    try:
        bot.load_extension(f"cogs.{extension}")
        await ctx.reply(f"Cog {extension} loaded.")
    except commands.errors.ExtensionNotFound:
        await ctx.reply("Cog not found.")
    except commands.errors.ExtensionAlreadyLoaded:
        await ctx.reply("Cog already loaded.")


@bot.command()
async def unload(ctx, extension):
    """Unload Cog."""
    try:
        bot.unload_extension(f"cogs.{extension}")
        await ctx.reply(f"Cog {extension} unloaded.")
    except commands.errors.ExtensionNotFound:
        await ctx.reply("Cog not found.")
    except commands.errors.ExtensionNotLoaded:
        await ctx.reply(f"Cog {extension} was not loaded.")


@bot.command()
async def reload(ctx, extension):
    """Reload Cog.
    If cog wasn't loaded, loads cog.
    """
    try:
        bot.unload_extension(f"cogs.{extension}")
        bot.load_extension(f"cogs.{extension}")
        await ctx.reply(f"Cog {extension} reloaded.")
    except commands.errors.ExtensionNotFound:
        await ctx.reply("Cog not found.")
    except commands.errors.ExtensionNotLoaded:
        try:
            bot.load_extension(f"cogs.{extension}")
            await ctx.reply(f"Cog {extension} loaded.")
        except commands.errors.ExtensionNotFound:
            await ctx.reply("Cog not found.")
        except commands.errors.ExtensionAlreadyLoaded:
            await ctx.reply("Cog already loaded.")


@bot.event
async def on_ready():
    # load all cogs
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"Cog {filename[:-3]} loaded.")

    print(f"System Version:\n{sys.version}")

    print(f"Nextcord Version:\n{nextcord.__version__}")

    print(f"We have logged in as {bot.user}")
    await bot.change_presence(activity=nextcord.Game(get_config("BOT", "status")))


token = get_config("KEYS", "discordapikey")
bot.run(token)
