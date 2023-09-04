import discord
from ...discord_utils import *
from ...config import bot, DB_STRING
from ..unsubscribe_dropdown.unsubscribe_dropdown import UnsubscribeDropdown
from discord import commands
import sqlite3

@bot.slash_command(name="unsubscribe", description="Unsubscribe from a topic in this channel")
@discord.option("channel", discord.ForumChannel)
async def unsubscribe(ctx, channel: discord.ForumChannel):
    if ctx.author.guild_permissions.manage_guild:  # Check if the user has the 'manage_guild' permission
        try:
            view = discord.ui.View()
            view.add_item(UnsubscribeDropdown(bot, channel.id))
            await ctx.respond(f"Pick the channel you'd like to unsubscribe {channel} from:", view=view)
        except ValueError as e:
            await ctx.respond(str(e))
    else:
        await ctx.respond("You don't have the required permissions to use this command.")
