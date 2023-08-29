from config import bot, DISCORD_TOKEN
from commands import *
from events import *

initialize_db()  # Initialize the database

bot.run(DISCORD_TOKEN)
