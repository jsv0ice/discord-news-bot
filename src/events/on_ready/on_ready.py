from ...config import bot

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')