import discord
from ...config import bot, DB_STRING
import sqlite3

@bot.slash_command(name="add_youtube_channel", description="Add a YouTube channel to the watch list")
@discord.option(name="youtube_channel_id", description="Enter the YouTube Channel ID", type=str, required=True)
@discord.option(name="youtube_channel_name", description="Enter the YouTube Channel Name", type=str, required=True)
@discord.option(name="discord_channel", description="Select the Discord channel to subscribe to", type=discord.TextChannel, required=True)
async def add_youtube_channel(ctx, youtube_channel_id: str, youtube_channel_name: str, discord_channel: discord.TextChannel):
    # Check if the user has the manage_guild permission
    if not ctx.author.guild_permissions.manage_guild:
        await ctx.respond("You don't have the required permissions to use this command!")
        return

    # Insert the provided values into the watch_channel table
    try:
        with sqlite3.connect(DB_STRING) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO watch_channel (youtube_channel_id, youtube_channel_name, discord_channel_id) VALUES (?, ?, ?)", 
                           (youtube_channel_id, youtube_channel_name, str(discord_channel.id)))
            conn.commit()
        await ctx.respond(f"YouTube channel {youtube_channel_name} ({youtube_channel_id}) has been added to the watch list for Discord channel {discord_channel.name}!")
    except sqlite3.Error as e:
        await ctx.respond(f"An error occurred: {e}")
