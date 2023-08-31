import os
from dotenv import load_dotenv
import discord

# Load environment variables from .env file
load_dotenv()

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN') or os.getenv('DISCORD_TOKEN')
OPENAI_TOKEN = os.environ.get('OPENAI_TOKEN') or os.getenv('OPENAI_TOKEN')
GUILD_ID = os.environ.get('SOURCE_GUILD_ID') or os.getenv('SOURCE_GUILD_ID')
DB_STRING = os.environ.get('DATABASE_SOURCE') or 'app/data/subscriptions.db'

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True


bot = discord.Bot(intents=intents)