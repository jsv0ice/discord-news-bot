import discord
import sqlite3
from ...database import *
from ...discord_utils import *
from ...openai_utils.generate_thread_name.generate_thread_name import *
from ...config import bot, DB_STRING
from discord import option

channels = fetch_channels()

@bot.slash_command(name="view_subscriptions", description="View all subscriptions in the database")
async def view_subscriptions(ctx):
    # Get a list of all channel IDs in the current server
    channel_ids = [channel.id for channel in ctx.guild.channels]

    # Create a placeholder string for the IN clause
    placeholders = ', '.join(['?'] * len(channel_ids))

    with sqlite3.connect(DB_STRING) as conn:
        cursor = conn.cursor()
        # Modify the SQL query to use the placeholders
        cursor.execute(f"SELECT channel, sub FROM subscriptions WHERE channel IN ({placeholders})", tuple(channel_ids))
        subscriptions = cursor.fetchall()

    if not subscriptions:
        await ctx.respond("No subscriptions found in the database for this server.")
        return

    # Formatting the results for better readability
    response = "Subscriptions in the database for this server:\n"
    for channel_id, sub in subscriptions:
        # Get the name of the channel using the channel ID
        channel_obj = ctx.guild.get_channel(int(channel_id))
        if channel_obj:  
            channel_name = channel_obj.name
        else:
            channel_name = f"ID: {channel_id} (Name not found)"

        # Get the name of the subscribed channel using the sub ID
        sub_channel_obj = bot.get_channel(int(sub))
        if sub_channel_obj:
            sub_channel_name = sub_channel_obj.name
        else:
            sub_channel_name = f"ID: {sub} (Name not found)"

        response += f"Channel: {channel_name}, Subscribed to: {sub_channel_name}\n"

    await ctx.respond(response)