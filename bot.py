from pyrogram import Client, filters
from yt_dlp import YoutubeDL
import os

# Bot Configuration
API_ID = "27884171"  # Replace with your API ID
API_HASH = "abe760b5d6b33e15c676577d6ae4a06a"  # Replace with your API Hash
BOT_TOKEN = "7902514308:AAGRWf0i1sN0hxgvVh75AlHNvcVpJ4j07HY"  # Replace with your bot token

# MP3 File Hosting Directory (Local or Server Path)
MUSIC_DIR = "hosted_music"  # Make sure this folder is accessible via your web server
WEB_URL = "https://teamsanki.github.io/SANKI_WEBMUSIC/songs"  # Public URL for hosted MP3 files

# Initialize Pyrogram Client
app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# YouTube Downloader Options
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': f'{MUSIC_DIR}/%(title)s.%(ext)s',  # Save files in MUSIC_DIR
    'quiet': True,
}


@app.on_message(filters.command("play") & filters.private)
async def play_command(client, message):
    """
    Handles the /play command. Fetches music from YouTube and generates a link.
    """
    if len(message.command) < 2:
        await message.reply_text("Please provide a song name or YouTube URL after /play command!\nExample: /play Tum Hi Ho")
        return

    query = " ".join(message.command[1:])
    await message.reply_text(f"🎶 Searching and downloading: {query}...")

    try:
        # Download from YouTube
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(query, download=True)
            song_title = info.get('title', 'Unknown Song')
            file_name = f"{song_title}.mp3"

        # Generate the public URL for the song
        song_url = f"{WEB_URL}/{file_name.replace(' ', '%20')}"

        # Send the playback link to the user
        await message.reply_text(
            f"🎶 Your song is ready! Click the link to play it:\n\n[Play Song]({song_url})",
            disable_web_page_preview=True
        )
    except Exception as e:
        await message.reply_text(f"❌ Failed to process your request. Error: {str(e)}")


if __name__ == "__main__":
    # Ensure the MUSIC_DIR exists
    if not os.path.exists(MUSIC_DIR):
        os.makedirs(MUSIC_DIR)

    print("Bot is running... Press Ctrl+C to stop.")
    app.run()
