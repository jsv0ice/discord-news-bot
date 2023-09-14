from ...config import bot, GUILD_ID
from ...events.on_message.on_message import on_message

@bot.slash_command(name="resend", description="Resend this message", guilds=[str(GUILD_ID)])
async def resend(ctx):
    if ctx.author.guild_permissions.manage_guild:  # Check if the user has the 'manage_guild' permission
        try:
            message = await ctx.channel.fetch_message(ctx.target_message_id)
            await on_message(message)
        except ValueError as e:
            await ctx.respond(str(e))
    else:
        await ctx.respond("You don't have the required permissions to use this command.")