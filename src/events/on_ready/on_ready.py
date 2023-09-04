from ...config import bot
from ..check_youtube.check_youtube import check_youtube_periodically

@bot.event
async def on_ready():
    check_youtube_periodically.start()
    print(f'We have logged in as {bot.user}')