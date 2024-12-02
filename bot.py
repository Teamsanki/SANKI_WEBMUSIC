from pyrogram import Client, filters
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask, render_template
import threading
import os

# Bot Configuration
API_ID = "27884171"  # Replace with your API ID
API_HASH = "abe760b5d6b33e15c676577d6ae4a06a"  # Replace with your API Hash
BOT_TOKEN = "7902514308:AAGRWf0i1sN0hxgvVh75AlHNvcVpJ4j07HY"  # Replace with your bot token

# MongoDB Configuration
MONGO_URI = "mongodb+srv://Teamsanki:Teamsanki@cluster0.jxme6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
  # MongoDB URI (update if needed)
DB_NAME = "music_bot"  # MongoDB database name

# Initialize Pyrogram Client
app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Initialize MongoDB Client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]

# Initialize Flask App and specify templates folder
web_app = Flask(__name__, template_folder='templates')  # Ensure template_folder is correctly specified

@app.on_message(filters.command("play") & filters.private)
async def play_command(client, message):
    """
    Handles the /play command. Stores the song in MongoDB and generates a link.
    """
    if len(message.command) < 2:
        await message.reply_text("Please provide a song name after /play command!\nExample: /play Tum Hi Ho")
        return

    song_name = " ".join(message.command[1:])
    room_data = {"user_id": message.from_user.id, "song_name": song_name}
    room_id = db.rooms.insert_one(room_data).inserted_id

    room_link = f"http://localhost:5000/room/{room_id}"
    await message.reply_text(
        f"🎶 Your song is ready! Click the link below to join your room:\n\n[Join Room]({room_link})",
        disable_web_page_preview=True
    )

@web_app.route("/room/<room_id>", methods=["GET"])
def room_page(room_id):
    """
    Serves the room page to play the song based on the room ID.
    """
    room_data = db.rooms.find_one({"_id": ObjectId(room_id)})
    if not room_data:
        return "Invalid room ID or the room has expired!", 404

    song_name = room_data["song_name"]
    return render_template("room.html", song_name=song_name)

def run_flask():
    """
    Run the Flask app in a separate thread.
    """
    web_app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print("Bot is running... Press Ctrl+C to stop.")
    app.run() 
