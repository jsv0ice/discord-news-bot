import discord
import sqlite3
from ...config import bot, DB_STRING
from ..check_youtube.check_youtube import check_youtube_periodically
from ..on_message.on_message import on_message

@bot.event
async def on_ready():
    await process_backlog_messages()
    await check_youtube_periodically.start()
    print(f"Bot is connected as {bot.user}")

async def process_backlog_messages():
    with sqlite3.connect(DB_STRING) as conn:
        cursor = conn.cursor()
        
        # Retrieve the last message ID processed by the bot
        cursor.execute("SELECT message_id FROM message_tracking ORDER BY message_id DESC LIMIT 1")
        last_message_id = cursor.fetchone()
        
        if last_message_id:
            last_message_id = last_message_id[0]
            
            # Get the channels subscribed to
            cursor.execute("SELECT DISTINCT channel FROM subscriptions")
            subscribed_channels = cursor.fetchall()
            
            for (channel_id,) in subscribed_channels:
                target_channel = bot.get_channel(int(channel_id))
                
                if target_channel:
                    async for message in target_channel.history(limit=5, oldest_first=True):
                        await on_message(message)
        else:
            print("No previous message found in the database.")