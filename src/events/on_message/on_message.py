import sqlite3
import json
from ...database import *
from ...discord_utils import *
from ...openai_utils.generate_thread_name.generate_thread_name import *
from ...config import bot, GUILD_ID, DB_STRING
from ...discord_utils import send_error_dm

channels = fetch_channels()

@bot.event
async def on_message(message):
    if str(message.guild.id) == str(GUILD_ID):
        
        with sqlite3.connect(DB_STRING) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT channel FROM subscriptions WHERE sub=?", (message.channel.id,))
            subscribed_channels = cursor.fetchall()
            
            # Create a new entry in the message_tracking table for the message
            message_id = str(message.id)
            content = message.content
            sent_status = 0  # 0 for not sent, 1 for sent successfully, -1 for error
            target_channels = json.dumps([])  # Initialize with an empty list
            
            cursor.execute("INSERT INTO message_tracking (message_id, content, sent_status, target_channels) VALUES (?, ?, ?, ?)",
                            (message_id, content, sent_status, target_channels))
            conn.commit()

            # Generate a name for the thread using OpenAI
            thread_name = await generate_thread_name(message.content, message.embeds, message.attachments)
            if thread_name[0] == '"':
                thread_name = thread_name[1:]
            if thread_name[len(thread_name) - 1] == '"':
                thread_name = thread_name[:(len(thread_name) - 2)]
                
            for (channel_id,) in subscribed_channels:
                target_channel = bot.get_channel(int(channel_id))
                if target_channel:
                    try:
                        await target_channel.create_thread(
                            name=thread_name[:100],
                            content=message.content,
                            embeds=message.embeds,
                            files=[await attachment.to_file() for attachment in message.attachments],
                        )
                        
                        # Update the sent_status to 1 for successful thread creation
                        cursor.execute("UPDATE message_tracking SET sent_status = 1 WHERE message_id = ?", (message_id,))
                        conn.commit()
                        
                        # Update the target_channels to include the successful channel
                        target_channels_list = json.loads(target_channels)
                        target_channels_list.append({"channel_id": str(target_channel.id), "status": "Success"})
                        target_channels = json.dumps(target_channels_list)
                        cursor.execute("UPDATE message_tracking SET target_channels = ? WHERE message_id = ?", (target_channels, message_id))
                        conn.commit()
                        
                    except Exception as e:
                        # Update the sent_status to -1 for error
                        cursor.execute("UPDATE message_tracking SET sent_status = -1 WHERE message_id = ?", (message_id,))
                        conn.commit()
                        
                        # Update the target_channels to include the error channel
                        target_channels_list = json.loads(target_channels)
                        target_channels_list.append({"channel_id": str(target_channel.id), "status": "Error: " + str(e)})
                        target_channels = json.dumps(target_channels_list)
                        cursor.execute("UPDATE message_tracking SET target_channels = ? WHERE message_id = ?", (target_channels, message_id))
                        conn.commit()
                        
                        # Send a DM to the bot owner with the error details and a button to remove the subscription
                        await send_error_dm(message, target_channel, e)
    else:
        pass