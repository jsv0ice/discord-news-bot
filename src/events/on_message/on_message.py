import sqlite3
from ...database import *
from ...discord_utils import *
from ...openai_utils.generate_thread_name.generate_thread_name import *
from ...config import bot, GUILD_ID, DB_STRING

channels = fetch_channels()

@bot.event
async def on_message(message):
    if str(message.guild.id) == str(GUILD_ID):
        with sqlite3.connect(DB_STRING) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT channel FROM subscriptions WHERE sub=?", (message.channel.id,))
            subscribed_channels = cursor.fetchall()

            # Generate a name for the thread using OpenAI
            thread_name = await generate_thread_name(message.content, message.embeds, message.attachments)
            if thread_name[0] == '"':
                thread_name = thread_name[1:]
            if thread_name[len(thread_name) - 1] == '"':
                thread_name = thread_name[:(len(thread_name) - 2)]
            for (channel_id,) in subscribed_channels:
                print('looking up target channel')
                target_channel = bot.get_channel(int(channel_id))
                print(target_channel)
                if target_channel:
                    # Create a thread in the target channel
                    try:
                        print('Creating a thread')
                        await target_channel.create_thread(name=thread_name[:100],content=message.content, embeds=message.embeds, files=[await attachment.to_file() for attachment in message.attachments])
                    except Exception as e:
                        print(e)
    else:
        pass
