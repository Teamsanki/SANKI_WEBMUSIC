from pyrogram import Client, filters
from yt_dlp import YoutubeDL
import os
import urllib.parse
from flask import Flask, render_template
import threading

# Bot Configuration
API_ID = "27884171"  # Replace with your API ID
API_HASH = "abe760b5d6b33e15c676577d6ae4a06a"  # Replace with your API Hash
BOT_TOKEN = "7902514308:AAGRWf0i1sN0hxgvVh75AlHNvcVpJ4j07HY"  # Replace with your bot token

# MP3 File Hosting Directory (Local or Server Path)
MUSIC_DIR = "songs"  # Folder where you will store downloaded MP3 files
WEB_URL = "https://teamsanki.github.io/SANKI_WEBMUSIC/songs"  # Public URL for hosted MP3 files

# Ensure the directory exists
if not os.path.exists(MUSIC_DIR):
    os.makedirs(MUSIC_DIR)

# Initialize Pyrogram Client
app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Initialize Flask App
web_app = Flask(__name__, template_folder='templates')

# YouTube Downloader Options
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': f'{MUSIC_DIR}/%(title)s.%(ext)s',  # Save files in MUSIC_DIR
    'quiet': False,  # Turn off quiet mode to see more output for debugging
    'default_search': 'ytsearch',  # Allow searching YouTube with plain text
    'cookiefile': 'cookies.txt',  # Path to your cookies file (Ensure cookies.txt is available)
}

@app.on_message(filters.command("play") & filters.private)
async def play_command(client, message):
    """
    Handles the /play command. Fetches and processes the song.
    """
    if len(message.command) < 2:
        await message.reply_text("Please provide a song name after /play command!\nExample: /play Tum Hi Ho")
        return

    song_name = " ".join(message.command[1:])
    query = f"ytsearch:{song_name}"  # Prepending ytsearch: to perform YouTube search

    # Prepare yt-dlp options and download the song
    try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info_dict = ydl.extract_info(query, download=True)
            if 'entries' in info_dict:
                video = info_dict['entries'][0]  # Get the first result
            else:
                video = info_dict  # Single video result

            # Extract the title of the song
            song_title = video.get('title', None)
            song_url = f"{WEB_URL}/{urllib.parse.quote(song_title)}.mp3"  # URL to the hosted MP3

        # Send the direct URL link for the song
        await message.reply_text(
            f"🎶 Your song '{song_title}' is ready! Click the link to listen: {song_url}",
            disable_web_page_preview=True
        )
    except Exception as e:
        await message.reply_text(f"❌ Error while fetching the song: {str(e)}")
        print(f"Error: {e}")  # For debugging purposes


def run_flask():
    """
    Run the Flask app in a separate thread.
    """
    web_app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print("Bot is running... Press Ctrl+C to stop.")
    app.run()
