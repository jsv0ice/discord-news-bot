import requests
from . import config
import sqlite3
import discord

headers = {
    "Authorization": f"Bot {config.DISCORD_TOKEN}",
    "User-Agent": "DiscordBot (https://github.com/zeinestone/scorg-news, v0.1)",
    "Content-Type": "application/json",
}

def get_subscriptions_category_id(guild_id):
    response = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/channels", headers=headers)
    if response.status_code == 200:
        for channel in response.json():
            if channel['type'] == 4 and channel['name'] == 'subscriptions':  # 4 is the type for category channels
                return channel['id']
    return None

def fetch_channels():
    if config.channels == None:
        channels = {}
        subscriptions_category_id = get_subscriptions_category_id(config.GUILD_ID)
        if subscriptions_category_id is None:
            print("Failed to find 'subscriptions' category.")
        else:
            response = requests.get(f"https://discord.com/api/v10/guilds/{config.GUILD_ID}/channels", headers=headers)
            if response.status_code == 200:
                channel_data = response.json()
                for channel in channel_data:
                    if channel['parent_id'] == subscriptions_category_id:
                        channels[channel['name']] = channel['id']
                print(channels)
            else:
                print(f"Failed to retrieve channels. Status code: {response.status_code}, Message: {response.text}")
        config.channels = channels
    return config.channels

class AdminRemoveSubscriptionButton(discord.ui.View):
    def __init__(self, target_channel_id):
        super().__init__()
        self.target_channel_id = target_channel_id
    
    @discord.ui.button(label="Remove Subscription", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        target_channel_id = self.target_channel_id
        
        with sqlite3.connect(config.DB_STRING) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM subscriptions WHERE channel=?", (target_channel_id,))
            if cursor.rowcount > 0:
                await interaction.response.send_message("Subscription removed.", ephemeral=True)
            else:
                await interaction.response.send_message("Failed to remove subscription.", ephemeral=True)
        await interaction.message.delete()

async def send_error_dm(message, target_channel, error):
    bot_owner_id = 231574499013820417  # Replace with your Discord user ID
    
    bot_owner = await config.bot.fetch_user(bot_owner_id)
    
    error_details = f"Error sending message to channel {target_channel.name} ({target_channel.id}):\n\n{str(error)}"
    
    embed = discord.Embed(title="Error Sending Message", description=error_details, color=discord.Color.red())
    
    # Create the message content
    content = message
    
    # Send the error message as a direct message to the bot owner
    try:
        dm_channel = await bot_owner.create_dm()
        target_channel_id = target_channel.id
        await dm_channel.send(content=content, embed=embed, view=AdminRemoveSubscriptionButton(target_channel_id=target_channel_id))
    except discord.DiscordException:
        # If the bot owner has disabled DMs from the bot, log the error to console
        print(f"Error sending error message to bot owner: {error_details}")