import discord
from ...config import bot, GUILD_ID
from ...events.on_message.on_message import on_message

@bot.message_command(name="resend", description="Resend this message", guild_ids=[str(GUILD_ID)])
async def resend(ctx, message: discord.Message):
    if ctx.author.guild_permissions.manage_guild:  # Check if the user has the 'manage_guild' permission
        try:
            message = await ctx.channel.fetch_message(message.id)
            await on_message(message)
            ctx.respond("Message resent.")
        except ValueError as e:
            await ctx.respond(str(e))
    else:
        await ctx.respond("You don't have the required permissions to use this command.")