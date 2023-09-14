import discord
from discord.ext import commands
from discord.ui import Button, ButtonStyle, ActionRow
#from discord_components import Button, ButtonStyle, ActionRow
from ...config import bot, DB_STRING

async def send_error_dm(message, target_channel, error):
    bot_owner_id = 231574499013820417  # Replace with your Discord user ID
    
    bot_owner = await bot.fetch_user(bot_owner_id)
    
    error_details = f"Error sending message to channel {target_channel.name} ({target_channel.id}):\n\n{str(error)}"
    
    embed = discord.Embed(title="Error Sending Message", description=error_details, color=discord.Color.red())
    
    # Create a button to remove the subscription
    remove_subscription_button = Button(style=ButtonStyle.red, label="Remove Subscription", custom_id=f"remove_subscription_{target_channel.id}")
    action_row = ActionRow(remove_subscription_button)
    
    # Create the message content
    content = f"<@{bot_owner.id}>"
    
    # Send the error message as a direct message to the bot owner
    try:
        dm_channel = await bot_owner.create_dm()
        await dm_channel.send(content=content, embed=embed, components=[action_row])
    except discord.DiscordException:
        # If the bot owner has disabled DMs from the bot, log the error to console
        print(f"Error sending error message to bot owner: {error_details}")