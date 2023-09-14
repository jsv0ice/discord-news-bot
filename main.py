from src import config
from src.database import initialize_db
import src.events
import src.commands
from src.youtube_utils.youtube_oauth import authenticate

initialize_db()  # Initialize the database
print('Database Initialized')

#config.youtube_client = authenticate()  # Modify the global youtube_client from config.py
#print('Youtube Client initialized')
#print(config.youtube_client)

config.bot.run(config.DISCORD_TOKEN)
