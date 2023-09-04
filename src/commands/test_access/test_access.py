import discord
import sqlite3
from ...database import *
from ...discord_utils import *
from ...openai_utils.generate_thread_name.generate_thread_name import *
from ...config import bot, DB_STRING
from discord import option
from ...youtube_utils.youtube_checker import check_new_video


channels = fetch_channels()

@bot.slash_command(name="test_access", description="Test the bot's access to the channel")
@option("channel", discord.ForumChannel)
async def test_access(ctx, channel: discord.ForumChannel):
    if ctx.author.guild_permissions.manage_guild:  # Check if the user has the 'manage_guild' permission
        try:
            await channel.create_thread(name='Test Thread',content='This is a simple Test')
        except Exception as e:
            await ctx.respond(str(e))
    else:
        await ctx.respond("You don't have the required permissions to use this command.")