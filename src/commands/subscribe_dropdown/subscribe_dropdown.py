import discord
import sqlite3
from ...database import *
from ...discord_utils import *
from ...openai_utils.generate_thread_name.generate_thread_name import *
from ...config import bot, DB_STRING
from discord import option

channels = fetch_channels()

class SubscribeDropdown(discord.ui.Select):
    def __init__(self, bot_: discord.Bot, target_channel_id):
        self.bot = bot_
        self.target_channel_id = target_channel_id  # Store the target channel ID
        options = []

        # Limit to the first 25 channels
        for channel in list(channels.keys())[:25]:
            options.append(discord.SelectOption(label=channel))

        if not options:
            raise ValueError("No channels available for subscription.")

        super().__init__(
            placeholder="Which source do you want to subscribe to?",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        sub = channels[self.values[0]]  # Get the channel ID using the channel name

        with sqlite3.connect(DB_STRING) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM subscriptions WHERE channel=? AND sub=?", (self.target_channel_id, sub))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO subscriptions (channel, sub) VALUES (?, ?)", (self.target_channel_id, sub))
                
                # Check if the bot has the required permissions in the target channel
                target_channel = self.bot.get_channel(self.target_channel_id)
                permissions = target_channel.permissions_for(target_channel.guild.me)
                if not permissions.read_messages or not permissions.send_messages:
                    await interaction.response.send_message(
                        f"Your channel has been subscribed to {self.values[0]}. However, the bot doesn't have the required permissions to view and post in that channel. "
                        "Please grant the 'View Channel' permissions to the bot's role in that channel."
                    )
                else:
                    await interaction.response.send_message(f"Your channel has been subscribed to {self.values[0]}")
            else:
                await interaction.response.send_message(f"Your channel is already subscribed to {self.values[0]}")