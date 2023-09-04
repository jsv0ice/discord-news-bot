import os
from dotenv import load_dotenv
import discord

# Load environment variables from .env file
load_dotenv()

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN') or os.getenv('DISCORD_TOKEN')
OPENAI_TOKEN = os.environ.get('OPENAI_TOKEN') or os.getenv('OPENAI_TOKEN')
GUILD_ID = os.environ.get('SOURCE_GUILD_ID') or os.getenv('SOURCE_GUILD_ID')
DB_STRING = os.environ.get('DATABASE_SOURCE') or 'app/data/subscriptions.db'
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY') or os.getenv('YOUTUBE_API_KEY')
#YOUTUBE_CHANNEL_ID = 'UCRiVHK_3XpMqXkkZsW4g8Tg'
YOUTUBE_CHANNEL_ID = 'UCTeLqJq1mXUX5WWoNXLmOIA'
DISCORD_POST_CHANNEL_ID = '1147956523620892753'


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

youtube_client = None
bot = discord.Bot(intents=intents)