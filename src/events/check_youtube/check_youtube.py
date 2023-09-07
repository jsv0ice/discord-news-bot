from discord.ext import tasks
from ...config import DISCORD_POST_CHANNEL_ID, bot, DB_STRING
from discord import Embed
from ...youtube_utils.youtube_checker import check_new_video
import sqlite3

@tasks.loop(seconds=3000)
async def check_youtube_periodically():
    try:
        with sqlite3.connect(DB_STRING) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT youtube_channel_id, discord_channel_id FROM watch_channel")
            channels = cursor.fetchall()
    except Exception as e:
        print(e)
        return

    if channels:
        for youtube_channel_id, discord_channel_id in channels:
            video_data = await check_new_video(youtube_channel_id)
            if video_data:
                video_url = video_data["video_url"]
                video_name = video_data["video_name"]
                transcript = video_data["transcript"]
                channel_name = video_data["channel_name"]
                thumbnail_url = video_data["thumbnail_url"]

                # Create an embed object
                embed = Embed(title=video_name, description=transcript, url=video_url, color=0x3498db, image=thumbnail_url)
                embed.set_author(name=channel_name)
                embed.set_footer(text="Discovered Automatically.")
                embed.add_field(name="Channel", value=channel_name, inline=True)
                embed.add_field(name="Video URL", value=video_url, inline=True)

                # Get the Discord channel object using the discord_channel_id
                channel = bot.get_channel(int(discord_channel_id))
                await channel.send(embed=embed)
    else:
        print('No youtube channels to watch')
