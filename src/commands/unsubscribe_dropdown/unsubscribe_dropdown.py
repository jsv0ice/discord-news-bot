import discord
import sqlite3
from ...database import *
from ...discord_utils import *
from ...openai_utils.generate_thread_name.generate_thread_name import *
from ...config import bot, DB_STRING

channels = fetch_channels()

class UnsubscribeDropdown(discord.ui.Select):
    def __init__(self, bot_: discord.Bot, channel_id):
        self.bot = bot_
        self.channel_id = channel_id

        with sqlite3.connect(DB_STRING) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT sub FROM subscriptions WHERE channel=?", (int(channel_id),))
            subs = cursor.fetchall()

        # Fetch channel names from the channels dictionary using the stored channel IDs
        options = []
        for (channel_id,) in subs:
            channel_name = next((name for name, id in channels.items() if id == channel_id), None)
            if channel_name:
                options.append(discord.SelectOption(label=channel_name, value=channel_id))

        if not options:
            raise ValueError("No subscriptions available for unsubscription.")

        super().__init__(
            placeholder="Which source do you want to unsubscribe from?",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        sub_id = self.values[0]  # This will now be the channel ID
        with sqlite3.connect(DB_STRING) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM subscriptions WHERE channel=? AND sub=?", (self.channel_id, sub_id))
            if cursor.rowcount > 0:
                # Fetch the channel name for the response message
                channel_name = next((name for name, id in channels.items() if id == sub_id), "Unknown Channel")
                await interaction.response.send_message(f"Your channel has been unsubscribed from {channel_name}")
            else:
                await interaction.response.send_message(f"Failed to unsubscribe. No matching subscription found.")