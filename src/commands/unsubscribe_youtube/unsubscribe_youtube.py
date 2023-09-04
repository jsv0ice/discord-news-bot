from discord.ext import commands
from discord.ui import Select, View
from discord import SelectOption
from ...config import GUILD_ID, DB_STRING, bot
import sqlite3

class YouTubeChannelSelect(Select):
    def __init__(self, channels):
        options = [
            SelectOption(label=channel[1], value=channel[0]) for channel in channels
        ]
        super().__init__(placeholder='Select a YouTube channel to unsubscribe', options=options)

    async def callback(self, interaction):
        try:
            with sqlite3.connect(DB_STRING) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM watch_channel WHERE youtube_channel_id=?", (self.values[0],))
                conn.commit()

            await interaction.response.send_message(f"YouTube channel {self.values[0]} has been unsubscribed!")
        except sqlite3.Error as e:
            await interaction.response.send_message(f"An error occurred: {e}")

@bot.slash_command(name="unsubscribe_youtube", description="Unsubscribe from a YouTube channel", guild_ids=[GUILD_ID])
async def unsubscribe_youtube(ctx):
    # Check if the user has the manage_guild permission
    if not ctx.author.guild_permissions.manage_guild:
        await ctx.respond("You don't have the required permissions to use this command!")
        return

    try:
        with sqlite3.connect(DB_STRING) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT youtube_channel_id, youtube_channel_name FROM watch_channel")
            channels = cursor.fetchall()

        if not channels:
            await ctx.respond("No YouTube channels found to unsubscribe from!")
            return

        view = View()
        view.add_item(YouTubeChannelSelect(channels))
        await ctx.respond("Select a YouTube channel to unsubscribe from:", view=view)
    except sqlite3.Error as e:
        await ctx.respond(f"An error occurred: {e}")


@bot.slash_command(name="remove_all_videos", description="Remove all videos in the database", guild_ids=[GUILD_ID])
async def remove_all_videos(ctx):
    with sqlite3.connect(DB_STRING) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM video_data")
        conn.commit()

    await ctx.respond("All videos have been removed from the database!")