import discord
from ...database import *
from ...discord_utils import *
from ...openai_utils.generate_thread_name.generate_thread_name import *
from ...config import bot, DB_STRING
from ..subscribe_dropdown.subscribe_dropdown import SubscribeDropdown
from discord import commands

@bot.slash_command(name="subscribe", description="Set up subscriptions in this channel")
@discord.option("channel", discord.ForumChannel)
async def subscribe(ctx, channel: discord.ForumChannel):
    if ctx.author.guild_permissions.manage_guild:  # Check if the user has the 'manage_guild' permission
        try:
            view = discord.ui.View()
            view.add_item(SubscribeDropdown(bot, channel.id))
            await ctx.respond(f"Pick the channel you'd like to subscribe {channel} to:", view=view)
        except ValueError as e:
            await ctx.respond(str(e))
    else:
        await ctx.respond("You don't have the required permissions to use this command.")