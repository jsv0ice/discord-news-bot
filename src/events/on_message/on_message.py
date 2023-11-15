import sqlite3
import json
from datetime import datetime
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

            # Check if the current message and the previous message are within one minute
            try:
                last_messages = await message.channel.history(limit=2).flatten()
                if len(last_messages) > 1:
                    last_message = last_messages[1]
                    time_difference = (message.created_at - last_message.created_at).total_seconds()
                    if time_difference < 60:
                        # If within one minute, check if the last message has a thread
                        if last_message.thread:
                            # Post current message in the previous message's thread
                            await last_message.thread.send(content=message.content, embeds=message.embeds, files=[await attachment.to_file() for attachment in message.attachments])
                            return
            except Exception as e:
                print(f"Error in checking message timestamps: {e}")

            # Rest of your original code for normal message processing starts here
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
            if thread_name[-1] == '"':
                thread_name = thread_name[:-1]
                
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
