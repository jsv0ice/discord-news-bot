import discord
import sqlite3
from database import *
from discord_utils import *
from openai_utils import *
from config import bot, DB_STRING
from discord import option

channels = fetch_channels()

class Dropdown(discord.ui.Select):
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

@bot.slash_command(name="subscribe", description="Set up subscriptions in this channel")
@option("channel", discord.ForumChannel)
async def setup_channel_subscriptions(ctx, channel: discord.ForumChannel):
    if ctx.author.guild_permissions.manage_guild:  # Check if the user has the 'manage_guild' permission
        try:
            view = discord.ui.View()
            view.add_item(Dropdown(bot, channel.id))
            await ctx.respond(f"Pick the channel you'd like to subscribe {channel} to:", view=view)
        except ValueError as e:
            await ctx.respond(str(e))
    else:
        await ctx.respond("You don't have the required permissions to use this command.")

@bot.slash_command(name="unsubscribe", description="Unsubscribe from a topic in this channel")
@option("channel", discord.ForumChannel)
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

@bot.slash_command(name="test_access", description="Test the bot's access to the channel")
@option("channel", discord.ForumChannel)
async def setup_channel_subscriptions(ctx, channel: discord.ForumChannel):
    if ctx.author.guild_permissions.manage_guild:  # Check if the user has the 'manage_guild' permission
        try:
            await channel.create_thread(name='Test Thread',content='This is a simple Test')
        except Exception as e:
            await ctx.respond(str(e))
    else:
        await ctx.respond("You don't have the required permissions to use this command.")
