
@bot.slash_command(name="check_youtube", description="manually check youtube")
async def check_youtube(ctx):
    video_data = await check_new_video()
    print(video_data)
    if video_data:
        video_url = video_data["video_url"]
        video_name = video_data["video_name"]
        transcript = video_data["transcript"]
        channel_name = video_data["channel_name"]
        thumbnail_url = video_data["thumbnail_url"]

        # Create an embed object
        embed = Embed(title=video_name, description=transcript, url=video_url, color=0x3498db, image=thumbnail_url)
        embed.set_author(name=channel_name)
        embed.set_footer(text="Checked manually")
        #embed.set_thumbnail(url="URL_TO_A_THUMBNAIL_IMAGE")  # Optional: You can set a thumbnail image for the video if available
        embed.add_field(name="Channel", value=channel_name, inline=True)
        embed.add_field(name="Video URL", value=video_url, inline=True)
        
        await ctx.respond(embed=embed)
    else:
        await ctx.respond("No new video found!")

@bot.slash_command(name="list_videos", description="List all videos in the database")
async def list_videos(ctx):
    with sqlite3.connect(config.DB_STRING) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT video_name, video_url FROM video_data")
        videos = cursor.fetchall()

    if videos:
        response = "\n".join([f"[{video[0]}]({video[1]})" for video in videos])
        await ctx.respond(response)
    else:
        await ctx.respond("No videos found in the database!")



class VideoSelect(Select):
    def __init__(self, videos, **kwargs):
        options = [SelectOption(label=video[0], value=video[0]) for video in videos]
        super().__init__(placeholder='Select a video to remove...', min_values=1, max_values=1, options=options, **kwargs)

    async def callback(self, interaction):
        selected_video = self.values[0]
        with sqlite3.connect(config.DB_STRING) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM video_data WHERE video_name=?", (selected_video,))
            conn.commit()
        await interaction.response.send_message(f"Video '{selected_video}' has been removed from the database!")


@bot.slash_command(name="remove_video", description="Remove a specific video from the database")
async def remove_video(ctx):
    with sqlite3.connect(config.DB_STRING) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT video_name FROM video_data")
        videos = cursor.fetchall()

    if not videos:
        await ctx.respond("No videos found in the database!")
        return

    view = View()
    view.add_item(VideoSelect(videos))
    await ctx.respond("Please select a video to remove:", view=view)

