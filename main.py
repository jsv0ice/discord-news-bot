from src.config import bot, DISCORD_TOKEN
from src.database import initialize_db
import src.events
import src.commands

initialize_db()  # Initialize the database

bot.run(DISCORD_TOKEN)